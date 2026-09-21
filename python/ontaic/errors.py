"""Error boundaries and error handling for ontaic."""
import traceback
import sys
from typing import Any, Callable, Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class ErrorInfo:
    """Error information."""
    error_type: str
    message: str
    stack_trace: str = ""
    component: str = ""
    timestamp: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "errorType": self.error_type,
            "message": self.message,
            "stackTrace": self.stack_trace,
            "component": self.component,
            "timestamp": self.timestamp,
            "metadata": self.metadata,
        }
    
    def to_html(self) -> str:
        return f"""
        <div class="bg-red-50 border border-red-200 rounded-lg p-4">
            <div class="flex items-center mb-2">
                <svg class="w-5 h-5 text-red-500 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
                <h3 class="text-red-800 font-medium">{self.error_type}</h3>
            </div>
            <p class="text-red-700 text-sm">{self.message}</p>
            {f'<pre class="mt-2 text-xs text-red-600 overflow-auto">{self.stack_trace}</pre>' if self.stack_trace else ''}
        </div>
        """


class ErrorHandler:
    """Global error handler."""
    
    def __init__(self):
        self.errors: List[ErrorInfo] = []
        self.handlers: Dict[str, Callable] = {}
        self.default_handler: Optional[Callable] = None
        self.max_errors: int = 100
    
    def handle(self, error: Exception, component: str = "", metadata: Dict[str, Any] = None):
        """Handle an error."""
        error_info = ErrorInfo(
            error_type=type(error).__name__,
            message=str(error),
            stack_trace=traceback.format_exc(),
            component=component,
            metadata=metadata or {},
        )
        
        self.errors.append(error_info)
        
        # Keep only max_errors
        if len(self.errors) > self.max_errors:
            self.errors = self.errors[-self.max_errors:]
        
        # Call specific handler if registered
        error_type = type(error).__name__
        if error_type in self.handlers:
            self.handlers[error_type](error_info)
        elif self.default_handler:
            self.default_handler(error_info)
        
        return error_info
    
    def on(self, error_type: str, handler: Callable):
        """Register a handler for a specific error type."""
        self.handlers[error_type] = handler
    
    def on_all(self, handler: Callable):
        """Register a default handler for all errors."""
        self.default_handler = handler
    
    def get_errors(self, limit: int = 100) -> List[ErrorInfo]:
        """Get recent errors."""
        return self.errors[-limit:]
    
    def clear_errors(self):
        """Clear all errors."""
        self.errors.clear()
    
    def get_error_count(self) -> int:
        """Get total error count."""
        return len(self.errors)
    
    def generate_js_code(self) -> str:
        """Generate JavaScript error handling code."""
        return """
        // Error Handler
        const errorHandler = {
            errors: [],
            maxErrors: 100,
            handlers: {},
            
            handle(error, component = '', metadata = {}) {
                const errorInfo = {
                    errorType: error.name || 'Error',
                    message: error.message || String(error),
                    stackTrace: error.stack || '',
                    component,
                    timestamp: new Date().toISOString(),
                    metadata
                };
                
                this.errors.push(errorInfo);
                
                // Keep only maxErrors
                if (this.errors.length > this.maxErrors) {
                    this.errors = this.errors.slice(-this.maxErrors);
                }
                
                // Call handler if registered
                if (this.handlers[errorInfo.errorType]) {
                    this.handlers[errorInfo.errorType](errorInfo);
                }
                
                // Log to console
                console.error(`[Ontaic Error] ${errorInfo.errorType}: ${errorInfo.message}`);
                
                return errorInfo;
            },
            
            on(errorType, handler) {
                this.handlers[errorType] = handler;
            },
            
            getErrors(limit = 100) {
                return this.errors.slice(-limit);
            },
            
            clearErrors() {
                this.errors = [];
            },
            
            getErrorCount() {
                return this.errors.length;
            }
        };
        
        // Global error handlers
        window.addEventListener('error', (event) => {
            errorHandler.handle(event.error, 'window', {
                filename: event.filename,
                lineno: event.lineno,
                colno: event.colno
            });
        });
        
        window.addEventListener('unhandledrejection', (event) => {
            errorHandler.handle(event.reason, 'promise');
        });
        """


