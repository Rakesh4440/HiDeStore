# src/hasher.py
# -----------------------------------
# Computes SHA-1 fingerprint for a chunk.

import hashlib

def get_fingerprint(chunk_data):
    """
    Returns the SHA-1 fingerprint of the given chunk data.
    Output: a hex string
    """
    sha1 = hashlib.sha1()
    sha1.update(chunk_data)
    return sha1.hexdigest()
