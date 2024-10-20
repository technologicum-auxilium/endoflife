import httpx
import logging
from cachetools import cached, TTLCache

logger = logging.getLogger(__name__)

# Cache com 100 itens e TTL de 1 hora
product_cache = TTLCache(maxsize=100, ttl=3600)

@cached(product_cache)
def fetch_product_data_sync(base_url: str, product: str):
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
def fetch_product_data_specific_sync(base_url: str, endpoint: str):
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
