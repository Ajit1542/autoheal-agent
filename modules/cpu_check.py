import psutil

def run(threshold):
    cpu = psutil.cpu_percent(interval=1)

    if cpu > threshold:
        return {
            "check": "cpu",
            "status": "ALERT",
            "severity": "HIGH",
            "message": f"High CPU usage: {cpu}%",
            "remediation": None,
            "retryable": False
        }

    return {
        "check": "cpu",
        "status": "OK",
        "message": f"CPU normal: {cpu}%"
    }
