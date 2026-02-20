import json
import os
import uuid
from datetime import datetime
from core.logger import log

INCIDENT_FILE = "incidents/active_incidents.json"

def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def load_incidents():
    if not os.path.exists(INCIDENT_FILE):
        return {}
    try: 
        with open(INCIDENT_FILE, "r") as f:
            content = f.read().strip()
            return json.loads(content) if content else {}
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

def build_payload(r, server, incident):
    return {
        "incident_id": incident["incident_id"],
        "server": server,
        "check": r.get("check"),
        "resource": r.get("resource", "global"),
        "status": incident["status"],
        "message": r.get("message", ""),
        "timestamp": now()
    }

def process_incidents(results, server="local"):
    incidents = load_incidents()
    final_results = []
    backend_payload = []

    log(f"Processing {len(results)} results")

    for r in results:

        if r.get("status") not in ["ALERT", "FAILED"]:
            final_results.append(r)
            continue

        key = generate_key(r, server)

        if key in incidents:
            incident = incidents[key]
            incident["last_seen"] = now()
            incident["status"] = "OPEN"
            incident["attempts"] += 1

            r["incident"] = incident["incident_id"]
            r["note"] = "Existing incident updated"

        else:
            incident = {
                "incident_id": str(uuid.uuid4()),
                "status": "OPEN",
                "first_seen": now(),
                "last_seen": now(),
                "attempts": 1
            }
            incidents[key] = incident

            r["incident"] = incident["incident_id"]
            r["note"] = "New incident created"

            log(f"Created new incident: {incident['incident_id']}")

        backend_payload.append(build_payload(r, server, incident))
        final_results.append(r)

    save_incidents(incidents)

    log(f"Incident processing done. Backend payload count: {len(backend_payload)}")

    return final_results, backend_payload


# Incident structure:
# {
#     "check:server:resource": {
#         "incident_id": "uuid",
#         "status": "OPEN" | "CLOSED",
#        "first_seen": "timestamp",
#        "last_seen": "timestamp",
#       "attempts": 1
#    }
# }
# Key is a combination of check name, server name, and resource to ensure uniqueness.
# This allows us to track incidents per resource and avoid duplicates.
# The "status" field can be used to track if the incident is still open or has been resolved.
# The "attempts" field can be used to track how many times we've seen this issue, which can help with prioritization and decision making.
# The "first_seen" and "last_seen" timestamps can help with tracking the age of the incident and when it was last observed.
# This structure allows us to easily update existing incidents or create new ones based on incoming results from the checks.
# When processing results, we can generate a key based on the check, server, and resource. If that key already exists in our incidents dictionary, we update the existing incident's "last_seen" timestamp and increment the "attempts" count. If it doesn't exist, we create a new incident entry with a unique ID and set the initial values.
# This approach ensures that we have a clear and organized way to manage incidents, track their status, and correlate them with the results from our health checks.    
# load_incidents function is responsible for loading the current state of incidents from a JSON file. It checks if the "active_incidents.json" file exists, and if it does, it reads the content and parses it as JSON to return a dictionary of incidents. If the file doesn't exist or if there's an error during loading, it returns an empty dictionary. This allows us to maintain a persistent state of incidents across runs of the agent, enabling us to track ongoing issues and their history.
# save_incidents function is responsible for saving the current state of incidents to a JSON file. It ensures that the "incidents" directory exists and then writes the incidents data to "active_incidents.json". This allows us to persist incident information across runs of the agent, enabling us to track ongoing issues and their history.
# generate_key function creates a unique key for each incident based on the check name, server name, and resource. This key is used to identify incidents in the incidents dictionary, allowing us to easily update existing incidents or create new ones without duplication.
# build_payload function constructs the payload that will be sent to the backend for each incident. It includes the incident ID, server name, check name, resource, status, message, and timestamp. This structured payload allows the backend to process and store incident information effectively.
# process_incidents function takes the results from the health checks, processes them to create or update incidents, and builds a payload for the backend. It iterates through the results, checks if they are in an alert or failed state, generates a key for each issue, and either updates an existing incident or creates a new one. Finally, it saves the updated incidents and returns the final results along with the payload for the backend.
# This incident engine allows us to manage and track incidents effectively, ensuring that we have a clear record of ongoing issues and their history, which can be crucial for troubleshooting and improving system reliability.
