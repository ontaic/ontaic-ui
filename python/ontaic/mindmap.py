"""Mind map component for visualizing hierarchical information."""
from typing import Any, Callable, Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum


class LayoutType(str, Enum):
    """Mind map layout type."""
    RADIAL = "radial"
    TREE = "tree"
    ORGANIC = "organic"
    FORCE = "force"


class NodeShape(str, Enum):
    """Node shape."""
    ROUNDED = "rounded"
    CIRCLE = "circle"
    RECTANGLE = "rectangle"
    DASHED = "dashed"


@dataclass
class MindNode:
    """A node in the mind map."""
    id: str
    label: str
    parent_id: str = ""
    color: str = "#3b82f6"
    text_color: str = "#ffffff"
    border_color: str = "#2563eb"
    border_width: int = 2
    size: int = 80
    icon: str = ""
    note: str = ""
    collapsed: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)
    children: List["MindNode"] = field(default_factory=list)
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "label": self.label,
            "parentId": self.parent_id,
            "color": self.color,
            "textColor": self.text_color,
            "borderColor": self.border_color,
            "borderWidth": self.border_width,
            "size": self.size,
            "icon": self.icon,
            "note": self.note,
            "collapsed": self.collapsed,
        }


class MindMap:
    """Mind map component for visualizing hierarchical information."""
    
    def __init__(self):
        self._nodes: List[MindNode] = []
        self._layout: LayoutType = LayoutType.RADIAL
        self._show_controls: bool = True
        self._show_minimap: bool = True
        self._show_toolbar: bool = True
        self._editable: bool = True
        self._draggable: bool = True
        self._center_text: str = "Main Topic"
        self._center_color: str = "#8b5cf6"
        self._width: int = 1000
        self._height: int = 700
        self._on_node_click: Optional[Callable] = None
        self._on_node_add: Optional[Callable] = None
        self._on_node_delete: Optional[Callable] = None
        self._on_node_edit: Optional[Callable] = None
        self._class_name: str = ""
        self._label: str = ""
        self._help_text: str = ""
    
    def add_node(self, node: MindNode) -> "MindMap":
        """Add a node."""
        self._nodes.append(node)
        return self
    
    def node(self, id: str, label: str, parent_id: str = "", **kwargs) -> "MindMap":
        """Add a node."""
        n = MindNode(id=id, label=label, parent_id=parent_id, **kwargs)
        self._nodes.append(n)
        return self
    
    def add_nodes(self, nodes: List[MindNode]) -> "MindMap":
        """Add multiple nodes."""
        self._nodes.extend(nodes)
        return self
    
    def layout(self, layout: LayoutType) -> "MindMap":
        """Set layout type."""
        self._layout = layout
        return self
    
    def center_text(self, text: str) -> "MindMap":
        """Set center text."""
        self._center_text = text
        return self
    
    def center_color(self, color: str) -> "MindMap":
        """Set center color."""
        self._center_color = color
        return self
    
    def show_controls(self, show: bool = True) -> "MindMap":
        """Toggle controls."""
        self._show_controls = show
        return self
    
    def show_minimap(self, show: bool = True) -> "MindMap":
        """Toggle minimap."""
        self._show_minimap = show
        return self
    
    def show_toolbar(self, show: bool = True) -> "MindMap":
        """Toggle toolbar."""
        self._show_toolbar = show
        return self
    
    def editable(self, editable: bool = True) -> "MindMap":
        """Set editable."""
        self._editable = editable
        return self
    
    def size(self, width: int, height: int) -> "MindMap":
        """Set size."""
        self._width = width
        self._height = height
        return self
    
    def on_node_click(self, callback: Callable) -> "MindMap":
        """Set node click handler."""
        self._on_node_click = callback
        return self
    
    def on_node_add(self, callback: Callable) -> "MindMap":
        """Set node add handler."""
        self._on_node_add = callback
        return self
    
    def on_node_delete(self, callback: Callable) -> "MindMap":
        """Set node delete handler."""
        self._on_node_delete = callback
        return self
    
    def class_name(self, class_name: str) -> "MindMap":
        """Set CSS class."""
        self._class_name = class_name
        return self
    
    def label(self, label: str) -> "MindMap":
        """Set label."""
        self._label = label
        return self
    
    def help_text(self, text: str) -> "MindMap":
        """Set help text."""
        self._help_text = text
        return self
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "nodes": [n.to_dict() for n in self._nodes],
            "layout": self._layout.value,
            "showControls": self._show_controls,
            "showMinimap": self._show_minimap,
            "showToolbar": self._show_toolbar,
            "editable": self._editable,
            "centerText": self._center_text,
            "centerColor": self._center_color,
            "width": self._width,
            "height": self._height,
        }
    
    def to_html(self) -> str:
        """Generate HTML."""
        label_html = f'<h3 class="mindmap-label">{self._label}</h3>' if self._label else ""
        help_html = f'<p class="mindmap-help">{self._help_text}</p>' if self._help_text else ""
        class_attr = f" {self._class_name}" if self._class_name else ""
        
        # Toolbar
        toolbar_html = ""
        if self._show_toolbar:
            toolbar_html = f'''<div class="mindmap-toolbar">
                <button type="button" class="mindmap-tool-btn" data-action="add">+ Add Topic</button>
                <button type="button" class="mindmap-tool-btn" data-action="collapse">Collapse</button>
                <button type="button" class="mindmap-tool-btn" data-action="expand">Expand All</button>
                <button type="button" class="mindmap-tool-btn" data-action="center">Center</button>
                <button type="button" class="mindmap-tool-btn" data-action="export">Export</button>
            </div>'''
        
        # Minimap
        minimap_html = ""
        if self._show_minimap:
            minimap_html = '<div class="mindmap-minimap"><canvas class="mindmap-minimap-canvas" width="150" height="100"></canvas></div>'
        
        return f'''<div class="mindmap-container{class_attr}">
            {label_html}
            {toolbar_html}
            <div class="mindmap-main">
                <canvas id="mindmap-canvas" width="{self._width}" height="{self._height}"></canvas>
                {minimap_html}
            </div>
            {help_html}
        </div>'''
    
    def generate_js_code(self) -> str:
        """Generate JavaScript."""
        config = self.to_dict()
        nodes_json = str(config["nodes"]).replace("'", '"')
        
        return f"""
        // Mind Map
        (function() {{
            const config = {{
                nodes: {nodes_json},
                layout: "{config['layout']}",
                centerText: "{config['centerText']}",
                centerColor: "{config['centerColor']}",
                editable: {str(config['editable']).lower()},
            }};
            
            const canvas = document.getElementById('mindmap-canvas');
            if (!canvas) return;
            
            const ctx = canvas.getContext('2d');
            const centerX = canvas.width / 2;
            const centerY = canvas.height / 2;
            
            // Draw background
            ctx.fillStyle = '#f9fafb';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            
            // Draw center node
            ctx.fillStyle = config.centerColor;
            ctx.beginPath();
            ctx.arc(centerX, centerY, 50, 0, Math.PI * 2);
            ctx.fill();
            
            ctx.fillStyle = '#ffffff';
            ctx.font = 'bold 14px system-ui';
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            ctx.fillText(config.centerText, centerX, centerY);
            
            // Calculate node positions
            const nodes = config.nodes;
            const angleStep = (Math.PI * 2) / Math.max(nodes.length, 1);
            const radius = Math.min(canvas.width, canvas.height) * 0.3;
            
            // Draw connections and nodes
            nodes.forEach((node, i) => {{
                const angle = i * angleStep - Math.PI / 2;
                const x = centerX + Math.cos(angle) * radius;
                const y = centerY + Math.sin(angle) * radius;
                
                // Draw connection
                ctx.strokeStyle = '#d1d5db';
                ctx.lineWidth = 2;
                ctx.beginPath();
                ctx.moveTo(centerX, centerY);
                ctx.lineTo(x, y);
                ctx.stroke();
                
                // Draw node
                ctx.fillStyle = node.color;
                ctx.beginPath();
                ctx.arc(x, y, node.size / 2, 0, Math.PI * 2);
                ctx.fill();
                
                ctx.strokeStyle = node.borderColor;
                ctx.lineWidth = node.borderWidth;
                ctx.stroke();
                
                // Draw label
                ctx.fillStyle = node.textColor;
                ctx.font = '12px system-ui';
                ctx.textAlign = 'center';
                ctx.textBaseline = 'middle';
                
                const words = node.label.split(' ');
                const lineHeight = 16;
                const startY = y - ((words.length - 1) * lineHeight) / 2;
                
                words.forEach((word, j) => {{
                    ctx.fillText(word, x, startY + j * lineHeight);
                }});
                
                // Draw children
                if (node.children && node.children.length > 0) {{
                    const childAngleStep = (Math.PI * 0.5) / Math.max(node.children.length - 1, 1);
                    const childRadius = 120;
                    
                    node.children.forEach((child, k) => {{
                        const childAngle = angle - Math.PI / 4 + k * childAngleStep;
                        const childX = x + Math.cos(childAngle) * childRadius;
                        const childY = y + Math.sin(childAngle) * childRadius;
                        
                        ctx.strokeStyle = '#e5e7eb';
                        ctx.lineWidth = 1;
                        ctx.beginPath();
                        ctx.moveTo(x, y);
                        ctx.lineTo(childX, childY);
                        ctx.stroke();
                        
                        ctx.fillStyle = child.color;
                        ctx.beginPath();
                        ctx.arc(childX, childY, child.size / 2, 0, Math.PI * 2);
                        ctx.fill();
                        
                        ctx.fillStyle = child.textColor;
                        ctx.font = '10px system-ui';
                        ctx.fillText(child.label, childX, childY);
                    }});
                }}
            }});
            
            // Click handler
            canvas.addEventListener('click', (e) => {{
                const rect = canvas.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;
                
                nodes.forEach((node, i) => {{
                    const angle = i * angleStep - Math.PI / 2;
                    const nx = centerX + Math.cos(angle) * radius;
                    const ny = centerY + Math.sin(angle) * radius;
                    const dist = Math.sqrt((x - nx) ** 2 + (y - ny) ** 2);
                    
                    if (dist < node.size / 2) {{
                        console.log('Clicked:', node.label);
                    }}
                }});
            }});
            
            // Toolbar
            document.querySelectorAll('.mindmap-tool-btn').forEach(btn => {{
                btn.addEventListener('click', () => {{
                    console.log('Action:', btn.dataset.action);
                }});
            }});
        }})();
        """


