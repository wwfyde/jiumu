import logging

# Creating and Configuring Logger

Log_Format = "%(levelname)s %(asctime)s - %(message)s"

logging.basicConfig(filename="logfile.log",
                    format=Log_Format,
                    level=logging.DEBUG)

logger = logging.getLogger()

# Testing our Logger
logger.info("Our First Log Message")
