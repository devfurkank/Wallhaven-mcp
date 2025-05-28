# Wallhaven MCP Server

A Model Context Protocol (MCP) server for accessing the [Wallhaven](https://wallhaven.cc/) API, allowing AI assistants to search for and retrieve wallpapers.

## Features

- **Wallpaper Search**: Search for wallpapers with various filters (categories, purity, resolution, etc.)
- **Wallpaper Details**: Get detailed information about specific wallpapers
- **Tag Information**: Retrieve information about wallpaper tags
- **Collections**: Access user collections and their wallpapers
- **User Settings**: Retrieve authenticated user settings
- **Smithery Support**: Easy deployment and usage through the Smithery platform

## Smithery Setup (Recommended)

This MCP server can be easily used through the Smithery platform:

1. Log in to your [Smithery](https://smithery.ai) account
2. Find and install the Wallhaven MCP Server
3. Add your Wallhaven API key to the configuration
4. Start using it with Claude Desktop or other MCP clients

### Getting a Wallhaven API Key

1. Go to [Wallhaven Settings](https://wallhaven.cc/settings/account)
2. Create an account or log in
3. Find your API key in the account settings
4. Use this key in your Smithery configuration

## Manual Setup (Development)

### Requirements

- Python 3.11+
- Wallhaven API key (optional, but required for NSFW content and user-specific features)

### Installation Steps

```bash
# 1. Clone the repository
git clone <repo-url>
cd wallhaven-mcp

# 2. Create a virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate     # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set environment variable (optional)
export WALLHAVEN_API_KEY="your-api-key-here"

# 5. Run the server
python server.py
```

### Using with Claude Desktop

Add to your `~/Library/Application Support/Claude/claude_desktop_config.json` file:

```json
{
  "mcpServers": {
    "wallhaven": {
      "command": "python3",
      "args": ["/path/to/wallhaven-mcp/server.py"],
      "env": {
        "WALLHAVEN_API_KEY": "your-api-key-here",
        "PYTHONPATH": "/path/to/wallhaven-mcp"
      }
    }
  }
}
```

## MCP Tools

### get_wallpaper
Get detailed information about a specific wallpaper by ID.

**Parameters:**
- `wallpaper_id`: The ID of the wallpaper (e.g., "94x38z")

**Example Usage:**
```
Get information about wallpaper with ID 94x38z
```

### search_wallpapers
Search for wallpapers on Wallhaven.

**Parameters:**
- `query`: Search query (tags, keywords, etc.)
- `categories`: Categories to include (e.g., "100" for general only, "110" for general+anime)
- `purity`: Purity filter (e.g., "100" for SFW only)
- `sorting`: How to sort results (date_added, relevance, random, views, favorites, toplist)
- `order`: Sort order (desc, asc)
- `top_range`: Time range for toplist (1d, 3d, 1w, 1M, 3M, 6M, 1y)
- `atleast`: Minimum resolution (e.g., "1920x1080")
- `resolutions`: Exact resolutions (e.g., "1920x1080,2560x1440")
- `ratios`: Aspect ratios (e.g., "16x9,16x10")
- `colors`: Color hex code (e.g., "0066cc")
- `page`: Page number (default: 1)
- `seed`: Seed for random results

**Example Usage:**
```
Search for nature wallpapers with minimum resolution 1920x1080
```

### get_tag_info
Get information about a specific tag by ID.

**Parameters:**
- `tag_id`: The ID of the tag

**Example Usage:**
```
Get information about tag with ID 1
```

### get_user_settings
Get authenticated user settings (requires API key).

**Example Usage:**
```
Get my Wallhaven user settings
```

### get_collections
Get user collections.

**Parameters:**
- `username`: Username to get collections for. If None, gets authenticated user's collections (requires API key)

**Example Usage:**
```
Get collections for user "example_user"
```

### get_collection_wallpapers
Get wallpapers from a specific collection.

**Parameters:**
- `username`: Username who owns the collection
- `collection_id`: ID of the collection
- `purity`: Purity filter (e.g., "100" for SFW only)
- `page`: Page number (default: 1)

**Example Usage:**
```
Get wallpapers from collection ID 15 owned by user "example_user"
```

## Docker Usage

```bash
# Build Docker image
docker build -t wallhaven-mcp .

# Run container
docker run -e WALLHAVEN_API_KEY="your-api-key" -it wallhaven-mcp
```

## Development

### Testing

You can test using MCP Inspector:

```bash
# Install MCP Inspector
npm install -g @modelcontextprotocol/inspector

# Test the server
mcp-inspector python server.py
```

### Debugging

For verbose logging:

```bash
export DEBUG=1
python server.py
```

## Troubleshooting

### Common Issues

1. **"Rate limiting error"**
   - Wallhaven API limits requests to 45 per minute
   - Wait and try again later

2. **"Unauthorized error for NSFW content"**
   - Make sure you've provided a valid API key
   - Check that your Wallhaven account has NSFW content enabled

3. **"Module not found"**
   - Ensure all dependencies are installed: `pip install -r requirements.txt`
   - Make sure Python path is set correctly

## License

MIT License

## Contributing

1. Fork this repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Changelog

### v1.0.0
- Initial release
- Basic Wallhaven API functionality
- MCP server implementation




