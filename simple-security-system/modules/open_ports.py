"""Feature 11: open (listening) ports check.

Lists TCP ports your laptop is listening on, the program behind each one and
whether it is reachable only from this laptop (127.0.0.1) or from the network.
Also shows Windows Firewall status. Only TCP is covered, and it does not scan
from outside - it reads what your own laptop reports.
"""
import json
import re
import subprocess

from modules import connections, file_monitor, wifi_safety

HIGH_RISK = {
    21: "FTP", 23: "Telnet", 3389: "Remote Desktop", 5900: "VNC", 5985: "Windows Remote Management",
    3306: "MySQL", 5432: "PostgreSQL", 1433: "SQL Server", 27017: "MongoDB", 6379: "Redis",
}
MEDIUM_RISK = {22: "SSH", 135: "Windows RPC", 139: "NetBIOS file sharing", 445: "SMB file sharing"}
WINDOWS_PROCS = {"system", "svchost.exe", "lsass.exe", "wininit.exe", "services.exe", "spoolsv.exe"}
LOCAL_ADDRS = {"127.0.0.1", "[::1]"}


def _run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True, errors="replace").stdout


def firewall_status():
    """Return (profile states dict, active profile name or None)."""
    states, current = {}, None
    for line in _run(["netsh", "advfirewall", "show", "allprofiles", "state"]).splitlines():
        m = re.match(r"(\w+) Profile Settings", line.strip())
        if m:
            current = m.group(1)
        elif line.strip().startswith("State") and current:
            states[current] = line.split()[-1].upper()
    active = None
    try:
        out = subprocess.run(
            ["powershell", "-NoProfile", "-Command", "(Get-NetConnectionProfile | Select-Object -First 1).NetworkCategory"],
            capture_output=True, text=True, timeout=30,
        ).stdout.strip()
        active = {"Public": "Public", "Private": "Private", "DomainAuthenticated": "Domain"}.get(out)
    except Exception:
        pass
    return states, active


def _process_paths():
    script = (
        "[Console]::OutputEncoding=[Text.Encoding]::UTF8; "
        "ConvertTo-Json -InputObject @(Get-Process | Where-Object { $_.Path } | Select-Object Id, Path) -Compress"
    )
    try:
        out = subprocess.run(["powershell", "-NoProfile", "-Command", script], capture_output=True, text=True, encoding="utf-8", timeout=60).stdout
        return {str(p["Id"]): p["Path"] for p in json.loads(out)}
    except Exception:
        return {}


def listeners():
    names = connections._process_names()
    found = {}
    for line in _run(["netstat", "-ano"]).splitlines():
        parts = line.split()
        if len(parts) == 5 and parts[0] == "TCP" and parts[3] == "LISTENING":
            addr, _, port = parts[1].rpartition(":")
            pid = parts[4]
            key = (int(port), pid)
            e = found.setdefault(key, {"Port": int(port), "PID": pid, "Process": names.get(pid, f"PID {pid}"), "Addrs": set()})
            e["Addrs"].add(addr)
    return list(found.values())


def scan():
    items = listeners()
    paths = _process_paths()
    sigs = file_monitor.check_signatures(sorted({paths[i["PID"]] for i in items if i["PID"] in paths}))
    states, active = firewall_status()
    fw_off = bool(active) and states.get(active) == "OFF"
    wifi_unsafe = wifi_safety.report().get("Safety rating") in ("UNSAFE", "WEAK")

    results = []
    for i in items:
        exposed = not i["Addrs"] <= LOCAL_ADDRS
        path = paths.get(i["PID"])
        sig = sigs.get(path) if path else None
        status = (sig or {}).get("Status")
        signer = (sig or {}).get("Signer") or ""
        is_windows = i["Process"].lower() in WINDOWS_PROCS or "microsoft" in signer.lower()
        level, reasons = 0, []

        def bump(l, why):
            nonlocal level
            level = max(level, l)
            reasons.append(why)

        if not exposed:
            reasons.append("Local only (127.0.0.1) - not reachable from other devices")
        else:
            if i["Port"] in HIGH_RISK:
                bump(2, f"{HIGH_RISK[i['Port']]} port open to the network - commonly attacked")
            elif i["Port"] in MEDIUM_RISK:
                bump(1, f"{MEDIUM_RISK[i['Port']]} port open to the network")
            elif is_windows:
                reasons.append("Windows system service reachable from the network (normal)")
            else:
                bump(1, "Reachable from other devices on the network")
            if status == "NotSigned":
                bump(2, "Listening program is NOT digitally signed")
            elif status and status not in ("Valid", "Unknown", "NotSigned"):
                bump(2, f"Listening program has a signature problem ({status})")
            if level >= 1 and (fw_off or wifi_unsafe):
                note = "Windows Firewall is OFF for this network" if fw_off else "your current Wi-Fi is open/weak"
                reasons.append(f"Higher risk because {note}")
                if fw_off:
                    level = 2
        results.append(
            {
                "Ports": [i["Port"]],
                "Process": i["Process"],
                "Reach": "network" if exposed else "local only",
                "Path": path or "unknown (needs admin to read)",
                "Rating": ["SAFE", "CAUTION", "WARNING"][level],
                "Reasons": reasons,
            }
        )
    # merge rows of the same program with identical findings (e.g. one app with 15 ports)
    merged = {}
    for r in results:
        key = (r["Process"], r["Reach"], r["Rating"], tuple(r["Reasons"]))
        if key in merged:
            merged[key]["Ports"] += r["Ports"]
        else:
            merged[key] = r
    results = list(merged.values())
    for r in results:
        r["Ports"].sort()
    order = {"WARNING": 0, "CAUTION": 1, "SAFE": 2}
    results.sort(key=lambda r: (order[r["Rating"]], r["Ports"][0]))
    return results, states, active


def report():
    results, states, active = scan()
    fw = ", ".join(f"{k} {v}" for k, v in states.items()) or "unknown"
    summary = {
        "Firewall": fw,
        "Active network profile": active or "unknown",
        "Listening TCP ports": sum(len(r["Ports"]) for r in results),
        "Reachable from network": sum(len(r["Ports"]) for r in results if r["Reach"] == "network"),
        "WARNING (programs)": sum(r["Rating"] == "WARNING" for r in results),
        "CAUTION (programs)": sum(r["Rating"] == "CAUTION" for r in results),
    }
    if active and states.get(active) == "ON":
        summary["Firewall note"] = f"ON for {active} network: incoming connections to these ports are normally blocked"
    elif active and states.get(active) == "OFF":
        summary["Firewall note"] = f"OFF for {active} network: exposed ports can be reached directly!"
    return summary, results
