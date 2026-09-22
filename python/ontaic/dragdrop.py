"""Drag and drop support for ontaic."""
import json
from typing import Any, Callable, Dict, List, Optional
from dataclasses import dataclass, field


@dataclass
class DragData:
    """Drag data payload."""
    source_id: str
    source_type: str
    data: Any = None
    index: int = 0
    
    def to_json(self) -> str:
        return json.dumps({
            "sourceId": self.source_id,
            "sourceType": self.source_type,
            "data": self.data,
            "index": self.index,
        })
    
    @classmethod
    def from_json(cls, json_str: str) -> "DragData":
        data = json.loads(json_str)
        return cls(
            source_id=data["sourceId"],
            source_type=data["sourceType"],
            data=data.get("data"),
            index=data.get("index", 0),
        )


@dataclass
class DropZone:
    """Drop zone configuration."""
    id: str
    accept: List[str] = field(default_factory=lambda: ["*"])
    max_items: int = 0
    on_drop: Optional[Callable] = None
    on_drag_over: Optional[Callable] = None
    on_drag_enter: Optional[Callable] = None
    on_drag_leave: Optional[Callable] = None


@dataclass
class DragOptions:
    """Drag options."""
    enabled: bool = True
    ghost: bool = True
    handle: bool = False
    axis: str = "both"
    grid: Optional[int] = None
    delay: int = 0
    animation: int = 150
    data: Optional[Dict[str, Any]] = None


class Draggable:
    """Make an element draggable."""
    
    def __init__(self, element_id: str, options: DragOptions = None):
        self.element_id = element_id
        self.options = options or DragOptions()
        self._on_drag_start: Optional[Callable] = None
        self._on_drag_end: Optional[Callable] = None
    
    def on_drag_start(self, callback: Callable) -> "Draggable":
        """Set drag start handler."""
        self._on_drag_start = callback
        return self
    
    def on_drag_end(self, callback: Callable) -> "Draggable":
        """Set drag end handler."""
        self._on_drag_end = callback
        return self
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "elementId": self.element_id,
            "options": {
                "enabled": self.options.enabled,
                "ghost": self.options.ghost,
                "handle": self.options.handle,
                "axis": self.options.axis,
                "grid": self.options.grid,
                "delay": self.options.delay,
                "animation": self.options.animation,
                "data": self.options.data,
            },
        }
    
    def generate_js_code(self) -> str:
        """Generate JavaScript for draggable."""
        opts = self.options
        return f"""
        // Draggable: {self.element_id}
        (function() {{
            const el = document.getElementById('{self.element_id}');
            if (!el) return;
            
            el.setAttribute('draggable', '{str(opts.enabled).lower()}');
            
            el.addEventListener('dragstart', (e) => {{
                e.dataTransfer.effectAllowed = 'move';
                e.dataTransfer.setData('text/plain', el.id);
                
                if ({str(opts.ghost).lower()}) {{
                    el.style.opacity = '0.5';
                }}
                
                {f'el.style.animation = "none";' if opts.animation else ''}
            }});
            
            el.addEventListener('dragend', (e) => {{
                el.style.opacity = '1';
                el.style.animation = '';
            }});
        }})();
        """


class Droppable:
    """Make an element a drop zone."""
    
    def __init__(self, element_id: str, zone: DropZone = None):
        self.element_id = element_id
        self.zone = zone or DropZone(id=element_id)
        self._on_drop: Optional[Callable] = None
        self._on_drag_over: Optional[Callable] = None
        self._on_drag_enter: Optional[Callable] = None
        self._on_drag_leave: Optional[Callable] = None
    
    def on_drop(self, callback: Callable) -> "Droppable":
        """Set drop handler."""
        self._on_drop = callback
        return self
    
    def on_drag_over(self, callback: Callable) -> "Droppable":
        """Set drag over handler."""
        self._on_drag_over = callback
        return self
    
    def on_drag_enter(self, callback: Callable) -> "Droppable":
        """Set drag enter handler."""
        self._on_drag_enter = callback
        return self
    
    def on_drag_leave(self, callback: Callable) -> "Droppable":
        """Set drag leave handler."""
        self._on_drag_leave = callback
        return self
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "elementId": self.element_id,
            "zone": {
                "id": self.zone.id,
                "accept": self.zone.accept,
                "maxItems": self.zone.max_items,
            },
        }
    
    def generate_js_code(self) -> str:
        """Generate JavaScript for droppable."""
        zone = self.zone
        return f"""
        // Droppable: {self.element_id}
        (function() {{
            const el = document.getElementById('{self.element_id}');
            if (!el) return;
            
            el.classList.add('droppable-zone');
            
            el.addEventListener('dragover', (e) => {{
                e.preventDefault();
                e.dataTransfer.dropEffect = 'move';
                el.classList.add('drag-over');
            }});
            
            el.addEventListener('dragenter', (e) => {{
                e.preventDefault();
                el.classList.add('drag-active');
            }});
            
            el.addEventListener('dragleave', (e) => {{
                el.classList.remove('drag-active');
                el.classList.remove('drag-over');
            }});
            
            el.addEventListener('drop', (e) => {{
                e.preventDefault();
                el.classList.remove('drag-active');
                el.classList.remove('drag-over');
                
                const sourceId = e.dataTransfer.getData('text/plain');
                const source = document.getElementById(sourceId);
                
                if (source) {{
                    el.appendChild(source);
                }}
            }});
        }})();
        """


