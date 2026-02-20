import yaml
import json
from core.logger import log
from core.runner import run_all_checks
from core.decision_engine import evaluate
from core.remediation_engine import execute
from core.backend_client import send_to_backend
from core.severity_engine import assign
from core.risk_engine import calculate


SERVER_NAME = "prod-01"


def main():
    log("Agent started")

    # Load config
    try:
        with open("config.yaml") as f:
            config = yaml.safe_load(f)

        log("Configuration loaded successfully")

    except Exception as e:
        log(f"Failed to load config.yaml: {e}")
        return

    # Run health checks
    results = run_all_checks(config)

    # Decision Layer
    results = evaluate(results, environment=config.get("env", "dev"))

    # Remediation Layer
    results = execute(
        results,
        max_attempts=config.get("retry", {}).get("max_attempts", 2)
    )

    # Severity Layer
    results = assign(results, environment=config.get("env", "dev"))

    # Risk Score
    results = calculate(results, environment=config.get("env", "dev"))

    # Attach server name
    for r in results:
        r["server"] = SERVER_NAME

    # Send to backend
    try:
        log(f"Sending {len(results)} events to backend")
        send_to_backend(results)
    except Exception as e:
        log(f"Backend send failed: {e}")

    # Local critical logging
    for r in results:
        if r["status"] in ["ALERT", "FAILED"]:
            log(f"{r['status']}: {r['check']} - {r.get('message')}")

    print(json.dumps(results, indent=2))
    log("Agent run completed")


if __name__ == "__main__":
    main()