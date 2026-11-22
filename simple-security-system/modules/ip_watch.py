"""Feature 9: alerts for IP addresses your laptop has not connected to before.

Known IPs are stored in known_ips.json (project folder). The first scan builds a
silent baseline. After that every new internet IP raises an alert:
  NEW  - ordinary new address (added to the known list after the alert)
  HIGH - unusual port or a program not seen before; stays flagged and keeps
         alerting until you trust it from the menu.
A new IP is a reason to look, not proof of a problem.
"""
import json
import os
import urllib.request
from datetime import datetime

from modules import connections

DATA = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "known_ips.json")
COMMON_PORTS = {"80", "443"}
MAX_LOOKUPS = 10  # owner lookups per scan (keeps scans fast)


def _load():
    try:
        with open(DATA, "r", encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return None


def _save(db):
    with open(DATA, "w", encoding="utf-8") as f:
        json.dump(db, f, indent=2)


def _owner(ip):
    try:
        req = urllib.request.Request(f"https://ipinfo.io/{ip}/json", headers={"User-Agent": "simple-security-system"})
        with urllib.request.urlopen(req, timeout=5) as r:
            d = json.load(r)
        return f"{d.get('org', '?')} ({d.get('country', '?')})"
    except Exception:
        return "lookup failed"


def scan():
    """Return (alerts, baseline_created, total_known_ips)."""
    by_ip = {}
    for c in connections.get_connections():
        if c["Type"] != "internet":
            continue
        d = by_ip.setdefault(c["Remote IP"], {"ports": set(), "procs": set()})
        d["ports"].add(c["Port"])
        d["procs"].add(c["Process"])

    db = _load()
    baseline = db is None
    db = db or {}
    now = datetime.now().isoformat(timespec="seconds")
    known_procs = {p for e in db.values() if e["status"] != "flagged" for p in e["processes"]}
    alerts, lookups = [], 0

    for ip, info in by_ip.items():
        entry = db.get(ip)
        if entry is None:
            reasons = []
            if not baseline:
                odd = sorted(info["ports"] - COMMON_PORTS)
                if odd:
                    reasons.append("Unusual port(s): " + ", ".join(odd))
                fresh = sorted(info["procs"] - known_procs)
                if fresh:
                    reasons.append("Program(s) not seen before: " + ", ".join(fresh))
            entry = {
                "first_seen": now,
                "last_seen": now,
                "ports": sorted(info["ports"]),
                "processes": sorted(info["procs"]),
                "owner": "",
                "status": "flagged" if reasons else "known",
            }
            db[ip] = entry
            if not baseline:
                if lookups < MAX_LOOKUPS:
                    entry["owner"] = _owner(ip)
                    lookups += 1
                alerts.append(
                    {
                        "Level": "HIGH" if reasons else "NEW",
                        "IP": ip,
                        "Ports": entry["ports"],
                        "Programs": entry["processes"],
                        "Owner": entry["owner"] or "not looked up",
                        "Reasons": reasons or ["First time this address has been contacted"],
                    }
                )
        else:
            entry["last_seen"] = now
            entry["ports"] = sorted(set(entry["ports"]) | info["ports"])
            entry["processes"] = sorted(set(entry["processes"]) | info["procs"])
            if entry["status"] == "flagged":
                alerts.append(
                    {
                        "Level": "HIGH",
                        "IP": ip,
                        "Ports": entry["ports"],
                        "Programs": entry["processes"],
                        "Owner": entry["owner"] or "unknown",
                        "Reasons": ["Still flagged and not trusted yet"],
                    }
                )
    _save(db)
    return alerts, baseline, len(db)


def flagged_ips():
    db = _load() or {}
    return [ip for ip, e in db.items() if e["status"] == "flagged"]


def trust(ip):
    db = _load() or {}
    if ip not in db:
        return False
    db[ip]["status"] = "trusted"
    _save(db)
    return True
