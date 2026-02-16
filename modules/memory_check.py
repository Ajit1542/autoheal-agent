import psutil
from core.logger import log

def run(threshold):
    mem = psutil.virtual_memory().percent
    log(f"Memory usage checked: {mem}%")

    if mem > threshold:
        alert = {
            "check": "memory",
            "status": "ALERT",
            "severity": "HIGH",
            "message": f"High memory usage: {mem}%",
            "remediation": None,
            "resource": "memory",
            "retryable": False
        }
        log(f"Memory ALERT triggered: {alert['message']}")
        return alert

    return {
        "check": "memory",
        "status": "OK",
        "message": f"Memory normal: {mem}%"
    }
