TARGET_USER=$1
CEPH_USER_DIR=/ceph/cms/store/user

if [[ "$TARGET_USER" != "" ]]; then
    mkdir -p $CEPH_USER_DIR/$TARGET_USER
    chown ${TARGET_USER}:${TARGET_USER} $CEPH_USER_DIR/$TARGET_USER

    cd $CEPH_USER_DIR
    setfacl -m g:tmartin:rwx $TARGET_USER/
    setfacl -d -m u:$TARGET_USER:rwx $TARGET_USER/
    setfacl -d -m g:$TARGET_USER:rwx $TARGET_USER/
    cd -
else
    echo "ERROR: no user specified!"
    exit 1
fi
