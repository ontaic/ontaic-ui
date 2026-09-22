"""Server-side rendering (SSR) support for ontaic."""
import json
import time
import hashlib
from typing import Any, Callable, Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
from functools import wraps
from html import escape as html_escape


@dataclass
class SSRContext:
    """Context for server-side rendering."""
    request_url: str = "/"
    request_method: str = "GET"
    request_headers: Dict[str, str] = field(default_factory=dict)
    request_cookies: Dict[str, str] = field(default_factory=dict)
    request_query: Dict[str, str] = field(default_factory=dict)
    user_agent: str = ""
    is_bot: bool = False
    language: str = "en"
    meta: Dict[str, Any] = field(default_factory=dict)
    
    @classmethod
    def from_request(cls, url: str, method: str = "GET", headers: Dict[str, str] = None, cookies: Dict[str, str] = None, query: Dict[str, str] = None) -> "SSRContext":
        """Create SSRContext from HTTP request."""
        headers = headers or {}
        cookies = cookies or {}
        query = query or {}
        
        user_agent = headers.get("user-agent", "")
        is_bot = any(bot in user_agent.lower() for bot in ["googlebot", "bingbot", "slurp", "duckduckbot", "baiduspider", "yandexbot"])
        
        return cls(
            request_url=url,
            request_method=method,
            request_headers=headers,
            request_cookies=cookies,
            request_query=query,
            user_agent=user_agent,
            is_bot=is_bot,
        )


@dataclass
class SSRMeta:
    """Meta tags for SSR."""
    title: str = ""
    description: str = ""
    keywords: str = ""
    og_title: str = ""
    og_description: str = ""
    og_image: str = ""
    og_url: str = ""
    og_type: str = "website"
    twitter_card: str = "summary_large_image"
    twitter_title: str = ""
    twitter_description: str = ""
    twitter_image: str = ""
    canonical_url: str = ""
    robots: str = "index, follow"
    viewport: str = "width=device-width, initial-scale=1.0"
    charset: str = "UTF-8"
    extra: Dict[str, str] = field(default_factory=dict)
    
    def to_html(self) -> str:
        """Generate HTML meta tags."""
        tags = []
        
        tags.append(f'<meta charset="{self.charset}">')
        tags.append(f'<meta name="viewport" content="{self.viewport}">')
        
        if self.title:
            tags.append(f'<title>{html_escape(self.title)}</title>')
            tags.append(f'<meta property="og:title" content="{html_escape(self.og_title or self.title)}">')
            tags.append(f'<meta name="twitter:title" content="{html_escape(self.twitter_title or self.title)}">')
        
        if self.description:
            tags.append(f'<meta name="description" content="{html_escape(self.description)}">')
            tags.append(f'<meta property="og:description" content="{html_escape(self.og_description or self.description)}">')
            tags.append(f'<meta name="twitter:description" content="{html_escape(self.twitter_description or self.description)}">')
        
        if self.keywords:
            tags.append(f'<meta name="keywords" content="{html_escape(self.keywords)}">')
        
        if self.og_image:
            tags.append(f'<meta property="og:image" content="{html_escape(self.og_image)}">')
            tags.append(f'<meta name="twitter:image" content="{html_escape(self.twitter_image or self.og_image)}">')
        
        if self.og_url:
            tags.append(f'<meta property="og:url" content="{html_escape(self.og_url)}">')
        
        tags.append(f'<meta property="og:type" content="{self.og_type}">')
        tags.append(f'<meta name="twitter:card" content="{self.twitter_card}">')
        
        if self.canonical_url:
            tags.append(f'<link rel="canonical" href="{html_escape(self.canonical_url)}">')
        
        tags.append(f'<meta name="robots" content="{self.robots}">')
        
        for key, value in self.extra.items():
            tags.append(f'<meta name="{html_escape(key)}" content="{html_escape(value)}">')
        
        return "\n    ".join(tags)


