markdown
# NIC eProcurement Tender Scraper (India)

A **production-ready Python automation system** to scrape tenders from **all NIC GePN–based e-Procurement portals in India** — covering **States, UTs, Central Government, CPSEs, PSUs, Defence, Power, Infrastructure, and Strategic agencies** — with **strong identity hashing, bulletproof deduplication, and historical tracking**.

This tool is designed for **daily execution**, **zero false positives**, and **long-term data integrity**.

---

## 🚀 Key Capabilities

- 🔍 Keyword-based tender search (default: `batter`)
- 🌍 Covers **States, UTs, Central Govt, CPSEs, PSUs, Defence & Infra portals**
- 🧠 **Tender-ID–only identity hashing (production-safe)**
- 🧱 **DOM-level + Excel-level deduplication**
- 🆕 Accurate `New Today` flagging (idempotent across runs)
- 📊 Maintains a single historical Excel master file
- 📅 Tracks **First Seen Date** for every tender
- ♻️ Automatic retry handling for DNS / network failures
- 🖱️ One-click execution via Windows batch launcher
- 🧩 Portal-specific handling (e.g. NTPC popup auto-close)
- 🧪 Deterministic results across repeated runs

---

## 🌐 Covered Portals

### 🏛️ State & Union Territory NIC GePN Portals
All Indian States & Union Territories using:
```

*.gov.in/nicgep/app

```

### 🇮🇳 Central Government
- **Central Government e-Procurement**  
  https://eprocure.gov.in/eprocure/app

### 🏢 Central Public Sector Enterprises (CPSE)
- **CPSE e-Procurement**  
  https://etenders.gov.in/eprocure/app

### ⚡ Power & Energy
- **NTPC Limited**  
  https://eprocurentpc.nic.in/nicgep/app  
- **BHEL**  
  https://eprocurebhel.co.in/nicgep/app  
- **BEL (Defence Electronics)**  
  https://eprocurebel.co.in/nicgep/app  

### 🛢️ Oil, Gas & Process Industries
- **Indian Oil Corporation Ltd (IOCL)**  
  https://iocletenders.nic.in/nicgep/app  
- **CPCL**  
  https://cpcletenders.nic.in/nicgep/app  

### 🚢 Shipbuilding & Heavy Engineering
- **Mazagon Dock Shipbuilders Ltd**  
  https://eprocuremdl.nic.in/nicgep/app  
- **Hindustan Shipyard Ltd**  
  https://eprocurehsl.nic.in/nicgep/app  
- **Goa Shipyard Ltd**  
  https://eprocuregsl.nic.in/nicgep/app  
- **Garden Reach Shipbuilders & Engineers (GRSE)**  
  https://eprocuregrse.co.in/nicgep/app  

### 🏗️ Infrastructure & Mining
- **Coal India Limited**  
  https://coalindiatenders.nic.in/nicgep/app  
- **PMGSY**  
  https://pmgsytenders.gov.in/nicgep/app  

### 🛡️ Defence & Strategic
- **Defence e-Procurement Portal**  
  https://defproc.gov.in/nicgep/app  
- **MIDHANI (Mishra Dhatu Nigam Limited)**  
  https://eprocuremidhani.nic.in/nicgep/app  

---

## 🧠 Strong Data Extraction Methodology

### 🔑 Tender ID Extraction (Authoritative Key)

NIC GePN portals consistently follow this pattern:

```

[Title / Description] [Reference / NIT] [ACTUAL_TENDER_ID]

```

Example:
```

[Work of Supply and Commissioning of Battery Bank]
[Tender-09/25-26]
[2026_ED_27105_2]

````

📌 **Rule applied**:
- Extract the **LAST bracket value**
- This value is treated as the **single source of truth**
- All identity, deduplication, and comparison logic is based on this key

---

## 🔐 Identity Hashing (Deduplication Backbone)

### Why Tender-ID-Only Hashing?

- Tender ID is:
  - Issuer-generated
  - Immutable
  - Unique across the entire NIC ecosystem
- State names, titles, dates, and organisations may vary or normalize differently over time

### ✅ Identity Hash Formula

```text
Identity Hash = SHA256(Tender ID)
````

