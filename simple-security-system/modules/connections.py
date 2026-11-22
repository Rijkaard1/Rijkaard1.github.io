"""Feature 3: active connections and remote IPs seen (uses `netstat -ano` and `tasklist`)."""
import csv
import io
import subprocess


def _run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True, errors="replace").stdout


def _process_names():
    names = {}
    for row in csv.reader(io.StringIO(_run(["tasklist", "/fo", "csv", "/nh"]))):
        if len(row) >= 2:
            names[row[1]] = row[0]
    return names


def _is_private(ip):
    return (
        ip.startswith(("10.", "192.168.", "127.", "169.254.", "[::1]", "0.0.0.0", "[::]"))
        or any(ip.startswith(f"172.{n}.") for n in range(16, 32))
    )


def get_connections():
    names = _process_names()
    result = []
    for line in _run(["netstat", "-ano", "-p", "TCP"]).splitlines():
        parts = line.split()
        if len(parts) == 5 and parts[0] == "TCP" and parts[3] == "ESTABLISHED":
            remote_ip, _, remote_port = parts[2].rpartition(":")
            result.append(
                {
                    "Remote IP": remote_ip,
                    "Port": remote_port,
                    "Process": names.get(parts[4], f"PID {parts[4]}"),
                    "Type": "local" if _is_private(remote_ip) else "internet",
                }
            )
    return result


def report():
    conns = get_connections()
    external = [c for c in conns if c["Type"] == "internet"]
    return {
        "Established connections": len(conns),
        "Internet connections": len(external),
        "Unique remote IPs": len({c["Remote IP"] for c in external}),
    }, external
