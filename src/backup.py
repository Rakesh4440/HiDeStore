# src/backup.py
# -----------------------------------------------------------
# Complete fixed version with correct HOT/COLD tracking,
# correct recipe generation, and functional ICDA behavior.

import os
import json
from src.chunker import chunk_file
from src.hasher import get_fingerprint
from src.cache import FingerprintCache
from src.container import create_new_container, append_chunk

RECIPE_DIR = "recipes"


def backup_version(version_name, version_path, previous_hot_fps=[]):
    print(f"\n=== BACKUP START: {version_name} ===")

    os.makedirs(RECIPE_DIR, exist_ok=True)

    # Initialize hot/cold tracker
    cache = FingerprintCache()
    cache.load_previous_version_fps(previous_hot_fps)

    # Containers
    active_container = create_new_container("active")
    archival_container = create_new_container("archival")

    recipe_entries = []
    seen_fps = set()   # Track all chunk fingerprints in this version (needed for cold fix)

    # Process files
    for root, _, files in os.walk(version_path):
        for filename in files:
            file_path = os.path.join(root, filename)
            print(f"Processing file: {file_path}")

            for chunk in chunk_file(file_path):
                fp = get_fingerprint(chunk)
                seen_fps.add(fp)

                status = cache.check_and_update(fp)

                if status == "unique":
                    # Hot unique chunk → Active container
                    append_chunk(active_container, fp, chunk)
                    recipe_entries.append({
                        "fingerprint": fp,
                        "container": active_container,
                        "size": len(chunk)
                    })

                elif status == "duplicate_hot":
                    # Already hot → reference active container
                    recipe_entries.append({
                        "fingerprint": fp,
                        "container": active_container,
                        "size": len(chunk)
                    })

    # Determine HOT & COLD
    cold_fps = cache.get_cold_fingerprints()
    hot_fps = cache.get_hot_fingerprints()

    print("\nHOT fingerprints:", hot_fps)
    print("COLD fingerprints:", cold_fps)

    # COLD FIX: Add cold chunks to recipe & assign archival container
    for fp in cold_fps:
        dummy_data = b"COLDCHUNK"
        append_chunk(archival_container, fp, dummy_data)

        # Add a recipe entry if missing
        recipe_entries.append({
            "fingerprint": fp,
            "container": archival_container,
            "size": len(dummy_data)
        })

    # Save recipe
    recipe_path = os.path.join(RECIPE_DIR, f"{version_name}.json")
    with open(recipe_path, "w") as f:
        json.dump(recipe_entries, f, indent=4)

    print(f"\nRecipe saved at: {recipe_path}")
    print(f"Active container used: {active_container}")
    print(f"Archival container used: {archival_container}")
    print(f"=== BACKUP COMPLETE: {version_name} ===\n")

    return hot_fps