class SSRCache:
    """Cache for SSR rendered pages."""
    
    def __init__(self, max_size: int = 1000, ttl: float = 300):
        self.max_size = max_size
        self.ttl = ttl
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._timestamps: Dict[str, float] = {}
    
    def _make_key(self, url: str, context: SSRContext) -> str:
        """Generate cache key."""
        key_data = f"{url}:{context.language}:{context.is_bot}"
        return hashlib.md5(key_data.encode()).hexdigest()
    
    def get(self, url: str, context: SSRContext) -> Optional[str]:
        """Get cached HTML."""
        key = self._make_key(url, context)
        
        if key in self._cache:
            if time.time() - self._timestamps[key] < self.ttl:
                return self._cache[key]["html"]
            else:
                del self._cache[key]
                del self._timestamps[key]
        
        return None
    
    def set(self, url: str, context: SSRContext, html: str):
        """Cache rendered HTML."""
        key = self._make_key(url, context)
        
        if len(self._cache) >= self.max_size:
            oldest_key = min(self._timestamps.keys(), key=lambda k: self._timestamps[k])
            del self._cache[oldest_key]
            del self._timestamps[oldest_key]
        
        self._cache[key] = {"html": html, "url": url}
        self._timestamps[key] = time.time()
    
    def invalidate(self, url: str = None):
        """Invalidate cache entries."""
        if url:
            keys_to_delete = [k for k, v in self._cache.items() if v["url"] == url]
            for key in keys_to_delete:
                del self._cache[key]
                del self._timestamps[key]
        else:
            self._cache.clear()
            self._timestamps.clear()
    
    def size(self) -> int:
        """Get cache size."""
        return len(self._cache)


class SSRRenderer:
    """Server-side renderer for ontaic components."""
    
    def __init__(self):
        self.cache = SSRCache()
        self._routes: Dict[str, Callable] = {}
        self._layouts: Dict[str, Callable] = {}
        self._middleware: List[Callable] = []
    
    def route(self, path: str, handler: Callable):
        """Register a route handler."""
        self._routes[path] = handler
        return handler
    
    def layout(self, name: str, handler: Callable):
        """Register a layout."""
        self._layouts[name] = handler
        return handler
    
    def middleware(self, handler: Callable):
        """Register middleware."""
        self._middleware.append(handler)
        return handler
    
    def render(self, component, context: SSRContext = None, meta: SSRMeta = None) -> str:
        """Render a component to HTML string."""
        if context is None:
            context = SSRContext()
        
        # Run middleware
        for mw in self._middleware:
            result = mw(context)
            if result is False:
                return ""
        
        # Check cache
        cached = self.cache.get(context.request_url, context)
        if cached:
            return cached
        
        # Render component
        html = self._render_component(component, context)
        
        # Generate full page
        meta_html = meta.to_html() if meta else ""
        
        full_html = f"""<!DOCTYPE html>
<html lang="{context.language}">
<head>
    {meta_html}
</head>
<body>
    {html}
    <script>
        // Hydration - attach event listeners
        window.__SSR_DATA__ = {json.dumps(context.meta)};
    </script>
</body>
</html>"""
        
        # Cache the result
        self.cache.set(context.request_url, context, full_html)
        
        return full_html
    
    def _render_component(self, component, context: SSRContext) -> str:
        """Recursively render a component to HTML."""
        if isinstance(component, str):
            return html_escape(component)
        
        if isinstance(component, (int, float)):
            return str(component)
        
        if isinstance(component, bool):
            return "true" if component else "false"
        
        if isinstance(component, list):
            return "".join(self._render_component(item, context) for item in component)
        
        if hasattr(component, "render"):
            try:
                rendered = component.render()
                if isinstance(rendered, str):
                    return rendered
                return self._render_component(rendered, context)
            except Exception as e:
                return f'<!-- Error rendering component: {html_escape(str(e))} -->'
        
        return html_escape(str(component))
    
    def render_page(self, url: str, handler: Callable, meta: SSRMeta = None, context: SSRContext = None) -> str:
        """Render a page by URL."""
        if context is None:
            context = SSRContext(request_url=url)
        
        # Run middleware
        for mw in self._middleware:
            result = mw(context)
            if result is False:
                return "<html><body><h1>403 Forbidden</h1></body></html>"
        
        # Get handler
        handler_func = self._routes.get(url)
        if handler_func is None:
            return "<html><body><h1>404 Not Found</h1></body></html>"
        
        # Execute handler
        try:
            result = handler_func(context)
        except Exception as e:
            return f"<html><body><h1>500 Internal Server Error</h1><p>{html_escape(str(e))}</p></body></html>"
        
        # Render result
        if isinstance(result, dict):
            component = result.get("component")
            meta = result.get("meta", meta)
        else:
            component = result
        
        return self.render(component, context, meta)
    
    def generate_hydration_script(self) -> str:
        """Generate JavaScript hydration script."""
        return """
        <script>
        // SSR Hydration
        (function() {
            const ssrData = window.__SSR_DATA__ || {};
            
            // Find all interactive elements
            document.querySelectorAll('[data-ssr-click]').forEach(el => {
                const handler = el.getAttribute('data-ssr-click');
                el.addEventListener('click', () => {
                    eval(handler);
                });
            });
            
            document.querySelectorAll('[data-ssr-change]').forEach(el => {
                const handler = el.getAttribute('data-ssr-change');
                el.addEventListener('change', () => {
                    eval(handler);
                });
            });
            
            console.log('SSR hydration complete');
        })();
        </script>
        """


