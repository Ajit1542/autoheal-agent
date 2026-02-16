from core.logger import log

def run():
    results = []

    try:
        with open("/etc/fstab") as f:
            fstab_lines = [line.split()[1] for line in f if line.strip() and not line.startswith("#")]

        with open("/etc/mtab") as f:
            mtab_lines = [line.split()[1] for line in f]

        log(f"fstab entries: {fstab_lines}")
        log(f"mtab entries: {mtab_lines}")

        for mount in fstab_lines:
            if mount not in mtab_lines:
                alert = {
                    "check": "mount",
                    "status": "ALERT",
                    "severity": "HIGH",
                    "message": f"{mount} present in fstab but not mounted",
                    "remediation": "AI_DECIDE",
                    "resource": mount,
                    "retryable": False
                }
                log(f"Mount ALERT: {alert['message']}")
                results.append(alert)
            else:
                alert = {
                    "check": "check-mtab",
                    "status": "ALERT",
                    "severity": "LOW",
                    "message": f"{mount} is mounted but not present in fstab",
                    "remediation": "AI_DECIDE",
                    "resource": mount,
                    "retryable": False
                }
                log(f"Mount ALERT: {alert['message']}")
                results.append(alert)

        if not results:
            results.append({"check": "mount", "status": "OK", "message": "All fstab mounts present in mtab"})
            log("All mounts are OK")

    except Exception as e:
        log(f"Mount check failed: {e}", level="ERROR")
        return [{"check": "mount", "status": "ERROR", "message": str(e)}]

    return results
