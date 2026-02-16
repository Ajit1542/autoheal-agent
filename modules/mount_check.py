def run():
    results = []

    try:
        # Read fstab entries
        with open("/etc/fstab") as f:
            fstab_lines = [
                line.split()[1]
                for line in f
                if line.strip() and not line.startswith("#") # Only consider non-empty, non-comment lines   
            ]

        # Read mounted paths
        with open("/etc/mtab") as f:
            mtab_lines = [
                line.split()[1]
                for line in f
            ]

        for mount in fstab_lines:
            if mount not in mtab_lines:  # If fstab entry is not in mtab, it's an issue
                results.append({
                    "check": "mount",
                    "status": "ALERT",
                    "severity": "HIGH",
                    "message": f"{mount} present in fstab but not mounted",
                    "remediation": "AI_DECIDE",
                    "resource": mount,
                    "retryable": False
                })
            else: # if mount is mounted but not in fstab, its mtab issue
                results.append({
                    "check": "check-mtab",
                    "status": "ALERT",
                    "severity": "Low",
                    "message": f"{mount} is mounted but not present in fstab",
                    "remediation": "AI_DECIDE",
                    "resource": mount,
                    "retryable": False
                })

        if not results:
            results.append({
                "check": "mount",
                "status": "OK",
                "message": "All fstab mounts present in mtab"
            })

        

    except Exception as e:
        return [{
            "check": "mount",
            "status": "ERROR",
            "message": str(e)
        }]
    
    return results
