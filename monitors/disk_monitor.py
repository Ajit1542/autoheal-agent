import psutil
import subprocess
from core.logger import log


def run(config):
    threshold = config.get("disk_threshold", 80)
    results = []

    # -------------------------
    # Disk Usage Check
    # -------------------------
    for partition in psutil.disk_partitions():
        mount = partition.mountpoint

        try:
            usage = psutil.disk_usage(mount)
            percent = usage.percent
            log(f"Disk {mount} usage checked: {percent}%")

            if percent > threshold:
                results.append({
                    "check": "disk",
                    "resource": mount,
                    "status": "ALERT",
                    "message": f"High disk usage: {percent}%",
                    "retryable": False,
                    "remediation": {
                        "type": "clean_disk",
                        "target": mount
                    }
                })
            else:
                results.append({
                    "check": "disk",
                    "resource": mount,
                    "status": "OK",
                    "message": f"Usage normal: {percent}%",
                    "retryable": False,
                    "remediation": None
                })

        except Exception as e:
            log(f"Disk check failed for {mount}: {e}", level="ERROR")

            results.append({
                "check": "disk",
                "resource": mount,
                "status": "ALERT",
                "message": f"Disk check failed: {str(e)}",
                "retryable": False,
                "remediation": None
            })

    # -------------------------
    # df Hang Check (Stale Mount Detection)
    # -------------------------
    try:
        subprocess.run(
            ["df", "-h"],
            timeout=5,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    except subprocess.TimeoutExpired:
        results.append({
            "check": "df_hang",
            "resource": "system",
            "status": "ALERT",
            "message": "df command hanging - possible stale mount",
            "retryable": False,
            "remediation": {
                "type": "investigate_stale_mount",
                "target": "system"
            }
        })

    return results