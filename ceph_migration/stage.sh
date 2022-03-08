TARGET_USER=$1

if [[ "$TARGET_USER" != "" ]]; then
    echo "Making directory for $TARGET_USER..."
    mkdir -p users/$TARGET_USER
    cd users/$TARGET_USER
    # Now in ORIG/users/TARGET_USER
    echo "Listing all files under /cms/store/user/$TARGET_USER..."
    if [[ -d "/ceph/cms/store/user/$TARGET_USER" ]]; then
        find /ceph/cms/store/user/$TARGET_USER/ -type f -printf '%p\t%s\n' | awk -F'/ceph' '{print $2}' &> allCeph
    else
        sh ../../mkcephdir.sh $TARGET_USER
        touch allCeph
    fi
    echo "Made Ceph list"
    hdfs dfs -ls -R /cms/store/user/$TARGET_USER/ &> allHdfs
    echo "Made HDFS list"
    mkdir -p missing
    echo "Finding missing (Ceph vs. HDFS) files..."
    python2 ../../find_diff.py | awk -F'/cms/store' '{print "/store" $2}' &> missing/allMissing
    cd missing;
    # Now in ORIG/users/TARGET_USER/missing
    if [[ $(head -10 allMissing | wc -l) -gt 0 ]]; then
        echo "Found $(cat allMissing | wc -l) missing files; here are the first ten:"
        head -10 allMissing;
        split -l 10000 allMissing newTransfers_
        echo "Staged transfers for missing files; here are the first ten:"
        head -10 newTransfers_aa
        rm -f allMissing
        echo "The rest are in these files:"
        ls .
    else
        echo "No missing files found (or all skipped)"
    fi
    cd ../../..
    # Now in ORIG
    # screen $TARGET_USER
    # python2 migrator.py $PWD/$TARGET_USER/missing/
    # Ctrl + A + D
else
    echo "ERROR: no user provided"
    exit 1
fi
