import yaml
import json
from core.runner import run_all_checks
from core.logger import log

with open("config.yaml") as f:
    config = yaml.safe_load(f)

results = run_all_checks(config)

for r in results:
    if r["status"] == "ALERT":
        log(r["message"])

print(json.dumps(results, indent=2))
