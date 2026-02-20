import subprocess

def run(config):
    services = config.get("services", [])
    results = []

    for svc in services:
        try:
            status = subprocess.getoutput(f"systemctl is-active {svc}").strip()

            if status == "active":
                results.append({
                    "check": "service",
                    "resource": svc,
                    "status": "OK",
                    "message": f"{svc} running",
                    "retryable": False,
                    "remediation": None
                })
            else:
                results.append({
                    "check": "service",
                    "resource": svc,
                    "status": "ALERT",
                    "message": f"{svc} is {status.upper()}",
                    "retryable": True,
                    "remediation": {
                        "type": "restart_service",
                        "target": svc
                    }
                })

        except Exception as e:
            results.append({
                "check": "service",
                "resource": svc,
                "status": "ALERT",
                "message": f"{svc} check failed: {str(e)}",
                "retryable": False,
                "remediation": None
            })

    return results