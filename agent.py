import yaml
import json
from core.logger import log
from core.runner import run_all_checks
from core.remediation_engine import handle_issues
from core.incident_engine import process_incidents
from core.backend_client import send_to_backend

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

    # 1️⃣ Run health checks
    log("Running health checks")
    results = run_all_checks(config)

    # 2️⃣ Attempt remediation
    log("Handling remediation attempts")
    results = handle_issues(results, config["retry"]["max_attempts"])

    # 3️⃣ Process incidents
    log("Processing incidents")
    results, backend_payload = process_incidents(results, server=SERVER_NAME)

    # 4️⃣ Send ALERT incidents to backend
    if backend_payload:
        try:
            log(f"Sending {len(backend_payload)} ALERT(s) to backend")
            send_to_backend(backend_payload)
        except Exception as e:
            log(f"Backend send failed: {e}")

    # 5️⃣ Log ALERTs locally
    for r in results:
        if r["status"] in ["ALERT", "FAILED"]:
            log(f"ALERT logged: {r['check']} - {r.get('message')} - Note: {r.get('note')}")

    # 6️⃣ Print final results
    print(json.dumps(results, indent=2))
    log("Agent run completed")

if __name__ == "__main__":
    main()
