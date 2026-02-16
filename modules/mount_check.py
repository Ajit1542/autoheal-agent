def run():
    results = []

    try:
        # Read fstab entries
        with open("/etc/fstab") as f:
            fstab_lines = [
                line.split()[1]
                for line in f
                if line.strip() and not line.startswith("#")
            ]

        # Read mounted paths
        with open("/etc/mtab") as f:
            mtab_lines = [
                line.split()[1]
                for line in f
            ]

        for mount in fstab_lines:
            if mount not in mtab_lines:
                results.append({
                    "check": "mount",
                    "status": "ALERT",
                    "severity": "HIGH",
                    "message": f"{mount} present in fstab but not mounted",
                    "remediation": f"mount {mount}",
                    "retryable": True
                })

        if not results:
            results.append({
                "check": "mount",
                "status": "OK",
                "message": "All fstab mounts present in mtab"
            })

        return results

    except Exception as e:
        return [{
            "check": "mount",
            "status": "ERROR",
            "message": str(e)
        }]
