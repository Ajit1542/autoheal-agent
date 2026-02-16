import json
import os
from datetime import datetime

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
    except Exception:
        return {}


def save_incidents(data):
    os.makedirs(os.path.dirname(INCIDENT_FILE), exist_ok=True)
    with open(INCIDENT_FILE, "w") as f:
        json.dump(data, f, indent=2)


def generate_key(issue, server="local"):
    resource = issue.get("resource", "global")
    return f"{issue.get('check')}:{server}:{resource}"


def build_payload(r, server, incident_id):
    return {
        "incident_id": incident_id,
        "server": server,
        "check": r.get("check"),
        "resource": r.get("resource", "global"),
        "status": r.get("status"),
        "severity": r.get("severity", "MEDIUM"),
        "message": r.get("message", ""),
        "remediation": r.get("remediation"),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }


def process_incidents(results, server="local"):
    incidents = load_incidents()
    final_results = []

    for r in results:

        # Only create incidents for ALERT
        if r.get("status") != "ALERT":
            final_results.append(r)
            continue

        key = generate_key(r, server)

        if key in incidents:
            incident_id = incidents[key]
            r["incident"] = incident_id
            r["note"] = "Incident already exists"
        else:
            incident_id = f"INC{len(incidents)+1:04}"
            incidents[key] = incident_id
            r["incident"] = incident_id
            r["note"] = "New incident created"

        # Attach backend-ready payload inside result
        r["backend_payload"] = build_payload(r, server, incident_id)

        final_results.append(r)

    save_incidents(incidents)

    return final_results
