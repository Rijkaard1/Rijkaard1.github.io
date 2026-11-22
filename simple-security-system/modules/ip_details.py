"""Feature 2: public IP details via ipinfo.io (your public IP is visible to that service)."""
import json
import urllib.request


def report():
    try:
        req = urllib.request.Request(
            "https://ipinfo.io/json", headers={"User-Agent": "simple-security-system"}
        )
        with urllib.request.urlopen(req, timeout=8) as r:
            data = json.load(r)
    except Exception as e:
        return {"Error": f"Could not reach ipinfo.io ({e})"}
    return {
        "Public IP": data.get("ip", "?"),
        "ISP / Org": data.get("org", "?"),
        "City": data.get("city", "?"),
        "Region": data.get("region", "?"),
        "Country": data.get("country", "?"),
        "Timezone": data.get("timezone", "?"),
        "Hostname": data.get("hostname", "n/a"),
    }
