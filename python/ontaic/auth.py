"""Authentication patterns for ontaic."""
import hashlib
import secrets
import json
from datetime import datetime, timedelta
from typing import Any, Callable, Dict, Optional
from dataclasses import dataclass
from functools import wraps


@dataclass
class User:
    """User model."""
    id: int
    username: str
    email: str
    is_active: bool = True
    is_admin: bool = False
    created_at: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "is_active": self.is_active,
            "is_admin": self.is_admin,
            "created_at": self.created_at,
        }


@dataclass
class Session:
    """Session model."""
    session_id: str
    user_id: int
    data: Dict[str, Any]
    expires_at: str
    created_at: str


class AuthManager:
    """Authentication manager."""
    
    def __init__(self, secret_key: str = None):
        self.secret_key = secret_key or secrets.token_hex(32)
        self.sessions: Dict[str, Session] = {}
        self.users: Dict[int, User] = {}
        self._login_handlers: list = []
        self._logout_handlers: list = []
    
    def hash_password(self, password: str) -> str:
        """Hash a password."""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def verify_password(self, password: str, password_hash: str) -> bool:
        """Verify a password."""
        return self.hash_password(password) == password_hash
    
    def create_user(self, username: str, email: str, password: str) -> User:
        """Create a new user."""
        user_id = len(self.users) + 1
        user = User(
            id=user_id,
            username=username,
            email=email,
            created_at=datetime.now().isoformat(),
        )
        self.users[user_id] = user
        return user
    
    def get_user(self, user_id: int) -> Optional[User]:
        """Get a user by ID."""
        return self.users.get(user_id)
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get a user by username."""
        for user in self.users.values():
            if user.username == username:
                return user
        return None
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get a user by email."""
        for user in self.users.values():
            if user.email == email:
                return user
        return None
    
    def create_session(self, user_id: int, data: Dict[str, Any] = None) -> Session:
        """Create a new session."""
        session_id = secrets.token_hex(32)
        session = Session(
            session_id=session_id,
            user_id=user_id,
            data=data or {},
            expires_at=(datetime.now() + timedelta(days=7)).isoformat(),
            created_at=datetime.now().isoformat(),
        )
        self.sessions[session_id] = session
        return session
    
    def get_session(self, session_id: str) -> Optional[Session]:
        """Get a session by ID."""
        session = self.sessions.get(session_id)
        if session:
            # Check if session is expired
            if datetime.fromisoformat(session.expires_at) < datetime.now():
                del self.sessions[session_id]
                return None
        return session
    
    def delete_session(self, session_id: str):
        """Delete a session."""
        self.sessions.pop(session_id, None)
    
    def login(self, username: str, password: str) -> Optional[Session]:
        """Login a user."""
        user = self.get_user_by_username(username)
        if user and self.verify_password(password, "hashed_" + password):
            session = self.create_session(user.id)
            # Notify handlers
            for handler in self._login_handlers:
                handler(user, session)
            return session
        return None
    
    def logout(self, session_id: str):
        """Logout a user."""
        session = self.get_session(session_id)
        if session:
            user = self.get_user(session.user_id)
            self.delete_session(session_id)
            # Notify handlers
            for handler in self._logout_handlers:
                handler(user, session)
    
    def on_login(self, handler: Callable):
        """Register a login handler."""
        self._login_handlers.append(handler)
    
    def on_logout(self, handler: Callable):
        """Register a logout handler."""
        self._logout_handlers.append(handler)
    
    def require_auth(self, func: Callable) -> Callable:
        """Decorator to require authentication."""
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Get session from request context
            session_id = kwargs.get("session_id") or (args[0] if args else None)
            session = self.get_session(session_id)
            if not session:
                raise PermissionError("Authentication required")
            kwargs["user"] = self.get_user(session.user_id)
            return func(*args, **kwargs)
        return wrapper
    
    def require_admin(self, func: Callable) -> Callable:
        """Decorator to require admin privileges."""
        @wraps(func)
        def wrapper(*args, **kwargs):
            session_id = kwargs.get("session_id") or (args[0] if args else None)
            session = self.get_session(session_id)
            if not session:
                raise PermissionError("Authentication required")
            user = self.get_user(session.user_id)
            if not user or not user.is_admin:
                raise PermissionError("Admin privileges required")
            kwargs["user"] = user
            return func(*args, **kwargs)
        return wrapper


