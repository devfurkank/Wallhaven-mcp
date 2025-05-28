from mcp.server.fastmcp import FastMCP
from app import WallhavenAPI
import json
import os
import sys

# Initialize MCP server
mcp = FastMCP("wallhaven-mcp")

# Global API instance
api = None

def initialize_api(config=None):
    """Initialize the Wallhaven API with configuration"""
    global api
    api_key = None
    
    if config and 'wallhavenApiKey' in config:
        api_key = config['wallhavenApiKey']
    else:
        api_key = os.getenv('WALLHAVEN_API_KEY')
    
    # API can be initialized without a key for public endpoints
    api = WallhavenAPI(api_key=api_key)
    return api

@mcp.tool()
async def get_wallpaper(wallpaper_id: str) -> str:
    """Get detailed information about a specific wallpaper by ID
    
    Args:
        wallpaper_id: The ID of the wallpaper (e.g., "94x38z")
    """
    if api is None:
        initialize_api()
    
    result = api.get_wallpaper(wallpaper_id)
    return json.dumps(result, ensure_ascii=False, indent=2)

@mcp.tool()
async def search_wallpapers(query: str = None, categories: str = None, purity: str = None, 
                           sorting: str = "date_added", order: str = "desc", top_range: str = None,
                           atleast: str = None, resolutions: str = None, ratios: str = None,
                           colors: str = None, page: int = 1, seed: str = None) -> str:
    """Search for wallpapers on Wallhaven
    
    Args:
        query: Search query (tags, keywords, etc.)
        categories: Categories to include (e.g., "100" for general only, "110" for general+anime)
        purity: Purity filter (e.g., "100" for SFW only, "110" for SFW+sketchy)
        sorting: How to sort results (date_added, relevance, random, views, favorites, toplist)
        order: Sort order (desc, asc)
        top_range: Time range for toplist (1d, 3d, 1w, 1M, 3M, 6M, 1y)
        atleast: Minimum resolution (e.g., "1920x1080")
        resolutions: Exact resolutions (e.g., "1920x1080,2560x1440")
        ratios: Aspect ratios (e.g., "16x9,16x10")
        colors: Color hex code (e.g., "0066cc")
        page: Page number
        seed: Seed for random results
    """
    if api is None:
        initialize_api()
    
    result = api.search_wallpapers(
        query=query, 
        categories=categories, 
        purity=purity,
        sorting=sorting,
        order=order,
        top_range=top_range,
        atleast=atleast,
        resolutions=resolutions,
        ratios=ratios,
        colors=colors,
        page=page,
        seed=seed
    )
    return json.dumps(result, ensure_ascii=False, indent=2)

@mcp.tool()
async def get_tag_info(tag_id: int) -> str:
    """Get information about a specific tag by ID
    
    Args:
        tag_id: The ID of the tag
    """
    if api is None:
        initialize_api()
    
    result = api.get_tag_info(tag_id)
    return json.dumps(result, ensure_ascii=False, indent=2)

@mcp.tool()
async def get_user_settings() -> str:
    """Get authenticated user settings (requires API key)"""
    if api is None:
        initialize_api()
    
    result = api.get_user_settings()
    return json.dumps(result, ensure_ascii=False, indent=2)

@mcp.tool()
async def get_collections(username: str = None) -> str:
    """Get user collections
    
    Args:
        username: Username to get collections for. If None, gets authenticated user's collections (requires API key)
    """
    if api is None:
        initialize_api()
    
    result = api.get_collections(username)
    return json.dumps(result, ensure_ascii=False, indent=2)

@mcp.tool()
async def get_collection_wallpapers(username: str, collection_id: int, purity: str = None, page: int = 1) -> str:
    """Get wallpapers from a specific collection
    
    Args:
        username: Username who owns the collection
        collection_id: ID of the collection
        purity: Purity filter (e.g., "100" for SFW only)
        page: Page number
    """
    if api is None:
        initialize_api()
    
    result = api.get_collection_wallpapers(username, collection_id, purity, page)
    return json.dumps(result, ensure_ascii=False, indent=2)

# Configuration callback for runtime configuration
def configure_server(config):
    """Server configuration callback function"""
    try:
        initialize_api(config)
        return {"success": True, "message": "Server configured successfully"}
    except Exception as e:
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    # If configuration is provided via command line
    if len(sys.argv) > 1:
        try:
            config = json.loads(sys.argv[1])
            initialize_api(config)
        except json.JSONDecodeError:
            # If not JSON, try to get from environment variable
            initialize_api()
    else:
        # Try to get from environment variable
        initialize_api()
    
    # Run the MCP server
    mcp.run(transport="stdio")