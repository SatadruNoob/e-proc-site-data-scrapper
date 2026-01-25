# NIC eProcurement Tender Scraper (India)

A robust, production-grade Python automation tool to scrape tenders from **all NIC GePN–based e-Procurement portals in India**, including **State/UT portals, Central Government, CPSEs, PSUs, Defence, and Infrastructure agencies**, track new tenders daily, and maintain a deduplicated historical Excel database.

---

## 🚀 Features

- 🔍 Searches tenders using a configurable keyword (default: `batter`)
- 🌍 Covers **States, UTs, Central Govt, CPSEs, PSUs, Defence & Infra portals**
- ♻️ Automatic retry handling for network/DNS failures
- 📊 Generates and maintains a single Excel master file
- 🆕 Flags newly discovered tenders using a `New Today` column
- 🗂️ Preserves historical tender data (no overwrites, no duplicates)
- 🧠 Tracks *First Seen Date* for every tender
- 🖱️ One-click execution via Windows batch launcher
- 🧱 Built on Playwright for reliability and dynamic content handling
- 🧩 Portal-specific handling (e.g. NTPC popup auto-close)

---

## 🌐 Covered Portals

### 🏛️ State & Union Territory NIC GePN Portals
- All Indian States & Union Territories using `*.gov.in/nicgep/app`

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



---

## 📁 Output Overview

The scraper generates or updates:

NIC_Batter_Tenders_All_States.xlsx

### 📊 Excel Columns

| Column Name | Description |
|--------------|-------------|
| State/UT | State, UT, or Central/PSU entity |
| S.No | Serial number from portal |
| e-Published Date | Tender publish date |
| Closing Date | Bid submission closing date |
| Opening Date | Bid opening date |
| Title and Ref.No./Tender ID | Tender title with reference and ID |
| Organisation Chain | Issuing authority |
| First Seen Date | Date when tender first appeared |
| New Today | YES if new in current run, otherwise NO |

---

## 🧠 How “New Today” Works

- **YES** → Tender not present in Excel before this run  
- **NO** → Tender already exists from previous runs  
- Multiple runs on the same day do **not** duplicate data  

Ideal for **daily monitoring**, **bid opportunity alerts**, and **market intelligence**.

---

## 🛠️ Tech Stack

- Python 3.10+
- Playwright (Chromium)
- Pandas
- OpenPyXL
- Async-safe (Colab / Jupyter compatible)
- Windows-friendly execution

---

## 📦 Installation

### 1️⃣ Clone the repository

```bash
git clone https://github.com/your-username/nic-eproc-tender-scraper.git
cd nic-eproc-tender-scraper

2️⃣ Create and activate virtual environment

python -m venv venv

Windows (PowerShell)

venv\Scripts\Activate.ps1

3️⃣ Install dependencies

pip install playwright pandas openpyxl
playwright install chromium


---

▶️ Running the Scraper

Option 1: Run directly

python eproc_data_scraper.py


Option 2: One-click Windows launcher (Recommended for Windows)

This repository includes a ready-to-use Windows batch file:

`run_eproc_scraper.bat`

Features:
- Automatically creates and activates a virtual environment
- Installs required Python dependencies (first run only)
- Installs Playwright Chromium (first run only)
- Runs the scraper with a single double-click
- Works regardless of where the batch file is launched from

Simply double-click `run_eproc_scraper.bat` to run the scraper.

---

🔁 Retry & Failure Handling

Each portal retried up to 3 times

DNS/network failures isolated per portal

Failed portals recorded in Excel

Script never crashes due to a single portal failure



---

🧪 Sample Console Output

🔍 Searching in Maharashtra
  Attempt 1

🔍 Searching in NTPC Limited
  Attempt 1
  (Popup closed automatically)

🔍 Searching in Goa
  Attempt 1
  ⚠ Error: net::ERR_NAME_NOT_RESOLVED
  Attempt 2
  Attempt 3

✅ Done. Excel updated with 'New Today' column.


---

📌 Use Cases

Daily tender monitoring

Business development & bid tracking

PSU / Defence opportunity scanning

Market intelligence

Procurement automation

Integration with email alerts or dashboards



---

🔒 Compliance & Ethics

Scrapes publicly available data only

No authentication bypass

No CAPTCHA circumvention

Designed for responsible and compliant usage



---

🧭 Roadmap

Email alerts for New Today tenders

Closed / expired tender detection

Power BI / Tableau-ready datasets

Parallel async scraping for speed

Windows Task Scheduler & CI automation



---

🤝 Contributions

Contributions, improvements, and issue reports are welcome.
Please open an issue or submit a pull request.


---

📄 License

Released under the MIT
