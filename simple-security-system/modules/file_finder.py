"""Feature 8: find where a file was saved, by file name and extension.

Searches all fixed drives (skipping Windows/system folders). The name can be
partial; the extension is matched exactly. Case-insensitive.
"""
import ctypes
import os
import string
from datetime import datetime

SKIP_DIRS = {
    "windows", "$recycle.bin", "system volume information", "program files",
    "program files (x86)", "programdata", "$windows.~bt", "recovery", "node_modules", ".git",
}
MAX_RESULTS = 50


def fixed_drives():
    DRIVE_FIXED = 3
    mask = ctypes.windll.kernel32.GetLogicalDrives()
    drives = []
    for i, letter in enumerate(string.ascii_uppercase):
        root = f"{letter}:\\"
        if mask & (1 << i) and ctypes.windll.kernel32.GetDriveTypeW(root) == DRIVE_FIXED:
            drives.append(root)
    return drives


def find(name, ext):
    name = name.strip().lower()
    ext = ext.strip().lower().lstrip(".")
    ext = "." + ext if ext else ""
    matches = []
    for drive in fixed_drives():
        for dirpath, dirnames, filenames in os.walk(drive):
            dirnames[:] = [d for d in dirnames if d.lower() not in SKIP_DIRS]
            for fn in filenames:
                stem, fext = os.path.splitext(fn)
                if name in stem.lower() and (not ext or fext.lower() == ext):
                    full = os.path.join(dirpath, fn)
                    try:
                        st = os.stat(full)
                    except OSError:
                        continue
                    matches.append(
                        {
                            "Location": full,
                            "Size (KB)": round(st.st_size / 1024, 1),
                            "Modified": datetime.fromtimestamp(st.st_mtime).strftime("%Y-%m-%d %H:%M"),
                        }
                    )
    matches.sort(key=lambda m: m["Modified"], reverse=True)
    return matches
