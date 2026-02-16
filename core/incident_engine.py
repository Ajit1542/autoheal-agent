import json
import os
from datetime import datetime
from core.logger import log

INCIDENT_FILE = "incidents/active_incidents.json"

def load_incidents():
    if not os.path.exists(INCIDENT_FILE):
        return {}
    try:
        with open(INCIDENT_FILE, "r") as f:
            content = f.read().strip()
            if not content:
                return {}
            return json.loads(content)
    except Exception as e:
        log(f"Failed to load incidents file: {e}", level="ERROR")
        return {}

def save_incidents(data):
    os.makedirs("incidents", exist_ok=True)
    with open(INCIDENT_FILE, "w") as f:
        json.dump(data, f, indent=2)

def generate_key(issue, server="local"):
    resource = issue.get("resource", "global")
    return f"{issue['check']}:{server}:{resource}"

def build_payload(r, server, incident_id):
    return {
        "incident_id": incident_id,
        "server": server,
        "check": r.get("check"),
        "resource": r.get("resource", "global"),
        "status": r.get("status"),
        "message": r.get("message", ""),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

def process_incidents(results, server="local"):
    incidents = load_incidents()
    final_results = []
    backend_payload = []

    log(f"Processing incidents for {len(results)} results")

    for r in results:
        if r.get("status") != "ALERT":
            final_results.append(r)
            continue

        key = generate_key(r, server)

        if key in incidents:
            incident_id = incidents[key]
            r["note"] = "Incident already exists. Skipping."
            r["incident"] = incident_id
        else:
            incident_id = f"INC{len(incidents)+1:04}"
            incidents[key] = incident_id
            r["incident"] = incident_id
            r["note"] = "New incident created"
            log(f"Created new incident: {incident_id} for {r.get('check')}")

        backend_payload.append(build_payload(r, server, incident_id))
        final_results.append(r)

    save_incidents(incidents)
    log(f"Incident processing completed. Total backend payload: {len(backend_payload)}")
    return final_results, backend_payload
