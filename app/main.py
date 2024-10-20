from fastapi import FastAPI
from app.controllers import product_controller
from dotenv import load_dotenv
import os
import logging
from app.health.custom_json_formatter import CustomJSONFormatter
from app.health.health_checker import HealthChecker
from app.utils.garbage_collector import GarbageCollector

load_dotenv()

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
formatter = CustomJSONFormatter()

json_handler = logging.StreamHandler()
json_handler.setFormatter(formatter)

logging.basicConfig(
    level=LOG_LEVEL,
    handlers=[json_handler]
)

logger = logging.getLogger()
for handler in logger.handlers:
    handler.setFormatter(formatter)

app = FastAPI()
health_checker = HealthChecker()
garbage_collector = GarbageCollector()

app.include_router(product_controller.router)

@app.get("/health/liveness")
async def liveness():
    response = await health_checker.liveness()
    garbage_collector.collect()
    return response

@app.get("/health/readiness")
async def readiness():
    response = await health_checker.readiness()
    garbage_collector.collect()
    return response
