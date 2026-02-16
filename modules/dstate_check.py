import subprocess

def run():
    try:
        result = subprocess.run(
            ["ps", "-eo", "stat"],
            capture_output=True,
            text=True,
            timeout=5
        )

        lines = result.stdout.strip().split("\n")

        # Count lines starting with 'D'
        dstate_count = sum(1 for line in lines if line.startswith("D"))

        if dstate_count > 0:
            return [{
                "check": "dstate",
                "status": "ALERT",
                "severity": "CRITICAL",
                "message": f"{dstate_count} processes in D-state (possible I/O issue)",
                "remediation": None,
                "resource": "system",
                "retryable": False,
                "value": dstate_count
            }]
        else:
            return [{
                "check": "dstate",
                "status": "OK",
                "severity": "INFO",
                "message": "No D-state processes detected",
                "resource": "system",
                "value": 0
            }]

    except subprocess.TimeoutExpired:
        return [{
            "check": "dstate",
            "status": "ALERT",
            "severity": "CRITICAL",
            "message": "ps command timed out while checking D-state",
            "resource": "system",
            "retryable": False
        }]

    except Exception as e:
        return [{
            "check": "dstate",
            "status": "ALERT",
            "severity": "LOW",
            "message": f"D-state check failed: {str(e)}",
            "resource": "system",
            "retryable": False
        }]
