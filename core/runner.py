from modules import (
    cpu_check,
    memory_check,
    service_check,
    disk_check,
    dstate_check,
    mount_check
)

def safe_run(check_func, *args):
    try:
        result = check_func(*args)
        # Ensure result is always a list
        if not isinstance(result, list):
            result = [result]
        return result
    except Exception as e:
        return [{
            "check": check_func.__module__,
            "status": "ALERT",
            "severity": "LOW",
            "message": f"Check execution failed: {str(e)}",
            "resource": "system",
            "retryable": False
        }]

def run_all_checks(config):
    results = []

    results.extend(safe_run(cpu_check.run, config["thresholds"]["cpu"]))
    results.extend(safe_run(memory_check.run, config["thresholds"]["memory"]))
    results.extend(safe_run(service_check.run, config["services"]))
    results.extend(safe_run(disk_check.run, config["thresholds"]["disk"]))
    results.extend(safe_run(dstate_check.run))
    results.extend(safe_run(mount_check.run))

    return results
