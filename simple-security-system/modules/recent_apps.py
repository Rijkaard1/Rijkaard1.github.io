"""Feature 6: apps opened in the last 24 hours.

Source: Windows UserAssist registry key (per-user, no admin needed). It records
programs launched through Explorer/Start menu, with run count and last-run time.
Programs started from a terminal or scripts may not appear there.
"""
import codecs
import struct
import winreg
from datetime import datetime, timedelta, timezone

BASE = r"Software\Microsoft\Windows\CurrentVersion\Explorer\UserAssist"
EPOCH = datetime(1601, 1, 1, tzinfo=timezone.utc)


def _filetime_to_dt(ft):
    return EPOCH + timedelta(microseconds=ft // 10)


def get_recent(hours=24):
    cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)
    apps = []
    try:
        root = winreg.OpenKey(winreg.HKEY_CURRENT_USER, BASE)
    except OSError:
        return apps
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
                    if codecs.decode(name, "rot13").lower().endswith(".lnk"):
                        continue  # shortcut duplicate of the app entry
                    if last >= cutoff:
                        apps.append(
                            {
                                "App": codecs.decode(name, "rot13"),
                                "Last run": last.astimezone().strftime("%Y-%m-%d %H:%M"),
                                "Total runs": count,
                            }
                        )
    apps.sort(key=lambda a: a["Last run"], reverse=True)
    return apps


def report(hours=24):
    apps = get_recent(hours)
    return {"Apps opened in last %d hours" % hours: len(apps)}, apps
