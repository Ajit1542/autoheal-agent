import subprocess

def run(services):
    results = []

    for svc in services:
        try:
            result = subprocess.run(
                ["systemctl", "is-active", svc],
                capture_output=True,
                text=True,
                timeout=5
            )

            status_output = result.stdout.strip()

            if result.returncode != 0 or status_output != "active":
                results.append({
                    "check": "service",
                    "status": "ALERT",
                    "severity": "HIGH",
                    "message": f"{svc} is DOWN",
                    "remediation": f"bash/restart_service.sh {svc}",
                    "resource": svc,
                    "retryable": True,
                    "value": status_output
                })
            else:
                results.append({
                    "check": "service",
                    "status": "OK",
                    "severity": "INFO",
                    "message": f"{svc} running",
                    "resource": svc,
                    "value": status_output
                })

        except subprocess.TimeoutExpired:
            results.append({
                "check": "service",
                "status": "ALERT",
                "severity": "CRITICAL",
                "message": f"{svc} check timed out",
                "resource": svc,
                "retryable": False
            })

        except Exception as e:
            results.append({
                "check": "service",
                "status": "ALERT",
                "severity": "CRITICAL",
                "message": f"{svc} check failed: {str(e)}",
                "resource": svc,
                "retryable": False
            })

    return results
