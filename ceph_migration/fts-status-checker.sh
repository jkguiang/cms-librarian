#!/bin/bash

TARGET_USER=$1
GROUP_ID=$2
SERVER_NAME=$3 # fnal or cms

if [[ "$1" == "" ]]; then
    echo "ERROR: no user specified!"
fi
if [[ "$2" == "all" ]]; then
    GROUP_ID=""
fi
if [[ "$3" == "cms" ]]; then
    FTS_SERVER="https://fts3-cms.cern.ch:8446"
elif [[ "$3" == "fnal" ]]; then
    FTS_SERVER="https://cmsfts3.fnal.gov:8446"
else
    echo "ERROR: no FTS server ('cms' or 'fnal') specified!"
fi
echo "Checking $FTS_SERVER"

transfercheck () {
cat $1 | while read line
do
    ST=`fts-transfer-status -s $FTS_SERVER $line`
    echo "$line $ST"
    if [[ "$ST" =~ ^(FAILED|FINISHEDDIRTY)$ ]]; then
        echo "To debug failed transfer. execute: fts-transfer-status -s $FTS_SERVER $line -l | grep -B 2 -A 4 FAILED"
    fi
done

}

if [ -f ~/.FTS_IDS_ ]; then
    SUM=`cat ~/.FTS_IDS_${TARGET_USER}_* | wc -l`
    echo "There is $SUM FTS Transfers to check"
    if [[ "$GROUP_ID" != "" ]]; then
        transfercheck ~/.FTS_IDS_${TARGET_USER}_$GROUP_ID
    else
        for f in $(ls ~/.FTS_IDS_${TARGET_USER}_*); do
            echo "Checking transfer IDs in $f"
            transfercheck $f
        done
    fi
fi

if [ -f ~/.FTS_IDS_RESUB ]; then
    SUM=`cat ~/.FTS_IDS_RESUB | wc -l`
    echo "There is $SUM FTS Transfers to check in RESUBMIT"
    transfercheck ~/.FTS_IDS_RESUB
fi


