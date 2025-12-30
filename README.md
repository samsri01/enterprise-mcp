# Enterprise MCP Server

Enterprise-grade Model Context Protocol (MCP) server with Streamable HTTP transport, built on Starlette and FastMCP. Features authentication strategies, health monitoring, and a modular architecture for production deployments.

## Features

- **MCP Protocol Support**: Built with FastMCP for Model Context Protocol implementation
- **Streamable HTTP Transport**: Efficient streaming HTTP transport for MCP communication
- **Authentication Framework**: Pluggable authentication strategies (JWT, NoAuth)
- **Health Check Endpoint**: Built-in `/health` endpoint for monitoring
- **Configuration Management**: Environment-based configuration with Pydantic
- **Modular Architecture**: Dependency injection pattern for easy testing and extension
- **Production Ready**: Built on Starlette for robust async HTTP handling

## Project Structure

```
enterprise-mcp/
├── src/
│   └── enterprise_mcp/
│       ├── __init__.py
│       ├── app.py              # Starlette application and middleware setup
│       ├── config.py            # Configuration management with Pydantic
│       ├── container.py         # Dependency injection for auth strategies
│       └── mcp_server.py        # MCP server with FastMCP
├── tests/
│   ├── test_health.py          # Health endpoint tests
│   └── test_auth_mcp.py        # Authentication tests
├── pyproject.toml              # Project metadata and dependencies
└── README.md
```

## Installation

### Prerequisites

- Python 3.8 or higher
- pip

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/samsri01/enterprise-mcp.git
   cd enterprise-mcp
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv enterprise_mcp_venv
   
   # Windows
   .\enterprise_mcp_venv\Scripts\Activate.ps1
   
   # Linux/Mac
   source enterprise_mcp_venv/bin/activate
   ```

3. **Install the package in editable mode**
   ```bash
   pip install -e .
   ```

## Configuration

Configuration is managed through environment variables. Create a `.env` file in the project root:

```env
# Application Settings
DEBUG=true

# Authentication Mode: "none" or "jwt"
AUTH_MODE=none

# JWT Settings (required if AUTH_MODE=jwt)
JWT_SECRET=your-secret-key-here
JWT_ISSUER=your-issuer
JWT_AUDIENCE=your-audience
```

### Configuration Options

| Variable | Default | Description |
|----------|---------|-------------|
| `DEBUG` | `true` | Enable debug mode |
| `AUTH_MODE` | `none` | Authentication mode: `none` or `jwt` |
| `JWT_SECRET` | `dev-secret-change-me` | JWT signing secret |
| `JWT_ISSUER` | `None` | JWT issuer claim |
| `JWT_AUDIENCE` | `None` | JWT audience claim |

## Usage

### Running the Server

Start the server using uvicorn:

```bash
uvicorn enterprise_mcp.app:app --reload --app-dir src
```

The server will start on `http://127.0.0.1:8000`

### Endpoints

- **`GET /health`** - Health check endpoint (public)
  ```bash
  curl http://127.0.0.1:8000/health
  # Response: OK
  ```

- **`/mcp`** - MCP protocol endpoint (protected by auth middleware)
  - Supports streaming HTTP transport for MCP protocol
  - Protected by authentication when `AUTH_MODE=jwt`

### MCP Tools

The server exposes the following MCP tools:

#### `add(a: int, b: int) -> int`
Add two integers together.

**Example:**
```json
{
  "tool": "add",
  "arguments": {
    "a": 5,
    "b": 3
  }
}
```

## Authentication

### NoAuth Strategy (Default)

When `AUTH_MODE=none`, all requests are allowed. Suitable for development and trusted environments.

### JWT Strategy

When `AUTH_MODE=jwt`, the server validates JWT tokens in the `Authorization` header:

```bash
curl -H "Authorization: Bearer YOUR_JWT_TOKEN" http://127.0.0.1:8000/mcp
```

**Protected routes**: `/mcp`  
**Public routes**: `/health`

## Development

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=enterprise_mcp

# Run specific test file
pytest tests/test_health.py
```

### Adding New MCP Tools

Edit `src/enterprise_mcp/mcp_server.py`:

```python
@mcp.tool()
def your_tool(param: str) -> str:
    """Your tool description."""
    return f"Result: {param}"
```

### Adding New Authentication Strategies

1. Create a new strategy class inheriting from `AuthStrategy`
2. Implement the `authenticate(token: str | None) -> dict | None` method
3. Update `container.py` to include your strategy

## Dependencies

- **mcp** - Model Context Protocol implementation
- **starlette** - ASGI framework for HTTP handling
- **pydantic** - Data validation and settings management
- **pydantic-settings** - Settings management for Pydantic
- **python-dotenv** - Environment variable management
- **httpx** - HTTP client library
- **pytest** - Testing framework

## Architecture

### Components

1. **app.py**: Main Starlette application
   - Routes configuration
   - Middleware setup
   - Health check endpoint

2. **mcp_server.py**: FastMCP server
   - MCP protocol implementation
   - Tool definitions

3. **container.py**: Dependency injection
   - Auth strategy factory
   - Configuration-based strategy selection

4. **config.py**: Configuration management
   - Environment variable loading
   - Pydantic settings validation

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
