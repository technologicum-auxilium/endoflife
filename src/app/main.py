import sys
import os
from fastapi import FastAPI
from .controllers import product_controller
from dotenv import load_dotenv
import logging
from .utils.custom_json_formatter import CustomJSONFormatter
from .health.health_checker import HealthChecker
from .utils.garbage_collector import GarbageCollector

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

load_dotenv()

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
formatter = CustomJSONFormatter()

json_handler = logging.StreamHandler()
json_handler.setFormatter(formatter)

logging.basicConfig(level=LOG_LEVEL, handlers=[json_handler])

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


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
