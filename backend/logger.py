import logging
from enum import StrEnum
from logging.handlers import TimedRotatingFileHandler
import os
import config

LOG_FORMAT = '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(message)s'



class LogLevels(StrEnum):
    debug = "DEBUG"
    info = "INFO"
    warning = "WARNING"
    error = "ERROR"
    critical = "CRITICAL"

class ColorFormatter(logging.Formatter):
    COLORS = {
        LogLevels.debug: "\033[94m",  # Blue
        LogLevels.info: "\033[37m",   # White
        LogLevels.warning: "\033[33m", # Yellow
        LogLevels.error: "\033[91m",   # Red
        LogLevels.critical: "\033[95m" # Magenta
    }
    RESET = "\033[0m"

    def format(self, record):
        log_color = self.COLORS.get(record.levelname, self.RESET)
        formatted_message = super().format(record)
        return f"{log_color}{formatted_message}{self.RESET}"
    
def configure_logging(log_level: LogLevels = LogLevels.debug, log_file: str = 'log.txt'):
    log_level = str(log_level).upper()
    log_levels = [level.value for level in LogLevels]
    
    logs_dir = config.log_directory
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
    log_file_path = os.path.join(logs_dir, log_file)

    if log_level not in log_levels:
        logging.basicConfig(level=logging.error)
        return
    
    handlers = []
    file_handler = TimedRotatingFileHandler(log_file_path, when='midnight', interval=1, backupCount=7)
    file_handler.setFormatter(logging.Formatter(LOG_FORMAT))
    handlers.append(file_handler)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(ColorFormatter(LOG_FORMAT))
    handlers.append(stream_handler)

    logging.basicConfig(level=log_level, handlers=handlers)


def get_log_file_as_json(log_file: str = 'log.txt'):
    log_file_path = os.path.join('logs', log_file)
    if not os.path.exists(log_file_path):
        return {"error": "Log file does not exist."}
    
    with open(log_file_path, 'r') as file:
        logs = file.readlines()
    
    log_entries = []
    for log in logs:
        parts = log.strip().split(' - ')
        if len(parts) >= 5:
            entry = {
                "timestamp": parts[0],
                "level": parts[1],
                "filename": parts[2],
                "function": parts[3],
                "message": ' - '.join(parts[4:])
            }
            log_entries.append(entry)
    
    return log_entries