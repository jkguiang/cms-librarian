import os
import sys
from os import listdir
from os.path import isfile, join
import time
import subprocess
import argparse

#fts_servers = ["https://cmsfts3.fnal.gov:8446", "https://fts3-cms.cern.ch:8446"]
#fts_servers = ["https://fts3-cms.cern.ch:8446"]
fts_servers = ["https://cmsfts3.fnal.gov:8446"]

skip_users = ["phchang"]

def submit_new(missdir, fts_server):
    onlyfiles = [f for f in listdir(missdir) if isfile(join(missdir, f))]
    if not onlyfiles:
        return False
    print 'Total FTS Submissions left: %s' % len(onlyfiles)
    full_path = '%s/%s' % (missdir, onlyfiles[0])
    user = missdir.split('/missing')[0]
    if '/' in user:
        user = user.split('/')[-1]
    submitfts = subprocess.Popen(["/root/ceph_migration/big_dir_migration/migrator-from-fillist-test.sh", full_path, user, full_path[-2:], fts_server])
    submitfts.communicate()
    print("The exit code was: %d" % submitfts.returncode)
    if submitfts.returncode == 0:
        os.remove(full_path)
    return True

def get_count(fts_server):
    cmd = 'fts-transfer-list -s %s | grep SUBMITTED | wc -l' % fts_server
    out = subprocess.check_output(cmd, shell=True)
    return int(out)

if __name__ == "__main__":
    cli = argparse.ArgumentParser(description='Submit batches of FTS transfers')
    cli.add_argument('missdir', type=str, help='/full/path/to/user/missing')
    cli.add_argument('--cms', action='store_true', help='Use CMS FTS server')
    cli.add_argument('--fnal', action='store_true', help='Use FNAL FTS server')
    args = cli.parse_args()
    fts_servers = []
    if args.cms:
        fts_servers.append('https://fts3-cms.cern.ch:8446')
    if args.fnal:
        fts_servers.append('https://cmsfts3.fnal.gov:8446')
    proceed = True
    if len(fts_servers) == 0:
        proceed = False
        print('ERROR: no FTS server(s) specified')
    for skip_user in skip_users:
        if skip_user in missdir:
            proceed = False
            print('We are skipping %s because we were told to' % (skip_user))
            break
    while proceed:
        for fts_server in fts_servers:
            substate = get_count(fts_server)
            print 'In submit state we have %s. FTS Server: %s' % (substate, fts_server)
            if substate <=20:
                proceed = submit_new(args.missdir, fts_server)
        print 'Sleep 10 seconds'
        time.sleep(10)
