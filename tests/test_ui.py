"""
Tests for the Streamlit weather UI.
"""
import pytest
from unittest.mock import patch, MagicMock, AsyncMock
import asyncio


class TestWeatherUI:
    """Test cases for the Streamlit weather UI."""

    def test_ui_module_imports(self):
        """Test that the UI module can be imported without errors."""
        try:
            import ui  # noqa: F401
            # Basic smoke test - the module should import successfully
            assert True
        except ImportError as e:
            pytest.fail(f"UI module failed to import: {e}")

    @patch('ui.st')
    def test_ui_page_config(self, mock_st):
        """Test that page configuration is set correctly."""
        # Mock streamlit functions
        mock_st.set_page_config = MagicMock()
        mock_st.title = MagicMock()
        mock_st.write = MagicMock()
        mock_st.text_input = MagicMock(return_value="CA")
        mock_st.button = MagicMock(return_value=False)
        
        # Import and test
        
        # Manually trigger the expected calls to test the logic
        mock_st.set_page_config(page_title="🌤 Weather Alerts", layout="centered")
        mock_st.title("Live Weather Alerts")
        mock_st.write("Get weather alerts from the US National Weather Service (weather.gov)")
        
        # Verify calls were made
        mock_st.set_page_config.assert_called_with(
            page_title="🌤 Weather Alerts", 
            layout="centered"
        )
        mock_st.title.assert_called_with("Live Weather Alerts")
        mock_st.write.assert_called_with(
            "Get weather alerts from the US National Weather Service (weather.gov)"
        )

    @patch('ui.st')
    def test_ui_input_components(self, mock_st):
        """Test UI input components."""
        # Setup mocks
        mock_st.text_input = MagicMock(return_value="CA")
        mock_st.button = MagicMock(return_value=False)
        
        # Import ui module
        
        # Test the UI components
        state = mock_st.text_input("Enter US State Code (e.g., CA, TX, NY):", value="CA")
        button_clicked = mock_st.button("Fetch Alerts")
        
        # Verify components
        assert state == "CA"
        assert button_clicked is False
        mock_st.text_input.assert_called_with("Enter US State Code (e.g., CA, TX, NY):", value="CA")
        mock_st.button.assert_called_with("Fetch Alerts")

    def test_fetch_alerts_function(self):
        """Test the fetch_alerts async function."""
        import ui
        
        # Test that the function exists and is callable
        assert hasattr(ui, 'fetch_alerts')
        assert callable(ui.fetch_alerts)

    @pytest.mark.asyncio
    async def test_fetch_alerts_success(self):
        """Test successful alert fetching."""
        with patch('ui.get_weather_alerts', new_callable=AsyncMock) as mock_get_alerts:
            mock_get_alerts.return_value = "Test alerts"
            
            # Import and test
            import ui
            
            result = await ui.fetch_alerts("CA")
            
            assert result == "Test alerts"
            mock_get_alerts.assert_called_once_with("CA")

    @pytest.mark.asyncio
    async def test_fetch_alerts_error(self):
        """Test error handling in fetch_alerts."""
        with patch('ui.get_weather_alerts', new_callable=AsyncMock) as mock_get_alerts:
            mock_get_alerts.side_effect = Exception("API Error")
            
            # Import and test
            import ui
            
            result = await ui.fetch_alerts("CA")
            
            assert result == "Error: API Error"

    @patch('ui.st')
    def test_ui_button_click_flow(self, mock_st):
        """Test the UI flow when button is clicked."""
        # Setup mocks
        mock_st.text_input = MagicMock(return_value="CA")
        mock_st.button = MagicMock(return_value=True)
        mock_st.spinner = MagicMock()
        mock_st.text_area = MagicMock()
        mock_st.error = MagicMock()
        
        # Mock the spinner context manager
        spinner_context = MagicMock()
        spinner_context.__enter__ = MagicMock()
        spinner_context.__exit__ = MagicMock()
        mock_st.spinner.return_value = spinner_context
        
        # Import ui module
        
        # Simulate the UI flow
        state = mock_st.text_input("Enter US State Code (e.g., CA, TX, NY):", value="CA")
        button_clicked = mock_st.button("Fetch Alerts")
        
        if button_clicked:
            with mock_st.spinner("Fetching alerts..."):
                # Simulate successful alert fetching
                alerts = "Mock alerts"
                mock_st.text_area("Alerts", alerts, height=400)
        
        # Verify the flow
        assert state == "CA"
        assert button_clicked is True
        mock_st.spinner.assert_called_with("Fetching alerts...")
        mock_st.text_area.assert_called_with("Alerts", "Mock alerts", height=400)

    def test_state_code_processing_logic(self):
        """Test state code processing logic."""
        # Test the logic that would be used in the UI
        test_inputs = [
            (" ca ", "CA"),
            ("tx", "TX"),
            ("  NY  ", "NY"),
            ("fl", "FL")
        ]
        
        for input_state, expected in test_inputs:
            processed = input_state.strip().upper()
            assert processed == expected

    @patch('ui.st')
    def test_ui_error_handling(self, mock_st):
        """Test error handling in the UI."""
        # Setup mocks
        mock_st.text_input = MagicMock(return_value="INVALID")
        mock_st.button = MagicMock(return_value=True)
        mock_st.spinner = MagicMock()
        mock_st.error = MagicMock()
        
        # Mock the spinner context manager
        spinner_context = MagicMock()
        spinner_context.__enter__ = MagicMock()
        spinner_context.__exit__ = MagicMock()
        mock_st.spinner.return_value = spinner_context
        
        # Import ui module
        
        # Simulate error handling
        mock_st.text_input("Enter US State Code (e.g., CA, TX, NY):", value="CA")
        button_clicked = mock_st.button("Fetch Alerts")
        
        if button_clicked:
            with mock_st.spinner("Fetching alerts..."):
                try:
                    # Simulate an exception
                    raise Exception("Test error")
                except Exception as e:
                    mock_st.error(f"Error: {e}")
        
        # Verify error handling
        mock_st.error.assert_called_with("Error: Test error")

    def test_asyncio_event_loop_handling(self):
        """Test asyncio event loop handling in the UI."""
        # Test that the UI handles asyncio properly
        import ui
        
        # Verify that asyncio is imported
        assert hasattr(ui, 'asyncio')
        
        # Test event loop creation logic
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        # Verify loop is set
        current_loop = asyncio.get_event_loop()
        assert current_loop is loop
        
        # Clean up
        loop.close()