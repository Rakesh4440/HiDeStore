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


