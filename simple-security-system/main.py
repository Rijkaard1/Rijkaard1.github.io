"""Simple Security System - command line menu."""
import json
import os

from modules import network_info, ip_details, connections, wifi_safety, recent_apps, file_monitor, file_finder, ip_watch, startup_check, open_ports, risk_score, log_viewer, logger
from modules.colors import c, cprint, level_color, BOLD, GREEN, PURPLE


def version_label():
    """Version text from version.json next to this file (empty if the file is missing)."""
    try:
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "version.json")
        with open(path, "r", encoding="utf-8") as f:
            v = json.load(f)
        return f" v{v['version']} (updated {v['updated']})"
    except (OSError, ValueError, KeyError):
        return ""


def show_banner():
    """Small hexagon logo with the name and version, shown once when the program starts."""
    def purple(s):
        return c(s, PURPLE)

    rows = [
        (purple("    _______   "), ""),
        (purple("   /       \\  "), c("Simple Security System", BOLD)),
        (purple("  /   ") + c("SSS", BOLD, GREEN) + purple("   \\ "), version_label().strip()),
        (purple("  \\         / "), "Network, downloads and startup checks"),
        (purple("   \\_______/  "), ""),
    ]
    cprint("")
    for logo, text in rows:
        cprint(f"{logo}   {text}".rstrip())


def show(title, data):
    cprint(f"\n=== {title} ===")
    for k, v in data.items():
        cprint(f"  {k:<26}: {v}")


def do_network():
    data = network_info.report()
    show("Current network", data)
    return "network", data


def do_ip():
    data = ip_details.report()
    show("Public IP details", data)
    return "ip_details", data


def do_connections():
    summary, external = connections.report()
    show("Active connections", summary)
    groups = {}
    for c in external:
        key = (c["Remote IP"], c["Port"], c["Process"])
        groups[key] = groups.get(key, 0) + 1
    cprint(f"\n  {'Remote IP':<40}{'Port':<8}{'Process':<28}Count")
    for (ip, port, proc), n in groups.items():
        cprint(f"  {ip:<40}{port:<8}{proc:<28}{n}")
    return "connections", {"summary": summary, "internet": external}


def do_wifi():
    data = wifi_safety.report()
    show("Wi-Fi safety check", data)
    return "wifi_safety", data


def do_apps():
    summary, apps = recent_apps.report()
    show("Recently opened apps", summary)
    cprint(f"\n  {'Last run':<18}{'Runs':<7}App")
    for a in apps:
        cprint(f"  {a['Last run']:<18}{a['Total runs']:<7}{a['App']}")
    return "recent_apps", {"summary": summary, "apps": apps}


def do_files():
    summary, results = file_monitor.report()
    show("Downloaded files (last 30 days)", summary)
    flagged = [r for r in results if r["Rating"] != "SAFE"]
    if flagged:
        cprint("\n  !! FILES NEEDING ATTENTION !!")
        for r in flagged:
            cprint(f"\n  [{r['Rating']}] {r['File']}  ({r['Size (KB)']} KB, {r['Modified']})")
            cprint(f"      Source : {r['Source']}")
            for why in r["Reasons"]:
                cprint(f"      - {why}")
    safe = [r for r in results if r["Rating"] == "SAFE"]
    if safe:
        cprint(f"\n  Safe-looking files ({len(safe)}):")
        for r in safe:
            cprint(f"  [SAFE] {r['File']}  ({r['Size (KB)']} KB, {r['Modified']})")
            for why in r["Reasons"]:
                if why.startswith("Signed by"):
                    cprint(f"         {why}")
            cprint(f"         SHA256: {r['SHA256']}")
    cprint("\n  Note: this is a heuristic check, not an antivirus scan.")
    return "file_monitor", {"summary": summary, "files": results}


def do_find():
    name = input("  File name (part of the name is OK): ").strip()
    if not name:
        cprint("  No name entered.")
        return
    ext = input("  File extension / type (e.g. pdf, docx; blank = any): ").strip()
    cprint("  Searching all drives, please wait...")
    matches = file_finder.find(name, ext)
    cprint(f"\n=== Found {len(matches)} file(s) ===")
    for m in matches[: file_finder.MAX_RESULTS]:
        cprint(f"  {m['Location']}")
        cprint(f"      {m['Size (KB)']} KB, modified {m['Modified']}")
    if len(matches) > file_finder.MAX_RESULTS:
        cprint(f"\n  Showing newest {file_finder.MAX_RESULTS} of {len(matches)}. Use a more specific name.")
    if not matches:
        cprint("  Nothing found. Check the spelling, or try a shorter part of the name.")


