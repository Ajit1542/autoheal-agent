import subprocess

def run(services):
    results = []

    for svc in services:
        try:
            # Check service status
            status = subprocess.getoutput(f"systemctl is-active {svc}").strip()
            
            if status == "active":
                results.append({
                    "check": "service",
                    "status": "OK",
                    "message": f"{svc} running"
                })
            else:
                # If service is inactive, failed, or unknown
                results.append({
                    "check": "service",
                    "status": "ALERT",
                    "severity": "HIGH",
                    "message": f"{svc} is {status.upper()}",
                    "remediation": f"bash/restart_service.sh {svc}",
                    "resource": svc,
                    "retryable": True
                })

        except Exception as e:
            # If systemctl command fails
            results.append({
                "check": "service",
                "status": "ALERT",
                "severity": "CRITICAL",
                "message": f"{svc} check failed: {str(e)}",
                "remediation": None,
                "resource": svc,
                "retryable": False
            })

    return results
