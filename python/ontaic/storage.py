"""Storage abstraction for client-side data persistence."""
import json
import time
from typing import Any, Callable, Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum


class StorageType(str, Enum):
    """Storage types."""
    LOCAL = "local"
    SESSION = "session"
    MEMORY = "memory"


@dataclass
class StorageItem:
    """Storage item with metadata."""
    key: str
    value: Any
    expires_at: Optional[float] = None
    created_at: float = field(default_factory=time.time)
    
    @property
    def is_expired(self) -> bool:
        if self.expires_at is None:
            return False
        return time.time() > self.expires_at
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "value": self.value,
            "expiresAt": self.expires_at,
            "createdAt": self.created_at,
        }
    
    @classmethod
    def from_dict(cls, key: str, data: Dict[str, Any]) -> "StorageItem":
        return cls(
            key=key,
            value=data.get("value"),
            expires_at=data.get("expiresAt"),
            created_at=data.get("createdAt", time.time()),
        )


class MemoryStorage:
    """In-memory storage (no persistence)."""
    
    def __init__(self):
        self._data: Dict[str, StorageItem] = {}
        self._listeners: Dict[str, List[Callable]] = {}
    
    def get(self, key: str) -> Optional[Any]:
        """Get item from storage."""
        item = self._data.get(key)
        if item is None:
            return None
        if item.is_expired:
            self.delete(key)
            return None
        return item.value
    
    def set(self, key: str, value: Any, ttl: float = None):
        """Set item in storage."""
        expires_at = time.time() + ttl if ttl else None
        item = StorageItem(key=key, value=value, expires_at=expires_at)
        self._data[key] = item
        self._notify(key, "set", value)
    
    def delete(self, key: str):
        """Delete item from storage."""
        if key in self._data:
            del self._data[key]
            self._notify(key, "delete", None)
    
    def clear(self):
        """Clear all items."""
        self._data.clear()
    
    def keys(self) -> List[str]:
        """Get all keys."""
        return list(self._data.keys())
    
    def size(self) -> int:
        """Get number of items."""
        return len(self._data)
    
    def has(self, key: str) -> bool:
        """Check if key exists."""
        return key in self._data
    
    def on_change(self, key: str, callback: Callable):
        """Listen for changes to a key."""
        if key not in self._listeners:
            self._listeners[key] = []
        self._listeners[key].append(callback)
    
    def _notify(self, key: str, action: str, value: Any):
        """Notify listeners of changes."""
        for callback in self._listeners.get(key, []):
            callback(key, action, value)
    
    def generate_js_code(self) -> str:
        """Generate JavaScript storage code."""
        return """
        // Memory Storage
        const memoryStorage = {
            _data: {},
            _listeners: {},
            
            get(key) {
                const item = this._data[key];
                if (!item) return null;
                if (item.expiresAt && Date.now() > item.expiresAt) {
                    this.delete(key);
                    return null;
                }
                return item.value;
            },
            
            set(key, value, ttl = null) {
                const expiresAt = ttl ? Date.now() + ttl * 1000 : null;
                this._data[key] = { value, expiresAt, createdAt: Date.now() };
                this._notify(key, 'set', value);
            },
            
            delete(key) {
                delete this._data[key];
                this._notify(key, 'delete', null);
            },
            
            clear() {
                this._data = {};
            },
            
            keys() {
                return Object.keys(this._data);
            },
            
            size() {
                return Object.keys(this._data).length;
            },
            
            has(key) {
                return key in this._data;
            },
            
            onChange(key, callback) {
                if (!this._listeners[key]) {
                    this._listeners[key] = [];
                }
                this._listeners[key].push(callback);
            },
            
            _notify(key, action, value) {
                (this._listeners[key] || []).forEach(cb => cb(key, action, value));
            }
        };
        """