def print_alerts(alerts):
    for a in alerts:
        cprint(f"\n  [{a['Level']}] New connection: {a['IP']}")
        cprint(f"      Ports   : {', '.join(a['Ports'])}")
        cprint(f"      Programs: {', '.join(a['Programs'])}")
        cprint(f"      Owner   : {a['Owner']}")
        for why in a["Reasons"]:
            cprint(f"      - {why}")


def ip_watch_once():
    alerts, baseline, total = ip_watch.scan()
    if baseline:
        cprint(f"\n  First run: saved {total} current IP addresses as your baseline.")
        cprint("  From now on, new addresses will be reported.")
        return
    cprint(f"\n=== Unknown IP alerts === ({total} known IPs)")
    if alerts:
        print_alerts(alerts)
        logger.save("ip_watch", alerts)
        cprint("\n  A new IP is a reason to look, not proof of a problem.")
    else:
        cprint("  No new IP addresses. All connections are to known addresses.")


def ip_watch_live(interval=30):
    from datetime import datetime
    import time

    cprint(f"\n  Live mode: checking every {interval}s. Press Ctrl+C to stop.")
    shown = set()
    try:
        while True:
            alerts, baseline, total = ip_watch.scan()
            stamp = datetime.now().strftime("%H:%M:%S")
            if baseline:
                cprint(f"  [{stamp}] Baseline saved ({total} IPs). Watching for new ones...")
            else:
                fresh = [a for a in alerts if a["IP"] not in shown]
                shown.update(a["IP"] for a in fresh)
                if fresh:
                    cprint(f"\n  [{stamp}] {len(fresh)} new alert(s):")
                    print_alerts(fresh)
                    logger.save("ip_watch", fresh)
                else:
                    cprint(f"  [{stamp}] No new IPs ({total} known)")
            time.sleep(interval)
    except KeyboardInterrupt:
        cprint("\n  Live mode stopped.")


def do_ip_watch():
    while True:
        cprint("\n  -- Unknown IP alerts --")
        cprint("  1) Scan once")
        cprint("  2) Live mode (every 30 seconds)")
        cprint("  3) Trust a flagged IP")
        cprint("  0) Back")
        c = input("  Choose: ").strip()
        if c == "1":
            ip_watch_once()
        elif c == "2":
            ip_watch_live()
        elif c == "3":
            flagged = ip_watch.flagged_ips()
            if not flagged:
                cprint("  No flagged IPs waiting for approval.")
                continue
            cprint("  Flagged IPs: " + ", ".join(flagged))
            ip = input("  IP to trust: ").strip()
            cprint("  Trusted." if ip_watch.trust(ip) else "  That IP is not in the known list.")
        elif c == "0":
            break
        else:
            cprint("  Invalid choice.")


def print_rated(items, label, detail_lines):
    """Print WARNING/CAUTION items in detail, then SAFE ones in one short line each."""
    flagged = [r for r in items if r["Rating"] != "SAFE"]
    safe = [r for r in items if r["Rating"] == "SAFE"]
    if flagged:
        cprint("\n  !! NEEDING ATTENTION !!")
        for r in flagged:
            cprint(f"\n  [{r['Rating']}] {label(r)}")
            for line in detail_lines(r):
                cprint(f"      {line}")
            for why in r["Reasons"]:
                cprint(f"      - {why}")
    if safe:
        cprint(f"\n  Safe-looking ({len(safe)}):")
        for r in safe:
            cprint(f"  [SAFE] {label(r)}")


def do_startup():
    summary, items = startup_check.report()
    show("Startup programs", summary)
    print_rated(items, lambda r: r["Name"], lambda r: [f"Source : {r['Source']}", f"Runs   : {r['Target']}"])
    cprint("\n  Note: this is a heuristic check, not an antivirus scan.")
    return "startup_check", {"summary": summary, "entries": items}


def do_ports():
    summary, items = open_ports.report()
    show("Open ports", summary)
    print_rated(
        items,
        lambda r: f"{r['Process']}  ({r['Reach']})  port{'s' if len(r['Ports']) > 1 else ''} "
        + ", ".join(map(str, r["Ports"][:6]))
        + (f" +{len(r['Ports']) - 6} more" if len(r["Ports"]) > 6 else ""),
        lambda r: [f"Program: {r['Path']}"],
    )
    cprint("\n  Note: shows what your laptop is listening on; it does not scan from outside.")
    return "open_ports", {"summary": summary, "ports": items}


