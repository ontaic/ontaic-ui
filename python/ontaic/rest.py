"""REST API helpers for CRUD operations."""
import json
from typing import Any, Callable, Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum


class HttpMethod(str, Enum):
    """HTTP methods."""
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"
    HEAD = "HEAD"
    OPTIONS = "OPTIONS"


@dataclass
class ApiResponse:
    """API response."""
    data: Any = None
    status: int = 200
    headers: Dict[str, str] = field(default_factory=dict)
    error: Optional[str] = None
    
    @property
    def success(self) -> bool:
        return 200 <= self.status < 300
    
    @property
    def json(self) -> Any:
        if isinstance(self.data, str):
            try:
                return json.loads(self.data)
            except json.JSONDecodeError:
                return self.data
        return self.data
    
    @classmethod
    def from_dict(cls, data: dict) -> "ApiResponse":
        return cls(
            data=data.get("data"),
            status=data.get("status", 200),
            headers=data.get("headers", {}),
            error=data.get("error"),
        )


@dataclass
class RequestConfig:
    """Request configuration."""
    base_url: str = ""
    headers: Dict[str, str] = field(default_factory=dict)
    timeout: float = 30
    retry_count: int = 0
    retry_delay: float = 1
    auth_token: Optional[str] = None
    auth_header: str = "Authorization"
    auth_prefix: str = "Bearer"


