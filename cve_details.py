import streamlit as st
import requests

# Backend API URL
API_URL = "http://127.0.0.1:5000/api/cve/details"

def fetch_cve_details(cve_id):
    """Fetch detailed CVE data from the API."""
    response = requests.get(f"{API_URL}/{cve_id}")
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Streamlit UI
def show_cve_details():
    st.title("CVE Details")

    # Input field for CVE ID
    cve_id = st.text_input("Enter CVE ID:", placeholder="e.g., CVE-2024-12345")

    if st.button("Search CVE"):
        if cve_id:
            cve_data = fetch_cve_details(cve_id)
            if cve_data:
                st.subheader(f"CVE ID: {cve_data['cve_id']}")
                st.write(f"**Description:** {cve_data['description']}")
                st.write(f"**Published Date:** {cve_data['published_date']}")
                st.write(f"**Severity:** {cve_data['severity']}")
                
                # Additional metadata if available
                if "references" in cve_data:
                    st.subheader("References")
                    for ref in cve_data["references"]:
                        st.markdown(f"- [{ref}]({ref})", unsafe_allow_html=True)
                
                if "cvss_score" in cve_data:
                    st.write(f"**CVSS Score:** {cve_data['cvss_score']}")
            else:
                st.error("CVE not found. Please check the CVE ID.")
        else:
            st.warning("Please enter a valid CVE ID.")

# Run the Streamlit app
if __name__ == "__main__":
    show_cve_details()
