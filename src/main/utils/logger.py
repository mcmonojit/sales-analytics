import logging
import sys


class Logger:
    def __init__(self, name: str = 'app_logger', level: int = logging.DEBUG, log_to_file: bool = False, log_file_path: str = 'logs/app.log'):
        logging.basicConfig(
            level=level,
            format='%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            stream=sys.stdout
            # TODO: implement dual stream logging - both stdout and stderr based on log level (e.g., INFO and below to stdout, WARNING and above to stderr)
            # TODO: Add file handler to log to a configurable file or in logs/ directory instead of console
            # filename='app.log',
            # filemode='a',  # Append to the log file
            # encoding='utf-8'
        )
        self.logger = logging.getLogger(name)

    def info(self, message: str):
        self.logger.info(message)

    def warning(self, message: str):
        self.logger.warning(message)

    def error(self, message: str):
        self.logger.error(message)

    def debug(self, message: str):
        self.logger.debug(message)

    def log(self, level: int, message: str):
        self.logger.log(level, message)



# TODO:
# Handle instantiation and usage:
# Ensure the class can be instantiated easily (e.g., logger = Logger()).
# To avoid duplicate logs, check if handlers are already added (use if not self.logger.handlers:).
# In other files (like main.py), import the class and create an instance at the top, then replace print() calls with logger methods.





#Working of log method:
# The log method calls self.logger.log(level, message), where self.logger is a logging.Logger instance. Here's what happens step by step:
# Level Check: The logger checks if the provided level (an integer like logging.DEBUG) is at or above the logger's effective level (set in __init__ via logging.basicConfig). If not, the message is ignored and no further action occurs.
# LogRecord Creation: If the level is enabled, a LogRecord object is created, containing details like the timestamp, level name, message, and logger name.
# Handler Propagation: The logger propagates the record to its handlers (and parent loggers if configured). Since logging.basicConfig is used without a file handler (as per the TODO), it typically adds a default StreamHandler that outputs to the console (stderr by default).
# Formatting and Output: Each handler formats the record using the configured format string ('%(asctime)s - %(levelname)s - %(message)s') and outputs it. For the stream handler, this means printing to the console.
# Completion: The process ends, with the message logged if conditions are met, or silently discarded otherwise. No return value is produced.