✔ No normalization
✔ No date dependency
✔ No state-name dependency
✔ Stable across Excel reads / writes
✔ Stable across multiple runs

This guarantees:

* **Zero false duplicates**
* **Zero false “New Today” flags**
* **Idempotent daily execution**

---

## 🧠 In-Memory vs Excel Comparison (How It Works)

1. **Load existing Excel**
2. Read `Identity Hash` column
3. Build an in-memory set of known hashes
4. Scrape new tenders
5. Compute `Identity Hash` for each scraped tender
6. Compare:

```python
if identity_hash in existing_hashes:
    New Today = "NO"
else:
    New Today = "YES"
```

7. Append new tenders
8. Drop duplicates by `Identity Hash`
9. Save Excel

📌 **Result**:

* First run → all tenders = `YES`
* Second run → same tenders = `NO`
* Only truly new Tender IDs → `YES`

---

## 📁 Output Overview

The scraper generates or updates:

```
NIC_Batter_Tenders_All_States.xlsx
```

### 📊 Excel Columns

| Column Name                 | Description                        |
| --------------------------- | ---------------------------------- |
| State/UT                    | State, UT, or Central / PSU entity |
| S.No                        | Serial number from portal          |
| e-Published Date            | Tender publish date                |
| Closing Date                | Bid submission closing date        |
| Opening Date                | Bid opening date                   |
| Title and Ref.No./Tender ID | Full tender text                   |
| Tender ID                   | Extracted final bracket value      |
| Organisation Chain          | Issuing authority                  |
| First Seen Date             | Date when tender first appeared    |
| Identity Hash               | SHA256(Tender ID)                  |
| New Today                   | YES only on first discovery        |

---

## 🧪 Sample Console Output

![Sample console execution](https://raw.githubusercontent.com/SatadruNoob/e-proc-site-data-scrapper/57b4075294d72ab6c64c2587f2cddbe2f287cb26/file_00000000ae0c7208a7a2b22b6d18e355%20\(1\).png)

---

## 🛠️ Tech Stack

* Python 3.10+
* Playwright (Chromium)
* Pandas
* OpenPyXL
* Async-safe (Colab / Jupyter compatible)
* Windows-friendly execution

---

## ▶️ Running the Scraper

### Option 1: Direct Run

```bash
python eproc_data_scraper.py
```

### Option 2: One-Click Windows Launcher (Recommended)

This repository includes:

```
run_eproc_scraper.bat
```

Features:

* Auto-creates & activates virtual environment
* Installs dependencies (first run only)
* Installs Playwright Chromium (first run only)
* Runs scraper with a single double-click

---

## 🔁 Retry & Failure Handling

* Each portal retried up to 3 times
* Network / DNS failures isolated per portal
* Failed portals do **not** crash the run
* Partial data is preserved safely

---

## 📌 Use Cases

* Daily tender monitoring
* PSU / Defence opportunity scanning
* Business development & bid tracking
* Market intelligence pipelines
* Procurement automation
* Dashboard & alert integrations

---

## 🔒 Compliance & Ethics

* Scrapes **publicly available data only**
* No authentication bypass
* No CAPTCHA circumvention
* Designed for responsible, compliant usage

---

## 🧭 Roadmap

* Email alerts for new tenders
* Closed / expired tender detection
* Power BI / Tableau ready exports
* Parallel async scraping
* Windows Task Scheduler / CI automation

---

## 🤝 Contributions

Contributions, improvements, and issue reports are welcome.
Please open an issue or submit a pull request.

---

## 📄 License

Released under the **MIT License**

```

---

If you want next, I can also deliver (one-shot copies):

- `ARCHITECTURE.md` (hashing & data-flow diagrams)
- `CHANGELOG.md` (pre-hash vs post-hash evolution)
- `CONTRIBUTING.md`
- CI-ready GitHub Actions workflow
- Excel schema migration notes

Just say the word.
```
