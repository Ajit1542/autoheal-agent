def run():
    results = []

    try:
        # -------- Read fstab --------
        fstab_mounts = set()
        with open("/etc/fstab") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue

                parts = line.split()
                if len(parts) < 2:
                    continue

                mount_point = parts[1]
                fstype = parts[2] if len(parts) > 2 else ""

                # Ignore virtual filesystems
                if fstype in ["swap", "proc", "sysfs", "devtmpfs", "tmpfs"]:
                    continue

                fstab_mounts.add(mount_point)

        # -------- Read actual mounts --------
        mounted = set()
        with open("/proc/self/mounts") as f:
            for line in f:
                parts = line.split()
                if len(parts) >= 2:
                    mounted.add(parts[1])

        # -------- Check 1: fstab but not mounted --------
        missing_mounts = fstab_mounts - mounted

        for mount in missing_mounts:
            results.append({
                "check": "mount",
                "status": "ALERT",
                "severity": "HIGH",
                "message": f"{mount} present in fstab but not mounted",
                "remediation": "AI_DECIDE",
                "resource": mount,
                "retryable": False
            })

        # -------- Check 2: mounted but not in fstab --------
        extra_mounts = mounted - fstab_mounts

        for mount in extra_mounts:
            # Skip system mounts
            if mount.startswith(("/proc", "/sys", "/dev", "/run")):
                continue

            results.append({
                "check": "mount-extra",
                "status": "ALERT",
                "severity": "LOW",
                "message": f"{mount} mounted but not present in fstab",
                "remediation": "AI_DECIDE",
                "resource": mount,
                "retryable": False
            })

        # -------- If Everything OK --------
        if not results:
            results.append({
                "check": "mount",
                "status": "OK",
                "severity": "INFO",
                "message": "All fstab mounts correctly mounted",
                "resource": "system"
            })

        return results

    except Exception as e:
        return [{
            "check": "mount",
            "status": "ALERT",
            "severity": "LOW",
            "message": f"Mount check failed: {str(e)}",
            "resource": "system",
            "retryable": False
        }]
