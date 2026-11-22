"""Feature 5: Wi-Fi safety check based on the encryption of the current connection."""
import subprocess

# authentication keyword -> (rating, advice)
RATINGS = [
    ("wpa3", ("SAFE", "WPA3 is the strongest Wi-Fi security available.")),
    ("wpa2", ("OK", "WPA2 is acceptable. Use a strong password; WPA3 is better if your router supports it.")),
    ("wpa", ("WEAK", "Original WPA is outdated. Upgrade the router setting to WPA2/WPA3.")),
    ("wep", ("UNSAFE", "WEP can be cracked in minutes. Change the router to WPA2/WPA3.")),
    ("open", ("UNSAFE", "Open network: traffic is not encrypted. Avoid sensitive logins or use a VPN.")),
]


def _interface_fields():
    out = subprocess.run(["netsh", "wlan", "show", "interfaces"], capture_output=True, text=True, errors="replace").stdout
    fields = {}
    for line in out.splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            fields.setdefault(k.strip(), v.strip())
    return fields


def report():
    f = _interface_fields()
    if "SSID" not in f:
        return {"Status": "Not connected to Wi-Fi"}
    auth = f.get("Authentication", "unknown")
    cipher = f.get("Cipher", "unknown")
    rating, advice = "UNKNOWN", "Could not determine security type."
    for key, value in RATINGS:
        if key in auth.lower():
            rating, advice = value
            break
    notes = []
    if "tkip" in cipher.lower():
        rating = "WEAK" if rating in ("SAFE", "OK") else rating
        notes.append("TKIP cipher is outdated; prefer AES (CCMP).")
    try:
        signal = int(f.get("Signal", "0").rstrip("%"))
        if signal < 30:
            notes.append("Very weak signal; connection may be unreliable.")
    except ValueError:
        pass
    data = {
        "Wi-Fi name (SSID)": f["SSID"],
        "Authentication": auth,
        "Cipher": cipher,
        "Radio type": f.get("Radio type", "?"),
        "Signal": f.get("Signal", "?"),
        "Safety rating": rating,
        "Advice": advice,
    }
    if notes:
        data["Notes"] = " ".join(notes)
    return data
