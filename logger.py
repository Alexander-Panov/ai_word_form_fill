import logging

logging.basicConfig(
    format='%(asctime)s %(levelname)-10s %(name)s: %(message)s',
    level=logging.INFO)

logger = logging.getLogger("app")
