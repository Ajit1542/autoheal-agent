import psutil
from core.logger import log

def run(threshold):
    cpu = psutil.cpu_percent(interval=1)
    log(f"CPU usage checked: {cpu}%")

    if cpu > threshold:
        alert = {
            "check": "cpu",
            "status": "ALERT",
            "severity": "HIGH",
            "message": f"High CPU usage: {cpu}%",
            "remediation": None,
            "resource": "global",
            "retryable": False
        }
        log(f"CPU ALERT triggered: {alert['message']}")
        return alert

    return {
        "check": "cpu",
        "status": "OK",
        "message": f"CPU normal: {cpu}%"
    }
