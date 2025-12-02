# src/container.py
# --------------------------------------------------------
# This file handles writing/reading chunks to containers.

import os
import json

ACTIVE_DIR = "storage/active"
ARCHIVAL_DIR = "storage/archival"

CONTAINER_MAX_SIZE = 4 * 1024 * 1024   # 4MB


def ensure_dirs():
    """Make sure container folders exist."""
    os.makedirs(ACTIVE_DIR, exist_ok=True)
    os.makedirs(ARCHIVAL_DIR, exist_ok=True)


def create_new_container(container_type):
    """
    Creates a new container file.
    container_type = 'active' or 'archival'
    Returns: container_path
    """
    ensure_dirs()

    if container_type == "active":
        dir_path = ACTIVE_DIR
    else:
        dir_path = ARCHIVAL_DIR

    # Count existing files to generate new ID
    count = len(os.listdir(dir_path))
    filename = f"container_{count}.bin"
    path = os.path.join(dir_path, filename)

    # Create empty file
    open(path, "wb").close()

    return path


def append_chunk(container_path, fingerprint, chunk_data):
    """
    Writes chunk into a container file.
    Format stored:
        [fingerprint length][fingerprint bytes][chunk length][chunk bytes]
    """
    with open(container_path, "ab") as f:
        fp_bytes = fingerprint.encode()
        chunk_len = len(chunk_data)

        # Write fingerprint size + fingerprint
        f.write(len(fp_bytes).to_bytes(4, "big"))
        f.write(fp_bytes)

        # Write chunk size + chunk data
        f.write(chunk_len.to_bytes(4, "big"))
        f.write(chunk_data)


def read_chunks_from_container(container_path):
    """
    Reads all chunks stored in a container.
    Returns list of (fingerprint, chunk_data)
    """
    chunks = []
    with open(container_path, "rb") as f:
        data = f.read()

    i = 0
    while i < len(data):
        # fingerprint length
        fp_len = int.from_bytes(data[i:i+4], "big")
        i += 4

        fp = data[i:i+fp_len].decode()
        i += fp_len

        # chunk length
        c_len = int.from_bytes(data[i:i+4], "big")
        i += 4

        chunk = data[i:i+c_len]
        i += c_len

        chunks.append((fp, chunk))

    return chunks
