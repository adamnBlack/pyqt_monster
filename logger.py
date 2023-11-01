import logging
from logging.handlers import TimedRotatingFileHandler
import os

base_dir = "logs"

logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
logger = logging.getLogger()

# fileHandler = logging.FileHandler(f"{os.path.join(os.getcwd(), base_dir)}/"
#                                   f"gmonster.log")

log_file_path = os.path.join(os.getcwd(), base_dir, "gmonster.log")
fileHandler = TimedRotatingFileHandler(log_file_path,
                                       when="midnight",
                                       interval=1,
                                       backupCount=7)

fileHandler.setFormatter(logFormatter)
logger.addHandler(fileHandler)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
logger.addHandler(consoleHandler)
logger.setLevel(level=logging.INFO)
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("apscheduler").setLevel(logging.ERROR)
