"""Feature 7: downloaded file monitor (last N days of the Downloads folder).

For each file it collects: size, type, modified time, SHA-256, download source
(Windows 'Zone.Identifier' stream) and Authenticode signature (for executables),
then gives a SAFE / CAUTION / WARNING rating with reasons.
This is a heuristic check, NOT an antivirus scan.
"""
import hashlib
import json
import os
import re
import subprocess
import tempfile
import time
import winreg
from datetime import datetime
from urllib.parse import urlparse

EXECUTABLE = {".exe", ".msi", ".dll", ".scr", ".com", ".pif", ".cpl", ".sys"}
SCRIPTS = {".bat", ".cmd", ".ps1", ".vbs", ".vbe", ".js", ".jse", ".wsf", ".hta", ".reg", ".lnk", ".jar", ".apk"}
ARCHIVES = {".zip", ".rar", ".7z", ".iso", ".img", ".cab", ".gz", ".tar"}
MACRO_DOCS = {".docm", ".xlsm", ".pptm", ".xlsb"}
DOC_EXT = {".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".txt", ".jpg", ".jpeg", ".png", ".gif", ".mp3", ".mp4"}
IN_PROGRESS = {".crdownload", ".part", ".download", ".opdownload", ".tmp"}
MAX_HASH_BYTES = 300 * 1024 * 1024  # skip hashing files larger than 300 MB


def downloads_folder():
    """Real Downloads path (handles OneDrive/redirected folders)."""
    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders"
        )
        value, _ = winreg.QueryValueEx(key, "{374DE290-123F-4565-9164-39C4925E467B}")
        return os.path.expandvars(value)
    except OSError:
        return os.path.join(os.path.expanduser("~"), "Downloads")


def sha256(path, size):
    if size > MAX_HASH_BYTES:
        return "skipped (file too large)"
    h = hashlib.sha256()
    try:
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(1024 * 1024), b""):
                h.update(chunk)
        return h.hexdigest()
    except OSError:
        return "unreadable"


def read_source(path):
    """Read the 'Mark of the Web' stream: where the file was downloaded from."""
    try:
        with open(path + ":Zone.Identifier", "r", errors="replace") as f:
            text = f.read()
    except OSError:
        return None, None
    zone = re.search(r"ZoneId=(\d)", text)
    host = re.search(r"HostUrl=(.+)", text)
    return (zone.group(1) if zone else None), (host.group(1).strip() if host else None)


def check_signatures(paths):
    """Authenticode status for many files in a single PowerShell call."""
    if not paths:
        return {}
    fd, list_file = tempfile.mkstemp(suffix=".json")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(paths, f)
    script = (
        "$p = Get-Content -LiteralPath '%s' -Raw -Encoding UTF8 | ConvertFrom-Json; "
        "$r = @($p | ForEach-Object { $s = Get-AuthenticodeSignature -LiteralPath $_; "
        "[pscustomobject]@{Path=$_; Status=$s.Status.ToString(); Signer=$s.SignerCertificate.Subject} }); "
        "[Console]::OutputEncoding=[Text.Encoding]::UTF8; ConvertTo-Json -InputObject $r -Compress" % list_file
    )
    try:
        out = subprocess.run(
            ["powershell", "-NoProfile", "-Command", script], capture_output=True, text=True, encoding="utf-8", timeout=120
        ).stdout
        return {r["Path"]: r for r in json.loads(out)}
    except Exception:
        return {}
    finally:
        os.remove(list_file)


def rate(name, ext, sig, zone, host):
    """Return (rating, [reasons])."""
    level, reasons = 0, []  # 0 SAFE, 1 CAUTION, 2 WARNING

    def bump(l, why):
        nonlocal level
        level = max(level, l)
        reasons.append(why)

    stem_ext = os.path.splitext(os.path.splitext(name)[0])[1].lower()
    if (ext in EXECUTABLE | SCRIPTS) and stem_ext in DOC_EXT:
        bump(2, f"Double extension disguise ('{stem_ext}{ext}') - looks like a document but runs as a program")
    if ext in IN_PROGRESS:
        reasons.append("Download still in progress / incomplete")
    if ext in EXECUTABLE:
        status = (sig or {}).get("Status", "Unknown")
        if status == "Valid":
            signer = re.search(r"CN=([^,]+)", (sig or {}).get("Signer") or "")
            reasons.append("Signed by " + (signer.group(1).strip('"') if signer else "a trusted publisher"))
        elif status == "NotSigned":
            bump(2, "Executable is NOT digitally signed - publisher unknown")
        elif status == "Unknown":
            bump(1, "Could not verify signature")
        else:
            bump(2, f"Signature problem ({status}) - file may be tampered with")
    elif ext in SCRIPTS:
        bump(1, "Script / shortcut file type can run commands - only open if you trust the source")
    elif ext in MACRO_DOCS:
        bump(1, "Macro-enabled document - macros can run malicious code")
    elif ext in ARCHIVES:
        bump(1, "Archive - check contents before opening anything inside")

    if host:
        netloc = urlparse(host).netloc.split(":")[0]
        if re.fullmatch(r"\d{1,3}(\.\d{1,3}){3}", netloc):
            bump(1 if level < 2 else 2, f"Downloaded from a raw IP address ({netloc}), not a named website")
    elif zone is None and ext in EXECUTABLE | SCRIPTS | ARCHIVES | MACRO_DOCS:
        reasons.append("No download-source record (copied from elsewhere, USB or source was stripped)")

    return ["SAFE", "CAUTION", "WARNING"][level], reasons


def scan(days=30):
    folder = downloads_folder()
    cutoff = time.time() - days * 86400
    files = []
    if not os.path.isdir(folder):
        return folder, files
    for entry in os.scandir(folder):
        if entry.is_file() and entry.stat().st_mtime >= cutoff:
            files.append(entry)
    sigs = check_signatures([e.path for e in files if os.path.splitext(e.name)[1].lower() in EXECUTABLE])
    results = []
    for e in files:
        st = e.stat()
        ext = os.path.splitext(e.name)[1].lower()
        zone, host = read_source(e.path)
        rating, reasons = rate(e.name, ext, sigs.get(e.path), zone, host)
        results.append(
            {
                "File": e.name,
                "Size (KB)": round(st.st_size / 1024, 1),
                "Type": ext or "(none)",
                "Modified": datetime.fromtimestamp(st.st_mtime).strftime("%Y-%m-%d %H:%M"),
                "Source": host or "unknown",
                "SHA256": sha256(e.path, st.st_size),
                "Rating": rating,
                "Reasons": reasons,
            }
        )
    order = {"WARNING": 0, "CAUTION": 1, "SAFE": 2}
    results.sort(key=lambda r: (order[r["Rating"]], r["Modified"]), reverse=False)
    return folder, results


def report(days=30):
    folder, results = scan(days)
    summary = {
        "Folder scanned": folder,
        "Files in last %d days" % days: len(results),
        "WARNING": sum(r["Rating"] == "WARNING" for r in results),
        "CAUTION": sum(r["Rating"] == "CAUTION" for r in results),
        "SAFE": sum(r["Rating"] == "SAFE" for r in results),
    }
    return summary, results