class ErrorBoundary:
    """Error boundary component for catching render errors."""
    
    def __init__(
        self,
        fallback: Any = None,
        onError: Optional[Callable] = None,
        component: str = "",
    ):
        self.fallback = fallback
        self.on_error = onError
        self.component = component
        self.error_handler = ErrorHandler()
    
    def render(self, content_func: Callable) -> str:
        """Render content with error boundary."""
        try:
            return content_func()
        except Exception as e:
            error_info = self.error_handler.handle(e, self.component)
            
            if self.on_error:
                self.on_error(error_info)
            
            if self.fallback:
                if callable(self.fallback):
                    return self.fallback(error_info)
                return str(self.fallback)
            
            return self._default_fallback(error_info)
    
    def _default_fallback(self, error_info: ErrorInfo) -> str:
        """Default fallback UI."""
        return f"""
        <div class="p-6 bg-red-50 border border-red-200 rounded-lg">
            <div class="flex items-center mb-4">
                <svg class="w-8 h-8 text-red-500 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path>
                </svg>
                <h2 class="text-xl font-bold text-red-800">Something went wrong</h2>
            </div>
            <p class="text-red-700 mb-4">{error_info.message}</p>
            <button 
                onclick="location.reload()"
                class="px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600"
            >
                Reload Page
            </button>
        </div>
        """


class ValidationError(Exception):
    """Validation error."""
    
    def __init__(self, field: str, message: str, code: str = "invalid"):
        self.field = field
        self.message = message
        self.code = code
        super().__init__(f"{field}: {message}")


class NotFoundError(Exception):
    """Not found error."""
    
    def __init__(self, resource: str, identifier: Any = None):
        self.resource = resource
        self.identifier = identifier
        message = f"{resource} not found"
        if identifier:
            message += f": {identifier}"
        super().__init__(message)


class AuthenticationError(Exception):
    """Authentication error."""
    
    def __init__(self, message: str = "Authentication required"):
        self.message = message
        super().__init__(message)


class AuthorizationError(Exception):
    """Authorization error."""
    
    def __init__(self, message: str = "Insufficient permissions"):
        self.message = message
        super().__init__(message)


class RateLimitError(Exception):
    """Rate limit error."""
    
    def __init__(self, retry_after: int = 60):
        self.retry_after = retry_after
        super().__init__(f"Rate limited. Retry after {retry_after} seconds")


class ApiError(Exception):
    """API error."""
    
    def __init__(self, status: int, message: str, response: Any = None):
        self.status = status
        self.message = message
        self.response = response
        super().__init__(f"API Error {status}: {message}")


# Retry utility
def retry(
    max_attempts: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
    exceptions: tuple = (Exception,),
):
    """Decorator for retrying functions on failure."""
    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            last_exception = None
            current_delay = delay
            
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        import time
                        time.sleep(current_delay)
                        current_delay *= backoff
            
            raise last_exception
        
        return wrapper
    return decorator


