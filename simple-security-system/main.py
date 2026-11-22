"""Simple Security System - command line menu."""
import json
import os

from modules import network_info, ip_details, connections, wifi_safety, recent_apps, file_monitor, file_finder, ip_watch, startup_check, open_ports, logger


def version_label():
    """Version text from version.json next to this file (empty if the file is missing)."""
    try:
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "version.json")
        with open(path, "r", encoding="utf-8") as f:
            v = json.load(f)
        return f" v{v['version']} (updated {v['updated']})"
    except (OSError, ValueError, KeyError):
        return ""


def show(title, data):
    print(f"\n=== {title} ===")
    for k, v in data.items():
        print(f"  {k:<26}: {v}")


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
    print(f"\n  {'Remote IP':<40}{'Port':<8}{'Process':<28}Count")
    for (ip, port, proc), n in groups.items():
        print(f"  {ip:<40}{port:<8}{proc:<28}{n}")
    return "connections", {"summary": summary, "internet": external}


def do_wifi():
    data = wifi_safety.report()
    show("Wi-Fi safety check", data)
    return "wifi_safety", data


def do_apps():
    summary, apps = recent_apps.report()
    show("Recently opened apps", summary)
    print(f"\n  {'Last run':<18}{'Runs':<7}App")
    for a in apps:
        print(f"  {a['Last run']:<18}{a['Total runs']:<7}{a['App']}")
    return "recent_apps", {"summary": summary, "apps": apps}


def do_files():
    summary, results = file_monitor.report()
    show("Downloaded files (last 30 days)", summary)
    flagged = [r for r in results if r["Rating"] != "SAFE"]
    if flagged:
        print("\n  !! FILES NEEDING ATTENTION !!")
        for r in flagged:
            print(f"\n  [{r['Rating']}] {r['File']}  ({r['Size (KB)']} KB, {r['Modified']})")
            print(f"      Source : {r['Source']}")
            for why in r["Reasons"]:
                print(f"      - {why}")
    safe = [r for r in results if r["Rating"] == "SAFE"]
    if safe:
        print(f"\n  Safe-looking files ({len(safe)}):")
        for r in safe:
            print(f"  [SAFE] {r['File']}  ({r['Size (KB)']} KB, {r['Modified']})")
            for why in r["Reasons"]:
                if why.startswith("Signed by"):
                    print(f"         {why}")
            print(f"         SHA256: {r['SHA256']}")
    print("\n  Note: this is a heuristic check, not an antivirus scan.")
    return "file_monitor", {"summary": summary, "files": results}


def do_find():
    name = input("  File name (part of the name is OK): ").strip()
    if not name:
        print("  No name entered.")
        return
    ext = input("  File extension / type (e.g. pdf, docx; blank = any): ").strip()
    print("  Searching all drives, please wait...")
    matches = file_finder.find(name, ext)
    print(f"\n=== Found {len(matches)} file(s) ===")
    for m in matches[: file_finder.MAX_RESULTS]:
        print(f"  {m['Location']}")
        print(f"      {m['Size (KB)']} KB, modified {m['Modified']}")
    if len(matches) > file_finder.MAX_RESULTS:
        print(f"\n  Showing newest {file_finder.MAX_RESULTS} of {len(matches)}. Use a more specific name.")
    if not matches:
        print("  Nothing found. Check the spelling, or try a shorter part of the name.")


def print_alerts(alerts):
    for a in alerts:
        print(f"\n  [{a['Level']}] New connection: {a['IP']}")
        print(f"      Ports   : {', '.join(a['Ports'])}")
        print(f"      Programs: {', '.join(a['Programs'])}")
        print(f"      Owner   : {a['Owner']}")
        for why in a["Reasons"]:
            print(f"      - {why}")


