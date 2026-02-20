def calculate(results, environment="dev"):
    """
    Assign numeric risk score (0–100)
    Adds 'risk_score' field.
    """

    updated = []

    for r in results:

        score = 0

        status = r.get("status")
        severity = r.get("severity")
        decision = r.get("decision")
        check_type = r.get("check")

        # Base score by severity
        severity_map = {
            "INFO": 5,
            "LOW": 20,
            "MEDIUM": 40,
            "HIGH": 65,
            "CRITICAL": 90
        }

        score += severity_map.get(severity, 10)

        # Increase if production
        if environment == "prod":
            score += 10

        # Increase if remediation failed
        if status == "FAILED":
            score += 15

        # Critical check boosts
        critical_checks = ["service", "disk", "stale_mount"]

        if check_type in critical_checks:
            score += 5

        # Escalation adds weight
        if decision == "ESCALATE":
            score += 10

        # Cap at 100
        score = min(score, 100)

        r["risk_score"] = score
        updated.append(r)

    return updated