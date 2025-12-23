# 🚀 HiDeStore – Enhanced Physical-Locality Deduplication System (Python Prototype)

This project is a working prototype based on the research paper:

**“An Enhanced Physical-Locality Deduplication System for Space Efficiency”**

It demonstrates how modern backup systems improve restore speed and storage locality by separating data chunks into:

- 🔥 **Hot Chunks** (likely to reappear)
- ❄️ **Cold Chunks** (unlikely to reappear)

Hot chunks are stored in **Active Containers**, cold chunks in **Archival Containers**.  
This improves **restore locality** and enables **instant deletion of old versions (ICDA)**.

---

## ⭐ Features

| Feature | Status |
|--------|--------|
| 4KB File Chunking | ✔️ |
| SHA-1 Fingerprinting | ✔️ |
| Hot/Cold Classification (T1/T2) | ✔️ |
| Active Containers (hot data) | ✔️ |
| Archival Containers (cold data) | ✔️ |
| Recipe JSON per version | ✔️ |
| Restore from recipe | ✔️ |
| ICDA – Instant Cold Data Deletion | ✔️ |
| Command-Line Interface | ✔️ |

---
Steps to run

HiDeStore – Versioned Backup, Restore, and Instant Delete Demonstration

This project demonstrates a HiDeStore-based deduplication system that supports
multi-version backups, efficient storage using HOT and COLD chunks,
recipe-based restoration, and instant deletion using ICDA (Instant Container Deletion Algorithm).

The demo is performed using three versions of data: v1, v2, and v3.

--------------------------------------------------------------------

RESET ENVIRONMENT (START FRESH)

Command:
cd D:\HIDESTORE
Remove-Item -Recurse -Force storage\*, recipes\*, restores\*, hot_tracker.json -ErrorAction SilentlyContinue

Explanation:
This command removes all previously stored containers, backup recipes,
restored outputs, and the HOT chunk tracker to ensure a clean environment.

--------------------------------------------------------------------

DELETE OLD VERSION DATA

Command:
Remove-Item -Recurse -Force data\v1, data\v2, data\v3 -ErrorAction SilentlyContinue

Explanation:
This deletes all old version directories so that new versions can be created from scratch.

--------------------------------------------------------------------

CREATE FRESH VERSION DIRECTORIES

Command:
New-Item -ItemType Directory -Force data\v1
New-Item -ItemType Directory -Force data\v2
New-Item -ItemType Directory -Force data\v3

Explanation:
This creates three separate directories representing three versions of the data.

--------------------------------------------------------------------

CREATE DATA FOR VERSION 1

Command:
Set-Content data\v1\file1.txt "This is version 1.`nThe project has started.`nEverything is new in this version."
Set-Content data\v1\notes.txt "These are notes for version 1.`nNo major updates yet."

Explanation:
Version 1 contains completely new data, so all chunks in this version will be classified as HOT chunks.

--------------------------------------------------------------------

CREATE DATA FOR VERSION 2

Command:
Set-Content data\v2\file1.txt "This is version 2.`nThe project has started.`nEverything is new in this version.`nOne new line is added in version 2."
Set-Content data\v2\file2.txt "This is a new file in version 2.`nIt contains some extra information."

Explanation:
Version 2 reuses many lines from version 1 but adds one new line and one new file.
Only the new content will be classified as COLD chunks.

--------------------------------------------------------------------

CREATE DATA FOR VERSION 3

Command:
Set-Content data\v3\file1.txt "This is version 3.`nThe project is almost finished.`nSome lines have changed in this version."

Explanation:
Version 3 changes multiple lines, resulting in more COLD chunks being generated.

--------------------------------------------------------------------

VERIFY ALL VERSIONS

Command:
Get-ChildItem data -Recurse

Explanation:
This displays all files in v1, v2, and v3 to verify that the versions were created correctly.

--------------------------------------------------------------------

BACKUP VERSION 1

Command:
python -m src.cli backup v1 data/v1

Explanation:
This performs the first backup.
Since all data is new, all chunks are treated as HOT and stored in active containers.
A recipe file for version 1 is created.

Verification Commands:
Get-Content recipes\v1.json
Get-ChildItem storage -Recurse

--------------------------------------------------------------------

BACKUP VERSION 2

Command:
python -m src.cli backup v2 data/v2

Explanation:
This backup detects duplicate chunks from version 1.
Only the new line and the new file are stored as COLD chunks in archival containers.
A recipe file for version 2 is generated.

Difference Check Command:
Compare-Object (Get-Content data\v1\file1.txt) (Get-Content data\v2\file1.txt)

--------------------------------------------------------------------

BACKUP VERSION 3

Command:
python -m src.cli backup v3 data/v3

Explanation:
This backup detects multiple modified lines.
Most chunks in this version are classified as COLD chunks and stored separately.

Difference Check Command:
Compare-Object (Get-Content data\v2\file1.txt) (Get-Content data\v3\file1.txt)

--------------------------------------------------------------------

RESTORE VERSION 2

Command:
python -m src.cli restore v2 restores/v2

Explanation:
This restores version 2 using its recipe file.
Required chunks are fetched from storage and the original version 2 data is reconstructed exactly.

Verification Command:
Get-Content restores\v2\restored_file.txt

--------------------------------------------------------------------

DELETE VERSION 2 (ICDA)

Command:
python -m src.cli delete v2

Explanation:
This deletes version 2 instantly using ICDA.
Only the COLD containers related to version 2 are removed.
No scanning of storage is required.

Verification Command:
Test-Path recipes\v2.json

Expected Output:
False

--------------------------------------------------------------------

CONCLUSION

This demonstration shows how HiDeStore:
- Separates HOT and COLD chunks for efficient storage
- Reduces redundancy across multiple versions
- Restores data accurately using recipes
- Deletes versions instantly using ICDA without scanning

--------------------------------------------------------------------


