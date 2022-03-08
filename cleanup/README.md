# Cleanup Scripts
1. `clean_nano.py`
    - Merges NanoAOD files (using `haddnano.py`) into appropriately sized chunks
    - Uses Python3, so CMSSW 11.X.x or greater is required
2. `archiveall.sh`
    - Tars each subdirectory in a given directory into a tarball
    - Useful for files that are not easily mergable (e.g. LHE files)
