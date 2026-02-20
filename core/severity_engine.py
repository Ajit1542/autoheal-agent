def assign(results, environment="dev"):
    """
    Assign dynamic severity to events.
    Adds 'severity' field.
    """

    updated = []

    for r in results:

        status = r.get("status")
        decision = r.get("decision")

        # Default
        severity = "INFO"

        if status == "OK":
            severity = "INFO"

        elif status == "RESOLVED":
            severity = "LOW"

        elif status == "FAILED":
            severity = "CRITICAL"

        elif status == "ALERT":

            if decision == "ESCALATE":
                severity = "CRITICAL" if environment == "prod" else "HIGH"

            elif decision == "AUTO_REMEDIATE":
                severity = "MEDIUM"

            else:
                severity = "HIGH"

        r["severity"] = severity
        updated.append(r)

    return updated