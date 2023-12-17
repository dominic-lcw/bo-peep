import os
import logging

logger = logging.getLogger()

logger.setLevel(logging.DEBUG)

# Create FileHandler
script_dir = os.path.dirname(os.path.realpath(__file__))
log_file = os.path.join(script_dir, 'file.log')
file_handler = logging.FileHandler(log_file, mode = "w")
file_handler.setLevel(logging.DEBUG)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)


# Create formatters and add it to handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)

# Add handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(stream_handler)
