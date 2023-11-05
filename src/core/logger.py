# src/core/logger.py
import logging
import sys

def setup_logger() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
        ],
    )

logger = logging.getLogger(__name__)