def create_mind_map() -> MindMap:
    """Create a mind map."""
    return MindMap()


def mind_node(id: str, label: str, **kwargs) -> MindNode:
    """Create a mind map node."""
    return MindNode(id=id, label=label, **kwargs)


MIND_MAP_CSS = """
.mindmap-container {
    border: 1px solid #e5e7eb;
    border-radius: 0.5rem;
    overflow: hidden;
    background: white;
}

.mindmap-label {
    padding: 0.75rem 1rem;
    margin: 0;
    font-size: 1.125rem;
    font-weight: 600;
    color: #111827;
    border-bottom: 1px solid #e5e7eb;
}

.mindmap-toolbar {
    display: flex;
    gap: 0.5rem;
    padding: 0.5rem 1rem;
    background: #f9fafb;
    border-bottom: 1px solid #e5e7eb;
}

.mindmap-tool-btn {
    padding: 0.375rem 0.75rem;
    border: 1px solid #d1d5db;
    background: white;
    border-radius: 0.375rem;
    cursor: pointer;
    font-size: 0.875rem;
}

.mindmap-tool-btn:hover {
    background: #f3f4f6;
}

.mindmap-main {
    position: relative;
    overflow: hidden;
    background: #f9fafb;
}

.mindmap-main canvas {
    display: block;
}

.mindmap-minimap {
    position: absolute;
    bottom: 1rem;
    right: 1rem;
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 0.375rem;
    padding: 0.25rem;
}

.mindmap-minimap-canvas {
    display: block;
}

.mindmap-help {
    padding: 0.75rem 1rem;
    margin: 0;
    font-size: 0.875rem;
    color: #6b7280;
    border-top: 1px solid #e5e7eb;
}
"""
