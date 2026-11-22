"""Feature 1: current network info (Windows)."""
import socket
import subprocess


def _run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True, errors="replace").stdout


def get_wifi_name():
    """Return the connected Wi-Fi SSID, or None if not on Wi-Fi."""
    for line in _run(["netsh", "wlan", "show", "interfaces"]).splitlines():
        line = line.strip()
        if line.startswith("SSID") and not line.startswith("SSID name"):
            return line.split(":", 1)[1].strip()
    return None


def get_local_ip():
    """Local IP used for outgoing traffic (no data is actually sent)."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    except OSError:
        return None
    finally:
        s.close()


def get_gateway():
    for line in _run(["ipconfig"]).splitlines():
        if "Default Gateway" in line and ":" in line:
            value = line.split(":", 1)[1].strip()
            if value and "." in value:
                return value
    return None


def report():
    wifi = get_wifi_name()
    return {
        "Hostname": socket.gethostname(),
        "Connection type": "Wi-Fi" if wifi else "Wired / other",
        "Wi-Fi name (SSID)": wifi or "n/a",
        "Local IP": get_local_ip() or "unknown",
        "Gateway (router)": get_gateway() or "unknown",
    }
