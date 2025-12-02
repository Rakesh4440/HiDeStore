# src/cache.py
# ---------------------------------------------------------
# Double-hash fingerprint cache (T1 = old version, T2 = new version)
# This decides which chunks are HOT or COLD.


class FingerprintCache:
    def __init__(self):
        # T1 = previous version's hot fingerprints
        # T2 = current version's hot fingerprints
        self.T1 = {}
        self.T2 = {}

    def load_previous_version_fps(self, fingerprint_list):
        """
        Preload T1 with fingerprints from last version (HOT)
        """
        self.T1 = {fp: True for fp in fingerprint_list}
        self.T2 = {}

    def check_and_update(self, fingerprint):
        """
        Process a new chunk fingerprint.
        Returns:
            "unique" -> new fingerprint
            "duplicate_hot" -> was hot previously (T1 or T2)
        """

        # Case 1: fingerprint in T1 -> HOT chunk
        if fingerprint in self.T1:
            # Move from T1 to T2
            self.T2[fingerprint] = True
            del self.T1[fingerprint]
            return "duplicate_hot"

        # Case 2: fingerprint already in T2 -> HOT duplicate within same version
        if fingerprint in self.T2:
            return "duplicate_hot"

        # Case 3: fingerprint not found -> NEW unique chunk
        self.T2[fingerprint] = True
        return "unique"

    def get_hot_fingerprints(self):
        """Return list of hot chunk fingerprints after finishing version"""
        return list(self.T2.keys())

    def get_cold_fingerprints(self):
        """Fingerprints left in T1 are cold (not reused)"""
        return list(self.T1.keys())
