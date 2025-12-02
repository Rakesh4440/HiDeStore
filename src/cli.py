# src/cli.py
# -----------------------------------------------------------
# HiDeStore Command-Line Interface

import sys
import os
import json

from src.backup import backup_version
from src.restore import restore_version
from src.icda import delete_version


HOT_TRACKER = "hot_tracker.json"   # Stores last version's HOT fingerprints


def load_hot_list():
    if not os.path.exists(HOT_TRACKER):
        return []
    with open(HOT_TRACKER, "r") as f:
        return json.load(f)


def save_hot_list(hot_fps):
    with open(HOT_TRACKER, "w") as f:
        json.dump(hot_fps, f)


def print_help():
    print("""
HiDeStore CLI Usage:

  Backup a version:
      python src/cli.py backup <version_name> <folder_path>

  Restore a version:
      python src/cli.py restore <version_name> <output_folder>

  Delete a version (ICDA):
      python src/cli.py delete <version_name>

  Show help:
      python src/cli.py help
    """)


def main():
    if len(sys.argv) < 2:
        print_help()
        return

    cmd = sys.argv[1]

    if cmd == "backup":
        if len(sys.argv) != 4:
            print("Usage: python src/cli.py backup <version> <folder>")
            return

        version = sys.argv[2]
        folder = sys.argv[3]

        prev_hot = load_hot_list()

        print(f"Using previous HOT list: {prev_hot}")

        hot_new = backup_version(version, folder, prev_hot)

        save_hot_list(hot_new)

    elif cmd == "restore":
        if len(sys.argv) != 4:
            print("Usage: python src/cli.py restore <version> <output_folder>")
            return

        version = sys.argv[2]
        out_folder = sys.argv[3]
        restore_version(version, out_folder)

    elif cmd == "delete":
        if len(sys.argv) != 3:
            print("Usage: python src/cli.py delete <version>")
            return

        version = sys.argv[2]
        delete_version(version)

    elif cmd == "help":
        print_help()

    else:
        print("Unknown command:", cmd)
        print_help()


if __name__ == "__main__":
    main()
