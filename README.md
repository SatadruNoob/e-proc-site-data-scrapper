Perfect — below is a ONE-SHOT, SINGLE COPY-PASTE READY README.md.

👉 Just click once, copy everything, and paste directly into README.md on GitHub.
No explanations, no breaks, no formatting issues.


---

# NIC eProcurement Tender Scraper (India)

A robust, production-grade Python automation tool to scrape tenders from all NIC GePN e-Procurement portals across Indian States and Union Territories, track new tenders daily, and maintain a deduplicated historical Excel database.

---

## 🚀 Features

- 🔍 Searches tenders using a configurable keyword (default: `batter`)
- 🌍 Covers all Indian States & Union Territories via NIC GePN portals
- ♻️ Automatic retry handling for network/DNS failures
- 📊 Generates and maintains a single Excel master file
- 🆕 Flags newly discovered tenders using a `New Today` column
- 🗂️ Preserves historical tender data (no overwrites, no duplicates)
- 🧠 Tracks First Seen Date for every tender
- 🖱️ One-click execution via Windows batch launcher
- 🧱 Built on Playwright for reliability and dynamic content handling

---

## 📁 Output Overview

The scraper generates or updates the following Excel file:

NIC_Batter_Tenders_All_States.xlsx

### 📊 Columns in Excel

| Column Name | Description |
|------------|------------|
| State/UT | State or Union Territory |
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

- YES → Tender did not exist in Excel before this run  
- NO → Tender already existed from previous runs  
- Multiple runs on the same day do not duplicate data  

Ideal for daily monitoring, opportunity alerts, and market intelligence.

---

## 🛠️ Tech Stack

- Python 3.10+
- Playwright (Chromium)
- Pandas
- OpenPyXL
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
playwright install


---

▶️ Running the Scraper

Option 1: Run directly

python eproc_data_scraper.py

Option 2: One-click Windows launcher

Use the provided batch file:

run_eproc_scraper.bat

This automatically:

Activates the virtual environment

Runs the scraper

Keeps the console open for logs



---

🔁 Retry & Failure Handling

Each State/UT is retried up to 3 times

DNS/network failures are isolated per state

Failed states are recorded in Excel for visibility

Script never crashes due to a single portal failure



---

🧪 Sample Console Output

🔍 Searching in Maharashtra
  Attempt 1

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

Closed tender detection

Power BI / Tableau-ready outputs

Parallel scraping for faster execution

Windows Task Scheduler integration



---

🤝 Contributions

Contributions, improvements, and issue reports are welcome.
Please open an issue or submit a pull request.


---

📄 License

This project is released under the MIT License.


---

📬 Contact

For customization, enterprise deployment, or support, feel free to reach out.


---

Built for reliability. Designed for daily automation.

---

If you want next, I can also give you (one-shot copies):
- `CONTRIBUTING.md`
- `LICENSE`
- `run_eproc_scraper.bat`
- GitHub badges
- GitHub Actions workflow

Just say the word.
