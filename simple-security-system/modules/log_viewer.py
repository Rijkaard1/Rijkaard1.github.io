"""Feature 13: log viewer - browse the scan logs saved in the logs folder.

Logs are one JSON object per line: {"time", "feature", "data"} (see logger.py).
"""
import json
import os

from modules.logger import LOG_DIR

NAMES = {
    "network": "Network info",
    "ip_details": "Public IP details",
    "connections": "Active connections",
    "wifi_safety": "Wi-Fi safety",
    "recent_apps": "Recent apps",
    "file_monitor": "Downloaded files",
    "startup_check": "Startup programs",
    "open_ports": "Open ports",
    "ip_watch": "Unknown IP alerts",
    "risk_score": "Risk score",
}


def list_logs():
    """Return [(date, path, entry_count)] newest first."""
    if not os.path.isdir(LOG_DIR):
        return []
    logs = []
    for fn in sorted(os.listdir(LOG_DIR), reverse=True):
        if fn.endswith(".log"):
            path = os.path.join(LOG_DIR, fn)
            logs.append((fn[:-4], path, len(load(path))))
    return logs


def load(path):
    """Read a log file; lines that cannot be read are skipped."""
    entries = []
    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    e = json.loads(line)
                    if isinstance(e, dict) and "feature" in e:
                        entries.append(e)
                except ValueError:
                    continue
    except OSError:
        pass
    return entries


def summarize(entry):
    """One short line describing an entry."""
    f, d = entry.get("feature", "?"), entry.get("data")
    try:
        if f == "network":
            return f"{d.get('Wi-Fi name (SSID)')}, local IP {d.get('Local IP')}"
        if f == "ip_details":
            return f"{d.get('Public IP')} ({d.get('City')}, {d.get('Country')})"
        if f == "connections":
            s = d["summary"]
            return f"{s['Internet connections']} internet connections, {s['Unique remote IPs']} unique IPs"
        if f == "wifi_safety":
            return f"{d.get('Safety rating')} on {d.get('Wi-Fi name (SSID)')}"
        if f == "recent_apps":
            return f"{list(d['summary'].values())[0]} apps in the last 24 hours"
        if f == "file_monitor":
            s = d["summary"]
            n = next(v for k, v in s.items() if k.startswith("Files in last"))
            return f"{n} files: {s['WARNING']} warning, {s['CAUTION']} caution, {s['SAFE']} safe"
        if f == "startup_check":
            s = d["summary"]
            return f"{s['Startup entries found']} entries: {s['WARNING']} warning, {s['CAUTION']} caution"
        if f == "open_ports":
            s = d["summary"]
            return f"{s['Listening TCP ports']} ports: {s['WARNING (programs)']} warning, {s['CAUTION (programs)']} caution"
        if f == "ip_watch":
            high = sum(1 for a in d if a.get("Level") == "HIGH")
            return f"{len(d)} alert(s), {high} high: " + ", ".join(a["IP"] for a in d[:3])
        if f == "risk_score":
            return f"{d['score']} / 100 [{d['band']}]"
    except (KeyError, TypeError, AttributeError, StopIteration, IndexError):
        pass
    return "(open to see details)"


def features_in(entries):
    return sorted({e.get("feature", "?") for e in entries})


def full_text(entry):
    """The complete entry as readable lines."""
    head = f"{NAMES.get(entry.get('feature'), entry.get('feature'))} - {entry.get('time')}"
    body = json.dumps(entry.get("data"), indent=2, ensure_ascii=False)
    return [head, "-" * len(head)] + body.splitlines()
