import subprocess

def run(services):
    results = []

    for svc in services:
        cmd = f"systemctl is-active {svc}"
        status = subprocess.getoutput(cmd).strip()

        if status != "active":
            results.append({
                "check": "service",
                "status": "ALERT",
                "severity": "HIGH",
                "message": f"{svc} is DOWN",
                "remediation": f"bash/restart_service.sh {svc}",
                "resource": svc,
                "retryable": True
            })
        else:
            results.append({
                "check": "service",
                "status": "OK",
                "message": f"{svc} running"
            })

    return results