class Sortable:
    """Create a sortable list."""
    
    def __init__(self, container_id: str, items: List[str] = None, options: DragOptions = None):
        self.container_id = container_id
        self.items = items or []
        self.options = options or DragOptions()
        self._on_sort: Optional[Callable] = None
    
    def on_sort(self, callback: Callable) -> "Sortable":
        """Set sort handler."""
        self._on_sort = callback
        return self
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "containerId": self.container_id,
            "items": self.items,
            "options": {
                "enabled": self.options.enabled,
                "ghost": self.options.ghost,
                "axis": self.options.axis,
                "animation": self.options.animation,
            },
        }
    
    def generate_js_code(self) -> str:
        """Generate JavaScript for sortable."""
        items_json = json.dumps(self.items)
        return f"""
        // Sortable: {self.container_id}
        (function() {{
            const container = document.getElementById('{self.container_id}');
            if (!container) return;
            
            const items = {items_json};
            let draggedItem = null;
            let draggedIndex = -1;
            
            items.forEach(itemId => {{
                const el = document.getElementById(itemId);
                if (!el) return;
                
                el.setAttribute('draggable', 'true');
                
                el.addEventListener('dragstart', (e) => {{
                    draggedItem = el;
                    draggedIndex = Array.from(container.children).indexOf(el);
                    e.dataTransfer.effectAllowed = 'move';
                    el.style.opacity = '0.5';
                }});
                
                el.addEventListener('dragend', (e) => {{
                    el.style.opacity = '1';
                    container.querySelectorAll('.sortable-placeholder').forEach(p => p.remove());
                }});
                
                el.addEventListener('dragover', (e) => {{
                    e.preventDefault();
                    e.dataTransfer.dropEffect = 'move';
                    
                    if (draggedItem && draggedItem !== el) {{
                        const rect = el.getBoundingClientRect();
                        const midY = rect.top + rect.height / 2;
                        
                        if (e.clientY < midY) {{
                            container.insertBefore(draggedItem, el);
                        }} else {{
                            container.insertBefore(draggedItem, el.nextSibling);
                        }}
                    }}
                }});
            }});
            
            container.addEventListener('drop', (e) => {{
                e.preventDefault();
                const newOrder = Array.from(container.children).map(el => el.id);
                console.log('New order:', newOrder);
            }});
        }})();
        """


class DragDropManager:
    """Manager for drag and drop operations."""
    
    def __init__(self):
        self._draggables: Dict[str, Draggable] = {}
        self._droppables: Dict[str, Droppable] = {}
        self._sortables: Dict[str, Sortable] = {}
        self._data: Dict[str, Any] = {}
    
    def draggable(self, element_id: str, options: DragOptions = None) -> Draggable:
        """Create a draggable element."""
        drag = Draggable(element_id, options)
        self._draggables[element_id] = drag
        return drag
    
    def droppable(self, element_id: str, zone: DropZone = None) -> Droppable:
        """Create a drop zone."""
        drop = Droppable(element_id, zone)
        self._droppables[element_id] = drop
        return drop
    
    def sortable(self, container_id: str, items: List[str] = None, options: DragOptions = None) -> Sortable:
        """Create a sortable list."""
        sort = Sortable(container_id, items, options)
        self._sortables[container_id] = sort
        return sort
    
    def set_data(self, key: str, value: Any):
        """Set shared data."""
        self._data[key] = value
    
    def get_data(self, key: str) -> Any:
        """Get shared data."""
        return self._data.get(key)
    
    def generate_js_code(self) -> str:
        """Generate all JavaScript code."""
        codes = []
        
        for drag in self._draggables.values():
            codes.append(drag.generate_js_code())
        
        for drop in self._droppables.values():
            codes.append(drop.generate_js_code())
        
        for sort in self._sortables.values():
            codes.append(sort.generate_js_code())
        
        return "\n".join(codes)
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "draggables": {k: v.to_dict() for k, v in self._draggables.items()},
            "droppables": {k: v.to_dict() for k, v in self._droppables.items()},
            "sortables": {k: v.to_dict() for k, v in self._sortables.items()},
        }


def create_drag_drop() -> DragDropManager:
    """Create a drag-drop manager."""
    return DragDropManager()


def make_draggable(element_id: str, options: DragOptions = None) -> Draggable:
    """Make an element draggable."""
    return Draggable(element_id, options)


def make_droppable(element_id: str, zone: DropZone = None) -> Droppable:
    """Make an element a drop zone."""
    return Droppable(element_id, zone)


def make_sortable(container_id: str, items: List[str] = None, options: DragOptions = None) -> Sortable:
    """Create a sortable list."""
    return Sortable(container_id, items, options)


DRAG_DROP_CSS = """
.draggable {
    cursor: grab;
    user-select: none;
}

.draggable:active {
    cursor: grabbing;
}

.draggable.ghosting {
    opacity: 0.5;
}

.droppable-zone {
    min-height: 100px;
    border: 2px dashed transparent;
    border-radius: 0.5rem;
    transition: all 0.2s ease;
}

.droppable-zone.drag-over {
    border-color: #3b82f6;
    background-color: #eff6ff;
}

.droppable-zone.drag-active {
    border-color: #2563eb;
    background-color: #dbeafe;
}

.sortable-item {
    padding: 0.75rem 1rem;
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 0.375rem;
    margin-bottom: 0.5rem;
    cursor: grab;
    transition: all 0.2s ease;
}

.sortable-item:hover {
    border-color: #d1d5db;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.sortable-item.dragging {
    opacity: 0.5;
    background: #f3f4f6;
}

.sortable-placeholder {
    border: 2px dashed #d1d5db;
    background: #f9fafb;
    border-radius: 0.375rem;
    margin-bottom: 0.5rem;
}
"""
