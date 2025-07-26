"""
Integration tests for the weather MCP project.
These tests verify that components work together correctly.
"""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from weather_mcp.tools import get_alerts, get_forecast
from weather_mcp.nws_api import make_nws_request


class TestIntegration:
    """Integration tests for weather MCP components."""

    @pytest.mark.asyncio
    async def test_end_to_end_alert_flow(self, mock_nws_response):
        """Test the complete flow from API request to formatted output."""
        with patch("weather_mcp.nws_api.httpx.AsyncClient") as mock_client:
            # Setup mock HTTP response
            mock_response = MagicMock()
            mock_response.json.return_value = mock_nws_response
            mock_response.raise_for_status = MagicMock()

            mock_client_instance = AsyncMock()
            mock_client_instance.get = AsyncMock(return_value=mock_response)
            mock_client.return_value.__aenter__.return_value = mock_client_instance

            # Test the complete flow
            result = await get_alerts("CA")

            # Verify the result contains formatted alerts
            assert "Winter Storm Warning" in result
            assert "Heat Advisory" in result
            assert "Los Angeles County" in result
            assert "Orange County" in result
            assert "---" in result  # Separator between alerts

            # Verify API was called correctly
            mock_client_instance.get.assert_called_once()
            call_args = mock_client_instance.get.call_args
            assert "https://api.weather.gov/alerts/active/area/CA" in call_args[0]

    @pytest.mark.asyncio
    async def test_end_to_end_forecast_flow(
        self, mock_forecast_points_response, mock_forecast_response
    ):
        """Test the complete forecast flow from API request to formatted output."""
        with patch("weather_mcp.nws_api.httpx.AsyncClient") as mock_client:
            # Setup mock HTTP responses
            mock_response_1 = MagicMock()
            mock_response_1.json.return_value = mock_forecast_points_response
            mock_response_1.raise_for_status = MagicMock()

            mock_response_2 = MagicMock()
            mock_response_2.json.return_value = mock_forecast_response
            mock_response_2.raise_for_status = MagicMock()

            mock_client_instance = AsyncMock()
            mock_client_instance.get = AsyncMock(
                side_effect=[mock_response_1, mock_response_2]
            )
            mock_client.return_value.__aenter__.return_value = mock_client_instance

            # Test the complete flow
            result = await get_forecast(34.0522, -118.2437)

            # Verify the result contains formatted forecast
            assert "Today" in result
            assert "Tonight" in result
            assert "75°F" in result
            assert "Sunny with clear skies" in result

            # Verify both API calls were made
            assert mock_client_instance.get.call_count == 2

    @pytest.mark.asyncio
    async def test_api_to_tools_integration(self, mock_nws_response):
        """Test integration between NWS API and tools modules."""
        with patch("weather_mcp.nws_api.httpx.AsyncClient") as mock_client:
            # Setup mock HTTP response
            mock_response = MagicMock()
            mock_response.json.return_value = mock_nws_response
            mock_response.raise_for_status = MagicMock()

            mock_client_instance = AsyncMock()
            mock_client_instance.get = AsyncMock(return_value=mock_response)
            mock_client.return_value.__aenter__.return_value = mock_client_instance

            # Test API call
            api_result = await make_nws_request(
                "https://api.weather.gov/alerts/active/area/TX"
            )
            assert api_result == mock_nws_response

            # Test tools integration
            tools_result = await get_alerts("TX")
            assert "Winter Storm Warning" in tools_result
            assert "Heat Advisory" in tools_result

    @pytest.mark.asyncio
    async def test_server_to_tools_integration(self, mock_nws_response):
        """Test integration between server and tools components."""
        from weather_mcp.server import _mcp_get_alerts_tool_impl

        with patch(
            "weather_mcp.tools.make_nws_request", new_callable=AsyncMock
        ) as mock_request:
            mock_request.return_value = mock_nws_response

            # Test server endpoint
            result = await _mcp_get_alerts_tool_impl("CA")

            # Verify the result
            assert "Winter Storm Warning" in result
            assert "Heat Advisory" in result

    @pytest.mark.asyncio
    async def test_error_propagation_through_stack(self):
        """Test that errors propagate correctly through the component stack."""
        with patch("weather_mcp.nws_api.httpx.AsyncClient") as mock_client:
            # Simulate network error
            mock_client_instance = AsyncMock()
            mock_client_instance.get = AsyncMock(side_effect=Exception("Network error"))
            mock_client.return_value.__aenter__.return_value = mock_client_instance

            # Test that error is handled gracefully in tools
            result = await get_alerts("CA")
            assert result == "Unable to fetch alerts or no alerts found."

    @pytest.mark.asyncio
    async def test_different_response_formats(self):
        """Test handling of different API response formats."""
        test_cases = [
            # Empty response
            (None, "Unable to fetch alerts or no alerts found."),
            # Malformed response
            ({"invalid": "data"}, "Unable to fetch alerts or no alerts found."),
            # Empty features
            ({"features": []}, "No active alerts for this state."),
        ]

        for mock_response, expected_result in test_cases:
            with patch(
                "weather_mcp.tools.make_nws_request", new_callable=AsyncMock
            ) as mock_request:
                mock_request.return_value = mock_response

                result = await get_alerts("CA")
                assert result == expected_result

    @pytest.mark.asyncio
    async def test_state_code_handling_integration(self, mock_nws_response):
        """Test that state codes are handled correctly throughout the stack."""
        test_states = ["CA", "TX", "NY", "FL", "WA"]

        with patch(
            "weather_mcp.tools.make_nws_request", new_callable=AsyncMock
        ) as mock_request:
            mock_request.return_value = mock_nws_response

            for state in test_states:
                await get_alerts(state)
                expected_url = f"https://api.weather.gov/alerts/active/area/{state}"
                mock_request.assert_called_with(expected_url)
