# src/restore.py
# --------------------------------------------------------
# Restores a version based on its recipe.

import os
import json
from src.container import read_chunks_from_container


def restore_version(version_name, output_folder):
    recipe_path = os.path.join("recipes", f"{version_name}.json")

    if not os.path.exists(recipe_path):
        print("Recipe not found:", recipe_path)
        return

    os.makedirs(output_folder, exist_ok=True)

    print(f"\n=== RESTORE START: {version_name} ===")

    # Load recipe
    with open(recipe_path, "r") as f:
        recipe = json.load(f)

    # Create a mapping: container -> loaded chunks
    container_cache = {}

    restored_data = b""

    for entry in recipe:
        fp = entry["fingerprint"]
        container_path = entry["container"]

        # Load container chunks if not loaded before
        if container_path not in container_cache:
            print(f"Reading container: {container_path}")
            container_cache[container_path] = read_chunks_from_container(container_path)

        # Find the chunk by fingerprint
        chunks = container_cache[container_path]

        for cfp, chunk in chunks:
            if cfp == fp:
                restored_data += chunk
                break

    # Save reconstructed file
    out_file = os.path.join(output_folder, "restored_file.txt")

    with open(out_file, "wb") as f:
        f.write(restored_data)

    print(f"Restored file saved at: {out_file}")
    print(f"Total containers read: {len(container_cache)}")
    print(f"=== RESTORE COMPLETE: {version_name} ===\n")
