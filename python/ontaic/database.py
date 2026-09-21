"""Database integration patterns for ontaic."""
import json
import sqlite3
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Column:
    """Database column definition."""
    name: str
    type: str = "TEXT"
    primary_key: bool = False
    nullable: bool = True
    default: Any = None
    unique: bool = False
    
    def to_sql(self) -> str:
        """Convert to SQL column definition."""
        parts = [self.name, self.type]
        if self.primary_key:
            parts.append("PRIMARY KEY")
        if not self.nullable:
            parts.append("NOT NULL")
        if self.unique:
            parts.append("UNIQUE")
        if self.default is not None:
            if isinstance(self.default, str):
                parts.append(f"DEFAULT '{self.default}'")
            else:
                parts.append(f"DEFAULT {self.default}")
        return " ".join(parts)


@dataclass
class Table:
    """Database table definition."""
    name: str
    columns: List[Column] = field(default_factory=list)
    
    def to_sql(self) -> str:
        """Convert to SQL CREATE TABLE statement."""
        cols = ",\n    ".join(col.to_sql() for col in self.columns)
        return f"CREATE TABLE IF NOT EXISTS {self.name} (\n    {cols}\n);"


class Database:
    """SQLite database wrapper."""
    
    def __init__(self, db_path: str = "ontaic.db"):
        self.db_path = db_path
        self.conn: Optional[sqlite3.Connection] = None
    
    def connect(self):
        """Connect to the database."""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        return self
    
    def disconnect(self):
        """Disconnect from the database."""
        if self.conn:
            self.conn.close()
            self.conn = None
    
    def __enter__(self):
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()
    
    def create_table(self, table: Table):
        """Create a table from a Table definition."""
        if not self.conn:
            self.connect()
        self.conn.execute(table.to_sql())
        self.conn.commit()
    
    def execute(self, query: str, params: tuple = ()) -> sqlite3.Cursor:
        """Execute a SQL query."""
        if not self.conn:
            self.connect()
        return self.conn.execute(query, params)
    
    def executemany(self, query: str, params_list: List[tuple]) -> sqlite3.Cursor:
        """Execute a SQL query with multiple parameter sets."""
        if not self.conn:
            self.connect()
        return self.conn.executemany(query, params_list)
    
    def fetchone(self, query: str, params: tuple = ()) -> Optional[Dict]:
        """Fetch a single row."""
        cursor = self.execute(query, params)
        row = cursor.fetchone()
        if row:
            return dict(row)
        return None
    
    def fetchall(self, query: str, params: tuple = ()) -> List[Dict]:
        """Fetch all rows."""
        cursor = self.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]
    
    def insert(self, table: str, data: Dict[str, Any]) -> int:
        """Insert a row and return the last row ID."""
        columns = ", ".join(data.keys())
        placeholders = ", ".join(["?" for _ in data])
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        cursor = self.execute(query, tuple(data.values()))
        self.conn.commit()
        return cursor.lastrowid
    
    def update(self, table: str, data: Dict[str, Any], where: str, where_params: tuple = ()) -> int:
        """Update rows and return the number of affected rows."""
        set_clause = ", ".join([f"{k} = ?" for k in data.keys()])
        query = f"UPDATE {table} SET {set_clause} WHERE {where}"
        params = tuple(data.values()) + where_params
        cursor = self.execute(query, params)
        self.conn.commit()
        return cursor.rowcount
    
    def delete(self, table: str, where: str, where_params: tuple = ()) -> int:
        """Delete rows and return the number of affected rows."""
        query = f"DELETE FROM {table} WHERE {where}"
        cursor = self.execute(query, where_params)
        self.conn.commit()
        return cursor.rowcount
    
    def exists(self, table: str, where: str = "1=1", params: tuple = ()) -> bool:
        """Check if a row exists."""
        query = f"SELECT EXISTS(SELECT 1 FROM {table} WHERE {where})"
        cursor = self.execute(query, params)
        return cursor.fetchone()[0]


class Repository:
    """Generic repository pattern for database operations."""
    
    def __init__(self, db: Database, table_name: str):
        self.db = db
        self.table_name = table_name
    
    def find_by_id(self, id: int) -> Optional[Dict]:
        """Find a record by ID."""
        return self.db.fetchone(
            f"SELECT * FROM {self.table_name} WHERE id = ?",
            (id,)
        )
    
    def find_all(self, limit: int = 100, offset: int = 0) -> List[Dict]:
        """Find all records with pagination."""
        return self.db.fetchall(
            f"SELECT * FROM {self.table_name} LIMIT ? OFFSET ?",
            (limit, offset)
        )
    
    def find_where(self, where: str, params: tuple = ()) -> List[Dict]:
        """Find records by condition."""
        return self.db.fetchall(
            f"SELECT * FROM {self.table_name} WHERE {where}",
            params
        )
    
    def find_one_where(self, where: str, params: tuple = ()) -> Optional[Dict]:
        """Find one record by condition."""
        return self.db.fetchone(
            f"SELECT * FROM {self.table_name} WHERE {where}",
            params
        )
    
    def create(self, data: Dict[str, Any]) -> int:
        """Create a new record."""
        return self.db.insert(self.table_name, data)
    
    def update(self, id: int, data: Dict[str, Any]) -> int:
        """Update a record by ID."""
        return self.db.update(self.table_name, data, "id = ?", (id,))
    
    def delete(self, id: int) -> int:
        """Delete a record by ID."""
        return self.db.delete(self.table_name, "id = ?", (id,))
    
    def count(self, where: str = "1=1", params: tuple = ()) -> int:
        """Count records."""
        result = self.db.fetchone(
            f"SELECT COUNT(*) as count FROM {self.table_name} WHERE {where}",
            params
        )
        return result["count"] if result else 0
    
    def exists(self, where: str = "1=1", params: tuple = ()) -> bool:
        """Check if a record exists."""
        return self.db.exists(self.table_name, where, params)


