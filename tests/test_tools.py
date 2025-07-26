"""
Tests for weather tools functionality.
"""
import pytest
from unittest.mock import AsyncMock, patch
from weather_mcp.tools import format_alert, get_alerts, get_forecast


class TestTools:
    """Test cases for weather tools functionality."""

    def test_format_alert_complete_data(self):
        """Test alert formatting with complete data."""
        feature = {
            "properties": {
                "event": "Winter Storm Warning",
                "areaDesc": "Los Angeles County",
                "severity": "Severe",
                "description": "Heavy snow expected with accumulations of 6-12 inches.",
                "instruction": "Avoid unnecessary travel. Use caution if you must travel."
            }
        }
        
        result = format_alert(feature)
        
        expected = """
    Event: Winter Storm Warning
    Area: Los Angeles County
    Severity: Severe
    Description: Heavy snow expected with accumulations of 6-12 inches.
    Instructions: Avoid unnecessary travel. Use caution if you must travel.
    """
        assert result == expected

    def test_format_alert_missing_data(self):
        """Test alert formatting with missing data fields."""
        feature = {
            "properties": {
                "event": "Heat Advisory"
                # Missing other fields
            }
        }
        
        result = format_alert(feature)
        
        expected = """
    Event: Heat Advisory
    Area: Unknown
    Severity: Unknown
    Description: No description available
    Instructions: No specific instructions provided
    """
        assert result == expected

    def test_format_alert_empty_properties(self):
        """Test alert formatting with empty properties."""
        feature = {
            "properties": {}
        }
        
        result = format_alert(feature)
        
        expected = """
    Event: Unknown
    Area: Unknown
    Severity: Unknown
    Description: No description available
    Instructions: No specific instructions provided
    """
        assert result == expected

    @pytest.mark.asyncio
    async def test_get_alerts_success_with_alerts(self, mock_nws_response):
        """Test successful alert retrieval with active alerts."""
        with patch('weather_mcp.tools.make_nws_request', new_callable=AsyncMock) as mock_request:
            mock_request.return_value = mock_nws_response
            
            result = await get_alerts("CA")
            
            # Verify the request was made with correct URL
            mock_request.assert_called_once_with("https://api.weather.gov/alerts/active/area/CA")
            
            # Verify the result contains both alerts separated by ---
            assert "Winter Storm Warning" in result
            assert "Heat Advisory" in result
            assert "---" in result
            assert result.count("---") == 1  # One separator for two alerts

    @pytest.mark.asyncio
    async def test_get_alerts_no_alerts(self, mock_empty_nws_response):
        """Test alert retrieval when no alerts are active."""
        with patch('weather_mcp.tools.make_nws_request', new_callable=AsyncMock) as mock_request:
            mock_request.return_value = mock_empty_nws_response
            
            result = await get_alerts("CA")
            
            assert result == "No active alerts for this state."

    @pytest.mark.asyncio
    async def test_get_alerts_api_failure(self):
        """Test alert retrieval when API request fails."""
        with patch('weather_mcp.tools.make_nws_request', new_callable=AsyncMock) as mock_request:
            mock_request.return_value = None
            
            result = await get_alerts("CA")
            
            assert result == "Unable to fetch alerts or no alerts found."

    @pytest.mark.asyncio
    async def test_get_alerts_malformed_response(self):
        """Test alert retrieval with malformed API response."""
        mock_data = {
            "invalid_key": "some_value"
            # Missing "features" key
        }
        
        with patch('weather_mcp.tools.make_nws_request', new_callable=AsyncMock) as mock_request:
            mock_request.return_value = mock_data
            
            result = await get_alerts("CA")
            
            assert result == "Unable to fetch alerts or no alerts found."

    @pytest.mark.asyncio
    async def test_get_forecast_success(self, mock_forecast_points_response, mock_forecast_response):
        """Test successful forecast retrieval."""
        with patch('weather_mcp.tools.make_nws_request', new_callable=AsyncMock) as mock_request:
            # First call returns points data, second call returns forecast data
            mock_request.side_effect = [mock_forecast_points_response, mock_forecast_response]
            
            result = await get_forecast(34.0522, -118.2437)  # Los Angeles coordinates
            
            # Verify both API calls were made
            assert mock_request.call_count == 2
            mock_request.assert_any_call("https://api.weather.gov/points/34.0522,-118.2437")
            mock_request.assert_any_call("https://api.weather.gov/gridpoints/LOX/123,456/forecast")
            
            # Verify the result contains forecast data
            assert "Today" in result
            assert "Tonight" in result
            assert "75°F" in result
            assert "Sunny with clear skies" in result

    @pytest.mark.asyncio
    async def test_get_forecast_points_failure(self):
        """Test forecast retrieval when points API fails."""
        with patch('weather_mcp.tools.make_nws_request', new_callable=AsyncMock) as mock_request:
            mock_request.return_value = None
            
            result = await get_forecast(34.0522, -118.2437)
            
            assert result == "Unable to fetch forecast data for this location."

    @pytest.mark.asyncio
    async def test_get_forecast_forecast_failure(self, mock_forecast_points_response):
        """Test forecast retrieval when forecast API fails."""
        with patch('weather_mcp.tools.make_nws_request', new_callable=AsyncMock) as mock_request:
            # First call succeeds, second call fails
            mock_request.side_effect = [mock_forecast_points_response, None]
            
            result = await get_forecast(34.0522, -118.2437)
            
            assert result == "Unable to fetch detailed forecast."

    @pytest.mark.asyncio
    async def test_get_alerts_different_states(self):
        """Test alert retrieval for different state codes."""
        mock_data = {"features": []}
        
        with patch('weather_mcp.tools.make_nws_request', new_callable=AsyncMock) as mock_request:
            mock_request.return_value = mock_data
            
            # Test different state codes
            await get_alerts("TX")
            mock_request.assert_called_with("https://api.weather.gov/alerts/active/area/TX")
            
            await get_alerts("NY")
            mock_request.assert_called_with("https://api.weather.gov/alerts/active/area/NY")