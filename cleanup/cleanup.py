import argparse
import glob
import os
from subprocess import Popen, PIPE
from itertools import islice
from haddnano import haddNano

def clean_dir(path, min_chunk_size, globber="output_*"):
    # Retrieve ROOT files to merge
    root_files = glob.glob(f"{path}/{globber}.root")
    if len(root_files) == 0:
        print("INFO: no files to merge")
        return
    # Get directory size in bytes
    du_cmd = Popen(f"du -bs {path}".split(), stdout=PIPE, stderr=PIPE)
    resp = du_cmd.communicate()
    size = int(resp[0].decode("utf-8").split("\t")[0])
    # Get number of files for each chunk (may be uneven)
    n_files_total = len(root_files)
    n_chunks = int(size//min_chunk_size)
    chunk_n_files = []
    if n_chunks > 0 and n_chunks < n_files_total:
        chunk_n_files = [n_files_total//n_chunks for _ in range(n_chunks)]
        # Distribute the remainders
        for chunk_i in range(n_files_total%n_chunks):
            chunk_n_files[chunk_i] += 1
    else:
        chunk_n_files = [n_files_total]
    # Organize ROOT files in directory into chunks
    iterator = iter(root_files)
    chunks = [list(islice(iterator, 0, n_files)) for n_files in chunk_n_files]
    # Merge ROOT files
    for chunk_i, chunk in enumerate(chunks):
        haddNano(f"{path}/merged_{chunk_i}.root", chunk)
        for root_file in chunk:
            os.remove(root_file)

def clean_subdirs(basedir, min_chunk_size, globber="output_*"):
    if min_chunk_size < 10*10**6:
        print("ERROR: minimum chunk size less than 10 MB")
        return
    for path in glob.glob(f"{basedir}/*"):
        if os.path.isdir(path):
            print(f"Cleaning up {path}")
            clean_dir(path, min_chunk_size, globber=globber)

if __name__ == "__main__":
    cli = argparse.ArgumentParser(description="Merge ROOT files in messy directories")
    cli.add_argument(
        "basedir", type=str,
        help="base directory to clean up"
    )
    cli.add_argument(
        "-c", "--chunksize", type=int, default=20*10**6,
        help="minimum chunk size in bytes (must be > 10 MB; default: 20 MB)"
    )
    cli.add_argument(
        "-g", "--globber", type=int, default="output_*",
        help="wildcard pattern for ROOT files to merge (default: 'output_*')"
    )
    cli.add_argument(
        "--no_subdirs", action="store_true",
        help="indicate that there are no subdirectories in basedir"
    )
    args = cli.parse_args()
    if args.no_subdirs:
        clean_dir(args.basedir, args.chunksize, globber=args.globber)
    else:
        clean_subdirs(args.basedir, args.chunksize, args.globber)