class RestClient:
    """REST API client with common patterns."""
    
    def __init__(self, config: RequestConfig = None):
        self.config = config or RequestConfig()
        self._interceptors: List[Callable] = []
        self._response_interceptors: List[Callable] = []
    
    def add_request_interceptor(self, interceptor: Callable):
        """Add request interceptor."""
        self._interceptors.append(interceptor)
    
    def add_response_interceptor(self, interceptor: Callable):
        """Add response interceptor."""
        self._response_interceptors.append(interceptor)
    
    def _build_headers(self, custom_headers: Dict[str, str] = None) -> Dict[str, str]:
        """Build request headers."""
        headers = {**self.config.headers}
        
        if self.config.auth_token:
            headers[self.config.auth_header] = f"{self.config.auth_prefix} {self.config.auth_token}"
        
        if custom_headers:
            headers.update(custom_headers)
        
        return headers
    
    def _build_url(self, path: str, params: Dict[str, str] = None) -> str:
        """Build full URL."""
        url = f"{self.config.base_url.rstrip('/')}/{path.lstrip('/')}"
        
        if params:
            query = "&".join(f"{k}={v}" for k, v in params.items())
            url = f"{url}?{query}"
        
        return url
    
    async def request(self, method: HttpMethod, path: str, data: Any = None, headers: Dict[str, str] = None, params: Dict[str, str] = None) -> ApiResponse:
        """Make an HTTP request."""
        try:
            import aiohttp
        except ImportError:
            return ApiResponse(error="aiohttp not installed. Run: pip install aiohttp")
        
        url = self._build_url(path, params)
        request_headers = self._build_headers(headers)
        
        payload = data
        if isinstance(data, dict):
            request_headers["Content-Type"] = "application/json"
            payload = json.dumps(data)
        
        # Run request interceptors
        for interceptor in self._interceptors:
            result = interceptor(method.value, url, request_headers, payload)
            if result is False:
                return ApiResponse(error="Request blocked by interceptor")
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.request(
                    method.value,
                    url,
                    headers=request_headers,
                    data=payload,
                    timeout=aiohttp.ClientTimeout(total=self.config.timeout)
                ) as resp:
                    response_data = await resp.text()
                    
                    result = ApiResponse(
                        data=response_data,
                        status=resp.status,
                        headers=dict(resp.headers),
                    )
                    
                    # Run response interceptors
                    for interceptor in self._response_interceptors:
                        result = interceptor(result)
                    
                    return result
        except Exception as e:
            return ApiResponse(error=str(e))
    
    def request_sync(self, method: HttpMethod, path: str, data: Any = None, headers: Dict[str, str] = None, params: Dict[str, str] = None) -> ApiResponse:
        """Make an HTTP request synchronously."""
        import requests
        
        url = self._build_url(path, params)
        request_headers = self._build_headers(headers)
        
        # Run request interceptors
        for interceptor in self._interceptors:
            result = interceptor(method.value, url, request_headers, data)
            if result is False:
                return ApiResponse(error="Request blocked by interceptor")
        
        try:
            response = requests.request(
                method.value,
                url,
                headers=request_headers,
                json=data if isinstance(data, dict) else None,
                data=data if isinstance(data, (str, bytes)) else None,
                timeout=self.config.timeout
            )
            
            result = ApiResponse(
                data=response.text,
                status=response.status_code,
                headers=dict(response.headers),
            )
            
            # Run response interceptors
            for interceptor in self._response_interceptors:
                result = interceptor(result)
            
            return result
        except Exception as e:
            return ApiResponse(error=str(e))
    
    async def get(self, path: str, params: Dict[str, str] = None, headers: Dict[str, str] = None) -> ApiResponse:
        """GET request."""
        return await self.request(HttpMethod.GET, path, headers=headers, params=params)
    
    async def post(self, path: str, data: Any = None, headers: Dict[str, str] = None) -> ApiResponse:
        """POST request."""
        return await self.request(HttpMethod.POST, path, data=data, headers=headers)
    
    async def put(self, path: str, data: Any = None, headers: Dict[str, str] = None) -> ApiResponse:
        """PUT request."""
        return await self.request(HttpMethod.PUT, path, data=data, headers=headers)
    
    async def patch(self, path: str, data: Any = None, headers: Dict[str, str] = None) -> ApiResponse:
        """PATCH request."""
        return await self.request(HttpMethod.PATCH, path, data=data, headers=headers)
    
    async def delete(self, path: str, headers: Dict[str, str] = None) -> ApiResponse:
        """DELETE request."""
        return await self.request(HttpMethod.DELETE, path, headers=headers)
    
    def get_sync(self, path: str, params: Dict[str, str] = None, headers: Dict[str, str] = None) -> ApiResponse:
        """GET request synchronously."""
        return self.request_sync(HttpMethod.GET, path, headers=headers, params=params)
    
    def post_sync(self, path: str, data: Any = None, headers: Dict[str, str] = None) -> ApiResponse:
        """POST request synchronously."""
        return self.request_sync(HttpMethod.POST, path, data=data, headers=headers)
    
    def put_sync(self, path: str, data: Any = None, headers: Dict[str, str] = None) -> ApiResponse:
        """PUT request synchronously."""
        return self.request_sync(HttpMethod.PUT, path, data=data, headers=headers)
    
    def patch_sync(self, path: str, data: Any = None, headers: Dict[str, str] = None) -> ApiResponse:
        """PATCH request synchronously."""
        return self.request_sync(HttpMethod.PATCH, path, data=data, headers=headers)
    
    def delete_sync(self, path: str, headers: Dict[str, str] = None) -> ApiResponse:
        """DELETE request synchronously."""
        return self.request_sync(HttpMethod.DELETE, path, headers=headers)


