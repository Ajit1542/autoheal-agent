import psutil
from core.logger import log


def run(config):
    threshold = config.get("cpu_threshold", 85)
    results = []

    try:
        percent = psutil.cpu_percent(interval=1)

        log(f"CPU usage checked: {percent}%")

        if percent > threshold:
            results.append({
                "check": "cpu",
                "resource": "system",
                "status": "ALERT",
                "message": f"High CPU usage: {percent}%",
                "retryable": False,
                "remediation": {
                    "type": "investigate_cpu",
                    "target": "system"
                }
            })
        else:
            results.append({
                "check": "cpu",
                "resource": "system",
                "status": "OK",
                "message": f"CPU usage normal: {percent}%",
                "retryable": False,
                "remediation": None
            })

    except Exception as e:
        log(f"CPU check failed: {e}", level="ERROR")

        results.append({
            "check": "cpu",
            "resource": "system",
            "status": "ALERT",
            "message": f"CPU check failed: {str(e)}",
            "retryable": False,
            "remediation": None
        })

    return results