class LocalStorage:
    """localStorage wrapper with expiration support."""
    
    def __init__(self, prefix: str = "ontaic_"):
        self.prefix = prefix
        self._listeners: Dict[str, List[Callable]] = {}
    
    def _key(self, key: str) -> str:
        return f"{self.prefix}{key}"
    
    def get(self, key: str) -> Optional[Any]:
        """Get item from localStorage."""
        try:
            raw = window.localStorage.getItem(self._key(key))
            if raw is None:
                return None
            
            item = StorageItem.from_dict(key, json.loads(raw))
            if item.is_expired:
                self.delete(key)
                return None
            
            return item.value
        except Exception:
            return None
    
    def set(self, key: str, value: Any, ttl: float = None):
        """Set item in localStorage."""
        expires_at = time.time() + ttl if ttl else None
        item = StorageItem(key=key, value=value, expires_at=expires_at)
        
        try:
            window.localStorage.setItem(self._key(key), json.dumps(item.to_dict()))
            self._notify(key, "set", value)
        except Exception as e:
            print(f"LocalStorage error: {e}")
    
    def delete(self, key: str):
        """Delete item from localStorage."""
        try:
            window.localStorage.removeItem(self._key(key))
            self._notify(key, "delete", None)
        except Exception:
            pass
    
    def clear(self):
        """Clear all items with this prefix."""
        try:
            keys_to_delete = []
            for i in range(len(window.localStorage)):
                k = window.localStorage.key(i)
                if k and k.startswith(self.prefix):
                    keys_to_delete.append(k)
            
            for k in keys_to_delete:
                window.localStorage.removeItem(k)
        except Exception:
            pass
    
    def keys(self) -> List[str]:
        """Get all keys with this prefix."""
        try:
            keys = []
            for i in range(len(window.localStorage)):
                k = window.localStorage.key(i)
                if k and k.startswith(self.prefix):
                    keys.append(k[len(self.prefix):])
            return keys
        except Exception:
            return []
    
    def size(self) -> int:
        """Get number of items."""
        return len(self.keys())
    
    def has(self, key: str) -> bool:
        """Check if key exists."""
        return self.get(key) is not None
    
    def on_change(self, key: str, callback: Callable):
        """Listen for changes to a key."""
        if key not in self._listeners:
            self._listeners[key] = []
        self._listeners[key].append(callback)
    
    def _notify(self, key: str, action: str, value: Any):
        """Notify listeners of changes."""
        for callback in self._listeners.get(key, []):
            callback(key, action, value)
    
    def generate_js_code(self) -> str:
        """Generate JavaScript localStorage wrapper."""
        return f"""
        // LocalStorage with expiration
        const localStorage = {{
            prefix: '{self.prefix}',
            
            _key(key) {{
                return this.prefix + key;
            }},
            
            get(key) {{
                try {{
                    const raw = window.localStorage.getItem(this._key(key));
                    if (!raw) return null;
                    
                    const item = JSON.parse(raw);
                    if (item.expiresAt && Date.now() > item.expiresAt) {{
                        this.delete(key);
                        return null;
                    }}
                    
                    return item.value;
                }} catch (e) {{
                    return null;
                }}
            }},
            
            set(key, value, ttl = null) {{
                try {{
                    const expiresAt = ttl ? Date.now() + ttl * 1000 : null;
                    const item = {{ value, expiresAt, createdAt: Date.now() }};
                    window.localStorage.setItem(this._key(key), JSON.stringify(item));
                }} catch (e) {{
                    console.error('LocalStorage error:', e);
                }}
            }},
            
            delete(key) {{
                window.localStorage.removeItem(this._key(key));
            }},
            
            clear() {{
                const keysToDelete = [];
                for (let i = 0; i < window.localStorage.length; i++) {{
                    const k = window.localStorage.key(i);
                    if (k && k.startsWith(this.prefix)) {{
                        keysToDelete.push(k);
                    }}
                }}
                keysToDelete.forEach(k => window.localStorage.removeItem(k));
            }},
            
            keys() {{
                const keys = [];
                for (let i = 0; i < window.localStorage.length; i++) {{
                    const k = window.localStorage.key(i);
                    if (k && k.startsWith(this.prefix)) {{
                        keys.push(k.slice(this.prefix.length));
                    }}
                }}
                return keys;
            }},
            
            size() {{
                return this.keys().length;
            }},
            
            has(key) {{
                return this.get(key) !== null;
            }}
        }};
        """


