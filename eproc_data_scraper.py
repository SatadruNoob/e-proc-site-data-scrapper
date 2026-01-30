from playwright.sync_api import sync_playwright
import pandas as pd
import time
import os
import re
import hashlib
from datetime import datetime

# ======================= CONFIG =======================

KEYWORD = "batter"
MAX_RETRIES = 3
OUTPUT_FILE = "NIC_Batter_Tenders_All_States.xlsx"
RUN_DATE = datetime.now().strftime("%Y-%m-%d")

# ======================= PORTALS =======================

SITES = {
    "Andaman": "https://eprocure.andamannicobar.gov.in/nicgep/app",
    "Arunachal": "https://arunachaltenders.gov.in/nicgep/app",
    "Assam": "https://assamtenders.gov.in/nicgep/app",
    "Chandigarh": "https://etenders.chd.nic.in/nicgep/app",
    "UT Nagar": "https://dnhtenders.gov.in/nicgep/app",
    "UT Daman": "https://ddtenders.gov.in/nicgep/app",
    "NCT Delhi": "https://govtprocurement.delhi.gov.in/nicgep/app",
    "Goa": "https://eprocure.goa.gov.in/nicgep/app",
    "Haryana": "https://etenders.hry.nic.in/nicgep/app",
    "Himachal": "https://hptenders.gov.in/nicgep/app",
    "Jammu": "https://jktenders.gov.in/nicgep/app",
    "Jharkhand": "https://jharkhandtenders.gov.in/nicgep/app",
    "Kerala": "https://etenders.kerala.gov.in/nicgep/app",
    "Lakshadweep": "https://tendersutl.gov.in/nicgep/app",
    "Maharashtra": "https://mahatenders.gov.in/nicgep/app",
    "MP": "https://mptenders.gov.in/nicgep/app",
    "Manipur": "https://manipurtenders.gov.in/nicgep/app",
    "Meghalaya": "https://meghalayatenders.gov.in/nicgep/app",
    "Mizoram": "https://mizoramtenders.gov.in/nicgep/app",
    "Nagaland": "https://nagalandtenders.gov.in/nicgep/app",
    "Odisha": "https://tendersodisha.gov.in/nicgep/app",
    "Puducherry": "https://pudutenders.gov.in/nicgep/app",
    "Punjab": "https://eproc.punjab.gov.in/nicgep/app",
    "Rajasthan": "https://eproc.rajasthan.gov.in/nicgep/app",
    "Sikkim": "https://sikkimtender.gov.in/nicgep/app",
    "Tamil Nadu": "https://tntenders.gov.in/nicgep/app",
    "Tripura": "https://tripuratenders.gov.in/nicgep/app",
    "Ladakh": "https://tenders.ladakh.gov.in/nicgep/app",
    "Uttarakhand": "https://uktenders.gov.in/nicgep/app",
    "Uttar Pradesh": "https://etender.up.nic.in/nicgep/app",
    "West Bengal": "https://wbtenders.gov.in/nicgep/app",

    "Central Govt eProcurement": "https://eprocure.gov.in/eprocure/app",
    "CPSE eProcurement": "https://etenders.gov.in/eprocure/app",
    "NTPC Limited": "https://eprocurentpc.nic.in/nicgep/app",
    "MIDHANI": "https://eprocuremidhani.nic.in/nicgep/app",
    "Mazagon Dock Shipbuilders": "https://eprocuremdl.nic.in/nicgep/app",
    "IOCL": "https://iocletenders.nic.in/nicgep/app",
    "Hindustan Shipyard Limited": "https://eprocurehsl.nic.in/nicgep/app",
    "Goa Shipyard Limited": "https://eprocuregsl.nic.in/nicgep/app",
    "Garden Reach Shipbuilders (GRSE)": "https://eprocuregrse.co.in/nicgep/app",
    "CPCL": "https://cpcletenders.nic.in/nicgep/app",
    "Coal India Limited": "https://coalindiatenders.nic.in/nicgep/app",
    "BHEL": "https://eprocurebhel.co.in/nicgep/app",
    "BEL Defence": "https://eprocurebel.co.in/nicgep/app",
    "PMGSY": "https://pmgsytenders.gov.in/nicgep/app",
    "Defence e-Procurement": "https://defproc.gov.in/nicgep/app"
}

# ======================= HELPERS =======================

def extract_tender_id(title: str) -> str:
    if not title:
        return ""
    matches = re.findall(r"\[([^\]]+)\]", title)
    return matches[-1].strip() if matches else ""

def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def compute_identity_hash(tender_id: str) -> str:
    return sha256(tender_id.strip())

# ======================= SCRAPING =======================

results = []
seen_hashes_run = set()

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)

    for state, url in SITES.items():
        print(f"\n🔍 Searching in {state}")

        for attempt in range(1, MAX_RETRIES + 1):
            page = browser.new_page()
            page.set_default_timeout(90000)

            try:
                print(f"  Attempt {attempt}")
                page.goto(url, wait_until="load")

                if page.locator("button.alertbutclose").count() > 0:
                    page.click("button.alertbutclose")
                    page.wait_for_timeout(800)

                page.fill("#SearchDescription", KEYWORD)
                page.click("#Go")
                page.wait_for_load_state("networkidle")

                rows = page.locator("tr.even, tr.odd")

                for i in range(rows.count()):
                    cols = rows.nth(i).locator("td")
                    title = cols.nth(4).inner_text().strip()
                    tender_id = extract_tender_id(title)

                    if not tender_id:
                        continue

                    identity_hash = compute_identity_hash(tender_id)

                    # DOM-level duplicate protection
                    if identity_hash in seen_hashes_run:
                        continue

                    seen_hashes_run.add(identity_hash)

                    results.append({
                        "State/UT": state,
                        "S.No": cols.nth(0).inner_text().strip(),
                        "e-Published Date": cols.nth(1).inner_text().strip(),
                        "Closing Date": cols.nth(2).inner_text().strip(),
                        "Opening Date": cols.nth(3).inner_text().strip(),
                        "Title and Ref.No./Tender ID": title,
                        "Tender ID": tender_id,
                        "Organisation Chain": cols.nth(5).inner_text().strip(),
                        "First Seen Date": RUN_DATE,
                        "Identity Hash": identity_hash
                    })

                break

            except Exception as e:
                print(f"  ⚠ Error: {e}")
                time.sleep(5)

            finally:
                page.close()

    browser.close()

# ======================= MERGE & FLAG =======================

new_df = pd.DataFrame(results)

if os.path.exists(OUTPUT_FILE):
    old_df = pd.read_excel(OUTPUT_FILE)
    old_df.columns = [c.strip() for c in old_df.columns]

    # Ensure hash exists
    if "Identity Hash" not in old_df.columns:
        old_df["Identity Hash"] = old_df["Tender ID"].apply(compute_identity_hash)

    # 🔴 CRITICAL FIX: reset flags every run
    old_df["New Today"] = "NO"

    existing_hashes = set(old_df["Identity Hash"].astype(str))
    new_df["New Today"] = new_df["Identity Hash"].apply(
        lambda h: "NO" if h in existing_hashes else "YES"
    )

    combined = pd.concat([old_df, new_df], ignore_index=True)
    combined.drop_duplicates(subset=["Identity Hash"], keep="first", inplace=True)

else:
    new_df["New Today"] = "YES"
    combined = new_df

combined.to_excel(OUTPUT_FILE, index=False)

print("\n✅ Done. Tender-ID-only identity enforced. New Today flags are now correct.")
