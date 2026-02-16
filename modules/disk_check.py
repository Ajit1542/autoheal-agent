import psutil
import subprocess
from core.logger import log

def run(threshold):
    results = []

    # Disk usage check
    for partition in psutil.disk_partitions():
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            percent = usage.percent
            log(f"Disk {partition.mountpoint} usage checked: {percent}%")

            if percent > threshold:
                alert = {
                    "check": "disk",
                    "status": "ALERT",
                    "severity": "HIGH",
                    "message": f"High disk usage on {partition.mountpoint}: {percent}%",
                    "remediation": None,
                    "resource": partition.mountpoint,
                    "retryable": False
                }
                log(f"Disk ALERT triggered: {alert['message']}")
                results.append(alert)
            else:
                results.append({
                    "check": "disk",
                    "status": "OK",
                    "message": f"{partition.mountpoint} usage normal: {percent}%"
                })
        except Exception as e:
            log(f"Disk check failed for {partition.mountpoint}: {e}", level="ERROR")
            continue

    # df hang check
    try:
        subprocess.run(["df", "-h"], timeout=5, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.TimeoutExpired:
        alert = {
            "check": "df_hang",
            "status": "ALERT",
            "severity": "CRITICAL",
            "message": "df command hanging - possible stale mount",
            "remediation": None,
            "retryable": False
        }
        log(f"Disk ALERT triggered: {alert['message']}")
        results.append(alert)

    return results
