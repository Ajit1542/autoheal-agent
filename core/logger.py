import logging
import os
import sys

# Ensure logs directory exists
os.makedirs("logs", exist_ok=True)

# Configure logging
logging.basicConfig(
    filename="logs/agent.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Console logging optional
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
logging.getLogger().addHandler(console_handler)

def log(msg, level="INFO"):
    """Log a message to file (and console)"""
    if level.upper() == "ERROR":
        logging.error(msg)
    elif level.upper() == "WARNING":
        logging.warning(msg)
    else:
        logging.info(msg)
