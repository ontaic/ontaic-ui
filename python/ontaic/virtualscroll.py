"""Virtual scrolling for large lists."""
from typing import Any, Callable, Dict, List, Optional
from dataclasses import dataclass, field


@dataclass
class VirtualScrollOptions:
    """Virtual scroll options."""
    item_height: int = 40
    container_height: int = 400
    overscan: int = 5
    threshold: int = 100
    horizontal: bool = False
    scroll_debounce: int = 16


class VirtualList:
    """Virtual list component for rendering large datasets."""
    
    def __init__(self, items: List[Any] = None, options: VirtualScrollOptions = None):
        self.items = items or []
        self.options = options or VirtualScrollOptions()
        self._on_scroll: Optional[Callable] = None
        self._on_render_item: Optional[Callable] = None
        self._visible_start: int = 0
        self._visible_end: int = 0
    
    def set_items(self, items: List[Any]):
        """Set the items list."""
        self.items = items
    
    def on_scroll(self, callback: Callable) -> "VirtualList":
        """Set scroll handler."""
        self._on_scroll = callback
        return self
    
    def render_item(self, callback: Callable) -> "VirtualList":
        """Set item renderer."""
        self._on_render_item = callback
        return self
    
    def get_visible_range(self, scroll_position: int = 0) -> tuple:
        """Get visible item range."""
        start = max(0, scroll_position // self.options.item_height - self.options.overscan)
        visible_count = self.options.container_height // self.options.item_height
        end = min(len(self.items), start + visible_count + self.options.overscan * 2)
        return start, end
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "items": self.items,
            "options": {
                "itemHeight": self.options.item_height,
                "containerHeight": self.options.container_height,
                "overscan": self.options.overscan,
                "threshold": self.options.threshold,
                "horizontal": self.options.horizontal,
            },
            "totalItems": len(self.items),
            "totalHeight": len(self.items) * self.options.item_height,
        }
    
    def generate_js_code(self) -> str:
        """Generate JavaScript for virtual list."""
        items_json = str(self.items).replace("'", '"')
        opts = self.options
        return f"""
        // Virtual List
        (function() {{
            const container = document.getElementById('virtual-list-container');
            if (!container) return;
            
            const items = {items_json};
            const itemHeight = {opts.item_height};
            const containerHeight = {opts.container_height};
            const overscan = {opts.overscan};
            
            const totalHeight = items.length * itemHeight;
            const visibleCount = Math.ceil(containerHeight / itemHeight);
            
            container.style.height = containerHeight + 'px';
            container.style.overflow = 'auto';
            container.style.position = 'relative';
            
            const viewport = document.createElement('div');
            viewport.style.height = totalHeight + 'px';
            viewport.style.position = 'relative';
            container.appendChild(viewport);
            
            let renderedItems = new Map();
            
            function renderVisibleItems() {{
                const scrollTop = container.scrollTop;
                const startIndex = Math.max(0, Math.floor(scrollTop / itemHeight) - overscan);
                const endIndex = Math.min(items.length, startIndex + visibleCount + overscan * 2);
                
                // Remove items that are no longer visible
                renderedItems.forEach((el, index) => {{
                    if (index < startIndex || index >= endIndex) {{
                        el.remove();
                        renderedItems.delete(index);
                    }}
                }});
                
                // Add new visible items
                for (let i = startIndex; i < endIndex; i++) {{
                    if (!renderedItems.has(i)) {{
                        const item = document.createElement('div');
                        item.className = 'virtual-list-item';
                        item.style.position = 'absolute';
                        item.style.top = (i * itemHeight) + 'px';
                        item.style.left = '0';
                        item.style.right = '0';
                        item.style.height = itemHeight + 'px';
                        item.textContent = items[i];
                        item.dataset.index = i;
                        viewport.appendChild(item);
                        renderedItems.set(i, item);
                    }}
                }}
            }}
            
            container.addEventListener('scroll', () => {{
                requestAnimationFrame(renderVisibleItems);
            }});
            
            renderVisibleItems();
        }})();
        """


