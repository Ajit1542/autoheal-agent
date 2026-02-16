import yaml
import json
from core.runner import run_all_checks
from core.logger import log
from core.remediation_engine import handle_issues
from core.incident_engine import process_incidents
from core.backend_client import send_to_backend

SERVER_NAME = "prod-01"

def main():
    # Load configuration
    try:
        with open("config.yaml") as f:
            config = yaml.safe_load(f)
    except Exception as e:
        print(f"Failed to load config.yaml: {e}")
        return

    # 1️⃣ Run health checks
    results = run_all_checks(config)

    # 2️⃣ Attempt auto-remediation
    results = handle_issues(results, config["retry"]["max_attempts"])

    # 3️⃣ Process incidents (generate incident_id + payload)
    results = process_incidents(results, server=SERVER_NAME)

    # 4️⃣ Send ALERT incidents to backend
    alert_payload = [
    r["backend_payload"]
    for r in results
    if r.get("status") == "ALERT" and r.get("backend_payload") ]


    if alert_payload:
        try:
            send_to_backend(alert_payload)
        except Exception as e:
            log(f"Backend send failed: {str(e)}")

    # 5️⃣ Log locally
    for r in results:
        if r["status"] == "ALERT":
            log(r["message"])

    # 6️⃣ Print final output
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
