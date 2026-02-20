from core.logger import log


def run(config=None):
    results = []

    try:
        # -------------------------
        # Read fstab (expected mounts)
        # -------------------------
        with open("/etc/fstab") as f:
            fstab_mounts = [
                line.split()[1]
                for line in f
                if line.strip() and not line.startswith("#")
            ]

        # -------------------------
        # Read mtab (currently mounted)
        # -------------------------
        with open("/etc/mtab") as f:
            mtab_mounts = [
                line.split()[1]
                for line in f
                if line.strip()
            ]

        log(f"fstab mounts: {fstab_mounts}")
        log(f"mtab mounts: {mtab_mounts}")

        # -------------------------
        # Check: Missing mounts
        # -------------------------
        for mount in fstab_mounts:
            if mount not in mtab_mounts:
                results.append({
                    "check": "mount",
                    "resource": mount,
                    "status": "ALERT",
                    "message": "Defined in fstab but not mounted",
                    "retryable": False,
                    "remediation": {
                        "type": "mount_filesystem",
                        "target": mount
                    }
                })

        # -------------------------
        # Check: Unexpected mounts
        # -------------------------
        for mount in mtab_mounts:
            if mount not in fstab_mounts:
                results.append({
                    "check": "mount",
                    "resource": mount,
                    "status": "ALERT",
                    "message": "Mounted but not defined in fstab",
                    "retryable": False,
                    "remediation": {
                        "type": "investigate_mount",
                        "target": mount
                    }
                })

        # -------------------------
        # If no problems
        # -------------------------
        if not results:
            results.append({
                "check": "mount",
                "resource": "system",
                "status": "OK",
                "message": "All mounts consistent",
                "retryable": False,
                "remediation": None
            })
            log("All mounts are consistent")

    except Exception as e:
        log(f"Mount check failed: {e}", level="ERROR")

        results.append({
            "check": "mount",
            "resource": "system",
            "status": "ALERT",
            "message": f"Mount check failed: {str(e)}",
            "retryable": False,
            "remediation": None
        })

    return results