import json
import os

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
    except:
        return {}


def save_incidents(data):
    with open(INCIDENT_FILE, "w") as f:
        json.dump(data, f, indent=2)

def generate_key(issue, server="local"):
    resource = issue.get("resource", "global")
    return f"{issue['check']}:{server}:{resource}"

def process_incidents(results, server="local"):
    incidents = load_incidents()

    final_results = []

    for r in results:
        if r.get("status") != "ALERT":
            final_results.append(r)
            continue

        key = generate_key(r, server)

        if key in incidents:
            r["note"] = "Incident already exists. Skipping."
            r["incident"] = incidents[key]
        else:
            incident_id = f"INC{len(incidents)+1:04}"
            incidents[key] = incident_id

            r["incident"] = incident_id
            r["note"] = "New incident created"

        final_results.append(r)

    save_incidents(incidents)
    return final_results
