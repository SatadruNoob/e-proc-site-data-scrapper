from playwright.sync_api import sync_playwright
import pandas as pd
import time
import os
from datetime import datetime

# ======================= PORTALS =======================

SITES = {
    # -------------------- STATES / UTs --------------------
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

    # -------------------- CENTRAL GOVT / CPSE --------------------
    "Central Govt eProcurement": "https://eprocure.gov.in/eprocure/app",
    "CPSE eProcurement": "https://etenders.gov.in/eprocure/app",

    # -------------------- PSU / DEFENCE --------------------
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

KEYWORD = "batter"
MAX_RETRIES = 3
OUTPUT_FILE = "NIC_Batter_Tenders_All_States.xlsx"

results = []
run_date = datetime.now().strftime("%Y-%m-%d")

# ======================= SCRAPER =======================

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)

    for state, url in SITES.items():
        print(f"\n🔍 Searching in {state}")
        success = False

        for attempt in range(1, MAX_RETRIES + 1):
            page = browser.new_page()
            page.set_default_timeout(90000)
            page.set_default_navigation_timeout(90000)

            try:
                print(f"  Attempt {attempt}")
                page.goto(url, wait_until="load")

                # -------- NTPC POPUP CLOSE (SAFE FOR ALL) --------
                try:
                    if page.locator("button.alertbutclose").count() > 0:
                        page.click("button.alertbutclose")
                        page.wait_for_timeout(1000)
                except:
                    pass

                page.wait_for_selector("#SearchDescription")
                page.fill("#SearchDescription", KEYWORD)
                page.click("#Go")
                page.wait_for_load_state("networkidle")

                if page.locator("span.error").count() > 0:
                    results.append({
                        "State/UT": state,
                        "S.No": "",
                        "e-Published Date": "",
                        "Closing Date": "",
                        "Opening Date": "",
                        "Title and Ref.No./Tender ID": "No Tenders found",
                        "Organisation Chain": "",
                        "First Seen Date": run_date,
                        "New Today": "YES"
                    })
                else:
                    rows = page.locator("tr.even")
                    for i in range(rows.count()):
                        cols = rows.nth(i).locator("td")
                        results.append({
                            "State/UT": state,
                            "S.No": cols.nth(0).inner_text().strip(),
                            "e-Published Date": cols.nth(1).inner_text().strip(),
                            "Closing Date": cols.nth(2).inner_text().strip(),
                            "Opening Date": cols.nth(3).inner_text().strip(),
                            "Title and Ref.No./Tender ID": cols.nth(4).inner_text().strip(),
                            "Organisation Chain": cols.nth(5).inner_text().strip(),
                            "First Seen Date": run_date,
                            "New Today": "YES"
                        })

                success = True
                break

            except Exception as e:
                print(f"  ⚠ Error: {e}")
                time.sleep(5)

            finally:
                page.close()

        if not success:
            results.append({
                "State/UT": state,
                "S.No": "",
                "e-Published Date": "",
                "Closing Date": "",
                "Opening Date": "",
                "Title and Ref.No./Tender ID": "FAILED after retries",
                "Organisation Chain": "",
                "First Seen Date": run_date,
                "New Today": "YES"
            })

    browser.close()

# ======================= EXCEL MERGE =======================

new_df = pd.DataFrame(results)

if os.path.exists(OUTPUT_FILE):
    old_df = pd.read_excel(OUTPUT_FILE)

    existing_keys = set(
        zip(old_df["State/UT"], old_df["Title and Ref.No./Tender ID"])
    )

    def mark_new(row):
        key = (row["State/UT"], row["Title and Ref.No./Tender ID"])
        return "NO" if key in existing_keys else "YES"

    new_df["New Today"] = new_df.apply(mark_new, axis=1)

    combined_df = pd.concat([old_df, new_df], ignore_index=True)

    combined_df.drop_duplicates(
        subset=["State/UT", "Title and Ref.No./Tender ID"],
        keep="first",
        inplace=True
    )
else:
    combined_df = new_df

combined_df.to_excel(OUTPUT_FILE, index=False)

print("\n✅ Done. Excel updated with 'New Today' column.")
