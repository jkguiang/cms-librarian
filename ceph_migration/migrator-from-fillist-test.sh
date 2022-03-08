#!/bin/bash

WORK_DIR=`mktemp -d`
DATA_PATH=$1
SPLIT_SIZE=100
#FTS_SERVER="https://cmsfts3.fnal.gov:8446"
#FTS_SERVER="https://fts3-cms.cern.ch:8446"
GSIFTP_FROM="davs://redirector.t2.ucsd.edu:1094"
GSIFTP_TO="davs://redirector.t2.ucsd.edu:1095"

if [ -z "$1" ]; then
    echo "No filename was specified."
    exit 1
fi

if [ -z "$2" ]; then
    echo "No target user was specified."
    exit 1
fi

if [ -z "$3" ]; then
    echo "No transfer group ID was specified."
    exit 1
fi

if [ -z "$4" ]; then
    echo "No FTS Server were specified."
    exit 1
fi

TRANSF_ID=$3
FTS_IDS_FILE="$HOME/.FTS_IDS_$2_$3"
FTS_SERVER=$4

if [ -f $FTS_IDS_FILE ]; then
    echo "=======================      WARNING      ======================="
    echo "FILE $FTS_IDS_FILE is present. Did you already submitted transfer requests?"
    echo "IF YOU ALREADY SUBMITTED TRANSFER. Do not delete $FTS_IDS_FILE file"
    echo "Move this file as it keeps all your transfer request IDs for monitoring transfers"
    echo "and restart this script again."
    echo "=======================      WARNING      ======================="
    # exit 1
else
    touch $FTS_IDS_FILE
fi

ftssubmit () {
    FTSID=`fts-transfer-submit -s $FTS_SERVER -f $WORK_DIR/fts-submit-file -o --retry 3 --retry-delay 60 --timeout 7200`
    rm -f $WORK_DIR/fts-submit-file
    echo $FTSID >> $FTS_IDS_FILE
    echo "FTSID=$FTSID"
    sleep 1
}

echo "=======================      INFO      ======================="
echo "WORK_DIR:   $WORK_DIR"
echo "DATA_PATH:  $DATA_PATH"
echo "SPLIT_SIZE: $SPLIT_SIZE"
echo "FTS_SERVER: $FTS_SERVER"
echo "FTS_ID_SAVED_FILE: $FTS_IDS_FILE"
echo "=============================================================="

cd $WORK_DIR
echo "Getting list of all file names from filename"
echo "--------------------------------------------------------------"
#hdfs dfs -ls -t -R $DATA_PATH  &> GOOD_FILES
cp $1 GOOD_FILES

SUM=`cat GOOD_FILES | wc -l`

echo "Total number of files: $SUM"
echo "Start to split files to $SPLIT_SIZE and submit to FTS at $FTS_SERVER"
cnt=0
cat GOOD_FILES | while read line
do
    if [[ "$cnt" -eq $SPLIT_SIZE ]]; then
        cnt=0
        ftssubmit
    fi
    fname=`echo $line`
    echo "$GSIFTP_FROM$fname $GSIFTP_TO$fname" >> fts-submit-file
    cnt=$[$cnt +1]
done
if [ -f $WORK_DIR/fts-submit-file ]; then
  ftssubmit
fi
