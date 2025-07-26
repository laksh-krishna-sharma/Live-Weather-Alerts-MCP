# Weather MCP Project

A **Model Context Protocol (MCP) server** that provides real-time weather alerts and forecasts from the US National Weather Service. Built with modern Python practices, comprehensive testing, and production-ready deployment.

[![Tests](https://img.shields.io/badge/tests-53%20passing-brightgreen)](tests/)
[![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen)](htmlcov/)
[![Type Checking](https://img.shields.io/badge/mypy-passing-brightgreen)](mypy.ini)
[![Code Quality](https://img.shields.io/badge/ruff-passing-brightgreen)](.ruff.toml)
[![Python](https://img.shields.io/badge/python-3.13%2B-blue)](pyproject.toml)

## Features

- **Weather Alerts** - Real-time alerts from the National Weather Service
- **Weather Forecasts** - Detailed forecasts for any US location
- **Web Interface** - Beautiful Streamlit UI for easy interaction
- **MCP Protocol** - Standards-compliant Model Context Protocol server
- **Async/Await** - High-performance asynchronous architecture
- **100% Test Coverage** - Comprehensive test suite with 53 tests
- **Type Safe** - Full MyPy type checking compliance
- **Production Ready** - Deployed and operational


## Quick Start

### Prerequisites

- Python 3.13

### 1. Clone and Install

```bash
git clone <your-repo-url>
cd weather-mcp-project
pip install -r requirements.txt
```

### 2. Run the Web Interface

```bash
streamlit run ui.py
```

Open your browser to `http://localhost:8501` and start exploring weather data!

### 3. Run the MCP Server

```bash
python -m weather_mcp.server
```

The MCP server will start on `http://localhost:8000` with SSE transport.

## Installation

### Using pip

```bash
pip install -r requirements.txt
```


## API Reference

### Weather Alerts

Get active weather alerts for any US state:

```python
await get_alerts(state: str) -> str
```

**Parameters:**
- `state` (str): Two-letter US state code (e.g., "CA", "TX", "NY")

**Returns:**
- Formatted string with active alerts or "No active alerts" message

**Example:**
```python
alerts = await get_alerts("CA")
print(alerts)
# Output: Winter Storm Warning for Los Angeles County...
```

### Weather Forecasts

Get detailed weather forecast for coordinates:

```python
await get_forecast(latitude: float, longitude: float) -> str
```

**Parameters:**
- `latitude` (float): Latitude coordinate
- `longitude` (float): Longitude coordinate

**Returns:**
- Formatted forecast string with 5-day outlook

**Example:**
```python
forecast = await get_forecast(34.0522, -118.2437)  # Los Angeles
print(forecast)
# Output: Today: Temperature: 75°F, Wind: 10 mph SW...
```

### MCP Tools

The server exposes two MCP tools:

1. **`get_alerts`** - Fetch weather alerts by state
2. **`get_forecast`** - Fetch weather forecast by coordinates

## Development

### Project Structure

```
weather-mcp-project/
├── weather_mcp/           # Core MCP server
│   ├── __init__.py
│   ├── server.py         # FastMCP server
│   ├── nws_api.py        # National Weather Service API client
│   └── tools.py          # Weather processing tools
├── client/               # MCP client
│   ├── __init__.py
│   └── client.py         # Client implementation
├── tests/                # Comprehensive test suite
│   ├── conftest.py       # Test configuration
│   ├── test_*.py         # Test modules
│   └── run_tests.py      # Test runner
├── ui.py                 # Streamlit web interface
├── requirements.txt      # Dependencies
├── pyproject.toml        # Project configuration
└── README.md            # This file
```

### Code Quality

This project maintains high code quality standards:

- **100% Test Coverage** - Every line of code is tested
- **Type Checking** - Full MyPy compliance
- **Linting** - Ruff for code formatting and style
- **Standards** - Follows Python best practices

## Testing


### Run with Coverage

```bash
python -m pytest --cov=weather_mcp --cov=client --cov-report=html --cov-report=term tests/
```

### Test Coverage Report

After running tests with coverage, open `htmlcov/index.html` in your browser for a detailed coverage report.

### Quality Checks

```bash
# Type checking
mypy .

# Linting and formatting
ruff check
ruff format

```
