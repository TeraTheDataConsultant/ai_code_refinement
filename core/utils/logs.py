import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# Suppress logs from `httpx` or other third-party libraries
logging.getLogger("httpx").setLevel(logging.WARNING)  # Suppresses INFO and DEBUG logs from httpx
logging.getLogger("urllib3").setLevel(logging.WARNING)  # If using libraries dependent on urllib3

logger = logging.getLogger(__name__)
logger.info("Logging handler set up complete. Proceed with adding data to files.")
