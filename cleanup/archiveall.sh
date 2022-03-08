#!/bin/bash
BASEDIR=/hadoop/cms/store/user/$USER
TARGETDIR=$1
if [[ "$TARGETDIR" != "" ]]; then
    for dir in $(ls -d $BASEDIR/$TARGETDIR/*); do 
        echo "$dir --> $(basename $dir).tar.gz"
        tar -zcf tarball.tar.gz $dir
        mv tarball.tar.gz $BASEDIR/$TARGETDIR/$(basename $dir).tar.gz
        rm -rf $dir
    done
else
    echo "ERROR: no target directory supplied; here are the available ones to choose from"
    ls $BASEDIR
fi
