def evaluate(results, environment="dev"):
    """
    Evaluate alerts and decide action.
    Adds 'decision' field.
    """

    updated = []

    for r in results:
        if r.get("status") != "ALERT":
            r["decision"] = "NONE"
            updated.append(r)
            continue

        if not r.get("retryable", False):
            r["decision"] = "ESCALATE"
            updated.append(r)
            continue

        if environment == "prod":
            r["decision"] = "ESCALATE"
        else:
            r["decision"] = "AUTO_REMEDIATE"

        updated.append(r)

    return updated

# The evaluate function is responsible for analyzing the results of the health checks and determining the appropriate action for each alert. It iterates through the results, checks the status of each check, and assigns a decision based on whether the issue is retryable and the environment (production or development). The decisions can be "ESCALATE" for critical issues that require immediate attention or "AUTO_REMEDIATE" for issues that can be automatically resolved. This function adds a 'decision' field to each result, which will be used later in the remediation process to determine how to handle each alert effectively.
# The logic in this function allows us to prioritize issues based on their severity and the environment, ensuring that critical issues in production are escalated while allowing for automated remediation in less critical environments. This helps to improve the efficiency of the agent and ensures that resources are focused on the most important issues.