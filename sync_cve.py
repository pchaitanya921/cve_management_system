import requests
import logging
import time
from datetime import datetime, timedelta
from backend.database import insert_cve_data, create_cve_table

# API Configuration
NVD_API_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"
PAGE_SIZE = 1000  # Adjust based on API limits
SYNC_INTERVAL = 24  # Hours between each data sync

# Logging Setup
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def fetch_cve_data(start_index=0):
    """
    Fetches CVE data from the NVD API in batches.
    """
    params = {
        "startIndex": start_index,
        "resultsPerPage": PAGE_SIZE
    }

    try:
        response = requests.get(NVD_API_URL, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching CVE data: {e}")
        return None

def extract_cve_details(cve_item):
    """
    Extracts relevant CVE details from the API response.
    """
    cve_id = cve_item.get("cve", {}).get("id", "Unknown")
    description = cve_item.get("cve", {}).get("descriptions", [{}])[0].get("value", "No description available")
    
    published_date = cve_item.get("published", None)
    last_modified_date = cve_item.get("lastModified", None)

    # Extract CVSS Score & Severity (V3 preferred, fallback to V2)
    cvss_v3 = cve_item.get("metrics", {}).get("cvssMetricV3", [{}])
    cvss_v2 = cve_item.get("metrics", {}).get("cvssMetricV2", [{}])

    if cvss_v3 and "cvssData" in cvss_v3[0]:
        cvss_score = cvss_v3[0]["cvssData"]["baseScore"]
        severity = cvss_v3[0]["cvssData"]["baseSeverity"]
    elif cvss_v2 and "cvssData" in cvss_v2[0]:
        cvss_score = cvss_v2[0]["cvssData"]["baseScore"]
        severity = cvss_v2[0]["cvssData"]["baseSeverity"]
    else:
        cvss_score, severity = None, "Unknown"

    return cve_id, description, published_date, last_modified_date, cvss_score, severity

def sync_cve_data():
    """
    Periodically syncs CVE data (incremental or full refresh).
    """
    logging.info("Starting CVE sync process...")

    create_cve_table()  # Ensure the database table exists
    total_records = 0
    start_index = 0

    while True:
        data = fetch_cve_data(start_index)

        if not data or "vulnerabilities" not in data:
            logging.warning("No new CVE data found.")
            break

        cve_list = data["vulnerabilities"]
        if not cve_list:
            logging.info("All CVE records have been processed.")
            break

        for cve_item in cve_list:
            cve_id, description, published_date, last_modified_date, cvss_score, severity = extract_cve_details(cve_item)

            if insert_cve_data(cve_id, description, published_date, last_modified_date, cvss_score, severity):
                total_records += 1

        logging.info(f"Processed {len(cve_list)} records...")

        start_index += PAGE_SIZE
        if start_index >= data.get("totalResults", 0):
            break  # Stop when all pages are processed

    logging.info(f"Sync completed. Total records updated: {total_records}")

def sync_incremental_cve_data(days=1):
    """
    Sync only modified CVEs from the last 'N' days.
    """
    last_modified_start = (datetime.utcnow() - timedelta(days=days)).isoformat()
    
    logging.info(f"Fetching CVEs modified in the last {days} days...")
    
    params = {
        "lastModStartDate": last_modified_start,
        "resultsPerPage": PAGE_SIZE
    }
    
    start_index = 0
    total_records = 0

    while True:
        params["startIndex"] = start_index
        response = requests.get(NVD_API_URL, params=params)

        if response.status_code != 200:
            logging.error(f"API request failed with status code {response.status_code}")
            break

        data = response.json()
        if "vulnerabilities" not in data or not data["vulnerabilities"]:
            logging.info("No recent CVEs found.")
            break

        for cve_item in data["vulnerabilities"]:
            cve_id, description, published_date, last_modified_date, cvss_score, severity = extract_cve_details(cve_item)

            if insert_cve_data(cve_id, description, published_date, last_modified_date, cvss_score, severity):
                total_records += 1

        start_index += PAGE_SIZE
        if start_index >= data.get("totalResults", 0):
            break

    logging.info(f"Incremental sync completed. Total records updated: {total_records}")

if __name__ == "__main__":
    while True:
        sync_incremental_cve_data(1)  # Sync modified CVEs in the last 1 day
        logging.info(f"Next sync in {SYNC_INTERVAL} hours...")
        time.sleep(SYNC_INTERVAL * 3600)  # Wait before next sync
