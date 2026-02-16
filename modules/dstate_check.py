import subprocess

def run():
    try:
        output = subprocess.getoutput(
            "ps -eo stat | grep '^D' | wc -l"
        )

        count = int(output.strip())

        if count > 0:
            return [{
                "check": "dstate",
                "status": "ALERT",
                "severity": "CRITICAL",
                "message": f"{count} processes in D-state (possible I/O issue)",
                "remediation": None,
                "resource": "system",
                "retryable": False
            }]
        else:
            return [{
                "check": "dstate",
                "status": "OK",
                "message": "No D-state processes detected"
            }]
    except Exception as e:
        return [{
            "check": "dstate",
            "status": "ERROR",
            "message": str(e)
        }]
