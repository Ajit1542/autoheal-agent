import yaml
import json
from core.runner import run_all_checks
from core.logger import log
from core.remediation_engine import handle_issues
from core.incident_engine import process_incidents

with open("config.yaml") as f:
    config = yaml.safe_load(f)

results = run_all_checks(config)
results = handle_issues(results, config["retry"]["max_attempts"])
results = process_incidents(results, server="prod-01")

for r in results:
    if r["status"] == "ALERT":
        log(r["message"])

print(json.dumps(results, indent=2))
