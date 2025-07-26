"""
Pytest configuration file for weather MCP project tests.
"""

import asyncio
import sys
from pathlib import Path
import pytest

# Add the project root to Python path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def mock_nws_response():
    """Fixture providing a mock NWS API response with alerts."""
    return {
        "features": [
            {
                "properties": {
                    "event": "Winter Storm Warning",
                    "areaDesc": "Los Angeles County",
                    "severity": "Severe",
                    "description": "Heavy snow expected with accumulations of 6-12 inches.",
                    "instruction": "Avoid unnecessary travel. Use caution if you must travel.",
                }
            },
            {
                "properties": {
                    "event": "Heat Advisory",
                    "areaDesc": "Orange County",
                    "severity": "Minor",
                    "description": "Dangerously hot conditions expected.",
                    "instruction": "Drink plenty of fluids and stay in air conditioning.",
                }
            },
        ]
    }


@pytest.fixture
def mock_forecast_points_response():
    """Fixture providing a mock NWS points API response."""
    return {
        "properties": {
            "forecast": "https://api.weather.gov/gridpoints/LOX/123,456/forecast"
        }
    }


@pytest.fixture
def mock_forecast_response():
    """Fixture providing a mock NWS forecast API response."""
    return {
        "properties": {
            "periods": [
                {
                    "name": "Today",
                    "temperature": 75,
                    "temperatureUnit": "F",
                    "windSpeed": "10 mph",
                    "windDirection": "SW",
                    "detailedForecast": "Sunny with clear skies.",
                },
                {
                    "name": "Tonight",
                    "temperature": 55,
                    "temperatureUnit": "F",
                    "windSpeed": "5 mph",
                    "windDirection": "W",
                    "detailedForecast": "Clear skies with light winds.",
                },
            ]
        }
    }


@pytest.fixture
def mock_empty_nws_response():
    """Fixture providing a mock empty NWS API response."""
    return {"features": []}


@pytest.fixture
def sample_alert_feature():
    """Fixture providing a sample alert feature for testing."""
    return {
        "properties": {
            "event": "Flash Flood Warning",
            "areaDesc": "Harris County",
            "severity": "Severe",
            "description": "Flash flooding in progress due to heavy rainfall.",
            "instruction": "Turn around, don't drown. Find alternate route.",
        }
    }
