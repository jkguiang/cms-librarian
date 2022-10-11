import argparse
import glob
import os
from subprocess import Popen, PIPE
from itertools import islice
from haddnano import haddNano

def clean_dir(path, min_chunk_size, globber="output_*", grim_reaper=None):
    """
    Cleans up a given directory by merging NanoAOD files into chunks

    Note: assumes files are approximately the same size
    """
    write_reaper = False
    if grim_reaper == None:   # compare against None because could be empty list
        write_reaper = True
        grim_reaper = []
    print(f"INFO: cleaning up {path}")

    # Retrieve ROOT files to merge
    root_files = glob.glob(f"{path}/{globber}.root")
    if len(root_files) == 0:
        print("INFO: no files to merge")
        return

    # Get directory size in bytes
    du_cmd = Popen(f"du -bs {path}".split(), stdout=PIPE, stderr=PIPE)
    resp = du_cmd.communicate()
    size = int(resp[0].decode("utf-8").split("\t")[0])

    # Get total number of files
    n_files_total = len(root_files)
    if n_files_total == 1:
        print("INFO: only one file; nothing to merge")

    # Get number of files for each chunk (may be uneven)
    n_chunks = int(size//min_chunk_size)
    chunk_n_files = []
    if n_chunks > 0 and n_chunks < n_files_total:
        chunk_n_files = [n_files_total//n_chunks for _ in range(n_chunks)]
        # Distribute the remainders
        for chunk_i in range(n_files_total%n_chunks):
            chunk_n_files[chunk_i] += 1
    elif n_chunks >= n_files_total:
        print("INFO: files are sufficiently chunked")
        return
    else:
        chunk_n_files = [n_files_total]

    # Organize ROOT files in directory into chunks and merge
    grim_reaper.append(f"# Clean up {path}")
    iterator = iter(root_files)
    chunks = [list(islice(iterator, 0, n_files)) for n_files in chunk_n_files]
    for chunk_i, chunk in enumerate(chunks):
        if len(chunks) > 1:
            merged_file = f"{path}/merged_{chunk_i}.root"
        else:
            merged_file = f"{path}/merged.root"
        if os.path.exists(merged_file):
            raise Exception(f"{merged_file} already exists and would be overwritten!")
        # Merge chunk and delete old files
        haddNano(merged_file, chunk)
        for root_file in chunk:
            grim_reaper.append(f"rm {root_file}")

    if write_reaper:
        # Make kill file
        with open("grim_reaper.sh", "w") as f_out:
            f_out.write("\n".join(grim_reaper))

def clean_subdirs(basedir, min_chunk_size, globber="output_*"):
    """Cleans up each subdirectory in a given directory"""
    if min_chunk_size < 10*10**6:
        print("ERROR: minimum chunk size less than 10 MB")
        return
    grim_reaper = []
    for path in glob.glob(f"{basedir}/*"):
        if os.path.isdir(path):
            clean_dir(path, min_chunk_size, globber=globber, grim_reaper=grim_reaper)
    # Make kill file
    with open("grim_reaper.sh", "w") as f_out:
        f_out.write("\n".join(grim_reaper))

if __name__ == "__main__":
    cli = argparse.ArgumentParser(description="Merge NanoAOD ROOT files in messy directories")
    cli.add_argument(
        "basedir", type=str,
        help="base directory to clean up"
    )
    cli.add_argument(
        "-c", "--chunksize", type=int, default=20,
        help="minimum chunk size in MB (must be > 10 MB; default: 20 MB)"
    )
    cli.add_argument(
        "-g", "--globber", type=str, default="output_*",
        help="wildcard pattern for ROOT files to merge (default: 'output_*')"
    )
    cli.add_argument(
        "--no_subdirs", action="store_true",
        help="indicate that there are no subdirectories in basedir"
    )
    args = cli.parse_args()
    if args.no_subdirs:
        clean_dir(args.basedir, args.chunksize*10**6, globber=args.globber)
    else:
        clean_subdirs(args.basedir, args.chunksize*10**6, globber=args.globber)
