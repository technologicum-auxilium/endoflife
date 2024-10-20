import httpx
import os
import logging
from fastapi import HTTPException

logger = logging.getLogger(__name__)

class HealthChecker:
    def __init__(self):
        self.base_url = os.getenv("BASE_URL", "https://endoflife.date/api/")
        self.check_url = self.base_url + "all.json"

    async def check_site_health(self):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(self.check_url)
                response.raise_for_status()
                return response.status_code == 200
        except httpx.HTTPStatusError as exc:
            logger.error(f"HTTPStatusError: {exc.response.status_code} - {exc.response.text}")
        except Exception as exc:
            logger.exception("Unexpected error during health check")
        return False

    async def liveness(self):
        if await self.check_site_health():
            return {"status": "alive"}
        raise HTTPException(status_code=500, detail="Liveness check failed")

    async def readiness(self):
        if await self.check_site_health():
            return {"status": "ready"}
        raise HTTPException(status_code=500, detail="Readiness check failed")