# Predefined table schemas
USERS_TABLE = Table("users", [
    Column("id", "INTEGER", primary_key=True),
    Column("username", "TEXT", unique=True, nullable=False),
    Column("email", "TEXT", unique=True, nullable=False),
    Column("password_hash", "TEXT", nullable=False),
    Column("created_at", "TEXT", default="CURRENT_TIMESTAMP"),
    Column("updated_at", "TEXT", default="CURRENT_TIMESTAMP"),
])

POSTS_TABLE = Table("posts", [
    Column("id", "INTEGER", primary_key=True),
    Column("title", "TEXT", nullable=False),
    Column("content", "TEXT"),
    Column("author_id", "INTEGER"),
    Column("published", "INTEGER", default=0),
    Column("created_at", "TEXT", default="CURRENT_TIMESTAMP"),
    Column("updated_at", "TEXT", default="CURRENT_TIMESTAMP"),
])

SETTINGS_TABLE = Table("settings", [
    Column("id", "INTEGER", primary_key=True),
    Column("key", "TEXT", unique=True, nullable=False),
    Column("value", "TEXT"),
    Column("created_at", "TEXT", default="CURRENT_TIMESTAMP"),
    Column("updated_at", "TEXT", default="CURRENT_TIMESTAMP"),
])


class UserManager:
    """User management with authentication."""
    
    def __init__(self, db: Database):
        self.db = db
        self.repo = Repository(db, "users")
    
    def create_user(self, username: str, email: str, password: str) -> int:
        """Create a new user."""
        import hashlib
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        return self.repo.create({
            "username": username,
            "email": email,
            "password_hash": password_hash,
        })
    
    def authenticate(self, username: str, password: str) -> Optional[Dict]:
        """Authenticate a user."""
        import hashlib
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        user = self.repo.find_one_where(
            "username = ? AND password_hash = ?",
            (username, password_hash)
        )
        if user:
            # Remove password hash from returned data
            user.pop("password_hash", None)
        return user
    
    def get_user(self, user_id: int) -> Optional[Dict]:
        """Get a user by ID."""
        user = self.repo.find_by_id(user_id)
        if user:
            user.pop("password_hash", None)
        return user
    
    def get_user_by_email(self, email: str) -> Optional[Dict]:
        """Get a user by email."""
        user = self.repo.find_one_where("email = ?", (email,))
        if user:
            user.pop("password_hash", None)
        return user
    
    def update_user(self, user_id: int, data: Dict[str, Any]) -> int:
        """Update a user."""
        # Don't allow updating password hash directly
        data.pop("password_hash", None)
        return self.repo.update(user_id, data)
    
    def delete_user(self, user_id: int) -> int:
        """Delete a user."""
        return self.repo.delete(user_id)
    
    def list_users(self, limit: int = 100, offset: int = 0) -> List[Dict]:
        """List all users."""
        users = self.repo.find_all(limit, offset)
        for user in users:
            user.pop("password_hash", None)
        return users


class PostManager:
    """Post management."""
    
    def __init__(self, db: Database):
        self.db = db
        self.repo = Repository(db, "posts")
    
    def create_post(self, title: str, content: str, author_id: int, published: bool = False) -> int:
        """Create a new post."""
        return self.repo.create({
            "title": title,
            "content": content,
            "author_id": author_id,
            "published": 1 if published else 0,
        })
    
    def get_post(self, post_id: int) -> Optional[Dict]:
        """Get a post by ID."""
        return self.repo.find_by_id(post_id)
    
    def list_posts(self, published_only: bool = False, limit: int = 100, offset: int = 0) -> List[Dict]:
        """List posts."""
        if published_only:
            return self.repo.find_where("published = 1 LIMIT ? OFFSET ?", (limit, offset))
        return self.repo.find_all(limit, offset)
    
    def update_post(self, post_id: int, data: Dict[str, Any]) -> int:
        """Update a post."""
        return self.repo.update(post_id, data)
    
    def delete_post(self, post_id: int) -> int:
        """Delete a post."""
        return self.repo.delete(post_id)
    
    def get_posts_by_author(self, author_id: int) -> List[Dict]:
        """Get posts by author."""
        return self.repo.find_where("author_id = ?", (author_id,))


def init_database(db_path: str = "ontaic.db") -> Database:
    """Initialize database with default tables."""
    db = Database(db_path)
    db.connect()
    db.create_table(USERS_TABLE)
    db.create_table(POSTS_TABLE)
    db.create_table(SETTINGS_TABLE)
    return db
