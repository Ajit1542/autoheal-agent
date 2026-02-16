import subprocess
from core.logger import log

def run(services):
    results = []

    for svc in services:
        cmd = f"systemctl is-active {svc}"
        status = subprocess.getoutput(cmd).strip()
        log(f"Service check for {svc}: {status}")

        if status != "active":
            alert = {
                "check": "service",
                "status": "ALERT",
                "severity": "HIGH",
                "message": f"{svc} is DOWN",
                "remediation": f"bash/restart_service.sh {svc}",
                "resource": svc,
                "retryable": True
            }
            log(f"Service ALERT triggered: {alert['message']}")
            results.append(alert)
        else:
            results.append({
                "check": "service",
                "status": "OK",
                "message": f"{svc} running"
            })

    return results