class VirtualGrid:
    """Virtual grid component for rendering large datasets in a grid."""
    
    def __init__(self, items: List[Any] = None, columns: int = 3, options: VirtualScrollOptions = None):
        self.items = items or []
        self.columns = columns
        self.options = options or VirtualScrollOptions()
    
    def set_items(self, items: List[Any]):
        """Set the items list."""
        self.items = items
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        rows = (len(self.items) + self.columns - 1) // self.columns
        return {
            "items": self.items,
            "columns": self.columns,
            "options": {
                "itemHeight": self.options.item_height,
                "containerHeight": self.options.container_height,
                "overscan": self.options.overscan,
            },
            "totalRows": rows,
            "totalHeight": rows * self.options.item_height,
        }
    
    def generate_js_code(self) -> str:
        """Generate JavaScript for virtual grid."""
        items_json = str(self.items).replace("'", '"')
        opts = self.options
        columns = self.columns
        return f"""
        // Virtual Grid
        (function() {{
            const container = document.getElementById('virtual-grid-container');
            if (!container) return;
            
            const items = {items_json};
            const columns = {columns};
            const itemHeight = {opts.item_height};
            const containerHeight = {opts.container_height};
            const overscan = {opts.overscan};
            
            const rows = Math.ceil(items.length / columns);
            const totalHeight = rows * itemHeight;
            const visibleRows = Math.ceil(containerHeight / itemHeight);
            
            container.style.height = containerHeight + 'px';
            container.style.overflow = 'auto';
            container.style.position = 'relative';
            
            const viewport = document.createElement('div');
            viewport.style.height = totalHeight + 'px';
            viewport.style.position = 'relative';
            container.appendChild(viewport);
            
            let renderedItems = new Map();
            
            function renderVisibleItems() {{
                const scrollTop = container.scrollTop;
                const startRow = Math.max(0, Math.floor(scrollTop / itemHeight) - overscan);
                const endRow = Math.min(rows, startRow + visibleRows + overscan * 2);
                
                // Remove items that are no longer visible
                renderedItems.forEach((el, index) => {{
                    const row = Math.floor(index / columns);
                    if (row < startRow || row >= endRow) {{
                        el.remove();
                        renderedItems.delete(index);
                    }}
                }});
                
                // Add new visible items
                for (let row = startRow; row < endRow; row++) {{
                    for (let col = 0; col < columns; col++) {{
                        const index = row * columns + col;
                        if (index < items.length && !renderedItems.has(index)) {{
                            const item = document.createElement('div');
                            item.className = 'virtual-grid-item';
                            item.style.position = 'absolute';
                            item.style.top = (row * itemHeight) + 'px';
                            item.style.left = (col * (100 / columns)) + '%';
                            item.style.width = (100 / columns) + '%';
                            item.style.height = itemHeight + 'px';
                            item.style.boxSizing = 'border-box';
                            item.textContent = items[index];
                            item.dataset.index = index;
                            viewport.appendChild(item);
                            renderedItems.set(index, item);
                        }}
                    }}
                }}
            }}
            
            container.addEventListener('scroll', () => {{
                requestAnimationFrame(renderVisibleItems);
            }});
            
            renderVisibleItems();
        }})();
        """


def create_virtual_list(items: List[Any] = None, options: VirtualScrollOptions = None) -> VirtualList:
    """Create a virtual list."""
    return VirtualList(items, options)


def create_virtual_grid(items: List[Any] = None, columns: int = 3, options: VirtualScrollOptions = None) -> VirtualGrid:
    """Create a virtual grid."""
    return VirtualGrid(items, columns, options)


VIRTUAL_SCROLL_CSS = """
.virtual-list-container {
    overflow: auto;
    position: relative;
}

.virtual-list-item {
    position: absolute;
    left: 0;
    right: 0;
    padding: 0.5rem 1rem;
    border-bottom: 1px solid #e5e7eb;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.virtual-list-item:hover {
    background-color: #f9fafb;
}

.virtual-grid-container {
    overflow: auto;
    position: relative;
}

.virtual-grid-item {
    padding: 0.5rem;
    box-sizing: border-box;
}

.virtual-grid-item:hover {
    background-color: #f9fafb;
}
"""
