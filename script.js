document.addEventListener("DOMContentLoaded", function () {
    // Ensure elements exist before adding event listeners
    document.getElementById("domainLookupBtn")?.addEventListener("click", fetchDomainInfo);
    document.getElementById("dnsLookupBtn")?.addEventListener("click", fetchDNSInfo);
    document.getElementById("metadataExtractBtn")?.addEventListener("click", fetchMetadata);
    document.getElementById("ipDomainLookupBtn")?.addEventListener("click", fetchIPDomainInfo);
    document.getElementById("googleDorkBtn")?.addEventListener("click", fetchGoogleDork);
    document.getElementById("socialMediaLookupBtn")?.addEventListener("click", fetchSocialMedia);
    document.getElementById("phoneLookupBtn")?.addEventListener("click", fetchPhoneOSINT);
    document.getElementById("voipLookupBtn")?.addEventListener("click", fetchVoipOSINT);
    document.getElementById("webLookupBtn")?.addEventListener("click", fetchWebOSINT);
});

function fetchData(url, resultElementId) {
    fetch(url)
        .then(response => response.json())
        .then(data => {
            document.getElementById(resultElementId).textContent = JSON.stringify(data, null, 2);
        })
        .catch(error => console.error("Error fetching data:", error));
}

function fetchDomainInfo() {
    const domain = document.getElementById("domainInput").value;
    if (!domain) return alert("Please enter a domain");
    fetchData(`/domain-info?domain=${domain}`, "domainResult");
}

function fetchDNSInfo() {
    const domain = document.getElementById("dnsInput").value;
    if (!domain) return alert("Please enter a domain");
    fetchData(`/dns-lookup?domain=${domain}`, "dnsResult");
}



function fetchIPDomainInfo() {
    const query = document.getElementById("ipDomainInput").value;
    if (!query) return alert("Please enter an IP or domain");
    fetchData(`/ip-domain-info?query=${query}`, "ipDomainResult");
}

function fetchGoogleDork() {
    const domain = document.getElementById("dorkInput").value;
    if (!domain) return alert("Please enter a domain");
    fetchData(`/google-dork?domain=${domain}`, "dorkResult");
}

function fetchSocialMedia() {
    const username = document.getElementById("socialMediaInput").value;
    if (!username) return alert("Please enter a username");
    fetchData(`/social-media-osint?username=${username}`, "socialMediaResult");
}

function fetchPhoneOSINT() {
    const number = document.getElementById("phoneInput").value;
    if (!number) return alert("Please enter a phone number");
    fetchData(`/phone-osint?number=${number}`, "phoneResult");
}

function fetchVoipOSINT() {
    const number = document.getElementById("voipInput").value;
    if (!number) return alert("Please enter a phone number");
    fetchData(`/voip-osint?number=${number}`, "voipResult");
}

function fetchWebOSINT() {
    const url = document.getElementById("webInput").value;
    if (!url) return alert("Please enter a website URL");
    fetchData(`/web-osint?url=${encodeURIComponent(url)}`, "webResult");
}
function fetchData(url, resultElementId) {
    fetch(`http://127.0.0.1:5000${url}`)  // Explicitly call API
        .then(response => response.json())
        .then(data => {
            document.getElementById(resultElementId).textContent = JSON.stringify(data, null, 2);
        })
        .catch(error => console.error("Error fetching data:", error));
}
function fetchMetadata() {
    const fileInput = document.getElementById("fileInput");
    const file = fileInput.files[0];

    if (!file) {
        alert("Please select a file.");
        return;
    }

    const reader = new FileReader();
    reader.onload = function(event) {
        const content = event.target.result;
        document.getElementById("output").textContent = content; // Display metadata
    };
    reader.readAsText(file); // Read as text or use other methods (readAsArrayBuffer, readAsDataURL)
}
