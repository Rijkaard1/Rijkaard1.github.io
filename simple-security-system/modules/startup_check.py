"""Feature 10: startup programs check.

Lists programs that start automatically when you log in, from:
  - Windows startup registry keys (current user + all users)
  - Startup folders
  - Scheduled tasks that run at logon (non-Windows ones)
and rates each SAFE / CAUTION / WARNING using its digital signature, location
and command line. Heuristic check - not an antivirus scan.
"""
import json
import os
import re
import shutil
import subprocess
import tempfile
import winreg

from modules import file_monitor

RUN = r"Software\Microsoft\Windows\CurrentVersion\Run"
RUN_ONCE = r"Software\Microsoft\Windows\CurrentVersion\RunOnce"
REG_KEYS = [
    (winreg.HKEY_CURRENT_USER, RUN, "Registry (current user)"),
    (winreg.HKEY_CURRENT_USER, RUN_ONCE, "Registry RunOnce (current user)"),
    (winreg.HKEY_LOCAL_MACHINE, RUN, "Registry (all users)"),
    (winreg.HKEY_LOCAL_MACHINE, RUN_ONCE, "Registry RunOnce (all users)"),
    (winreg.HKEY_LOCAL_MACHINE, r"Software\WOW6432Node\Microsoft\Windows\CurrentVersion\Run", "Registry 32-bit (all users)"),
]
BINARIES = {".exe", ".dll", ".scr", ".com"}
SCRIPTS = {".bat", ".cmd", ".ps1", ".vbs", ".vbe", ".js", ".jse", ".wsf", ".hta"}
BAD_ARGS = re.compile(
    r"-enc\b|-encodedcommand|-w(indowstyle)?\s+hidden|frombase64string|downloadstring|invoke-expression|\biex\b|mshta|bitsadmin",
    re.I,
)
URL_ARGS = re.compile(r"https?://", re.I)
BAD_LOCATIONS = ("\\temp\\", "\\downloads\\", "\\users\\public\\", "\\$recycle.bin\\")


def _ps_list(paths, body):
    """Run `body` (PowerShell, uses $_ as each path) over paths; return parsed JSON list."""
    if not paths:
        return []
    fd, list_file = tempfile.mkstemp(suffix=".json")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(paths, f)
    script = (
        "$p = Get-Content -LiteralPath '%s' -Raw -Encoding UTF8 | ConvertFrom-Json; "
        "$r = @($p | ForEach-Object { %s }); "
        "[Console]::OutputEncoding=[Text.Encoding]::UTF8; ConvertTo-Json -InputObject $r -Compress" % (list_file, body)
    )
    try:
        out = subprocess.run(
            ["powershell", "-NoProfile", "-Command", script], capture_output=True, text=True, encoding="utf-8", timeout=120
        ).stdout
        return json.loads(out) if out.strip() else []
    except Exception:
        return []
    finally:
        os.remove(list_file)


def registry_entries():
    found = []
    for hive, path, label in REG_KEYS:
        try:
            key = winreg.OpenKey(hive, path)
        except OSError:
            continue
        with key:
            i = 0
            while True:
                try:
                    name, value, _ = winreg.EnumValue(key, i)
                except OSError:
                    break
                i += 1
                found.append({"Name": name, "Source": label, "Command": str(value)})
    return found


def folder_entries():
    found = []
    folders = [
        (os.path.join(os.environ.get("APPDATA", ""), r"Microsoft\Windows\Start Menu\Programs\Startup"), "Startup folder (current user)"),
        (os.path.join(os.environ.get("PROGRAMDATA", ""), r"Microsoft\Windows\Start Menu\Programs\StartUp"), "Startup folder (all users)"),
    ]
    for folder, label in folders:
        if os.path.isdir(folder):
            for fn in os.listdir(folder):
                if fn.lower() != "desktop.ini":
                    found.append({"Name": os.path.splitext(fn)[0], "Source": label, "Command": os.path.join(folder, fn)})
    return found


def task_entries():
    script = (
        "$t = Get-ScheduledTask | Where-Object { $_.State -ne 'Disabled' -and $_.TaskPath -notlike '\\Microsoft\\Windows\\*' "
        "-and ($_.Triggers | Where-Object { $_.CimClass.CimClassName -eq 'MSFT_TaskLogonTrigger' }) }; "
        "$r = @($t | ForEach-Object { $a = $_.Actions | Select-Object -First 1; "
        "[pscustomobject]@{Name=$_.TaskName; Command=(('' + $a.Execute + ' ' + $a.Arguments).Trim())} }); "
        "[Console]::OutputEncoding=[Text.Encoding]::UTF8; ConvertTo-Json -InputObject $r -Compress"
    )
    try:
        out = subprocess.run(
            ["powershell", "-NoProfile", "-Command", script], capture_output=True, text=True, encoding="utf-8", timeout=120
        ).stdout
        data = json.loads(out) if out.strip() else []
    except Exception:
        return []
    return [{"Name": d["Name"], "Source": "Scheduled task (at logon)", "Command": d["Command"]} for d in data if d.get("Command")]


