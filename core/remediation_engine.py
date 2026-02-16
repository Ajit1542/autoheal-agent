import time
import subprocess

def run_remediation_command(cmd):
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True
        )
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)


def handle_issues(results, max_attempts=2):
    final_results = []

    for r in results:

        # Only process ALERTs
        if r.get("status") != "ALERT":
            final_results.append(r)
            continue

        # Skip non-retryable
        if not r.get("retryable", False):
            final_results.append(r)
            continue

        # AI decision placeholder
        if r.get("remediation") == "AI_DECIDE":
            r["note"] = "Remediation deferred to AI decision engine"
            final_results.append(r)
            continue

        cmd = r.get("remediation")

        if not cmd:
            final_results.append(r)
            continue

        success = False

        for attempt in range(1, max_attempts + 1):
            r["note"] = f"Attempt {attempt} remediation"

            ok, out, err = run_remediation_command(cmd)

            r["last_output"] = out.strip()
            r["last_error"] = err.strip()

            if ok:
                r["status"] = "RESOLVED"
                r["note"] = f"Remediation succeeded on attempt {attempt}"
                success = True
                break

            time.sleep(2)

        if not success:
            r["status"] = "FAILED"

        final_results.append(r)

    return final_results
