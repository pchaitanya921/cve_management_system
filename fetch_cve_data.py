import streamlit as st
import requests
import pandas as pd
import sys
import os
import backend.fetch_cve_data
get_cve_data = backend.fetch_cve_data.get_cve_data


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


# API Endpoint (Replace with the actual CVE database API)
CVE_API_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"

def get_cve_data():
    # Function implementation
    pass


def fetch_cve_data(severity=None, start_date=None, end_date=None):
    """
    Fetch CVE data from the API with optional filters for severity and date range.
    """
    params = {}

    if severity:
        params["cvssV3Severity"] = severity  # Filter by CVSS v3 severity
    
    if start_date and end_date:
        params["pubStartDate"] = f"{start_date}T00:00:00.000Z"
        params["pubEndDate"] = f"{end_date}T23:59:59.999Z"

    try:
        response = requests.get(CVE_API_URL, params=params)
        response.raise_for_status()  # Raise error if API request fails
        
        data = response.json()
        return data.get("vulnerabilities", [])  # Extract CVEs from response
    
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching CVE data: {e}")
        return []

# Streamlit UI
st.title("🔍 CVE Vulnerability Lookup")

# Sidebar Filters
st.sidebar.header("Filter Options")
severity = st.sidebar.selectbox("Select Severity", ["", "Low", "Medium", "High", "Critical"])
start_date = st.sidebar.date_input("Start Date")
end_date = st.sidebar.date_input("End Date")

if st.sidebar.button("Fetch CVEs"):
    cve_list = fetch_cve_data(severity, start_date, end_date)

    if cve_list:
        df = pd.DataFrame([
            {
                "CVE ID": cve["cve"]["id"],
                "Description": cve["cve"]["descriptions"][0]["value"],
                "Published Date": cve["cve"]["published"],
                "Severity": cve["cve"].get("metrics", {}).get("cvssMetricV31", [{}])[0].get("cvssData", {}).get("baseSeverity", "N/A")
            }
            for cve in cve_list
        ])

        st.write(f"✅ Fetched {len(df)} CVEs")
        st.dataframe(df)  # Display CVEs as a table
    else:
        st.warning("No CVEs found for the selected filters.")