def split_command(cmd):
    """Split a startup command into (target path, arguments)."""
    cmd = re.sub(r'^"+', '"', os.path.expandvars(cmd.strip()))  # some tasks have doubled opening quotes
    m = re.match(r'"([^"]+)"\s*(.*)', cmd)
    if m:
        return m.group(1), m.group(2)
    m = re.match(r"(.+?\.(?:exe|bat|cmd|com|scr|lnk|vbs|vbe|js|jse|wsf|hta|ps1|msi|dll))\b\s*(.*)", cmd, re.I)
    if m:
        return m.group(1).strip('"'), m.group(2)
    parts = cmd.split(" ", 1)
    return parts[0].strip('"'), parts[1] if len(parts) > 1 else ""


def rate(target, args, exists, sig):
    level, reasons = 0, []

    def bump(l, why):
        nonlocal level
        level = max(level, l)
        reasons.append(why)

    ext = os.path.splitext(target)[1].lower()
    low = target.lower()
    if not exists:
        bump(1, "Target file not found (leftover or broken entry)")
    if any(b in low for b in BAD_LOCATIONS):
        bump(2, "Runs from a Temp / Downloads / Public folder - unusual for legitimate startup programs")
    if BAD_ARGS.search(args):
        bump(2, "Suspicious command line (encoded, hidden or download-and-run commands)")
    status = (sig or {}).get("Status", "Unknown")
    if not BAD_ARGS.search(args) and URL_ARGS.search(args) and not (exists and ext in BINARIES and status == "Valid"):
        bump(1, "Command line contains a web address")
    if exists and ext in BINARIES:
        if status == "Valid":
            m = re.search(r"CN=([^,]+)", (sig or {}).get("Signer") or "")
            reasons.append("Signed by " + (m.group(1).strip('"') if m else "a trusted publisher"))
        elif status == "NotSigned":
            bump(2, "Program is NOT digitally signed - publisher unknown")
        elif status == "Unknown":
            bump(1, "Could not verify signature")
        else:
            bump(2, f"Signature problem ({status}) - file may be tampered with")
    elif exists and ext in SCRIPTS:
        bump(1, "Script runs at startup - make sure you know what it does")
    return ["SAFE", "CAUTION", "WARNING"][level], reasons


def scan():
    entries = registry_entries() + folder_entries() + task_entries()
    # resolve shortcuts in Startup folders
    lnks = [e["Command"] for e in entries if e["Command"].lower().endswith(".lnk")]
    resolved = {
        r["Path"]: r
        for r in _ps_list(
            lnks,
            "$s = (New-Object -ComObject WScript.Shell).CreateShortcut($_); "
            "[pscustomobject]@{Path=$_; Target=$s.TargetPath; Args=$s.Arguments}",
        )
    }
    prepared = []
    for e in entries:
        if e["Command"] in resolved:
            r = resolved[e["Command"]]
            target, args = r["Target"] or e["Command"], r["Args"] or ""
        else:
            target, args = split_command(e["Command"])
        full = target if os.path.isabs(target) else (shutil.which(target) or target)
        prepared.append((e, full, args, os.path.exists(full)))
    sig_paths = sorted({p for _, p, _, ok in prepared if ok and os.path.splitext(p)[1].lower() in BINARIES})
    sigs = file_monitor.check_signatures(sig_paths)
    results = []
    for e, full, args, ok in prepared:
        rating, reasons = rate(full, args, ok, sigs.get(full))
        results.append(
            {
                "Name": e["Name"],
                "Source": e["Source"],
                "Command": e["Command"],
                "Target": full,
                "Rating": rating,
                "Reasons": reasons,
            }
        )
    order = {"WARNING": 0, "CAUTION": 1, "SAFE": 2}
    results.sort(key=lambda r: (order[r["Rating"]], r["Name"].lower()))
    return results


def report():
    results = scan()
    summary = {
        "Startup entries found": len(results),
        "WARNING": sum(r["Rating"] == "WARNING" for r in results),
        "CAUTION": sum(r["Rating"] == "CAUTION" for r in results),
        "SAFE": sum(r["Rating"] == "SAFE" for r in results),
    }
    return summary, results
