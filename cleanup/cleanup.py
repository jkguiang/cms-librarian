import argparse
import glob
import os
from subprocess import Popen, PIPE
from itertools import islice
from haddnano import haddNano

class MessyDir:
    def __init__(self, path, min_chunk_size, globber="output_*"):
        self.path = path
        self.root_files = glob.glob(f"{path}/{globber}.root")
        # Get directory size in bytes
        du_cmd = Popen(f"du -bs {path}".split(), stdout=PIPE, stderr=PIPE)
        resp = du_cmd.communicate()
        self.size = int(resp[0].decode("utf-8").split("\t")[0])
        # Get number of files for each chunk (may be uneven)
        n_files_total = len(self.root_files)
        n_chunks = int(self.size//min_chunk_size)
        chunk_n_files = []
        if n_chunks > 0 and n_chunks < n_files_total:
            chunk_n_files = [n_files_total//n_chunks for _ in range(n_chunks)]
            # Distribute the remainders
            for chunk_i in range(n_files_total%n_chunks):
                chunk_n_files[chunk_i] += 1
        else:
            chunk_n_files = [n_files_total]
        # Organize ROOT files in directory into chunks
        iterator = iter(self.root_files)
        self.chunks = [list(islice(iterator, 0, n_files)) for n_files in chunk_n_files]

    def clean(self):
        if len(self.root_files) == 0:
            print("INFO: no files to merge")
            return
        for chunk_i, chunk in enumerate(self.chunks):
            haddNano(f"{self.path}/merged_{chunk_i}.root", chunk)
            for root_file in chunk:
                os.remove(root_file)

def cleanup(basedir, min_chunk_size, globber):
    if min_chunk_size < 10*10**6:
        print("ERROR: minimum chunk size less than 10 MB")
        return
    for path in glob.glob(f"{basedir}/*"):
        if os.path.isdir(path):
            print(f"Cleaning up {path}")
            messydir = MessyDir(path, min_chunk_size, globber=globber)
            messydir.clean()

if __name__ == "__main__":
    cli = argparse.ArgumentParser(description="Merge ROOT files in messy subdirs")
    cli.add_argument(
        "basedir", type=str,
        help="base dir of subdirs to clean up"
    )
    cli.add_argument(
        "-c", "--chunksize", type=int, default=20*10**6,
        help="minimum chunk size in bytes (default 20 MB; must be > 10 MB)"
    )
    cli.add_argument(
        "-g", "--globber", type=int, default="output_*",
        help="wildcard pattern for ROOT files to merge"
    )
    args = cli.parse_args()
    cleanup(args.basedir, args.chunksize, args.globber)
