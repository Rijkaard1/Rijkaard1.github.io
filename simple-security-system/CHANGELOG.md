# Changelog

Each release updates `version.json` (version number and date) and adds an entry here.

## 1.2.2 - 2026-11-28

- New: friendlier app names in "Apps opened in the last 24 hours" (for example "Snipping Tool" instead of `Microsoft.ScreenSketch_8wekyb3d8bbwe!App`)
- Changed: entries for the same app (such as several version folders) are merged into one row; the original names are kept in the log

## 1.2.1 - 2026-11-28

- New: logo (purple hexagon with green SSS) shown as a small banner with the name and version when the program starts

## 1.2.0 - 2026-11-27

- New: log viewer (menu option 12) - browse saved scan logs by date, see a one-line summary per scan, filter by feature and open any entry in full
- Changed: Run all and save to log is now option 13

## 1.1.0 - 2026-11-22

- New: overall risk score (0-100, LOW / MODERATE / HIGH) with a breakdown of what raised it and tips (menu option 11)
- New: colored output (red / yellow / green); turns off automatically when piped or saved
- Changed: Run all and save to log is now option 12 and ends with the risk score

## 1.0.0 - 2026-11-22

First public release.

- Network info, public IP details, active connections
- Wi-Fi safety check
- Apps opened in the last 24 hours
- Downloaded files check with SAFE / CAUTION / WARNING ratings
- Find a file location by name and extension
- Unknown IP alerts (scan once and live mode)
- Startup programs check
- Open ports check with firewall status
- Run all and save to log
