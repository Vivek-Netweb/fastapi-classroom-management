import logging
from logging.handlers import RotatingFileHandler
import sys
# get logger
logger = logging.getLogger()

# logger formatter
formatter = logging.Formatter(
    fmt="[%(levelname)s] | [%(asctime)s] | [%(name)s] - %(message)s"
)

# handler
stream_handler = logging.StreamHandler(sys.stdout)
file_handler = logging.FileHandler("app.log")

# set formatters
stream_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

#  add handlers to the logger

logger.handlers = [stream_handler, file_handler]

logger.setLevel(logging.INFO)