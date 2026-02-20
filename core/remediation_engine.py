import subprocess
import time
from core.logger import log

def execute(results, max_attempts=2):
    """
    Execute remediation based on decision.
    """

    final_results = []

    for r in results:

        if r.get("decision") != "AUTO_REMEDIATE":
            final_results.append(r)
            continue

        remediation = r.get("remediation")
        success = False

        for attempt in range(1, max_attempts + 1):
            log(f"Remediation attempt {attempt} for {r['resource']}")

            if remediation and remediation["type"] == "restart_service":

                service_name = remediation["target"]
                cmd = f"bash/restart_service.sh {service_name}"

                try:
                    subprocess.run(
                        cmd,
                        shell=True,
                        check=True,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True
                    )

                    status = subprocess.getoutput(
                        f"systemctl is-active {service_name}"
                    ).strip()

                    if status == "active":
                        success = True
                        break

                    time.sleep(2)

                except subprocess.CalledProcessError as e:
                    log(f"Remediation failed: {e.stderr.strip()}")
                    time.sleep(2)

        if success:
            r["status"] = "RESOLVED"
            log(f"{r['resource']} resolved successfully")
        else:
            r["status"] = "FAILED"
            log(f"{r['resource']} remediation failed")

        final_results.append(r)

    return final_results

# The execute function is responsible for performing remediation actions based on the decisions made in the decision engine. It iterates through the results, checks if the decision is "AUTO_REMEDIATE", and if so, it attempts to execute the specified remediation action (e.g., restarting a service) up to a maximum number of attempts. The function uses subprocess to run shell commands and checks the status of the service after each attempt. If the remediation is successful, it updates the status to "RESOLVED"; otherwise, it marks it as "FAILED". This allows the agent to automatically attempt to fix issues and track the outcome of those attempts effectively.
# The logic in this function ensures that we are making a concerted effort to resolve issues automatically while also providing feedback on the success or failure of those attempts, which can be crucial for improving system reliability and reducing the need for manual intervention.
#  