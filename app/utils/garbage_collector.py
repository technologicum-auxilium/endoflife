import gc
import logging

logger = logging.getLogger(__name__)

class GarbageCollector:
    def __init__(self, thresholds=(700, 10, 5)):
        self.thresholds = thresholds
        self.set_thresholds()

    def set_thresholds(self):
        gc.set_threshold(*self.thresholds)
        logger.info(f"Garbage collector thresholds set to: {self.thresholds}")

    def collect(self):
        gc.collect()
        logger.info("Garbage collection completed.")