# Circuit breaker utility
class CircuitBreaker:
    """Circuit breaker pattern for fault tolerance."""
    
    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: float = 60,
        expected_exception: type = Exception,
    ):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.expected_exception = expected_exception
        self.failure_count = 0
        self.last_failure_time = 0
        self.state = "closed"  # closed, open, half-open
    
    def __call__(self, func: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            import time
            
            if self.state == "open":
                if time.time() - self.last_failure_time > self.recovery_timeout:
                    self.state = "half-open"
                else:
                    raise ApiError(503, "Circuit breaker is open")
            
            try:
                result = func(*args, **kwargs)
                
                if self.state == "half-open":
                    self.state = "closed"
                    self.failure_count = 0
                
                return result
            except self.expected_exception as e:
                self.failure_count += 1
                self.last_failure_time = time.time()
                
                if self.failure_count >= self.failure_threshold:
                    self.state = "open"
                
                raise
        
        return wrapper
    
    def reset(self):
        """Reset the circuit breaker."""
        self.failure_count = 0
        self.state = "closed"
    
    def is_open(self) -> bool:
        """Check if circuit breaker is open."""
        return self.state == "open"


# Timeout utility
def timeout(seconds: float):
    """Decorator for adding timeout to functions."""
    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            import signal
            
            def handler(signum, frame):
                raise TimeoutError(f"Function timed out after {seconds} seconds")
            
            signal.signal(signal.SIGALRM, handler)
            signal.alarm(int(seconds))
            
            try:
                return func(*args, **kwargs)
            finally:
                signal.alarm(0)
        
        return wrapper
    return timeout


# Cache utility
class Cache:
    """Simple in-memory cache."""
    
    def __init__(self, max_size: int = 1000, ttl: float = 300):
        self.max_size = max_size
        self.ttl = ttl
        self._cache: Dict[str, Dict[str, Any]] = {}
    
    def get(self, key: str) -> Any:
        """Get a value from cache."""
        if key in self._cache:
            entry = self._cache[key]
            import time
            if time.time() - entry["created"] < self.ttl:
                return entry["value"]
            else:
                del self._cache[key]
        return None
    
    def set(self, key: str, value: Any):
        """Set a value in cache."""
        import time
        
        if len(self._cache) >= self.max_size:
            # Remove oldest entry
            oldest_key = min(self._cache.keys(), key=lambda k: self._cache[k]["created"])
            del self._cache[oldest_key]
        
        self._cache[key] = {
            "value": value,
            "created": time.time(),
        }
    
    def delete(self, key: str):
        """Delete a value from cache."""
        self._cache.pop(key, None)
    
    def clear(self):
        """Clear the cache."""
        self._cache.clear()
    
    def size(self) -> int:
        """Get cache size."""
        return len(self._cache)


# Rate limiter
class RateLimiter:
    """Rate limiter for API calls."""
    
    def __init__(self, max_requests: int = 100, window: float = 60):
        self.max_requests = max_requests
        self.window = window
        self._requests: List[float] = []
    
    def allow(self) -> bool:
        """Check if a request is allowed."""
        import time
        now = time.time()
        
        # Remove old requests
        self._requests = [r for r in self._requests if now - r < self.window]
        
        if len(self._requests) < self.max_requests:
            self._requests.append(now)
            return True
        
        return False
    
    def wait_time(self) -> float:
        """Get time to wait before next request is allowed."""
        import time
        if not self._requests:
            return 0
        
        oldest = min(self._requests)
        wait = self.window - (time.time() - oldest)
        return max(0, wait)
    
    def reset(self):
        """Reset the rate limiter."""
        self._requests.clear()


# Generate error handling CSS
ERROR_CSS = """
/* Error styles */
.error-boundary {
    padding: 1rem;
    background-color: #fef2f2;
    border: 1px solid #fecaca;
    border-radius: 0.5rem;
}

.error-boundary h2 {
    color: #991b1b;
    font-size: 1.25rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
}

.error-boundary p {
    color: #b91c1c;
    margin-bottom: 1rem;
}

.error-boundary button {
    padding: 0.5rem 1rem;
    background-color: #dc2626;
    color: white;
    border-radius: 0.375rem;
    cursor: pointer;
}

.error-boundary button:hover {
    background-color: #b91c1c;
}

/* Toast error styles */
.toast-error {
    background-color: #fef2f2;
    border-color: #fecaca;
    color: #991b1b;
}

/* Validation error styles */
.field-error {
    color: #dc2626;
    font-size: 0.875rem;
    margin-top: 0.25rem;
}

.input-error {
    border-color: #dc2626;
}

.input-error:focus {
    ring-color: #dc2626;
}
"""
