import asyncio
from fastapi import APIRouter, HTTPException
from app.views import product_view
from app.models import product_model
from concurrent.futures import ThreadPoolExecutor
import os
import logging

max_workers = int(os.getenv("MAX_WORKERS", 10))
base_url = os.getenv("BASE_URL", "https://endoflife.date/api/")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)

router = APIRouter()
executor = ThreadPoolExecutor(max_workers=max_workers)

async def run_blocking_task(task, *args):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(executor, task, *args)

@router.get("/products/{product}")
async def get_product(product: str):
    logger.info(f"Fetching product data for: {product}")
    try:
        data = await run_blocking_task(product_model.fetch_product_data_sync, base_url, product)
        if "error" in data:
            error = data["error"]
            logger.error(f"Error fetching product data: {error['message']} (Status Code: {error.get('status_code', 'N/A')})")
            raise HTTPException(status_code=error.get("status_code", 400), detail=error["message"])
        logger.info(f"Successfully fetched product data for: {product}")
        return product_view.render_product_data(data)
    except HTTPException as exc:
        logger.exception(f"HTTPException while fetching product data for: {product}")
        raise exc
    except Exception as exc:
        logger.exception(f"Exception while fetching product data for: {product}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {exc}")

@router.get("/products/{product}/{cycle}")
async def get_product_cycle(product: str, cycle: str):
    logger.info(f"Fetching product data for: {product} and cycle: {cycle}")
    try:
        data = await run_blocking_task(product_model.fetch_product_data_specific_sync, base_url, f"{product}/{cycle}")
        if "error" in data:
            error = data["error"]
            logger.error(f"Error fetching product data: {error['message']} (Status Code: {error.get('status_code', 'N/A')})")
            raise HTTPException(status_code=error.get("status_code", 400), detail=error["message"])
        logger.info(f"Successfully fetched product data for: {product} and cycle: {cycle}")
        return product_view.render_product_data(data)
    except HTTPException as exc:
        logger.exception(f"HTTPException while fetching product data for: {product} and cycle: {cycle}")
        raise exc
    except Exception as exc:
        logger.exception(f"Exception while fetching product data for: {product} and cycle: {cycle}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {exc}")
