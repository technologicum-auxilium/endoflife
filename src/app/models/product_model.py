import httpx
import logging
from cachetools import cached, TTLCache
from typing import Any, Dict, List, Union

logger = logging.getLogger(__name__)

product_cache: TTLCache[str, Any] = TTLCache(maxsize=100, ttl=3600)


@cached(product_cache)
def fetch_product_data_sync(base_url: str, product: str) -> Union[Dict[str, Any], Any]:
    url = f"{base_url}{product}.json"
    logger.info(f"Requesting URL: {url}")
    try:
        response = httpx.get(url)
        response.raise_for_status()
        logger.info(f"Received response for URL: {url}")
        return response.json()
    except httpx.HTTPStatusError as exc:
        status_code = exc.response.status_code
        detail = exc.response.text
        logger.error(f"HTTPStatusError: {status_code} - {detail}")
        return {
            "error": {
                "type": "HTTPStatusError",
                "message": f"HTTP error occurred with status code {status_code}",
                "status_code": status_code,
                "detail": detail,
            }
        }
    except httpx.RequestError as exc:
        logger.error(f"RequestError: {exc}")
        return {
            "error": {
                "type": "RequestError",
                "message": "An error occurred while requesting data",
                "detail": str(exc),
            }
        }
    except Exception as exc:
        logger.exception("Unexpected error")
        return {
            "error": {
                "type": "Exception",
                "message": "An unexpected error occurred",
                "detail": str(exc),
            }
        }


@cached(product_cache)
def fetch_product_data_specific_sync(
    base_url: str, endpoint: str
) -> Union[Dict[str, Any], Any]:
    url = f"{base_url}{endpoint}.json"
    logger.info(f"Requesting URL: {url}")
    try:
        response = httpx.get(url)
        response.raise_for_status()
        logger.info(f"Received response for URL: {url}")
        return response.json()
    except httpx.HTTPStatusError as exc:
        status_code = exc.response.status_code
        detail = exc.response.text
        logger.error(f"HTTPStatusError: {status_code} - {detail}")
        return {
            "error": {
                "type": "HTTPStatusError",
                "message": f"HTTP error occurred with status code {status_code}",
                "status_code": status_code,
                "detail": detail,
            }
        }
    except httpx.RequestError as exc:
        logger.error(f"RequestError: {exc}")
        return {
            "error": {
                "type": "RequestError",
                "message": "An error occurred while requesting data",
                "detail": str(exc),
            }
        }
    except Exception as exc:
        logger.exception("Unexpected error")
        return {
            "error": {
                "type": "Exception",
                "message": "An unexpected error occurred",
                "detail": str(exc),
            }
        }


def render_product_summarized(data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    summarized_data = []
    for item in data:
        if isinstance(item, dict) and "eol" in item:
            summarized_data.append({"eol": item["eol"]})
    return summarized_data


def render_product_data(data: Any) -> Any:
    return data