class SessionStorage:
    """sessionStorage wrapper with expiration support."""
    
    def __init__(self, prefix: str = "ontaic_"):
        self.prefix = prefix
        self._listeners: Dict[str, List[Callable]] = {}
    
    def _key(self, key: str) -> str:
        return f"{self.prefix}{key}"
    
    def get(self, key: str) -> Optional[Any]:
        """Get item from sessionStorage."""
        try:
            raw = window.sessionStorage.getItem(self._key(key))
            if raw is None:
                return None
            
            item = StorageItem.from_dict(key, json.loads(raw))
            if item.is_expired:
                self.delete(key)
                return None
            
            return item.value
        except Exception:
            return None
    
    def set(self, key: str, value: Any, ttl: float = None):
        """Set item in sessionStorage."""
        expires_at = time.time() + ttl if ttl else None
        item = StorageItem(key=key, value=value, expires_at=expires_at)
        
        try:
            window.sessionStorage.setItem(self._key(key), json.dumps(item.to_dict()))
            self._notify(key, "set", value)
        except Exception as e:
            print(f"SessionStorage error: {e}")
    
    def delete(self, key: str):
        """Delete item from sessionStorage."""
        try:
            window.sessionStorage.removeItem(self._key(key))
            self._notify(key, "delete", None)
        except Exception:
            pass
    
    def clear(self):
        """Clear all items with this prefix."""
        try:
            keys_to_delete = []
            for i in range(len(window.sessionStorage)):
                k = window.sessionStorage.key(i)
                if k and k.startswith(self.prefix):
                    keys_to_delete.append(k)
            
            for k in keys_to_delete:
                window.sessionStorage.removeItem(k)
        except Exception:
            pass
    
    def keys(self) -> List[str]:
        """Get all keys with this prefix."""
        try:
            keys = []
            for i in range(len(window.sessionStorage)):
                k = window.sessionStorage.key(i)
                if k and k.startswith(self.prefix):
                    keys.append(k[len(self.prefix):])
            return keys
        except Exception:
            return []
    
    def size(self) -> int:
        """Get number of items."""
        return len(self.keys())
    
    def has(self, key: str) -> bool:
        """Check if key exists."""
        return self.get(key) is not None
    
    def on_change(self, key: str, callback: Callable):
        """Listen for changes to a key."""
        if key not in self._listeners:
            self._listeners[key] = []
        self._listeners[key].append(callback)
    
    def _notify(self, key: str, action: str, value: Any):
        """Notify listeners of changes."""
        for callback in self._listeners.get(key, []):
            callback(key, action, value)
    
    def generate_js_code(self) -> str:
        """Generate JavaScript sessionStorage wrapper."""
        return f"""
        // SessionStorage with expiration
        const sessionStorage = {{
            prefix: '{self.prefix}',
            
            _key(key) {{
                return this.prefix + key;
            }},
            
            get(key) {{
                try {{
                    const raw = window.sessionStorage.getItem(this._key(key));
                    if (!raw) return null;
                    
                    const item = JSON.parse(raw);
                    if (item.expiresAt && Date.now() > item.expiresAt) {{
                        this.delete(key);
                        return null;
                    }}
                    
                    return item.value;
                }} catch (e) {{
                    return null;
                }}
            }},
            
            set(key, value, ttl = null) {{
                try {{
                    const expiresAt = ttl ? Date.now() + ttl * 1000 : null;
                    const item = {{ value, expiresAt, createdAt: Date.now() }};
                    window.sessionStorage.setItem(this._key(key), JSON.stringify(item));
                }} catch (e) {{
                    console.error('SessionStorage error:', e);
                }}
            }},
            
            delete(key) {{
                window.sessionStorage.removeItem(this._key(key));
            }},
            
            clear() {{
                const keysToDelete = [];
                for (let i = 0; i < window.sessionStorage.length; i++) {{
                    const k = window.sessionStorage.key(i);
                    if (k && k.startsWith(this.prefix)) {{
                        keysToDelete.push(k);
                    }}
                }}
                keysToDelete.forEach(k => window.sessionStorage.removeItem(k));
            }},
            
            keys() {{
                const keys = [];
                for (let i = 0; i < window.sessionStorage.length; i++) {{
                    const k = window.sessionStorage.key(i);
                    if (k && k.startsWith(this.prefix)) {{
                        keys.push(k.slice(this.prefix.length));
                    }}
                }}
                return keys;
            }},
            
            size() {{
                return this.keys().length;
            }},
            
            has(key) {{
                return this.get(key) !== null;
            }}
        }};
        """


