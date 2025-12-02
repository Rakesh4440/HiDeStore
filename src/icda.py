# src/icda.py
# -----------------------------------------------------------
# ICDA: delete old versions by deleting their archival containers.

import os
import json

RECIPE_DIR = "recipes"
ARCHIVAL_DIR = "storage/archival"


def delete_version(version_name):
    recipe_path = os.path.join(RECIPE_DIR, f"{version_name}.json")

    if not os.path.exists(recipe_path):
        print("Recipe not found:", recipe_path)
        return

    print(f"\n=== DELETE START: {version_name} ===")

    # Load recipe
    with open(recipe_path, "r") as f:
        recipe = json.load(f)

    # Collect archival containers used
    archival_containers_used = set()

    for entry in recipe:
        container_path = entry["container"]
        # If it is an archival container
        if "archival" in container_path.replace("/", "\\"):
            archival_containers_used.add(container_path)

    # Delete archival containers
    deleted = []
    for cont in archival_containers_used:
        if os.path.exists(cont):
            os.remove(cont)
            deleted.append(cont)

    print("Deleted archival containers:", deleted)

    # Delete recipe file also
    os.remove(recipe_path)
    print("Deleted recipe:", recipe_path)

    print(f"=== DELETE COMPLETE: {version_name} ===\n")
