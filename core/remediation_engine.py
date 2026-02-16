import subprocess
import time
from core.logger import log

def handle_issues(results, max_attempts=2):
    """
    Attempt remediation for ALERTs that are retryable
    Logs every attempt and outcome
    """
    final_results = []

    for r in results:
        if r.get("status") != "ALERT":
            final_results.append(r)
            continue

        if not r.get("retryable", False):
            log(f"Skipping non-retryable ALERT: {r['check']} - {r.get('message')}")
            final_results.append(r)
            continue

        if r.get("remediation") == "AI_DECIDE":
            r["note"] = "Remediation deferred to AI decision engine"
            log(f"ALERT {r['check']} deferred to AI decision")
            final_results.append(r)
            continue

        remediation_cmd = r.get("remediation")
        success = False

        for attempt in range(1, max_attempts + 1):
            r["note"] = f"Attempt {attempt} remediation"
            log(f"Attempt {attempt} remediation for {r['check']}: {remediation_cmd}")

            if remediation_cmd:
                try:
                    # Run the bash remediation
                    completed = subprocess.run(
                        remediation_cmd,
                        shell=True,
                        check=True,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True
                    )
                    log(f"Remediation output: {completed.stdout.strip()}")

                    # ✅ For services: check if service is now active
                    if r["check"] == "service":
                        service_name = r["resource"]
                        status = subprocess.getoutput(f"systemctl is-active {service_name}").strip()
                        log(f"Service {service_name} status after remediation: {status}")
                        if status == "active":
                            success = True
                            break
                        else:
                            log(f"Service {service_name} still {status}")
                            time.sleep(2)
                    else:
                        # For other checks, assume remediation worked if command didn't error
                        success = True
                        break

                except subprocess.CalledProcessError as e:
                    log(f"Remediation failed on attempt {attempt}: {e.stderr.strip()}")
                    time.sleep(2)
            else:
                log(f"No remediation command provided for {r['check']}")
                break

        if success:
            r["status"] = "RESOLVED"
            r["note"] += " - Remediation successful"
            log(f"ALERT {r['check']} resolved successfully")
        else:
            r["status"] = "FAILED"
            log(f"ALERT {r['check']} remediation failed after {max_attempts} attempts")

        final_results.append(r)

    return final_results
