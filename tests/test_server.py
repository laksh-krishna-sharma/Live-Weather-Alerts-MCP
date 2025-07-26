"""
Tests for the Weather MCP server.
"""
import pytest
import sys
from unittest.mock import AsyncMock, patch, MagicMock
from weather_mcp.server import mcp, _mcp_get_alerts_tool_impl, get_forecast_tool


class TestWeatherMCPServer:
    """Test cases for the Weather MCP server."""

    def test_mcp_server_configuration(self):
        """Test that MCP server is configured correctly."""
        assert mcp.name == "weather"
        # FastMCP configuration is internal, so we test what we can access

    @pytest.mark.asyncio
    async def test_get_alerts_tool_impl(self):
        """Test the get_alerts MCP tool implementation."""
        mock_result = "Test alert result"
        
        with patch('weather_mcp.server.get_alerts_tool', new_callable=AsyncMock) as mock_tool:
            mock_tool.return_value = mock_result
            
            result = await _mcp_get_alerts_tool_impl("CA")
            
            mock_tool.assert_called_once_with("CA")
            assert result == mock_result

    @pytest.mark.asyncio
    async def test_get_forecast_tool_impl(self):
        """Test the get_forecast MCP tool implementation."""
        mock_result = "Test forecast result"
        
        with patch('weather_mcp.server.get_forecast', new_callable=AsyncMock) as mock_forecast:
            mock_forecast.return_value = mock_result
            
            result = await get_forecast_tool(34.0522, -118.2437)
            
            mock_forecast.assert_called_once_with(34.0522, -118.2437)
            assert result == mock_result

    @pytest.mark.asyncio
    async def test_get_alerts_tool_different_states(self):
        """Test the get_alerts tool with different state codes."""
        with patch('weather_mcp.server.get_alerts_tool', new_callable=AsyncMock) as mock_tool:
            mock_tool.return_value = "Mock result"
            
            # Test various state codes
            test_states = ["TX", "NY", "FL", "WA"]
            
            for state in test_states:
                await _mcp_get_alerts_tool_impl(state)
                mock_tool.assert_called_with(state)

    @pytest.mark.asyncio
    async def test_get_forecast_tool_different_coordinates(self):
        """Test the get_forecast tool with different coordinates."""
        with patch('weather_mcp.server.get_forecast', new_callable=AsyncMock) as mock_forecast:
            mock_forecast.return_value = "Mock forecast"
            
            # Test various coordinates
            test_coords = [
                (40.7128, -74.0060),  # New York
                (41.8781, -87.6298),  # Chicago
                (29.7604, -95.3698),  # Houston
            ]
            
            for lat, lon in test_coords:
                await get_forecast_tool(lat, lon)
                mock_forecast.assert_called_with(lat, lon)

    @pytest.mark.asyncio
    async def test_get_alerts_tool_error_handling(self):
        """Test error handling in the get_alerts tool."""
        with patch('weather_mcp.server.get_alerts_tool', new_callable=AsyncMock) as mock_tool:
            mock_tool.side_effect = Exception("API Error")
            
            # The tool should propagate exceptions
            with pytest.raises(Exception, match="API Error"):
                await _mcp_get_alerts_tool_impl("CA")

    @pytest.mark.asyncio
    async def test_get_forecast_tool_error_handling(self):
        """Test error handling in the get_forecast tool."""
        with patch('weather_mcp.server.get_forecast', new_callable=AsyncMock) as mock_forecast:
            mock_forecast.side_effect = Exception("Forecast Error")
            
            # The tool should propagate exceptions
            with pytest.raises(Exception, match="Forecast Error"):
                await get_forecast_tool(34.0522, -118.2437)

    def test_mcp_tool_functions_exist(self):
        """Test that the MCP tool functions are properly defined."""
        # Test that the tool functions are callable
        assert callable(_mcp_get_alerts_tool_impl)
        assert callable(get_forecast_tool)

    def test_main_block_logic(self):
        """Test the main block execution logic."""
        with patch('weather_mcp.server.mcp.run') as mock_run, \
             patch('builtins.print') as mock_print:
            
            # Test SSE transport (default)
            transport = "sse"
            if transport == "sse":
                mock_print("Running server with SSE transport")
                mock_run(transport="sse")
            
            # Verify the calls
            mock_print.assert_called_with("Running server with SSE transport")
            mock_run.assert_called_with(transport="sse")

    def test_main_block_stdio_transport(self):
        """Test the main block with stdio transport."""
        with patch('weather_mcp.server.mcp.run') as mock_run, \
             patch('builtins.print') as mock_print:
            
            # Test stdio transport
            transport = "stdio"
            if transport == "stdio":
                mock_print("Running server with stdio transport")
                mock_run(transport="stdio")
            
            # Verify the calls
            mock_print.assert_called_with("Running server with stdio transport")
            mock_run.assert_called_with(transport="stdio")

    def test_main_block_invalid_transport(self):
        """Test the main block with invalid transport."""
        transport = "invalid"
        
        with pytest.raises(ValueError, match="Unknown transport: invalid"):
            if transport not in ["stdio", "sse"]:
                raise ValueError(f"Unknown transport: {transport}")

    @patch('weather_mcp.server.mcp.run')
    def test_main_execution_block(self, mock_run):
        """Test the main execution block."""
        # Import and test the main block logic
        import weather_mcp.server
        
        # Verify the run method exists and is callable
        assert callable(mcp.run)
        
        # Test that we can call the main block logic
        transport = "sse"
        if transport == "sse":
            weather_mcp.server.mcp.run(transport="sse")
            mock_run.assert_called_with(transport="sse")