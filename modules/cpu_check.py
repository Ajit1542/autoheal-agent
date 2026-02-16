import psutil

def run(threshold):
    try:
        cpu = psutil.cpu_percent(interval=1)

        if cpu > threshold:
            return {
                "check": "cpu",
                "status": "ALERT",
                "severity": "HIGH",
                "message": f"High CPU usage: {cpu}%",
                "remediation": None,
                "resource": "global",
                "retryable": False,
                "value": cpu
            }

        return {
            "check": "cpu",
            "status": "OK",
            "severity": "INFO",
            "message": f"CPU normal: {cpu}%",
            "resource": "global",
            "value": cpu
        }

    except Exception as e:
        return {
            "check": "cpu",
            "status": "ALERT",
            "severity": "CRITICAL",
            "message": f"CPU check failed: {str(e)}",
            "resource": "global",
            "retryable": False
        }