class CRUDBase:
    """Base CRUD operations for a resource."""
    
    def __init__(self, client: RestClient, resource_path: str):
        self.client = client
        self.resource_path = resource_path
    
    async def list(self, params: Dict[str, str] = None) -> ApiResponse:
        """List all resources."""
        return await self.client.get(self.resource_path, params=params)
    
    async def get(self, id: Any) -> ApiResponse:
        """Get a single resource."""
        return await self.client.get(f"{self.resource_path}/{id}")
    
    async def create(self, data: dict) -> ApiResponse:
        """Create a new resource."""
        return await self.client.post(self.resource_path, data=data)
    
    async def update(self, id: Any, data: dict) -> ApiResponse:
        """Update a resource."""
        return await self.client.put(f"{self.resource_path}/{id}", data=data)
    
    async def patch(self, id: Any, data: dict) -> ApiResponse:
        """Partially update a resource."""
        return await self.client.patch(f"{self.resource_path}/{id}", data=data)
    
    async def delete(self, id: Any) -> ApiResponse:
        """Delete a resource."""
        return await self.client.delete(f"{self.resource_path}/{id}")
    
    def list_sync(self, params: Dict[str, str] = None) -> ApiResponse:
        """List all resources synchronously."""
        return self.client.get_sync(self.resource_path, params=params)
    
    def get_sync(self, id: Any) -> ApiResponse:
        """Get a single resource synchronously."""
        return self.client.get_sync(f"{self.resource_path}/{id}")
    
    def create_sync(self, data: dict) -> ApiResponse:
        """Create a new resource synchronously."""
        return self.client.post_sync(self.resource_path, data=data)
    
    def update_sync(self, id: Any, data: dict) -> ApiResponse:
        """Update a resource synchronously."""
        return self.client.put_sync(f"{self.resource_path}/{id}", data=data)
    
    def patch_sync(self, id: Any, data: dict) -> ApiResponse:
        """Partially update a resource synchronously."""
        return self.client.patch_sync(f"{self.resource_path}/{id}", data=data)
    
    def delete_sync(self, id: Any) -> ApiResponse:
        """Delete a resource synchronously."""
        return self.client.delete_sync(f"{self.resource_path}/{id}")


class UsersCRUD(CRUDBase):
    """CRUD operations for users."""
    
    def __init__(self, client: RestClient):
        super().__init__(client, "/api/users")
    
    async def get_by_email(self, email: str) -> ApiResponse:
        """Get user by email."""
        return await self.client.get(f"{self.resource_path}/email/{email}")
    
    async def get_current(self) -> ApiResponse:
        """Get current user."""
        return await self.client.get(f"{self.resource_path}/me")


class PostsCRUD(CRUDBase):
    """CRUD operations for posts."""
    
    def __init__(self, client: RestClient):
        super().__init__(client, "/api/posts")
    
    async def get_by_author(self, author_id: Any) -> ApiResponse:
        """Get posts by author."""
        return await self.client.get(f"{self.resource_path}/author/{author_id}")
    
    async def get_published(self) -> ApiResponse:
        """Get published posts."""
        return await self.client.get(f"{self.resource_path}/published")
    
    async def search(self, query: str) -> ApiResponse:
        """Search posts."""
        return await self.client.get(f"{self.resource_path}/search", params={"q": query})


class CommentsCRUD(CRUDBase):
    """CRUD operations for comments."""
    
    def __init__(self, client: RestClient):
        super().__init__(client, "/api/comments")
    
    async def get_by_post(self, post_id: Any) -> ApiResponse:
        """Get comments by post."""
        return await self.client.get(f"{self.resource_path}/post/{post_id}")


class ApiFactory:
    """Factory for creating API clients."""
    
    def __init__(self, base_url: str, config: RequestConfig = None):
        if config is None:
            config = RequestConfig(base_url=base_url)
        else:
            config.base_url = base_url
        
        self.client = RestClient(config)
        self.users = UsersCRUD(self.client)
        self.posts = PostsCRUD(self.client)
        self.comments = CommentsCRUD(self.client)
    
    def set_auth_token(self, token: str):
        """Set authentication token."""
        self.client.config.auth_token = token
    
    def clear_auth_token(self):
        """Clear authentication token."""
        self.client.config.auth_token = None


def create_api(base_url: str, auth_token: str = None) -> ApiFactory:
    """Create an API factory."""
    factory = ApiFactory(base_url)
    if auth_token:
        factory.set_auth_token(auth_token)
    return factory


def create_client(base_url: str, headers: Dict[str, str] = None, auth_token: str = None) -> RestClient:
    """Create a REST client."""
    config = RequestConfig(
        base_url=base_url,
        headers=headers or {},
        auth_token=auth_token,
    )
    return RestClient(config)


def create_crud(client: RestClient, resource_path: str) -> CRUDBase:
    """Create a CRUD base."""
    return CRUDBase(client, resource_path)