class SSRMiddleware:
    """Common SSR middleware."""
    
    @staticmethod
    def cors(allowed_origins: List[str] = None):
        """CORS middleware."""
        def middleware(context: SSRContext):
            origin = context.request_headers.get("origin", "")
            if allowed_origins and origin not in allowed_origins:
                return False
            return True
        return middleware
    
    @staticmethod
    def rate_limit(max_requests: int = 100, window: int = 60):
        """Rate limiting middleware."""
        _requests: Dict[str, List[float]] = {}
        
        def middleware(context: SSRContext):
            client_ip = context.request_headers.get("x-forwarded-for", "unknown")
            now = time.time()
            
            if client_ip not in _requests:
                _requests[client_ip] = []
            
            # Remove old requests
            _requests[client_ip] = [t for t in _requests[client_ip] if now - t < window]
            
            if len(_requests[client_ip]) >= max_requests:
                return False
            
            _requests[client_ip].append(now)
            return True
        
        return middleware
    
    @staticmethod
    def authentication(require_auth: bool = True, require_admin: bool = False):
        """Authentication middleware."""
        def middleware(context: SSRContext):
            if not require_auth and not require_admin:
                return True
            
            token = context.request_cookies.get("session_token")
            if not token:
                token = context.request_headers.get("authorization", "").replace("Bearer ", "")
            
            if require_auth and not token:
                return False
            
            return True
        
        return middleware
    
    @staticmethod
    def compression():
        """Compression middleware (placeholder - actual compression in web server)."""
        def middleware(context: SSRContext):
            context.meta["compress"] = True
            return True
        return middleware


def ssr_route(path: str, meta: SSRMeta = None):
    """Decorator to register an SSR route."""
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(context: SSRContext = None):
            result = func(context)
            return {"component": result, "meta": meta}
        
        # Store route info
        if not hasattr(wrapper, "_ssr_routes"):
            wrapper._ssr_routes = {}
        wrapper._ssr_routes[path] = {"handler": wrapper, "meta": meta}
        
        return wrapper
    return decorator


def ssr_layout(name: str):
    """Decorator to register an SSR layout."""
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(content, context: SSRContext = None):
            return func(content, context)
        
        if not hasattr(wrapper, "_ssr_layouts"):
            wrapper._ssr_layouts = {}
        wrapper._ssr_layouts[name] = wrapper
        
        return wrapper
    return decorator


def get_ssr_renderer() -> SSRRenderer:
    """Get the global SSR renderer instance."""
    if not hasattr(get_ssr_renderer, "_instance"):
        get_ssr_renderer._instance = SSRRenderer()
    return get_ssr_renderer._instance


def render_ssr(component, meta: SSRMeta = None, context: SSRContext = None) -> str:
    """Convenience function to render SSR."""
    renderer = get_ssr_renderer()
    return renderer.render(component, context, meta)


def render_ssr_page(url: str, handler: Callable, meta: SSRMeta = None) -> str:
    """Convenience function to render a page."""
    renderer = get_ssr_renderer()
    return renderer.render_page(url, handler, meta)


SSR_CSS = """
.ssr-loading {
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    font-family: system-ui, -apple-system, sans-serif;
}

.ssr-skeleton {
    animation: skeleton-pulse 1.5s ease-in-out infinite;
}

@keyframes skeleton-pulse {
    0%, 100% { opacity: 0.4; }
    50% { opacity: 1; }
}

.ssr-hidden {
    display: none !important;
}
"""
