"""Feature 6: apps opened in the last 24 hours.

Source: Windows UserAssist registry key (per-user, no admin needed). It records
programs launched through Explorer/Start menu, with run count and last-run time.
Programs started from a terminal or scripts may not appear there.

Windows stores technical names (for example "Microsoft.ScreenSketch_8wekyb3d8bbwe!App").
friendly_name() turns them into readable ones ("Snipping Tool"): known apps come from
the tables below, anything else is cleaned up by simple rules. Entries that end up with
the same friendly name (for example one app launched from several version folders) are
merged. The original names are kept in "Raw names" for the log.
"""
import codecs
import os
import re
import struct
import winreg
from datetime import datetime, timedelta, timezone

BASE = r"Software\Microsoft\Windows\CurrentVersion\Explorer\UserAssist"
EPOCH = datetime(1601, 1, 1, tzinfo=timezone.utc)

# lower-case file name (without .exe) or full package name -> friendly name
EXACT = {
    "chrome": "Google Chrome", "msedge": "Microsoft Edge", "brave": "Brave Browser", "firefox": "Firefox",
    "code": "Visual Studio Code", "chatgpt": "ChatGPT", "claude": "Claude", "discord": "Discord",
    "telegram": "Telegram", "spotify": "Spotify", "steam": "Steam", "zoom": "Zoom", "slack": "Slack",
    "whatsapp": "WhatsApp", "robloxplayerbeta": "Roblox", "msteams": "Microsoft Teams", "ms-teams": "Microsoft Teams",
    "winword": "Microsoft Word", "excel": "Microsoft Excel", "powerpnt": "Microsoft PowerPoint",
    "outlook": "Microsoft Outlook", "onenote": "Microsoft OneNote",
    "explorer": "File Explorer", "notepad": "Notepad", "mspaint": "Paint", "calc": "Calculator",
    "taskmgr": "Task Manager", "cmd": "Command Prompt", "powershell": "PowerShell",
    "windowsterminal": "Windows Terminal", "wt": "Windows Terminal", "snippingtool": "Snipping Tool",
    "msiexec": "Windows Installer", "asusmyasus": "MyASUS",
}

# lower-case start of a technical package name -> friendly name
PREFIX = [
    ("microsoft.visualstudiocode", "Visual Studio Code"),
    ("com.squirrel.anthropicclaude", "Claude"),
    ("openai.codex", "Codex"),
    ("microsoft.office.winword", "Microsoft Word"),
    ("microsoft.office.excel", "Microsoft Excel"),
    ("microsoft.office.powerpnt", "Microsoft PowerPoint"),
    ("microsoft.office.outlook", "Microsoft Outlook"),
    ("microsoft.office.onenote", "Microsoft OneNote"),
    ("microsoft.office.msaccess", "Microsoft Access"),
    ("microsoft.screensketch", "Snipping Tool"),
    ("microsoft.windows.photos", "Photos"),
    ("microsoft.windowsnotepad", "Notepad"),
    ("microsoft.windowscalculator", "Calculator"),
    ("microsoft.windowscamera", "Camera"),
    ("microsoft.paint", "Paint"),
    ("microsoft.windowsterminal", "Windows Terminal"),
    ("microsoft.windows.explorer", "File Explorer"),
    ("microsoft.windows.administrativetools", "Windows Tools"),
    ("windows.immersivecontrolpanel", "Settings"),
    ("microsoft.xboxgamingoverlay", "Xbox Game Bar"),
    ("microsoft.desktopappinstaller", "App Installer"),
    ("microsoft.microsoftedge", "Microsoft Edge"),
    ("microsoft.windowsstore", "Microsoft Store"),
    ("telegram.telegramdesktop", "Telegram"),
    ("naver.win32_line", "LINE"),
    ("unitytechnologies.unityhub", "Unity Hub"),
    ("b9eced6f.armourycrate", "Armoury Crate"),
    ("b9eced6f.asuspcassistant", "MyASUS"),
    ("microsoft.zunemusic", "Media Player"),
    ("spotifyab.spotifymusic", "Spotify"),
    ("mozilla.firefox", "Firefox"),
]

