# src/chunker.py
# -------------------------
# This file breaks a file into 4KB chunks.
# Very simple, clean code.

CHUNK_SIZE = 4096   # 4 KB

def chunk_file(path):
    """
    Reads a file and yields (chunk_data) each of size 4KB.
    """
    with open(path, "rb") as f:
        while True:
            data = f.read(CHUNK_SIZE)
            if not data:
                break
            yield data