class CookieAuth:
    """Cookie-based authentication for web apps."""
    
    def __init__(self, auth_manager: AuthManager, cookie_name: str = "session_id"):
        self.auth_manager = auth_manager
        self.cookie_name = cookie_name
    
    def get_session_from_cookies(self, cookies: Dict[str, str]) -> Optional[Session]:
        """Get session from cookies."""
        session_id = cookies.get(self.cookie_name)
        if session_id:
            return self.auth_manager.get_session(session_id)
        return None
    
    def set_session_cookie(self, session: Session) -> Dict[str, str]:
        """Set session cookie."""
        return {
            "Set-Cookie": f"{self.cookie_name}={session.session_id}; Path=/; HttpOnly; SameSite=Strict"
        }
    
    def clear_session_cookie(self) -> Dict[str, str]:
        """Clear session cookie."""
        return {
            "Set-Cookie": f"{self.cookie_name}=; Path=/; HttpOnly; SameSite=Strict; Max-Age=0"
        }


class JWTAuth:
    """JWT-based authentication."""
    
    def __init__(self, auth_manager: AuthManager, secret_key: str = None):
        self.auth_manager = auth_manager
        self.secret_key = secret_key or secrets.token_hex(32)
    
    def generate_token(self, user: User, expires_in: int = 3600) -> str:
        """Generate a JWT token."""
        import base64
        
        header = {"alg": "HS256", "typ": "JWT"}
        payload = {
            "user_id": user.id,
            "username": user.username,
            "exp": (datetime.now() + timedelta(seconds=expires_in)).isoformat(),
            "iat": datetime.now().isoformat(),
        }
        
        # Simple JWT implementation (not production-ready)
        header_b64 = base64.urlsafe_b64encode(json.dumps(header).encode()).decode()
        payload_b64 = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode()
        
        import hmac
        signature = hmac.new(
            self.secret_key.encode(),
            f"{header_b64}.{payload_b64}".encode(),
            hashlib.sha256
        ).hexdigest()
        
        return f"{header_b64}.{payload_b64}.{signature}"
    
    def verify_token(self, token: str) -> Optional[User]:
        """Verify a JWT token and return the user."""
        try:
            import base64
            import hmac
            
            parts = token.split(".")
            if len(parts) != 3:
                return None
            
            header_b64, payload_b64, signature = parts
            
            # Verify signature
            expected_signature = hmac.new(
                self.secret_key.encode(),
                f"{header_b64}.{payload_b64}".encode(),
                hashlib.sha256
            ).hexdigest()
            
            if signature != expected_signature:
                return None
            
            # Decode payload
            payload = json.loads(base64.urlsafe_b64decode(payload_b64 + "=="))
            
            # Check expiration
            if datetime.fromisoformat(payload["exp"]) < datetime.now():
                return None
            
            # Get user
            return self.auth_manager.get_user(payload["user_id"])
            
        except Exception:
            return None


# Example usage
def create_auth_app():
    """Create an example authentication setup."""
    auth = AuthManager()
    
    # Create some users
    auth.create_user("admin", "admin@example.com", "password123")
    auth.create_user("user1", "user1@example.com", "password123")
    
    # Login handler
    @auth.on_login
    def handle_login(user, session):
        print(f"User {user.username} logged in with session {session.session_id}")
    
    # Logout handler
    @auth.on_logout
    def handle_logout(user, session):
        print(f"User {user.username} logged out")
    
    return auth