class IndexedDBStorage:
    """IndexedDB wrapper for large data storage."""
    
    def __init__(self, db_name: str = "ontaic_db", version: int = 1):
        self.db_name = db_name
        self.version = version
        self._store_name = "ontaic_store"
    
    async def _get_db(self):
        """Get database instance."""
        try:
            import indexeddb
            return await indexeddb.open(self.db_name, self.version)
        except ImportError:
            return None
    
    async def get(self, key: str) -> Optional[Any]:
        """Get item from IndexedDB."""
        try:
            import indexeddb
            db = await indexeddb.open(self.db_name, self.version)
            store = await db.object_store(self._store_name)
            result = await store.get(key)
            return result
        except Exception:
            return None
    
    async def set(self, key: str, value: Any):
        """Set item in IndexedDB."""
        try:
            import indexeddb
            db = await indexeddb.open(self.db_name, self.version)
            store = await db.object_store(self._store_name)
            await store.put(value, key)
        except Exception as e:
            print(f"IndexedDB error: {e}")
    
    async def delete(self, key: str):
        """Delete item from IndexedDB."""
        try:
            import indexeddb
            db = await indexeddb.open(self.db_name, self.version)
            store = await db.object_store(self._store_name)
            await store.delete(key)
        except Exception:
            pass
    
    async def clear(self):
        """Clear all items."""
        try:
            import indexeddb
            db = await indexeddb.open(self.db_name, self.version)
            store = await db.object_store(self._store_name)
            await store.clear()
        except Exception:
            pass
    
    async def keys(self) -> List[str]:
        """Get all keys."""
        try:
            import indexeddb
            db = await indexeddb.open(self.db_name, self.version)
            store = await db.object_store(self._store_name)
            return await store.get_all_keys()
        except Exception:
            return []
    
    def generate_js_code(self) -> str:
        """Generate JavaScript IndexedDB code."""
        return f"""
        // IndexedDB Storage
        const indexedDBStorage = {{
            dbName: '{self.db_name}',
            version: {self.version},
            storeName: '{self._store_name}',
            
            async open() {{
                return new Promise((resolve, reject) => {{
                    const request = indexedDB.open(this.dbName, this.version);
                    
                    request.onupgradeneeded = (event) => {{
                        const db = event.target.result;
                        if (!db.objectStoreNames.contains(this.storeName)) {{
                            db.createObjectStore(this.storeName);
                        }}
                    }};
                    
                    request.onsuccess = (event) => {{
                        resolve(event.target.result);
                    }};
                    
                    request.onerror = (event) => {{
                        reject(event.target.error);
                    }};
                }});
            }},
            
            async get(key) {{
                const db = await this.open();
                return new Promise((resolve, reject) => {{
                    const transaction = db.transaction(this.storeName, 'readonly');
                    const store = transaction.objectStore(this.storeName);
                    const request = store.get(key);
                    
                    request.onsuccess = (event) => {{
                        resolve(event.target.result);
                    }};
                    
                    request.onerror = (event) => {{
                        reject(event.target.error);
                    }};
                }});
            }},
            
            async set(key, value) {{
                const db = await this.open();
                return new Promise((resolve, reject) => {{
                    const transaction = db.transaction(this.storeName, 'readwrite');
                    const store = transaction.objectStore(this.storeName);
                    const request = store.put(value, key);
                    
                    request.onsuccess = () => {{
                        resolve();
                    }};
                    
                    request.onerror = (event) => {{
                        reject(event.target.error);
                    }};
                }});
            }},
            
            async delete(key) {{
                const db = await this.open();
                return new Promise((resolve, reject) => {{
                    const transaction = db.transaction(this.storeName, 'readwrite');
                    const store = transaction.objectStore(this.storeName);
                    const request = store.delete(key);
                    
                    request.onsuccess = () => {{
                        resolve();
                    }};
                    
                    request.onerror = (event) => {{
                        reject(event.target.error);
                    }};
                }});
            }},
            
            async clear() {{
                const db = await this.open();
                return new Promise((resolve, reject) => {{
                    const transaction = db.transaction(this.storeName, 'readwrite');
                    const store = transaction.objectStore(this.storeName);
                    const request = store.clear();
                    
                    request.onsuccess = () => {{
                        resolve();
                    }};
                    
                    request.onerror = (event) => {{
                        reject(event.target.error);
                    }};
                }});
            }},
            
            async keys() {{
                const db = await this.open();
                return new Promise((resolve, reject) => {{
                    const transaction = db.transaction(this.storeName, 'readonly');
                    const store = transaction.objectStore(this.storeName);
                    const request = store.getAllKeys();
                    
                    request.onsuccess = (event) => {{
                        resolve(event.target.result);
                    }};
                    
                    request.onerror = (event) => {{
                        reject(event.target.error);
                    }};
                }});
            }}
        }};
        """


