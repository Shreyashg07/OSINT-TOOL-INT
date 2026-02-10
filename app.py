from flask import Flask, request, jsonify
from flask_cors import CORS
import whois
import dns.resolver
import socket
import random
import requests
from exif import Image
import phonenumbers
from phonenumbers import geocoder, carrier

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# 🔹 HTML UI
@app.route('/')
def home():
    return render_template("index.html")



# 🔹 Domain Info
@app.route('/domain-info')
def domain_info():
    domain = request.args.get('domain')
    if not domain:
        return jsonify({"error": "No domain provided"}), 400
    try:
        domain_data = whois.whois(domain)
        return jsonify({
            "domain": domain,
            "registrar": domain_data.registrar,
            "creation_date": str(domain_data.creation_date),
            "expiration_date": str(domain_data.expiration_date),
            "updated_date": str(domain_data.updated_date),
            "name_servers": domain_data.name_servers
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 🔹 DNS Lookup
@app.route('/dns-lookup')
def dns_lookup():
    domain = request.args.get('domain')
    if not domain:
        return jsonify({"error": "No domain provided"}), 400

    dns_records = ["A", "MX", "NS", "TXT", "CNAME"]
    results = {}
    try:
        for record in dns_records:
            try:
                answers = dns.resolver.resolve(domain, record, raise_on_no_answer=False)
                results[record] = [rdata.to_text() for rdata in answers] if answers.rrset else "No records found"
            except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.resolver.NoNameservers):
                results[record] = "No records found"
            except Exception as e:
                results[record] = f"Error: {str(e)}"
        return jsonify({"domain": domain, "dns_records": results})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 🔹 IP/Domain Info
@app.route('/ip-domain-info')
def ip_domain_info():
    query = request.args.get('query')
    if not query:
        return jsonify({"error": "No IP or domain provided"}), 400
    try:
        ip = socket.gethostbyname(query)
        return jsonify({"query": query, "ip": ip})
    except socket.gaierror:
        return jsonify({"error": "Invalid domain or IP"}), 400


# 🔹 Google Dork Generator
@app.route('/google-dork')
def google_dork():
    dorks = [
        "site:{domain} intitle:index.of",
        "inurl:admin site:{domain}",
        "filetype:pdf site:{domain}",
        "ext:sql | ext:db | ext:sqlite site:{domain}"
    ]
    domain = request.args.get('domain', 'example.com')
    selected_dork = random.choice(dorks).format(domain=domain)
    return jsonify({"google_dork": selected_dork})


# 🔹 Metadata Extractor
@app.route('/metadata', methods=['POST'])
def metadata_extractor():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    file = request.files['file']
    try:
        img = Image(file)
        metadata = {tag: img.get(tag) for tag in img.list_all()}
        return jsonify(metadata)
    except Exception as e:
        return jsonify({"error": str(e)})


# 🔹 Social Media OSINT
def check_profile(url):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    try:
        response = requests.get(url, headers=headers, timeout=5)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

@app.route('/social-media-osint')
def social_media_osint():
    username = request.args.get('username')
    if not username:
        return jsonify({"error": "No username provided"}), 400
    platforms = {
        "LinkedIn": f"https://www.linkedin.com/in/{username}",
        "Instagram": f"https://www.instagram.com/{username}",
        "Facebook": f"https://www.facebook.com/{username}",
        "GitHub": f"https://github.com/{username}",
        "Reddit": f"https://www.reddit.com/user/{username}",
        "Twitter": f"https://twitter.com/{username}",
        "Threads": f"https://www.threads.net/@{username}"
    }
    valid_profiles = {platform: url for platform, url in platforms.items() if check_profile(url)}
    return jsonify({"username": username, "valid_platforms": valid_profiles})


# 🔹 Phone OSINT
@app.route('/phone-osint')
def phone_osint():
    phone = request.args.get('number')
    if not phone:
        return jsonify({"error": "No phone number provided"}), 400
    try:
        parsed_number = phonenumbers.parse(phone, "IN")
        valid = phonenumbers.is_valid_number(parsed_number)
        country = geocoder.country_name_for_number(parsed_number, "en")
        city = geocoder.description_for_number(parsed_number, "en") or "Unknown"
        carrier_name = carrier.name_for_number(parsed_number, "en") or "Unknown"
        return jsonify({
            "number": phone,
            "valid": valid,
            "country": country,
            "city": city,
            "carrier": carrier_name
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 🔹 VoIP OSINT
@app.route('/voip-osint')
def voip_osint():
    phone = request.args.get('number')
    if not phone:
        return jsonify({"error": "No phone number provided"}), 400
    try:
        parsed_number = phonenumbers.parse(phone, "IN")
        is_voip = carrier.name_for_number(parsed_number, "en") in ["Google Voice", "Skype", "TextNow", "Vonage", "Twilio"]
        return jsonify({
            "number": phone,
            "voip": is_voip
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 🔹 Web OSINT
@app.route('/web-osint')
def web_osint():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "No URL provided"}), 400
    if not url.startswith("http"):
        url = "http://" + url
    try:
        response = requests.get(url, timeout=5)
        headers = response.headers
        security_headers = {h: headers[h] for h in headers if h.lower() in ["x-frame-options", "strict-transport-security", "content-security-policy"]}
        google_search_url = f"https://www.google.com/search?q=site:{url.replace('http://', '').replace('https://', '')}"
        robots_url = url + "/robots.txt"
        sitemap_url = url + "/sitemap.xml"
        robots_exists = requests.get(robots_url).status_code == 200
        sitemap_exists = requests.get(sitemap_url).status_code == 200
        return jsonify({
            "url": url,
            "status_code": response.status_code,
            "headers": dict(headers),
            "security_headers": security_headers,
            "indexed_pages_check": google_search_url,
            "robots_txt": robots_exists,
            "sitemap_xml": sitemap_exists
        })
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500


# 🔹 Run the Flask server
if __name__ == '__main__':
    app.run(debug=True)
