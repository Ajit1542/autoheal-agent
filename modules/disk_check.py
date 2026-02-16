import psutil
import subprocess

def run(threshold):
    results = []

    # -------- 1️⃣ Check Disk Usage --------
    for partition in psutil.disk_partitions():
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
                    "retryable": False
                })
            else:
                results.append({
                    "check": "disk",
                    "status": "OK",
                    "message": f"{partition.mountpoint} usage normal: {percent}%"
                })
        except Exception:
            continue

    # -------- 2️⃣ Check df hang --------
    try:
        subprocess.run(
            ["df", "-h"],
            timeout=5,   # If df takes more than 5 sec → assume hang
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
            "retryable": False
        })

    return results
