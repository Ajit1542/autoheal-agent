import psutil
import subprocess

EXCLUDE_FS = ["tmpfs", "devtmpfs", "proc", "sysfs", "overlay"]

def run(threshold):
    results = []

    # -------- 1️⃣ Check Disk Usage --------
    for partition in psutil.disk_partitions():
        if any(fs in partition.fstype.lower() for fs in EXCLUDE_FS):
            continue

        try:
            usage = psutil.disk_usage(partition.mountpoint)
            percent = usage.percent

            if percent > threshold:
                results.append({
                    "check": "disk",
                    "status": "ALERT",
                    "severity": "HIGH",
                    "message": f"High disk usage on {partition.mountpoint}: {percent}%",
                    "remediation": None,
                    "resource": partition.mountpoint,
                    "retryable": False,
                    "value": percent
                })
            else:
                results.append({
                    "check": "disk",
                    "status": "OK",
                    "severity": "INFO",
                    "message": f"{partition.mountpoint} usage normal: {percent}%",
                    "resource": partition.mountpoint,
                    "value": percent
                })

        except Exception as e:
            results.append({
                "check": "disk",
                "status": "ALERT",
                "severity": "LOW",
                "message": f"Disk check failed on {partition.mountpoint}: {str(e)}",
                "resource": partition.mountpoint,
                "retryable": False
            })

    # -------- 2️⃣ Check df hang --------
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
            "status": "ALERT",
            "severity": "CRITICAL",
            "message": "df command hanging - possible stale mount",
            "remediation": None,
            "resource": "global",
            "retryable": False,
            "value": "timeout"
        })

    return results
