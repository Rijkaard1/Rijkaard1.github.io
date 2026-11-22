"""Overall risk score (0-100, higher = more risk) built from the other checks.

Each area adds points, with a cap so one noisy area cannot dominate:
  Wi-Fi            UNSAFE +25, WEAK +15, OK +5
  Firewall off     +20 (on your active network profile)
  Downloads        WARNING +10 each (max 20), CAUTION +2 each (max 10)
  Startup          WARNING +8 each (max 16),  CAUTION +1 each (max 5)
  Open ports       WARNING +8 each (max 16),  CAUTION +1 each (max 6)
  Flagged IPs      +5 each (max 10)
Bands: LOW 0-19, MODERATE 20-49, HIGH 50-100.
This is a rough guide built from heuristic checks, not a guarantee of safety.
"""
from modules import file_monitor, ip_watch, open_ports, startup_check, wifi_safety


def band(score):
    return "LOW" if score < 20 else "MODERATE" if score < 50 else "HIGH"


def _count(items, rating):
    return sum(1 for i in items if i.get("Rating") == rating)


def compute(wifi, files, startup, ports, ports_summary, flagged_ips):
    """Build the score from already-collected results."""
    parts = []

    def add(area, points, advice):
        if points > 0:
            parts.append({"Area": area, "Points": points, "Advice": advice})

    rating = wifi.get("Safety rating", "")
    wifi_advice = {
        "UNSAFE": "Avoid sensitive logins on this network or use a VPN; prefer a WPA2/WPA3 network.",
        "WEAK": "Ask for WPA2/WPA3 with AES encryption.",
        "OK": "WPA3 is stronger if your router supports it.",
    }
    add(f"Wi-Fi rated {rating}", {"UNSAFE": 25, "WEAK": 15, "OK": 5}.get(rating, 0), wifi_advice.get(rating, ""))

    if str(ports_summary.get("Firewall note", "")).startswith("OFF"):
        add("Windows Firewall is OFF", 20, "Turn Windows Firewall back on for your current network profile.")

    n = _count(files, "WARNING")
    add(f"{n} download(s) rated WARNING", min(20, n * 10), "Review the WARNING files in option 6 and delete any you do not trust.")
    n = _count(files, "CAUTION")
    add(f"{n} download(s) rated CAUTION", min(10, n * 2), "Check archives, scripts and unsigned files in option 6 before opening them.")

    n = _count(startup, "WARNING")
    add(f"{n} startup program(s) rated WARNING", min(16, n * 8), "Open option 9 and disable startup entries you do not recognize.")
    n = _count(startup, "CAUTION")
    add(f"{n} startup program(s) rated CAUTION", min(5, n * 1), "Open option 9; remove leftover entries for software you uninstalled.")

    n = _count(ports, "WARNING")
    add(f"{n} program(s) with WARNING open ports", min(16, n * 8), "Open option 10 and close or block exposed ports you do not need.")
    n = _count(ports, "CAUTION")
    add(f"{n} program(s) with CAUTION open ports", min(6, n * 1), "Open option 10 to see which programs accept connections from the network.")

    n = len(flagged_ips)
    add(f"{n} flagged IP address(es) not yet trusted", min(10, n * 5), "Open option 8 and trust or investigate the flagged IPs.")

    parts.sort(key=lambda p: p["Points"], reverse=True)
    score = min(100, sum(p["Points"] for p in parts))
    return {"score": score, "band": band(score), "breakdown": parts}


def run():
    """Run the needed checks and compute the score (used by menu option 11)."""
    wifi = wifi_safety.report()
    files = file_monitor.report()[1]
    startup = startup_check.report()[1]
    ports_summary, ports = open_ports.report()
    return compute(wifi, files, startup, ports, ports_summary, ip_watch.flagged_ips())


def from_results(res):
    """Compute from the results 'Run all' already collected, keyed by feature name."""
    return compute(
        res["wifi_safety"],
        res["file_monitor"]["files"],
        res["startup_check"]["entries"],
        res["open_ports"]["ports"],
        res["open_ports"]["summary"],
        ip_watch.flagged_ips(),
    )
