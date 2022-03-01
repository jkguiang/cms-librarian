# Making Hadoop Reports (Hadoop Snooping)

1. `./mkreports --users [--nolist]`
    - Runs `ls -R` and `du` on hadoop user areas to get access (roughly) and usage metrics
    - Writes access report to `user_reports/YEAR-MM-DD/user_access_report.txt.gz`
    - Writes usage report to `user_reports/YEAR-MM-DD/user_usage_report.txt.gz`
    - Writes list of all files to `user_reports/YEAR-MM-DD/all_user_files.txt.gz` (skipped if `--nolist` is used)
2. `./mkreports --phedex [--nolist]`
    - Runs `ls -R` on hadoop phedex areas to get list of all files
    - Writes list of all files to `phedex_reports/YEAR-MM-DD/all_phedex_files.txt.gz` (skipped if `--nolist` is used)
3. `./mkreports --users --phedex`
    - Runs (1) and (2)
