import psutil
from core.logger import log


def run(config):
    threshold = config.get("memory_threshold", 80)
    results = []

    try:
        memory = psutil.virtual_memory()
        percent = memory.percent

        log(f"Memory usage checked: {percent}%")

        if percent > threshold:
            results.append({
                "check": "memory",
                "resource": "system",
                "status": "ALERT",
                "message": f"High memory usage: {percent}%",
                "retryable": False,
                "remediation": {
                    "type": "investigate_memory",
                    "target": "system"
                }
            })
        else:
            results.append({
                "check": "memory",
                "resource": "system",
                "status": "OK",
                "message": f"Memory usage normal: {percent}%",
                "retryable": False,
                "remediation": None
            })

    except Exception as e:
        log(f"Memory check failed: {e}", level="ERROR")

        results.append({
            "check": "memory",
            "resource": "system",
            "status": "ALERT",
            "message": f"Memory check failed: {str(e)}",
            "retryable": False,
            "remediation": None
        })

    return results