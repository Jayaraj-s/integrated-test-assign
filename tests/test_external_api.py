import httpx
import pytest
from services.external_api import ExternalService

EXTERNAL_API_URL = "https://api.example.com/data"

@pytest.mark.asyncio
async def test_fetch_data_success(httpx_mock):
    mock_data = {"id": 1, "name": "Test Item"}
    
    # Include the query param in the URL exactly as used in the request
    httpx_mock.add_response(
        method="GET",
        url=f"{EXTERNAL_API_URL}?param=param1",
        json=mock_data,
        status_code=200
    )

    result = await ExternalService.fetch_data("param1")
    assert result == mock_data

    
@pytest.mark.asyncio
async def test_fetch_data_failure(httpx_mock):
    httpx_mock.add_response(
        method="GET",
        url=f"{EXTERNAL_API_URL}?param=param1",
        status_code=500
    )

    with pytest.raises(httpx.HTTPStatusError):
        await ExternalService.fetch_data("param1")