GENERIC_FILES = {"setup", "launcher", "installer", "install", "update", "updater", "uninstall", "unins000"}
SKIP_FOLDERS = {
    "application", "app", "installer", "bin", "versions", "windowsapps", "program files",
    "program files (x86)", "programdata", "appdata", "local", "roaming", "users", "windows", "system32",
}
_HASH = re.compile(r"_[a-z0-9]{13}$", re.I)  # publisher id Windows appends to package names
_VERSION = re.compile(r"^[\d._ x-]+$|^version-", re.I)


def _filetime_to_dt(ft):
    return EPOCH + timedelta(microseconds=ft // 10)


def _camel(s):
    """Split CamelCase words ("VisualStudioCode" -> "Visual Studio Code"); acronyms like GPT stay whole."""
    return re.sub(r"(?<=[a-z0-9])(?=[A-Z][a-z])", " ", s)


def _strip_tags(name):
    """Remove download-copy and architecture tags: "setup (1)", "Postman (x64)", "App-x64"."""
    name = re.sub(r"\s*\((?:\d+|x64|x86|64-bit|32-bit)\)", "", name, flags=re.I)
    return re.sub(r"[-_ ]x(?:64|86)$", "", name, flags=re.I).strip()


def _tidy(name):
    name = _strip_tags(name)
    name = name.replace("_", " ").strip()
    if re.fullmatch(r"[A-Za-z0-9]+", name):  # one run-together word: split it; leave real names alone
        name = _camel(name)
    return name[:1].upper() + name[1:] if name.islower() else name


def friendly_name(raw):
    """Readable name for a technical UserAssist name."""
    if "\\" in raw or "/" in raw:  # a program path
        parts = [p for p in re.split(r"[\\/]", raw) if p]
        base = _strip_tags(os.path.splitext(parts[-1])[0])
        low = base.lower()
        if low in EXACT:
            return EXACT[low]
        if low in GENERIC_FILES:  # "setup.exe" says nothing: name the folder it lives in
            for p in reversed(parts[:-1]):
                if not _VERSION.match(p) and p.lower() not in SKIP_FOLDERS and not p.startswith("{") and ":" not in p:
                    return f"{_camel(p)} ({low})"
        return _tidy(base or raw)
    family = _HASH.sub("", raw.split("!")[0])  # "Pkg_hash!App" -> "Pkg"
    low = family.lower()
    if low in EXACT:
        return EXACT[low]
    for prefix, name in PREFIX:
        if low.startswith(prefix):
            return name
    if re.search(r"\{[0-9a-f-]{36}\}", low):  # "Microsoft.AutoGenerated.{GUID}" carries no name
        return "Unnamed Windows app"
    parts = [p for p in family.split(".") if p and not p.isdigit() and p.lower() != "exe"]
    return _tidy(parts[-1] if parts else family)


def get_recent(hours=24):
    cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)
    found = []
    try:
        root = winreg.OpenKey(winreg.HKEY_CURRENT_USER, BASE)
    except OSError:
        return found
    with root:
        i = 0
        while True:
            try:
                guid = winreg.EnumKey(root, i)
            except OSError:
                break
            i += 1
            try:
                key = winreg.OpenKey(root, guid + r"\Count")
            except OSError:
                continue
            with key:
                j = 0
                while True:
                    try:
                        name, data, _ = winreg.EnumValue(key, j)
                    except OSError:
                        break
                    j += 1
                    if len(data) < 68:
                        continue
                    count = struct.unpack_from("<I", data, 4)[0]
                    ft = struct.unpack_from("<Q", data, 60)[0]
                    if ft == 0:
                        continue
                    last = _filetime_to_dt(ft)
                    raw = codecs.decode(name, "rot13")
                    if raw.lower().endswith(".lnk"):
                        continue  # shortcut duplicate of the app entry
                    if last >= cutoff:
                        found.append(
                            {
                                "App": friendly_name(raw),
                                "Last run": last.astimezone().strftime("%Y-%m-%d %H:%M"),
                                "Total runs": count,
                                "Raw names": [raw],
                            }
                        )
    merged = {}
    for r in found:  # same app from several entries: newest time, runs added up
        m = merged.get(r["App"])
        if m is None:
            merged[r["App"]] = r
        else:
            m["Total runs"] += r["Total runs"]
            m["Last run"] = max(m["Last run"], r["Last run"])
            m["Raw names"] += r["Raw names"]
    apps = list(merged.values())
    apps.sort(key=lambda a: a["Last run"], reverse=True)
    return apps


def report(hours=24):
    apps = get_recent(hours)
    return {"Apps opened in last %d hours" % hours: len(apps)}, apps
