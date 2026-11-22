# Simple Security System

A small command-line security checker for Windows, written in Python. It runs from a text menu and reports on your laptop's network, connections, downloads and startup items. No extra libraries are needed, only Python 3 and Windows.

## Run it

```powershell
cd simple-security-system
python main.py
```

The menu shows the current version and the date it was last updated.

## Features

| # | Option | What it does |
|---|--------|--------------|
| 1 | Current network info | Connection type, Wi-Fi name, local IP, router address |
| 2 | My public IP details | Public IP, ISP, city and country (via ipinfo.io) |
| 3 | Active connections | Remote IPs your laptop is connected to, and the program using each |
| 4 | Wi-Fi safety check | Rates the Wi-Fi encryption: SAFE / OK / WEAK / UNSAFE |
| 5 | Apps opened in 24 hours | Programs launched recently (Windows UserAssist) |
| 6 | Downloaded files check | Last 30 days of Downloads: signature, source, risky types; rated SAFE / CAUTION / WARNING |
| 7 | Find a file location | Search all drives by file name and extension |
| 8 | Unknown IP alerts | Warns about IPs your laptop has not connected to before; scan once or live mode |
| 9 | Startup programs check | Registry, Startup folders and logon tasks; flags unsigned or odd entries |
| 10 | Open ports check | Listening TCP ports, who can reach them, firewall status |
| 11 | Risk score | Overall 0-100 score (LOW / MODERATE / HIGH) built from the other checks, with what raised it and tips |
| 12 | Run all and save to log | Runs the read-only checks, ends with the risk score and saves results to `logs/` |

Output is colored: red for WARNING / UNSAFE / HIGH, yellow for CAUTION, green for SAFE. Colors turn off automatically when output is piped or saved, or if the `NO_COLOR` environment variable is set.

## Limits

- Ratings are **heuristics, not an antivirus scan**. A signed file can still be unwanted, and an unsigned one can be harmless.
- Some details (such as program paths of system services) need administrator rights to read.
- The tool only reads information from your own laptop; it does not scan other devices.

## Privacy

- Option 2 and the new-IP alerts send your public IP (or the remote IP) to ipinfo.io for the lookup.
- Logs (`logs/`) and the known-IP list (`known_ips.json`) stay on your computer and are not part of this repository.

## Versions

The current version and update date live in [`version.json`](version.json). The project page on the website reads that file, so visitors always see the latest version. See [`CHANGELOG.md`](CHANGELOG.md) for what changed.
