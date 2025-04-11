# 🕵️‍♂️ OSINT-TOOL-INT

An all-in-one **OSINT (Open Source Intelligence)** tool for ethical hackers, cybersecurity researchers, and info-sec professionals. Built using **Flask**, this web app helps gather, analyze, and display publicly available information across multiple categories — all in one place.

🔗 Live Repo: [OSINT-TOOL-INT](https://github.com/Shreyashg07/OSINT-TOOL-INT)

---

## 🚀 Features

- 🔍 **Domain Info Lookup** – WHOIS data, registrar, domain age
- 🌐 **DNS Lookup** – A, MX, NS, CNAME records + subdomain support
- 📍 **IP Info** – Geolocation, reverse DNS, blacklist check
- 🎯 **Google Dork Generator** – Find exposed login pages, directories, cams
- 📱 **Phone OSINT** – Number analysis, carrier check, format validation
- 📞 **VoIP OSINT** – VoIP number detection, anonymizer flagging
- 🧠 **Web OSINT** – HTTP headers, meta tags, and page scraping

---

## 🛠️ Tech Stack

- **Backend:** Flask (Python)
- **Frontend:** HTML, CSS, JS (Jinja templates)
- **Libraries/Modules:** `whois`, `dnspython`, `ipwhois`, `phonenumbers`, `requests`

---

## ⚙️ Installation Guide

### 🔧 Step-by-step Setup

```bash
# Clone the repo
git clone https://github.com/Shreyashg07/OSINT-TOOL-INT
cd OSINT-TOOL-INT

# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate  # For Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the Flask app
python app.py
