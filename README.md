# CVE Vulnerability Lookup

## Overview
CVE Vulnerability Lookup is a Python-based tool that allows users to fetch and analyze CVE (Common Vulnerabilities and Exposures) data. It provides a web interface for searching and displaying details about known vulnerabilities.

## Features
- Search CVE vulnerabilities by ID.
- Fetch vulnerability details from online databases.
- Display results in a user-friendly web interface.
- Backend processing using Python and Flask.
- Frontend built with HTML, CSS, and JavaScript.

## Installation

### Prerequisites
Ensure you have the following installed:
- Python 3.x
- Flask
- Required dependencies (listed in `requirements.txt`)

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/cve-vulnerability-lookup.git
   cd cve-vulnerability-lookup
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python -m frontend.app
   ```
4. Open the web interface:
   ```
http://127.0.0.1:5000
```

## File Structure
```
cve_management_system/
│
├── backend/
│   ├── fetch_cve_data.py  # Fetches CVE data
│   ├── __init__.py        # Backend module
│
├── frontend/
│   ├── app.py             # Flask application
│   ├── templates/         # HTML files
│   ├── static/            # CSS & JS files
│
├── requirements.txt       # Dependencies
├── README.md              # Documentation
```

## Troubleshooting
### ImportError: cannot import name 'get_cve_data'
- Ensure you are running the script from the **root** directory:
  ```bash
  cd cve_management_system
  python -m frontend.app
  ```
- Check for circular imports. Avoid importing `app.py` inside `fetch_cve_data.py`.

### AttributeError: cannot access submodule 'fetch_cve_data'
- Use absolute imports in `app.py`:
  ```python
  import backend.fetch_cve_data
  get_cve_data = backend.fetch_cve_data.get_cve_data
  ```

## Contribution
1. Fork the repository
2. Create a new branch (`feature-branch`)
3. Commit your changes
4. Push to your fork and submit a PR

