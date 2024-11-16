import asyncio
from fastapi import APIRouter, HTTPException
from ..views import product_view
from ..models import product_model
from concurrent.futures import ThreadPoolExecutor
import os
import logging
from ..utils.garbage_collector import GarbageCollector

max_workers = int(os.getenv("MAX_WORKERS", 10))
base_url = os.getenv("BASE_URL", "https://endoflife.date/api/")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)

router = APIRouter()
executor = ThreadPoolExecutor(max_workers=max_workers)
garbage_collector = GarbageCollector()


async def run_blocking_task(task, *args):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(executor, task, *args)


@router.get("/products/{product}")
async def get_product(product: str):
    logger.info(f"Fetching data for: {product}")
    try:
        data = await run_blocking_task(
            product_model.fetch_product_data_sync, base_url, product
        )
        if "error" in data:
            error = data["error"]
            logger.error(
                f"Error fetching data: {error['message']} "
                f"(Status Code: {error.get('status_code', 'N/A')})"
            )
            raise HTTPException(
                status_code=error.get("status_code", 400), detail=error["message"]
            )
        logger.info(f"Fetched data for: {product}")
        garbage_collector.collect()
        return product_view.render_product_data(data)
    except HTTPException as exc:
        logger.exception(f"Error fetching data for {product}")
        raise exc
    except Exception as exc:
        logger.exception(f"Error fetching data for {product}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {exc}")


@router.get("/products/{product}/{cycle}")
async def get_product_cycle(product: str, cycle: str):
    logger.info(f"Fetching data for: {product} and cycle: {cycle}")
    try:
        data = await run_blocking_task(
            product_model.fetch_product_data_specific_sync,
            base_url,
            f"{product}/{cycle}",
        )
        if "error" in data:
            error = data["error"]
            logger.error(
                f"Error fetching data: {error['message']} "
                f"(Status Code: {error.get('status_code', 'N/A')})"
            )
            raise HTTPException(
                status_code=error.get("status_code", 400), detail=error["message"]
            )
        logger.info(f"Fetched data for: {product} and cycle: {cycle}")
        garbage_collector.collect()
        return product_view.render_product_data(data)
    except HTTPException as exc:
        logger.exception(f"Error fetching data for {product} and {cycle}")
        raise exc
    except Exception as exc:
        logger.exception(f"Error fetching data for {product} and {cycle}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {exc}")


@router.get("/products/{product}/{cycle}/summarized")
async def get_product_cycle_summarized(product: str, cycle: str):
    logger.info(f"Fetching summary for: {product} and {cycle}")
    try:
        data = await run_blocking_task(
            product_model.fetch_product_data_specific_sync,
            base_url,
            f"{product}/{cycle}",
        )
        if "error" in data:
            error = data["error"]
            logger.error(
                f"Error fetching data: {error['message']} "
                f"(Status Code: {error.get('status_code', 'N/A')})"
            )
            raise HTTPException(
                status_code=error.get("status_code", 400), detail=error["message"]
            )
        eol = data.get("eol")
        if eol is None:
            logger.error(f"'eol' not found in data for: {product} and {cycle}")
            raise HTTPException(status_code=404, detail="'eol' field not found in data")
        logger.info(f"Fetched 'eol' data for: {product} and {cycle}")
        garbage_collector.collect()
        return {"eol": eol}
    except HTTPException as exc:
        logger.exception(f"Error fetching summary for {product} and {cycle}")
        raise exc
    except Exception as exc:
        logger.exception(f"Error fetching summary for {product} and {cycle}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {exc}")
