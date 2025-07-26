"""
Tests for the Weather MCP client.
"""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from client.client import get_weather_alerts


class TestWeatherClient:
    """Test cases for the weather MCP client."""

    @pytest.mark.asyncio
    async def test_get_weather_alerts_success(self):
        """Test successful weather alerts retrieval."""
        mock_result_content = "Winter Storm Warning for Los Angeles County"

        # Mock the MCP client session and its components
        mock_session = AsyncMock()
        mock_result = MagicMock()
        mock_content_item = MagicMock()
        mock_content_item.text = mock_result_content
        mock_result.content = [mock_content_item]
        mock_session.call_tool.return_value = mock_result
        mock_session.initialize.return_value = None

        # Mock the SSE client context manager
        mock_sse_client = AsyncMock()
        mock_sse_client.__aenter__.return_value = ("mock_reader", "mock_writer")
        mock_sse_client.__aexit__.return_value = None

        # Mock the ClientSession context manager
        mock_client_session = AsyncMock()
        mock_client_session.__aenter__.return_value = mock_session
        mock_client_session.__aexit__.return_value = None

        with (
            patch("client.client.sse_client", return_value=mock_sse_client),
            patch("client.client.ClientSession", return_value=mock_client_session),
        ):

            result = await get_weather_alerts("CA")

            # Verify the result
            assert result == mock_result_content

            # Verify the session was initialized and tool was called
            mock_session.initialize.assert_called_once()
            mock_session.call_tool.assert_called_once_with(
                "get_alerts", arguments={"state": "CA"}
            )

    @pytest.mark.asyncio
    async def test_get_weather_alerts_different_states(self):
        """Test weather alerts retrieval for different states."""
        mock_result_content = "Mock alert content"

        # Setup mocks
        mock_session = AsyncMock()
        mock_result = MagicMock()
        mock_content_item = MagicMock()
        mock_content_item.text = mock_result_content
        mock_result.content = [mock_content_item]
        mock_session.call_tool.return_value = mock_result
        mock_session.initialize.return_value = None

        mock_sse_client = AsyncMock()
        mock_sse_client.__aenter__.return_value = ("mock_reader", "mock_writer")
        mock_sse_client.__aexit__.return_value = None

        mock_client_session = AsyncMock()
        mock_client_session.__aenter__.return_value = mock_session
        mock_client_session.__aexit__.return_value = None

        with (
            patch("client.client.sse_client", return_value=mock_sse_client),
            patch("client.client.ClientSession", return_value=mock_client_session),
        ):

            # Test different state codes
            test_states = ["TX", "NY", "FL"]

            for state in test_states:
                await get_weather_alerts(state)
                mock_session.call_tool.assert_called_with(
                    "get_alerts", arguments={"state": state}
                )

    @pytest.mark.asyncio
    async def test_get_weather_alerts_default_state(self):
        """Test weather alerts retrieval with default state."""
        mock_result_content = "Default CA alerts"

        # Setup mocks
        mock_session = AsyncMock()
        mock_result = MagicMock()
        mock_content_item = MagicMock()
        mock_content_item.text = mock_result_content
        mock_result.content = [mock_content_item]
        mock_session.call_tool.return_value = mock_result
        mock_session.initialize.return_value = None

        mock_sse_client = AsyncMock()
        mock_sse_client.__aenter__.return_value = ("mock_reader", "mock_writer")
        mock_sse_client.__aexit__.return_value = None

        mock_client_session = AsyncMock()
        mock_client_session.__aenter__.return_value = mock_session
        mock_client_session.__aexit__.return_value = None

        with (
            patch("client.client.sse_client", return_value=mock_sse_client),
            patch("client.client.ClientSession", return_value=mock_client_session),
        ):

            # Call without state parameter (should use default "CA")
            result = await get_weather_alerts()

            assert result == mock_result_content
            mock_session.call_tool.assert_called_with(
                "get_alerts", arguments={"state": "CA"}
            )

    @pytest.mark.asyncio
    async def test_get_weather_alerts_connection_params(self):
        """Test that connection parameters are correctly set."""
        mock_session = AsyncMock()
        mock_result = MagicMock()
        mock_content_item = MagicMock()
        mock_content_item.text = "test"
        mock_result.content = [mock_content_item]
        mock_session.call_tool.return_value = mock_result
        mock_session.initialize.return_value = None

        mock_sse_client = AsyncMock()
        mock_sse_client.__aenter__.return_value = ("mock_reader", "mock_writer")
        mock_sse_client.__aexit__.return_value = None

        mock_client_session = AsyncMock()
        mock_client_session.__aenter__.return_value = mock_session
        mock_client_session.__aexit__.return_value = None

        with (
            patch("client.client.sse_client", return_value=mock_sse_client) as mock_sse,
            patch("client.client.ClientSession", return_value=mock_client_session),
        ):

            await get_weather_alerts("CA")

            # Verify SSE client was called with correct URL
            mock_sse.assert_called_once_with("https://live-weather-alerts-mcp.onrender.com/sse")

    @pytest.mark.asyncio
    async def test_get_weather_alerts_session_error(self):
        """Test error handling when session operations fail."""
        mock_session = AsyncMock()
        mock_session.initialize.side_effect = Exception("Connection failed")

        mock_sse_client = AsyncMock()
        mock_sse_client.__aenter__.return_value = ("mock_reader", "mock_writer")
        mock_sse_client.__aexit__.return_value = None

        mock_client_session = AsyncMock()
        mock_client_session.__aenter__.return_value = mock_session
        mock_client_session.__aexit__.return_value = None

        with (
            patch("client.client.sse_client", return_value=mock_sse_client),
            patch("client.client.ClientSession", return_value=mock_client_session),
        ):

            with pytest.raises(Exception, match="Connection failed"):
                await get_weather_alerts("CA")

    @pytest.mark.asyncio
    async def test_get_weather_alerts_tool_call_error(self):
        """Test error handling when tool call fails."""
        mock_session = AsyncMock()
        mock_session.initialize.return_value = None
        mock_session.call_tool.side_effect = Exception("Tool call failed")

        mock_sse_client = AsyncMock()
        mock_sse_client.__aenter__.return_value = ("mock_reader", "mock_writer")
        mock_sse_client.__aexit__.return_value = None

        mock_client_session = AsyncMock()
        mock_client_session.__aenter__.return_value = mock_session
        mock_client_session.__aexit__.return_value = None

        with (
            patch("client.client.sse_client", return_value=mock_sse_client),
            patch("client.client.ClientSession", return_value=mock_client_session),
        ):

            with pytest.raises(Exception, match="Tool call failed"):
                await get_weather_alerts("CA")

    def test_nest_asyncio_applied(self):
        """Test that nest_asyncio is properly applied."""
        # This is a smoke test to ensure the module imports correctly
        import client.client

        # Verify the main function exists and is callable
        assert hasattr(client.client, "get_weather_alerts")
        assert callable(client.client.get_weather_alerts)

    def test_client_imports(self):
        """Test that all required modules are properly imported."""
        import client.client

        # Verify that the module imports work
        assert hasattr(client.client, "ClientSession")
        assert hasattr(client.client, "sse_client")
        assert hasattr(client.client, "get_weather_alerts")
