# Ceph Migration
Scripts stolen from Justas Balcas with some modifications by me. Must be run with root permissions.

## Instructions
1. Create a proxy for a user (e.g. `/tmp/x509up_u00000`) that has the appropriate writing permissions on Ceph
2. Stage one user as a test; look inside `user/USER` to see what was produced
```
sh stage.sh USER
```
3. Submit migration jobs for that user (best to submit in a screen)
```
screen -S mvUSER
export X509_USER_PROXY=/tmp/x509up_u00000
python2 migrator.py --fnal $PWD/users/USER/missing
ctrl+A+D
```
4. Wait for the results; you can check on the transfers by running the following:
```
sh fts-status-checker.sh USER all fnal
```
5. If things go well, you can stage all users (you may want to do this in a screen as well)
```
sh stageall.sh
```
6. Again in a screen, you can then migrate all users
```
screen -S mvUSER
export X509_USER_PROXY=/tmp/x509up_u00000
sh migrateall.sh
ctrl+A+D
```

## Notes
- A user with "appropriate" writing permissions on Ceph must be able to write to any user's directory
    - The `stage.sh` script will make a new Ceph directory using `mkcephdir.sh` that is owned by that user, but has file access control lists that allow the user `tmartin` to write to it; this user should be changed to whichever user's proxy is being used for the FTS transfers
- The `migrateall.sh` script will alternate between using the CMS and FNAL FTS servers