class Storage:
    """Unified storage interface."""
    
    def __init__(self, storage_type: StorageType = StorageType.LOCAL, prefix: str = "ontaic_"):
        self.storage_type = storage_type
        self.prefix = prefix
        self._memory = MemoryStorage()
        self._local = LocalStorage(prefix)
        self._session = SessionStorage(prefix)
        self._indexed = IndexedDBStorage()
    
    def get(self, key: str) -> Optional[Any]:
        """Get item from storage."""
        if self.storage_type == StorageType.MEMORY:
            return self._memory.get(key)
        elif self.storage_type == StorageType.LOCAL:
            return self._local.get(key)
        elif self.storage_type == StorageType.SESSION:
            return self._session.get(key)
        return None
    
    def set(self, key: str, value: Any, ttl: float = None):
        """Set item in storage."""
        if self.storage_type == StorageType.MEMORY:
            self._memory.set(key, value, ttl)
        elif self.storage_type == StorageType.LOCAL:
            self._local.set(key, value, ttl)
        elif self.storage_type == StorageType.SESSION:
            self._session.set(key, value, ttl)
    
    def delete(self, key: str):
        """Delete item from storage."""
        if self.storage_type == StorageType.MEMORY:
            self._memory.delete(key)
        elif self.storage_type == StorageType.LOCAL:
            self._local.delete(key)
        elif self.storage_type == StorageType.SESSION:
            self._session.delete(key)
    
    def clear(self):
        """Clear all items."""
        if self.storage_type == StorageType.MEMORY:
            self._memory.clear()
        elif self.storage_type == StorageType.LOCAL:
            self._local.clear()
        elif self.storage_type == StorageType.SESSION:
            self._session.clear()
    
    def keys(self) -> List[str]:
        """Get all keys."""
        if self.storage_type == StorageType.MEMORY:
            return self._memory.keys()
        elif self.storage_type == StorageType.LOCAL:
            return self._local.keys()
        elif self.storage_type == StorageType.SESSION:
            return self._session.keys()
        return []
    
    def size(self) -> int:
        """Get number of items."""
        if self.storage_type == StorageType.MEMORY:
            return self._memory.size()
        elif self.storage_type == StorageType.LOCAL:
            return self._local.size()
        elif self.storage_type == StorageType.SESSION:
            return self._session.size()
        return 0
    
    def has(self, key: str) -> bool:
        """Check if key exists."""
        return self.get(key) is not None
    
    def on_change(self, key: str, callback: Callable):
        """Listen for changes."""
        if self.storage_type == StorageType.MEMORY:
            self._memory.on_change(key, callback)
        elif self.storage_type == StorageType.LOCAL:
            self._local.on_change(key, callback)
        elif self.storage_type == StorageType.SESSION:
            self._session.on_change(key, callback)


def create_storage(storage_type: str = "local", prefix: str = "ontaic_") -> Storage:
    """Create a storage instance."""
    st = StorageType(storage_type)
    return Storage(st, prefix)


def localStorage(prefix: str = "ontaic_") -> LocalStorage:
    """Create localStorage instance."""
    return LocalStorage(prefix)


def sessionStorage(prefix: str = "ontaic_") -> SessionStorage:
    """Create sessionStorage instance."""
    return SessionStorage(prefix)


def memoryStorage() -> MemoryStorage:
    """Create memory storage instance."""
    return MemoryStorage()
