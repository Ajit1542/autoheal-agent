from modules import cpu_check, memory_check, service_check

def run_all_checks(config):
    results = []

    results.append(cpu_check.run(config["thresholds"]["cpu"]))
    results.append(memory_check.run(config["thresholds"]["memory"]))
    results.extend(service_check.run(config["services"]))

    return results
