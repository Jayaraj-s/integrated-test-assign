import httpx
from typing import Any
from fastapi import APIRouter

EXTERNAL_API_URL = "https://api.example.com/data"  # Dummy placeholder

class ExternalService:
    @staticmethod
    async def fetch_data(param: str) -> Any:
        """
        Fetch data from external API (mockable in tests)
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(EXTERNAL_API_URL, params={"param": param})
            response.raise_for_status()
            return response.json()


router = APIRouter()

@router.get("/external-data")
async def get_external_data(param: str):
    data = await ExternalService.fetch_data(param)
    return {"external_data": data}
