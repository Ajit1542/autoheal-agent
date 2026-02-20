import subprocess
from core.logger import log

def run():
    try:
        output = subprocess.getoutput("ps -eo stat | grep '^D' | wc -l")
        count = int(output.strip())
        log(f"D-state process count: {count}")

        if count > 0:
            alert = {
                "check": "dstate",
                "status": "ALERT",
                "severity": "CRITICAL",
                "message": f"{count} processes in D-state (possible I/O issue)",
                "remediation": None,
                "resource": "system",
                "retryable": False
            }
            log(f"D-state ALERT triggered: {alert['message']}")
            return [alert]

        return [{"check": "dstate", "status": "OK", "message": "No D-state processes detected"}]

    except Exception as e:
        log(f"D-state check failed: {e}", level="ERROR")
        return [{"check": "dstate", "status": "ERROR", "message": str(e)}]
