lastfts="cms"
for userdir in $(ls -d $PWD/users/*); do
    if [[ -f "$userdir/missing/newTransfers_aa" ]]; then
        if [[ "$lastfts" == "cms" ]]; then
            python2 migrator.py --fnal $userdir/missing
            lastfts="fnal"
        else
            python2 migrator.py --cms $userdir/missing
            lastfts="cms"
        fi
    else
        echo "Nothing found in $userdir/missing"
    fi
done
