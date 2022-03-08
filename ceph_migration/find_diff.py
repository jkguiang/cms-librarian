
allCephFiles = {}

with open('allCeph') as fd:
    lines = fd.readlines()
    for line in lines:
        splLine = line.split()
        if len(splLine) == 2:
            allCephFiles[splLine[0]] = splLine[1]
        else:
            print 'WARNING: %s' % splLine


FSIZE_THRESH = 10*1024*1024 # filesize threshold in bytes
excluded_dirs = set()
lines = []
with open('allHdfs') as fd:
    lines = fd.readlines()
for line in lines:
    splLine = line.split()
    if not splLine[0].startswith('d'):
        fname = splLine[7]
        fsize = int(splLine[4])
        dname = "/".join(fname.split("/")[:-1])
        if fsize < FSIZE_THRESH:
            excluded_dirs.add(dname)

last_excl_dir = ""
last_good_dir = ""
for line in lines:
    splLine = line.split()
    if not splLine[0].startswith('d'):
        fname = splLine[7]
        fsize = splLine[4]
        dname = "/".join(fname.split("/")[:-1])
        if not fname in allCephFiles:
            if dname != last_good_dir:
                if dname == last_excl_dir:
                    continue
                elif dname in excluded_dirs:
                    last_excl_dir = dname
                else:
                    last_good_dir = dname
                    print fname
            else:
                print fname
        elif fsize != allCephFiles[fname]:
            print fname
