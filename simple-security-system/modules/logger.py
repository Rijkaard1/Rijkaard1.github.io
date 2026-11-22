"""Feature 4: save each scan to a dated log file in the logs folder."""
import json
import os
from datetime import datetime

LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs")


def save(feature, data):
    os.makedirs(LOG_DIR, exist_ok=True)
    now = datetime.now()
    path = os.path.join(LOG_DIR, f"{now:%Y-%m-%d}.log")
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps({"time": now.isoformat(timespec="seconds"), "feature": feature, "data": data}) + "\n")
    return path
