import logging
import os
from datetime import datetime

# Define the logs directory
LOGS_DIR = "logs"

# Create the full path for the logs directory
log_dir_path = os.path.join(os.getcwd(), LOGS_DIR)

# Create the logs directory if it doesn't exist
# This should be done before defining the log file path
os.makedirs(log_dir_path, exist_ok=True)

# Define the log file name with a timestamp
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

# Create the full path to the log file
LOG_FILE_PATH = os.path.join(log_dir_path, LOG_FILE)

# Configure the basic logging setup
logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)


