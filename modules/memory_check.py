import psutil

def run(threshold):
    try:
        mem = psutil.virtual_memory().percent

        if mem > threshold:
            return {
                "check": "memory",
                "status": "ALERT",
                "severity": "HIGH",
                "message": f"High memory usage: {mem}%",
                "remediation": None,
                "resource": "memory",
                "retryable": False,
                "value": mem
            }

        return {
            "check": "memory",
            "status": "OK",
            "severity": "INFO",
            "message": f"Memory normal: {mem}%",
            "resource": "memory",
            "value": mem
        }

    except Exception as e:
        return {
            "check": "memory",
            "status": "ALERT",
            "severity": "CRITICAL",
            "message": f"Memory check failed: {str(e)}",
            "resource": "memory",
            "retryable": False
        }
