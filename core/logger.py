import logging
import os

# Ensure logs folder exists
os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="logs/agent.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def log(msg, level="INFO"):
    if level.upper() == "INFO":
        logging.info(msg)
        print(f"[INFO] {msg}")
    elif level.upper() == "ERROR":
        logging.error(msg)
        print(f"[ERROR] {msg}")
    elif level.upper() == "WARNING":
        logging.warning(msg)
        print(f"[WARN] {msg}")
    else:
        logging.debug(msg)
        print(f"[DEBUG] {msg}")
