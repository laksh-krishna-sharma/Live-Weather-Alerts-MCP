"""
Tests for the National Weather Service API client.
"""

import pytest
import httpx
from unittest.mock import AsyncMock, patch, MagicMock
from weather_mcp.nws_api import make_nws_request, USER_AGENT, NWS_API_BASE


class TestNWSAPI:
    """Test cases for the National Weather Service API client."""

    @pytest.mark.asyncio
    async def test_make_nws_request_success(self):
        """Test successful API request."""
        mock_response_data = {
            "features": [
                {
                    "properties": {
                        "event": "Winter Storm Warning",
                        "areaDesc": "Los Angeles County",
                        "severity": "Severe",
                    }
                }
            ]
        }

        with patch("weather_mcp.nws_api.httpx.AsyncClient") as mock_client:
            mock_response = MagicMock()
            mock_response.json.return_value = mock_response_data
            mock_response.raise_for_status = MagicMock()

            mock_client_instance = AsyncMock()
            mock_client_instance.get = AsyncMock(return_value=mock_response)
            mock_client.return_value.__aenter__.return_value = mock_client_instance

            result = await make_nws_request(
                "https://api.weather.gov/alerts/active/area/CA"
            )

            assert result == mock_response_data
            mock_client_instance.get.assert_called_once_with(
                "https://api.weather.gov/alerts/active/area/CA",
                headers={"User-Agent": USER_AGENT, "Accept": "application/geo+json"},
                timeout=30.0,
            )

    @pytest.mark.asyncio
    async def test_make_nws_request_http_error(self):
        """Test API request with HTTP error."""
        with patch("weather_mcp.nws_api.httpx.AsyncClient") as mock_client:
            mock_response = MagicMock()
            mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
                "404 Not Found", request=MagicMock(), response=MagicMock()
            )

            mock_client_instance = AsyncMock()
            mock_client_instance.get = AsyncMock(return_value=mock_response)
            mock_client.return_value.__aenter__.return_value = mock_client_instance

            result = await make_nws_request(
                "https://api.weather.gov/alerts/active/area/INVALID"
            )

            assert result is None

    @pytest.mark.asyncio
    async def test_make_nws_request_timeout(self):
        """Test API request with timeout."""
        with patch("weather_mcp.nws_api.httpx.AsyncClient") as mock_client:
            mock_client_instance = AsyncMock()
            mock_client_instance.get = AsyncMock(
                side_effect=httpx.TimeoutException("Timeout")
            )
            mock_client.return_value.__aenter__.return_value = mock_client_instance

            result = await make_nws_request(
                "https://api.weather.gov/alerts/active/area/CA"
            )

            assert result is None

    @pytest.mark.asyncio
    async def test_make_nws_request_general_exception(self):
        """Test API request with general exception."""
        with patch("weather_mcp.nws_api.httpx.AsyncClient") as mock_client:
            mock_client_instance = AsyncMock()
            mock_client_instance.get = AsyncMock(side_effect=Exception("Network error"))
            mock_client.return_value.__aenter__.return_value = mock_client_instance

            result = await make_nws_request(
                "https://api.weather.gov/alerts/active/area/CA"
            )

            assert result is None

    def test_constants(self):
        """Test that constants are properly defined."""
        assert USER_AGENT == "weather-app/1.0"
        assert NWS_API_BASE == "https://api.weather.gov"
