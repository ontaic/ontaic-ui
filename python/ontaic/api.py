"""API integration patterns for ontaic."""
import json
from typing import Any, Callable, Dict, List, Optional
from dataclasses import dataclass
from enum import Enum


class HttpMethod(str, Enum):
    """HTTP methods."""
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"


@dataclass
class Request:
    """API request."""
    method: HttpMethod
    url: str
    headers: Dict[str, str]
    data: Optional[Dict[str, Any]] = None
    params: Optional[Dict[str, str]] = None


@dataclass
class Response:
    """API response."""
    status: int
    data: Any
    headers: Dict[str, str]
    
    @property
    def ok(self) -> bool:
        return 200 <= self.status < 300
    
    def json(self) -> Any:
        return self.data


class ApiClient:
    """API client for making HTTP requests."""
    
    def __init__(self, base_url: str = "", headers: Dict[str, str] = None):
        self.base_url = base_url.rstrip("/")
        self.headers = headers or {}
        self.interceptors: Dict[str, list] = {
            "request": [],
            "response": [],
        }
    
    def intercept(self, event: str, handler: Callable):
        """Add an interceptor."""
        if event in self.interceptors:
            self.interceptors[event].append(handler)
    
    def _build_url(self, path: str, params: Dict[str, str] = None) -> str:
        """Build the full URL."""
        url = f"{self.base_url}{path}"
        if params:
            query_string = "&".join(f"{k}={v}" for k, v in params.items())
            url = f"{url}?{query_string}"
        return url
    
    async def request(
        self,
        method: HttpMethod,
        path: str,
        data: Dict[str, Any] = None,
        headers: Dict[str, str] = None,
        params: Dict[str, str] = None,
    ) -> Response:
        """Make an HTTP request."""
        import aiohttp
        
        url = self._build_url(path, params)
        merged_headers = {**self.headers, **(headers or {})}
        
        # Apply request interceptors
        request = Request(method, url, merged_headers, data, params)
        for interceptor in self.interceptors["request"]:
            request = interceptor(request)
        
        async with aiohttp.ClientSession() as session:
            async with session.request(
                method.value,
                request.url,
                headers=request.headers,
                json=request.data if request.data else None,
            ) as resp:
                response_data = await resp.json()
                response = Response(
                    status=resp.status,
                    data=response_data,
                    headers=dict(resp.headers),
                )
        
        # Apply response interceptors
        for interceptor in self.interceptors["response"]:
            response = interceptor(response)
        
        return response
    
    async def get(self, path: str, **kwargs) -> Response:
        """Make a GET request."""
        return await self.request(HttpMethod.GET, path, **kwargs)
    
    async def post(self, path: str, data: Dict[str, Any] = None, **kwargs) -> Response:
        """Make a POST request."""
        return await self.request(HttpMethod.POST, path, data=data, **kwargs)
    
    async def put(self, path: str, data: Dict[str, Any] = None, **kwargs) -> Response:
        """Make a PUT request."""
        return await self.request(HttpMethod.PUT, path, data=data, **kwargs)
    
    async def patch(self, path: str, data: Dict[str, Any] = None, **kwargs) -> Response:
        """Make a PATCH request."""
        return await self.request(HttpMethod.PATCH, path, data=data, **kwargs)
    
    async def delete(self, path: str, **kwargs) -> Response:
        """Make a DELETE request."""
        return await self.request(HttpMethod.DELETE, path, **kwargs)


class ApiEndpoint:
    """API endpoint definition."""
    
    def __init__(
        self,
        path: str,
        method: HttpMethod = HttpMethod.GET,
        response_type: str = "json",
    ):
        self.path = path
        self.method = method
        self.response_type = response_type
    
    async def call(self, client: ApiClient, **kwargs) -> Response:
        """Call the endpoint."""
        return await client.request(self.method, self.path, **kwargs)


# Predefined API endpoints
class UsersApi:
    """Users API endpoints."""
    
    def __init__(self, client: ApiClient):
        self.client = client
    
    async def list_users(self) -> Response:
        return await self.client.get("/api/users")
    
    async def get_user(self, user_id: int) -> Response:
        return await self.client.get(f"/api/users/{user_id}")
    
    async def create_user(self, data: Dict[str, Any]) -> Response:
        return await self.client.post("/api/users", data=data)
    
    async def update_user(self, user_id: int, data: Dict[str, Any]) -> Response:
        return await self.client.put(f"/api/users/{user_id}", data=data)
    
    async def delete_user(self, user_id: int) -> Response:
        return await self.client.delete(f"/api/users/{user_id}")


class PostsApi:
    """Posts API endpoints."""
    
    def __init__(self, client: ApiClient):
        self.client = client
    
    async def list_posts(self, params: Dict[str, str] = None) -> Response:
        return await self.client.get("/api/posts", params=params)
    
    async def get_post(self, post_id: int) -> Response:
        return await self.client.get(f"/api/posts/{post_id}")
    
    async def create_post(self, data: Dict[str, Any]) -> Response:
        return await self.client.post("/api/posts", data=data)
    
    async def update_post(self, post_id: int, data: Dict[str, Any]) -> Response:
        return await self.client.put(f"/api/posts/{post_id}", data=data)
    
    async def delete_post(self, post_id: int) -> Response:
        return await self.client.delete(f"/api/posts/{post_id}")


class AuthApi:
    """Authentication API endpoints."""
    
    def __init__(self, client: ApiClient):
        self.client = client
    
    async def login(self, username: str, password: str) -> Response:
        return await self.client.post("/api/auth/login", data={
            "username": username,
            "password": password,
        })
    
    async def logout(self) -> Response:
        return await self.client.post("/api/auth/logout")
    
    async def register(self, username: str, email: str, password: str) -> Response:
        return await self.client.post("/api/auth/register", data={
            "username": username,
            "email": email,
            "password": password,
        })
    
    async def get_profile(self) -> Response:
        return await self.client.get("/api/auth/profile")


def create_api_client(base_url: str, token: str = None) -> ApiClient:
    """Create an API client with default configuration."""
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    
    return ApiClient(base_url=base_url, headers=headers)


# JavaScript code generation for API calls
def generate_api_js_code() -> str:
    """Generate JavaScript code for API calls."""
    return """
    // API Client
    const api = {
        baseURL: '',
        
        async request(method, path, data = null, headers = {}) {
            const url = this.baseURL + path;
            const options = {
                method,
                headers: {
                    'Content-Type': 'application/json',
                    ...headers,
                },
            };
            
            if (data) {
                options.body = JSON.stringify(data);
            }
            
            const response = await fetch(url, options);
            const responseData = await response.json();
            
            return {
                status: response.status,
                data: responseData,
                ok: response.ok,
            };
        },
        
        get(path, headers) {
            return this.request('GET', path, null, headers);
        },
        
        post(path, data, headers) {
            return this.request('POST', path, data, headers);
        },
        
        put(path, data, headers) {
            return this.request('PUT', path, data, headers);
        },
        
        patch(path, data, headers) {
            return this.request('PATCH', path, data, headers);
        },
        
        delete(path, headers) {
            return this.request('DELETE', path, null, headers);
        },
    };
    
    // Example usage
    async function fetchUsers() {
        const response = await api.get('/api/users');
        if (response.ok) {
            return response.data;
        }
        throw new Error('Failed to fetch users');
    }
    
    async function createUser(userData) {
        const response = await api.post('/api/users', userData);
        if (response.ok) {
            return response.data;
        }
        throw new Error('Failed to create user');
    }
    """
