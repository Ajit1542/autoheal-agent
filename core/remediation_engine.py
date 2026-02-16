import time

def handle_issues(results, max_attempts=2):  # This function will handle remediation attempts for ALERTs 
    final_results = []

    for r in results:
        if r.get("status") != "ALERT": # Only handle ALERTs for remediation 
            final_results.append(r)
            continue

        if not r.get("retryable", False): # If not retryable, just log and move on 
            final_results.append(r)
            continue

        if r.get("remediation") == "AI_DECIDE": # If remediation is deferred to AI, just note it and move on    
            r["note"] = "Remediation deferred to AI decision engine"
            final_results.append(r)
            continue

        # If real remediation exists
        for attempt in range(1, max_attempts + 1):
            r["note"] = f"Attempt {attempt} remediation"

            # Here later we will run bash script
            
            time.sleep(2)

        r["status"] = "FAILED"
        final_results.append(r)

    return final_results