def show_risk(r):
    score, band = r["score"], r["band"]
    col = level_color(band)
    filled = round(score / 5)
    cprint("\n=== Risk score ===")
    cprint(f"  Score : {c(str(score), BOLD, col)} / 100   {c('[' + band + ']', BOLD, col)}")
    cprint("  " + c("[" + "#" * filled + "-" * (20 - filled) + "]", col))
    if r["breakdown"]:
        cprint("\n  What raised it:")
        for p in r["breakdown"]:
            cprint(f"    +{p['Points']:<3}{p['Area']}")
            if p["Advice"]:
                cprint(f"        Tip: {p['Advice']}")
    else:
        cprint("  Nothing raised the score. No risks found by these checks.")
    cprint("\n  Scale: LOW 0-19, MODERATE 20-49, HIGH 50-100. A rough guide, not a guarantee of safety.")


def do_risk():
    cprint("\n  Running the checks for the risk score (this can take a little while)...")
    r = risk_score.run()
    show_risk(r)
    return "risk_score", r


def page_lines(lines, size=40):
    """Show long text a page at a time."""
    for i in range(0, len(lines), size):
        for line in lines[i : i + size]:
            cprint("  " + line)
        if i + size < len(lines):
            try:
                if input(f"  -- {len(lines) - i - size} more lines. Enter = more, q = stop -- ").strip().lower() == "q":
                    return
            except EOFError:
                return


def do_logs():
    logs = log_viewer.list_logs()
    if not logs:
        cprint("\n  No logs yet. Run option 13 (Run all and save to log) first.")
        return
    cprint("\n=== Log viewer ===")
    for i, (date, _, n) in enumerate(logs, 1):
        cprint(f"  {i}) {date}   {n} entries")
    pick = input("  Pick a log (Enter = newest, 0 = back): ").strip()
    if pick == "0":
        return
    try:
        date, path, _ = logs[int(pick) - 1] if pick else logs[0]
    except (ValueError, IndexError):
        cprint("  Invalid choice.")
        return
    entries = log_viewer.load(path)
    shown = entries
    while True:
        cprint(f"\n=== Log {date} ({len(shown)} of {len(entries)} entries) ===")
        for i, e in enumerate(shown, 1):
            t = str(e.get("time", ""))[11:19]
            name = log_viewer.NAMES.get(e.get("feature"), e.get("feature"))
            cprint(f"  {i:>2})  {t}  {name:<19} {log_viewer.summarize(e)}")
        cmd = input("\n  Entry number to open, f = filter by feature, a = show all, 0 = back: ").strip().lower()
        if cmd == "0":
            return
        if cmd == "a":
            shown = entries
        elif cmd == "f":
            feats = log_viewer.features_in(entries)
            for i, f in enumerate(feats, 1):
                cprint(f"  {i}) {log_viewer.NAMES.get(f, f)}")
            sel = input("  Feature number: ").strip()
            if sel.isdigit() and 1 <= int(sel) <= len(feats):
                shown = [e for e in entries if e.get("feature") == feats[int(sel) - 1]]
            else:
                cprint("  Invalid choice.")
        elif cmd.isdigit() and 1 <= int(cmd) <= len(shown):
            cprint("")
            page_lines(log_viewer.full_text(shown[int(cmd) - 1]))
        else:
            cprint("  Invalid choice.")


MENU = {
    "1": do_network, "2": do_ip, "3": do_connections, "4": do_wifi, "5": do_apps, "6": do_files,
    "9": do_startup, "10": do_ports,
}


def main():
    show_banner()
    while True:
        cprint(f"\n--- Simple Security System{version_label()} ---")
        cprint("1) Current network info")
        cprint("2) My public IP details")
        cprint("3) Active connections / IPs seen")
        cprint("4) Wi-Fi safety check")
        cprint("5) Apps opened in last 24 hours")
        cprint("6) Downloaded files check (last 30 days)")
        cprint("7) Find a file location (by name and type)")
        cprint("8) Unknown IP alerts (new connections)")
        cprint("9) Startup programs check")
        cprint("10) Open ports check")
        cprint("11) Risk score (overall)")
        cprint("12) Log viewer (past scans)")
        cprint("13) Run all and save to log")
        cprint("0) Exit")
        choice = input("Choose: ").strip()
        if choice == "0":
            break
        if choice in MENU:
            MENU[choice]()
        elif choice == "7":
            do_find()
        elif choice == "8":
            do_ip_watch()
        elif choice == "11":
            do_risk()
        elif choice == "12":
            do_logs()
        elif choice == "13":
            results = {}
            for fn in MENU.values():
                feature, data = fn()
                results[feature] = data
                path = logger.save(feature, data)
            risk = risk_score.from_results(results)
            show_risk(risk)
            path = logger.save("risk_score", risk)
            cprint(f"\nSaved to {path}")
        else:
            cprint("Invalid choice.")


if __name__ == "__main__":
    main()
