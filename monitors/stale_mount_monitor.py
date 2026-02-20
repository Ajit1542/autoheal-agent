import subprocess
from core.logger import log


def run(config=None):
    results = []

    try:
        subprocess.run(
            ["df", "-h"],
            timeout=5,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        results.append({
            "check": "stale_mount",
            "resource": "system",
            "status": "OK",
            "message": "No stale mounts detected",
            "retryable": False,
            "remediation": None
        })

    except subprocess.TimeoutExpired:
        log("df command timeout — possible stale mount", level="ERROR")

        results.append({
            "check": "stale_mount",
            "resource": "system",
            "status": "ALERT",
            "message": "df command hanging — possible stale mount",
            "retryable": False,
            "remediation": {
                "type": "investigate_stale_mount",
                "target": "system"
            }
        })

    return results