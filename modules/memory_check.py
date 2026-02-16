import psutil

def run(threshold):
    mem = psutil.virtual_memory().percent

    if mem > threshold:
        return {
            "check": "memory",
            "status": "ALERT",
            "severity": "HIGH",
            "message": f"High memory usage: {mem}%",
            "remediation": None,
            "resource": "memory",
            "retryable": False
        }

    return {
        "check": "memory",
        "status": "OK",
        "message": f"Memory normal: {mem}%"
    }
