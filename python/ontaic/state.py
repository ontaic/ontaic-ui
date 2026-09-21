"""Persistent state management with localStorage."""
import json
from typing import Any, Callable, Dict, Optional
from pathlib import Path
import os


class PersistentState:
    """State that persists across sessions using localStorage or file storage."""
    
    def __init__(
        self,
        storage_type: str = "local",  # "local", "session", "file"
        storage_key: str = "ontaic_state",
        file_path: str = ".ontaic_state.json",
    ):
        self.storage_type = storage_type
        self.storage_key = storage_key
        self.file_path = file_path
        self.state: Dict[str, Any] = {}
        self._load()
    
    def _load(self):
        """Load state from storage."""
        if self.storage_type == "file":
            self._load_from_file()
        # For browser storage, state is loaded via JavaScript
    
    def _load_from_file(self):
        """Load state from file."""
        try:
            path = Path(self.file_path)
            if path.exists():
                with open(path, "r") as f:
                    self.state = json.load(f)
        except Exception as e:
            print(f"[ontaic] Failed to load state: {e}")
            self.state = {}
    
    def _save_to_file(self):
        """Save state to file."""
        try:
            with open(self.file_path, "w") as f:
                json.dump(self.state, f, indent=2)
        except Exception as e:
            print(f"[ontaic] Failed to save state: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a state value."""
        return self.state.get(key, default)
    
    def set(self, key: str, value: Any, persist: bool = True):
        """Set a state value."""
        self.state[key] = value
        if persist and self.storage_type == "file":
            self._save_to_file()
    
    def update(self, updates: Dict[str, Any], persist: bool = True):
        """Update multiple state values."""
        self.state.update(updates)
        if persist and self.storage_type == "file":
            self._save_to_file()
    
    def delete(self, key: str, persist: bool = True):
        """Delete a state value."""
        if key in self.state:
            del self.state[key]
            if persist and self.storage_type == "file":
                self._save_to_file()
    
    def clear(self, persist: bool = True):
        """Clear all state."""
        self.state = {}
        if persist and self.storage_type == "file":
            self._save_to_file()
    
    def get_all(self) -> Dict[str, Any]:
        """Get all state."""
        return self.state.copy()
    
    def generate_js_code(self) -> str:
        """Generate JavaScript code for browser-side storage."""
        if self.storage_type == "local":
            return f"""
            // LocalStorage persistence
            function loadState() {{
                const stored = localStorage.getItem('{self.storage_key}');
                return stored ? JSON.parse(stored) : {json.dumps(self.state)};
            }}
            
            function saveState(state) {{
                localStorage.setItem('{self.storage_key}', JSON.stringify(state));
            }}
            
            function clearState() {{
                localStorage.removeItem('{self.storage_key}');
            }}
            """
        elif self.storage_type == "session":
            return f"""
            // SessionStorage persistence
            function loadState() {{
                const stored = sessionStorage.getItem('{self.storage_key}');
                return stored ? JSON.parse(stored) : {json.dumps(self.state)};
            }}
            
            function saveState(state) {{
                sessionStorage.setItem('{self.storage_key}', JSON.stringify(state));
            }}
            
            function clearState() {{
                sessionStorage.removeItem('{self.storage_key}');
            }}
            """
        else:
            return f"""
            // File-based persistence (server-side)
            function loadState() {{
                return {json.dumps(self.state)};
            }}
            
            function saveState(state) {{
                // In file mode, state is managed server-side
                console.log('State saved server-side');
            }}
            
            function clearState() {{
                console.log('State cleared server-side');
            }}
            """


class ComputedState:
    """State that derives from other state values."""
    
    def __init__(self):
        self._computations: Dict[str, Callable] = {}
        self._cache: Dict[str, Any] = {}
        self._dirty: Dict[str, bool] = {}
    
    def computed(self, key: str, dependencies: list = None):
        """Decorator to define a computed state value."""
        def decorator(func: Callable) -> Callable:
            self._computations[key] = {
                "func": func,
                "dependencies": dependencies or [],
            }
            self._dirty[key] = True
            return func
        return decorator
    
    def get(self, key: str, state: Dict[str, Any]) -> Any:
        """Get a computed value."""
        if key not in self._computations:
            return None
        
        # Check if we need to recompute
        if self._dirty.get(key, True):
            comp = self._computations[key]
            deps = {dep: state.get(dep) for dep in comp["dependencies"]}
            self._cache[key] = comp["func"](**deps)
            self._dirty[key] = False
        
        return self._cache.get(key)
    
    def invalidate(self, key: str = None):
        """Mark computed values as dirty."""
        if key:
            self._dirty[key] = True
        else:
            for k in self._dirty:
                self._dirty[k] = True
    
    def invalidate_dependents(self, changed_key: str):
        """Invalidate all computations that depend on the changed key."""
        for key, comp in self._computations.items():
            if changed_key in comp["dependencies"]:
                self._dirty[key] = True


class StateManager:
    """Centralized state manager with persistence and computed values."""
    
    def __init__(
        self,
        storage_type: str = "local",
        storage_key: str = "ontaic_state",
    ):
        self.persistent = PersistentState(storage_type, storage_key)
        self.computed = ComputedState()
        self._listeners: Dict[str, list] = {}
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a state value."""
        return self.persistent.get(key, default)
    
    def set(self, key: str, value: Any, persist: bool = True):
        """Set a state value and notify listeners."""
        old_value = self.persistent.get(key)
        self.persistent.set(key, value, persist)
        
        # Invalidate computed values
        self.computed.invalidate_dependents(key)
        
        # Notify listeners
        if key in self._listeners:
            for listener in self._listeners[key]:
                listener(value, old_value)
    
    def computed_value(self, key: str, dependencies: list = None):
        """Register a computed value."""
        return self.computed.computed(key, dependencies)
    
    def get_computed(self, key: str) -> Any:
        """Get a computed value."""
        return self.computed.get(key, self.persistent.get_all())
    
    def on_change(self, key: str, listener: Callable):
        """Register a listener for state changes."""
        if key not in self._listeners:
            self._listeners[key] = []
        self._listeners[key].append(listener)
    
    def generate_js_code(self) -> str:
        """Generate JavaScript code for browser-side state management."""
        return f"""
        // State Manager
        const stateManager = {{
            state: loadState(),
            
            get(key) {{
                return this.state[key];
            }},
            
            set(key, value) {{
                const oldValue = this.state[key];
                this.state[key] = value;
                saveState(this.state);
                
                // Notify listeners
                if (window.onStateChange) {{
                    window.onStateChange(key, value, oldValue);
                }}
            }},
            
            update(updates) {{
                Object.assign(this.state, updates);
                saveState(this.state);
            }},
            
            getAll() {{
                return {{ ...this.state }};
            }}
        }};
        
        // State change listeners
        window.onStateChange = null;
        window.addEventListener('storage', (e) => {{
            if (e.key === '{self.persistent.storage_key}') {{
                stateManager.state = JSON.parse(e.newValue || '{{}}');
                if (window.onStateChange) {{
                    window.onStateChange('storage', stateManager.state);
                }}
            }}
        }});
        """
