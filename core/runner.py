# core/runner.py

from core.logger import log
from monitors import (
    cpu_monitor,
    memory_monitor,
    service_monitor,
    disk_monitor,
    mount_monitor,
    stale_mount_monitor
)

# Central monitor registry
MONITORS = [
    cpu_monitor,
    memory_monitor,
    service_monitor,
    disk_monitor,
    mount_monitor,
    stale_mount_monitor,
]


def safe_run(monitor, config):
    try:
        results = monitor.run(config)

        if not isinstance(results, list):
            results = [results]

        return results

    except Exception as e:
        log(f"Monitor {monitor.__name__} failed: {e}", level="ERROR")

        return [{
            "check": monitor.__name__,
            "resource": "system",
            "status": "ALERT",
            "message": f"Monitor execution failed: {str(e)}",
            "retryable": False,
            "remediation": None
        }]


def run_all_checks(config):
    log("Running all health checks")

    all_results = []

    for monitor in MONITORS:
        results = safe_run(monitor, config)
        all_results.extend(results)

    log(f"Checks completed. Total results: {len(all_results)}")

    return all_results