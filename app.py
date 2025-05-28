import requests
from typing import Dict, Any, Optional
import os

class WallhavenAPI:
    def __init__(self, api_key: Optional[str] = None):
        """
        Wallhaven API client
        
        Args:
            api_key: Wallhaven API key. If not provided, will try to get it from WALLHAVEN_API_KEY env var.
        """
        if api_key:
            self.api_key = api_key
        else:
            self.api_key = os.getenv('WALLHAVEN_API_KEY')
            
        self.base_url = "https://wallhaven.cc/api/v1"
        
    def _make_request(self, endpoint: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Make a request to the Wallhaven API"""
        url = f"{self.base_url}/{endpoint}"
        
        # Add API key if available
        headers = {}
        if self.api_key:
            headers['X-API-Key'] = self.api_key
        
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e), "success": False}
    
    def get_wallpaper(self, wallpaper_id: str) -> Dict[str, Any]:
        """Get information about a specific wallpaper by ID"""
        try:
            result = self._make_request(f"w/{wallpaper_id}")
            return {
                "data": result.get("data", {}),
                "success": True
            }
        except Exception as e:
            return {"error": f"Error fetching wallpaper: {str(e)}", "success": False}
    
    def search_wallpapers(self, 
                          query: str = None,
                          categories: str = None, 
                          purity: str = None,
                          sorting: str = None,
                          order: str = None,
                          top_range: str = None,
                          atleast: str = None,
                          resolutions: str = None,
                          ratios: str = None,
                          colors: str = None,
                          page: int = 1,
                          seed: str = None) -> Dict[str, Any]:
        """
        Search for wallpapers on Wallhaven
        
        Args:
            query: Search query (tags, keywords)
            categories: Categories to include (e.g., "100" for general only)
            purity: Purity filter (e.g., "100" for SFW only)
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
        params = {}
        
        # Add parameters if provided
        if query:
            params['q'] = query
        if categories:
            params['categories'] = categories
        if purity:
            params['purity'] = purity
        if sorting:
            params['sorting'] = sorting
        if order:
            params['order'] = order
        if top_range:
            params['topRange'] = top_range
        if atleast:
            params['atleast'] = atleast
        if resolutions:
            params['resolutions'] = resolutions
        if ratios:
            params['ratios'] = ratios
        if colors:
            params['colors'] = colors
        if page:
            params['page'] = page
        if seed:
            params['seed'] = seed
            
        try:
            result = self._make_request("search", params)
            return {
                "data": result.get("data", []),
                "meta": result.get("meta", {}),
                "success": True
            }
        except Exception as e:
            return {"error": f"Search error: {str(e)}", "success": False}
    
    def get_tag_info(self, tag_id: int) -> Dict[str, Any]:
        """Get information about a specific tag by ID"""
        try:
            result = self._make_request(f"tag/{tag_id}")
            return {
                "data": result.get("data", {}),
                "success": True
            }
        except Exception as e:
            return {"error": f"Error fetching tag: {str(e)}", "success": False}
    
    def get_user_settings(self) -> Dict[str, Any]:
        """Get authenticated user settings (requires API key)"""
        if not self.api_key:
            return {"error": "API key required for this endpoint", "success": False}
            
        try:
            result = self._make_request("settings")
            return {
                "data": result.get("data", {}),
                "success": True
            }
        except Exception as e:
            return {"error": f"Error fetching settings: {str(e)}", "success": False}
    
    def get_collections(self, username: str = None) -> Dict[str, Any]:
        """
        Get user collections
        
        Args:
            username: Username to get collections for. If None, gets authenticated user's collections.
        """
        endpoint = "collections"
        if username:
            endpoint = f"collections/{username}"
            
        try:
            result = self._make_request(endpoint)
            return {
                "data": result.get("data", []),
                "success": True
            }
        except Exception as e:
            return {"error": f"Error fetching collections: {str(e)}", "success": False}
    
    def get_collection_wallpapers(self, username: str, collection_id: int, purity: str = None, page: int = 1) -> Dict[str, Any]:
        """
        Get wallpapers from a specific collection
        
        Args:
            username: Username who owns the collection
            collection_id: ID of the collection
            purity: Purity filter
            page: Page number
        """
        params = {}
        if purity:
            params['purity'] = purity
        if page:
            params['page'] = page
            
        try:
            result = self._make_request(f"collections/{username}/{collection_id}", params)
            return {
                "data": result.get("data", []),
                "meta": result.get("meta", {}),
                "success": True
            }
        except Exception as e:
            return {"error": f"Error fetching collection: {str(e)}", "success": False}