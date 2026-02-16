from modules import cpu_check, memory_check, service_check, disk_check, dstate_check,mount_check

def run_all_checks(config):
    results = []

    results.append(cpu_check.run(config["thresholds"]["cpu"]))
    results.append(memory_check.run(config["thresholds"]["memory"]))
    results.extend(service_check.run(config["services"]))
    results.extend(disk_check.run(config["thresholds"]["disk"]))
    results.extend(dstate_check.run())
    results.extend(mount_check.run())
    return results
