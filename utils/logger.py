import logging
from datetime import datetime
import os

class LocalTimeFormatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        return datetime.fromtimestamp(record.created).strftime('%Y-%m-%d %H:%M:%S')

def setup_logging():
    # define the directory
    dir = os.path.join(os.getcwd(), 'logs')
    
    # Create the logs directory if it doesn't exist
    if not os.path.exists(dir):
        os.makedirs(dir)

    # Define log file paths
    activity_log_file= os.path.join(dir, 'activity.log')
    error_log_file = os.path.join(dir, 'error.log')

    # Create a custom formatter for local time
    formatter = LocalTimeFormatter('%(asctime)s - %(levelname)s - %(message)s')

    # Create file handlers for activity and error logs
    activity_handler = logging.FileHandler(activity_log_file)
    activity_handler.setLevel(logging.INFO)
    activity_handler.setFormatter(formatter)

    error_handler = logging.FileHandler(error_log_file)
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)

    # Create and configure the root logger
    logger = logging.getLogger("application_logger")
    logger.setLevel(logging.DEBUG)  # Log all levels
    logger.addHandler(activity_handler)
    logger.addHandler(error_handler)

    return logger