def ip_watch_once():
    alerts, baseline, total = ip_watch.scan()
    if baseline:
        print(f"\n  First run: saved {total} current IP addresses as your baseline.")
        print("  From now on, new addresses will be reported.")
        return
    print(f"\n=== Unknown IP alerts === ({total} known IPs)")
    if alerts:
        print_alerts(alerts)
        logger.save("ip_watch", alerts)
        print("\n  A new IP is a reason to look, not proof of a problem.")
    else:
        print("  No new IP addresses. All connections are to known addresses.")


def ip_watch_live(interval=30):
    from datetime import datetime
    import time

    print(f"\n  Live mode: checking every {interval}s. Press Ctrl+C to stop.")
    shown = set()
    try:
        while True:
            alerts, baseline, total = ip_watch.scan()
            stamp = datetime.now().strftime("%H:%M:%S")
            if baseline:
                print(f"  [{stamp}] Baseline saved ({total} IPs). Watching for new ones...")
            else:
                fresh = [a for a in alerts if a["IP"] not in shown]
                shown.update(a["IP"] for a in fresh)
                if fresh:
                    print(f"\n  [{stamp}] {len(fresh)} new alert(s):")
                    print_alerts(fresh)
                    logger.save("ip_watch", fresh)
                else:
                    print(f"  [{stamp}] No new IPs ({total} known)")
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\n  Live mode stopped.")


def do_ip_watch():
    while True:
        print("\n  -- Unknown IP alerts --")
        print("  1) Scan once")
        print("  2) Live mode (every 30 seconds)")
        print("  3) Trust a flagged IP")
        print("  0) Back")
        c = input("  Choose: ").strip()
        if c == "1":
            ip_watch_once()
        elif c == "2":
            ip_watch_live()
        elif c == "3":
            flagged = ip_watch.flagged_ips()
            if not flagged:
                print("  No flagged IPs waiting for approval.")
                continue
            print("  Flagged IPs: " + ", ".join(flagged))
            ip = input("  IP to trust: ").strip()
            print("  Trusted." if ip_watch.trust(ip) else "  That IP is not in the known list.")
        elif c == "0":
            break
        else:
            print("  Invalid choice.")


def print_rated(items, label, detail_lines):
    """Print WARNING/CAUTION items in detail, then SAFE ones in one short line each."""
    flagged = [r for r in items if r["Rating"] != "SAFE"]
    safe = [r for r in items if r["Rating"] == "SAFE"]
    if flagged:
        print("\n  !! NEEDING ATTENTION !!")
        for r in flagged:
            print(f"\n  [{r['Rating']}] {label(r)}")
            for line in detail_lines(r):
                print(f"      {line}")
            for why in r["Reasons"]:
                print(f"      - {why}")
    if safe:
        print(f"\n  Safe-looking ({len(safe)}):")
        for r in safe:
            print(f"  [SAFE] {label(r)}")


def do_startup():
    summary, items = startup_check.report()
    show("Startup programs", summary)
    print_rated(items, lambda r: r["Name"], lambda r: [f"Source : {r['Source']}", f"Runs   : {r['Target']}"])
    print("\n  Note: this is a heuristic check, not an antivirus scan.")
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
    print("\n  Note: shows what your laptop is listening on; it does not scan from outside.")
    return "open_ports", {"summary": summary, "ports": items}


MENU = {
    "1": do_network, "2": do_ip, "3": do_connections, "4": do_wifi, "5": do_apps, "6": do_files,
    "9": do_startup, "10": do_ports,
}


def main():
    while True:
        print(f"\n--- Simple Security System{version_label()} ---")
        print("1) Current network info")
        print("2) My public IP details")
        print("3) Active connections / IPs seen")
        print("4) Wi-Fi safety check")
        print("5) Apps opened in last 24 hours")
        print("6) Downloaded files check (last 30 days)")
        print("7) Find a file location (by name and type)")
        print("8) Unknown IP alerts (new connections)")
        print("9) Startup programs check")
        print("10) Open ports check")
        print("11) Run all and save to log")
        print("0) Exit")
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
            for fn in MENU.values():
                feature, data = fn()
                path = logger.save(feature, data)
            print(f"\nSaved to {path}")
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
