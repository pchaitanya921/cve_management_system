import logging
import os
from logging_setup import logger

logger.info("This is an informational log.")
logger.error("An error occurred!")


# Define log directory and file
LOG_DIR = "logs"
LOG_FILE = "app.log"

# Ensure log directory exists
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# Configure logging
logging.basicConfig(
    filename=os.path.join(LOG_DIR, LOG_FILE),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Create a logger instance
logger = logging.getLogger(__name__)

# Stream handler to print logs to console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

# Add the console handler to the logger
logger.addHandler(console_handler)

# Example usage
if __name__ == "__main__":
    logger.info("Logging setup initialized successfully.")
