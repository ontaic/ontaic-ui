"""Flow chart component for building visual workflows."""
from typing import Any, Callable, Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum


class NodeShape(str, Enum):
    """Node shape."""
    RECTANGLE = "rectangle"
    ROUNDED = "rounded"
    CIRCLE = "circle"
    DIAMOND = "diamond"
    HEXAGON = "hexagon"
    PARALLELOGRAM = "parallelogram"
    CYLINDER = "cylinder"
    DOCUMENT = "document"
    TERMINAL = "terminal"


class NodeStyle(str, Enum):
    """Node style."""
    FILLED = "filled"
    OUTLINED = "outlined"
    SHADOWED = "shadowed"
    GRADIENT = "gradient"


class EdgeType(str, Enum):
    """Edge type."""
    STRAIGHT = "straight"
    CURVED = "curved"
    ORTHOGONAL = "orthogonal"
    DASHED = "dashed"
    DOTTED = "dotted"
    THICK = "thick"


class LayoutDirection(str, Enum):
    """Layout direction."""
    TOP_BOTTOM = "TB"
    BOTTOM_TOP = "BT"
    LEFT_RIGHT = "LR"
    RIGHT_LEFT = "RL"


@dataclass
class FlowNode:
    """A node in the flow chart."""
    id: str
    label: str
    shape: NodeShape = NodeShape.ROUNDED
    style: NodeStyle = NodeStyle.FILLED
    color: str = "#3b82f6"
    text_color: str = "#ffffff"
    border_color: str = "#2563eb"
    border_width: int = 1
    width: int = 140
    height: int = 60
    x: int = 0
    y: int = 0
    icon: str = ""
    tooltip: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "label": self.label,
            "shape": self.shape.value,
            "style": self.style.value,
            "color": self.color,
            "textColor": self.text_color,
            "borderColor": self.border_color,
            "borderWidth": self.border_width,
            "width": self.width,
            "height": self.height,
            "x": self.x,
            "y": self.y,
            "icon": self.icon,
            "tooltip": self.tooltip,
        }


@dataclass
class FlowEdge:
    """An edge connecting two nodes."""
    id: str
    source: str
    target: str
    label: str = ""
    edge_type: EdgeType = EdgeType.STRAIGHT
    color: str = "#6b7280"
    width: int = 2
    animated: bool = False
    marker_end: str = "arrow"
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "source": self.source,
            "target": self.target,
            "label": self.label,
            "type": self.edge_type.value,
            "color": self.color,
            "width": self.width,
            "animated": self.animated,
            "markerEnd": self.marker_end,
        }


class FlowChart:
    """Flow chart component for building visual workflows."""
    
    def __init__(self):
        self._nodes: List[FlowNode] = []
        self._edges: List[FlowEdge] = []
        self._layout: LayoutDirection = LayoutDirection.TOP_BOTTOM
        self._show_controls: bool = True
        self._show_minimap: bool = True
        self._show_toolbar: bool = True
        self._editable: bool = True
        self._draggable: bool = True
        self._selectable: bool = True
        self._zoomable: bool = True
        self._pannable: bool = True
        self._width: int = 1000
        self._height: int = 700
        self._background_color: str = "#f9fafb"
        self._grid_size: int = 20
        self._show_grid: bool = True
        self._on_node_click: Optional[Callable] = None
        self._on_edge_click: Optional[Callable] = None
        self._on_node_drag: Optional[Callable] = None
        self._on_connect: Optional[Callable] = None
        self._class_name: str = ""
        self._label: str = ""
        self._help_text: str = ""
    
    def add_node(self, node: FlowNode) -> "FlowChart":
        """Add a node."""
        self._nodes.append(node)
        return self
    
    def node(self, id: str, label: str, **kwargs) -> "FlowChart":
        """Add a node."""
        n = FlowNode(id=id, label=label, **kwargs)
        self._nodes.append(n)
        return self
    
    def add_edge(self, edge: FlowEdge) -> "FlowChart":
        """Add an edge."""
        self._edges.append(edge)
        return self
    
    def edge(self, source: str, target: str, label: str = "", **kwargs) -> "FlowChart":
        """Add an edge."""
        id = f"e_{source}_{target}"
        e = FlowEdge(id=id, source=source, target=target, label=label, **kwargs)
        self._edges.append(e)
        return self
    
    def layout(self, direction: LayoutDirection) -> "FlowChart":
        """Set layout direction."""
        self._layout = direction
        return self
    
    def show_controls(self, show: bool = True) -> "FlowChart":
        """Toggle controls."""
        self._show_controls = show
        return self
    
    def show_minimap(self, show: bool = True) -> "FlowChart":
        """Toggle minimap."""
        self._show_minimap = show
        return self
    
    def show_toolbar(self, show: bool = True) -> "FlowChart":
        """Toggle toolbar."""
        self._show_toolbar = show
        return self
    
    def editable(self, editable: bool = True) -> "FlowChart":
        """Set editable."""
        self._editable = editable
        return self
    
    def size(self, width: int, height: int) -> "FlowChart":
        """Set size."""
        self._width = width
        self._height = height
        return self
    
    def background_color(self, color: str) -> "FlowChart":
        """Set background color."""
        self._background_color = color
        return self
    
    def show_grid(self, show: bool = True) -> "FlowChart":
        """Toggle grid."""
        self._show_grid = show
        return self
    
    def on_node_click(self, callback: Callable) -> "FlowChart":
        """Set node click handler."""
        self._on_node_click = callback
        return self
    
    def on_edge_click(self, callback: Callable) -> "FlowChart":
        """Set edge click handler."""
        self._on_edge_click = callback
        return self
    
    def on_connect(self, callback: Callable) -> "FlowChart":
        """Set connection handler."""
        self._on_connect = callback
        return self
    
    def class_name(self, class_name: str) -> "FlowChart":
        """Set CSS class."""
        self._class_name = class_name
        return self
    
    def label(self, label: str) -> "FlowChart":
        """Set label."""
        self._label = label
        return self
    
    def help_text(self, text: str) -> "FlowChart":
        """Set help text."""
        self._help_text = text
        return self
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "nodes": [n.to_dict() for n in self._nodes],
            "edges": [e.to_dict() for e in self._edges],
            "layout": self._layout.value,
            "showControls": self._show_controls,
            "showMinimap": self._show_minimap,
            "showToolbar": self._show_toolbar,
            "editable": self._editable,
            "draggable": self._draggable,
            "selectable": self._selectable,
            "width": self._width,
            "height": self._height,
            "backgroundColor": self._background_color,
            "gridSize": self._grid_size,
            "showGrid": self._show_grid,
        }
    
    def to_html(self) -> str:
        """Generate HTML."""
        label_html = f'<h3 class="flowchart-label">{self._label}</h3>' if self._label else ""
        help_html = f'<p class="flowchart-help">{self._help_text}</p>' if self._help_text else ""
        class_attr = f" {self._class_name}" if self._class_name else ""
        
        # Toolbar
        toolbar_html = ""
        if self._show_toolbar:
            toolbar_html = f'''<div class="flowchart-toolbar">
                <button type="button" class="flowchart-tool-btn" data-action="add-node">+ Node</button>
                <button type="button" class="flowchart-tool-btn" data-action="add-edge">+ Edge</button>
                <button type="button" class="flowchart-tool-btn" data-action="delete">Delete</button>
                <button type="button" class="flowchart-tool-btn" data-action="zoom-in">Zoom In</button>
                <button type="button" class="flowchart-tool-btn" data-action="zoom-out">Zoom Out</button>
                <button type="button" class="flowchart-tool-btn" data-action="fit">Fit</button>
                <button type="button" class="flowchart-tool-btn" data-action="export">Export</button>
            </div>'''
        
        # Minimap
        minimap_html = ""
        if self._show_minimap:
            minimap_html = '<div class="flowchart-minimap"><canvas class="flowchart-minimap-canvas" width="150" height="100"></canvas></div>'
        
        return f'''<div class="flowchart-container{class_attr}">
            {label_html}
            {toolbar_html}
            <div class="flowchart-main">
                <svg id="flowchart-svg" width="{self._width}" height="{self._height}" viewBox="0 0 {self._width} {self._height}">
                    <defs>
                        <marker id="arrowhead" viewBox="0 0 10 7" refX="10" refY="3.5" markerWidth="10" markerHeight="7" orient="auto">
                            <polygon points="0 0, 10 3.5, 0 7" fill="#6b7280"/>
                        </marker>
                    </defs>
                </svg>
                {minimap_html}
            </div>
            {help_html}
        </div>'''
    
    def generate_js_code(self) -> str:
        """Generate JavaScript."""
        config = self.to_dict()
        nodes_json = str(config["nodes"]).replace("'", '"')
        edges_json = str(config["edges"]).replace("'", '"')
        
        return f"""
        // Flow Chart
        (function() {{
            const config = {{
                nodes: {nodes_json},
                edges: {edges_json},
                layout: "{config['layout']}",
                editable: {str(config['editable']).lower()},
                showGrid: {str(config['showGrid']).lower()},
                gridSize: {config['gridSize']},
                backgroundColor: "{config['backgroundColor']}",
            }};
            
            const svg = document.getElementById('flowchart-svg');
            if (!svg) return;
            
            let scale = 1;
            let translateX = 0;
            let translateY = 0;
            let selectedNode = null;
            
            // Draw grid
            function drawGrid() {{
                if (!config.showGrid) return;
                
                const gridSize = config.gridSize * scale;
                let gridHtml = '<pattern id="grid" width="' + gridSize + '" height="' + gridSize + '" patternUnits="userSpaceOnUse">';
                gridHtml += '<path d="M ' + gridSize + ' 0 L 0 0 0 ' + gridSize + '" fill="none" stroke="#e5e7eb" stroke-width="0.5"/>';
                gridHtml += '</pattern>';
                gridHtml += '<rect width="100%" height="100%" fill="url(#grid)"/>';
                
                const defs = svg.querySelector('defs');
                defs.insertAdjacentHTML('afterend', gridHtml);
            }}
            
            // Render nodes
            function renderNodes() {{
                let nodesHtml = '<g class="nodes">';
                
                config.nodes.forEach(node => {{
                    const x = node.x * scale + translateX;
                    const y = node.y * scale + translateY;
                    const w = node.width * scale;
                    const h = node.height * scale;
                    
                    let shapeHtml = '';
                    const rx = node.shape === 'rounded' ? 10 : (node.shape === 'circle' ? w / 2 : 0);
                    
                    if (node.shape === 'circle') {{
                        shapeHtml = '<circle cx="' + (x + w / 2) + '" cy="' + (y + h / 2) + '" r="' + (w / 2) + '"';
                    }} else if (node.shape === 'diamond') {{
                        const points = (x + w / 2) + ',' + y + ' ' + (x + w) + ',' + (y + h / 2) + ' ' + (x + w / 2) + ',' + (y + h) + ' ' + x + ',' + (y + h / 2);
                        shapeHtml = '<polygon points="' + points + '"';
                    }} else {{
                        shapeHtml = '<rect x="' + x + '" y="' + y + '" width="' + w + '" height="' + h + '" rx="' + rx + '"';
                    }}
                    
                    const fill = node.style === 'outlined' ? 'none' : node.color;
                    const stroke = node.borderColor;
                    const strokeWidth = node.borderWidth;
                    
                    nodesHtml += shapeHtml + ' fill="' + fill + '" stroke="' + stroke + '" stroke-width="' + strokeWidth + '" class="flowchart-node" data-id="' + node.id + '" style="cursor: pointer;"/>';
                    
                    // Label
                    nodesHtml += '<text x="' + (x + w / 2) + '" y="' + (y + h / 2) + '" text-anchor="middle" dominant-baseline="middle" fill="' + node.textColor + '" font-size="14" font-family="system-ui">' + (node.icon ? node.icon + ' ' : '') + node.label + '</text>';
                    
                    // Tooltip
                    if (node.tooltip) {{
                        nodesHtml += '<title>' + node.tooltip + '</title>';
                    }}
                }});
                
                nodesHtml += '</g>';
                svg.insertAdjacentHTML('beforeend', nodesHtml);
            }}
            
            // Render edges
            function renderEdges() {{
                let edgesHtml = '<g class="edges">';
                
                config.edges.forEach(edge => {{
                    const sourceNode = config.nodes.find(n => n.id === edge.source);
                    const targetNode = config.nodes.find(n => n.id === edge.target);
                    
                    if (!sourceNode || !targetNode) return;
                    
                    const sx = sourceNode.x * scale + translateX + (sourceNode.width * scale) / 2;
                    const sy = sourceNode.y * scale + translateY + (sourceNode.height * scale);
                    const tx = targetNode.x * scale + translateX + (targetNode.width * scale) / 2;
                    const ty = targetNode.y * scale + translateY;
                    
                    let path = '';
                    if (edge.type === 'curved') {{
                        const mx = (sx + tx) / 2;
                        const my = (sy + ty) / 2;
                        path = '<path d="M ' + sx + ' ' + sy + ' Q ' + mx + ' ' + (sy + 50) + ' ' + tx + ' ' + ty + '"';
                    }} else {{
                        path = '<path d="M ' + sx + ' ' + sy + ' L ' + tx + ' ' + ty + '"';
                    }}
                    
                    const strokeDash = edge.type === 'dashed' ? ' stroke-dasharray="5,5"' : (edge.type === 'dotted' ? ' stroke-dasharray="2,2"' : '');
                    const strokeWidth = edge.type === 'thick' ? 4 : edge.width;
                    
                    edgesHtml += path + ' fill="none" stroke="' + edge.color + '" stroke-width="' + strokeWidth + '"' + strokeDash + ' marker-end="url(#arrowhead)" class="flowchart-edge" data-id="' + edge.id + '" style="cursor: pointer;"/>';
                    
                    // Edge label
                    if (edge.label) {{
                        const lx = (sx + tx) / 2;
                        const ly = (sy + ty) / 2 - 10;
                        edgesHtml += '<text x="' + lx + '" y="' + ly + '" text-anchor="middle" fill="#374151" font-size="12" font-family="system-ui">' + edge.label + '</text>';
                    }}
                }});
                
                edgesHtml += '</g>';
                svg.insertAdjacentHTML('beforeend', edgesHtml);
            }}
            
            // Node click
            svg.addEventListener('click', (e) => {{
                const node = e.target.closest('.flowchart-node');
                if (node) {{
                    document.querySelectorAll('.flowchart-node').forEach(n => n.removeAttribute('data-selected'));
                    node.setAttribute('data-selected', 'true');
                    node.setAttribute('stroke-width', '3');
                    selectedNode = node.dataset.id;
                    console.log('Selected node:', selectedNode);
                }}
            }});
            
            // Toolbar
            document.querySelectorAll('.flowchart-tool-btn').forEach(btn => {{
                btn.addEventListener('click', () => {{
                    const action = btn.dataset.action;
                    console.log('Action:', action);
                    
                    if (action === 'zoom-in') {{
                        scale *= 1.2;
                        render();
                    }} else if (action === 'zoom-out') {{
                        scale *= 0.8;
                        render();
                    }} else if (action === 'fit') {{
                        scale = 1;
                        translateX = 0;
                        translateY = 0;
                        render();
                    }}
                }});
            }});
            
            function render() {{
                svg.innerHTML = '<defs><marker id="arrowhead" viewBox="0 0 10 7" refX="10" refY="3.5" markerWidth="10" markerHeight="7" orient="auto"><polygon points="0 0, 10 3.5, 0 7" fill="#6b7280"/></marker></defs>';
                renderNodes();
                renderEdges();
            }}
            
            drawGrid();
            renderNodes();
            renderEdges();
        }})();
        """


def create_flow_chart() -> FlowChart:
    """Create a flow chart."""
    return FlowChart()


def flow_node(id: str, label: str, **kwargs) -> FlowNode:
    """Create a flow node."""
    return FlowNode(id=id, label=label, **kwargs)


def flow_edge(source: str, target: str, label: str = "", **kwargs) -> FlowEdge:
    """Create a flow edge."""
    return FlowEdge(id=f"e_{source}_{target}", source=source, target=target, label=label, **kwargs)


FLOW_CHART_CSS = """
.flowchart-container {
    border: 1px solid #e5e7eb;
    border-radius: 0.5rem;
    overflow: hidden;
    background: white;
}

.flowchart-label {
    padding: 0.75rem 1rem;
    margin: 0;
    font-size: 1.125rem;
    font-weight: 600;
    color: #111827;
    border-bottom: 1px solid #e5e7eb;
}

.flowchart-toolbar {
    display: flex;
    gap: 0.5rem;
    padding: 0.5rem 1rem;
    background: #f9fafb;
    border-bottom: 1px solid #e5e7eb;
}

.flowchart-tool-btn {
    padding: 0.375rem 0.75rem;
    border: 1px solid #d1d5db;
    background: white;
    border-radius: 0.375rem;
    cursor: pointer;
    font-size: 0.875rem;
}

.flowchart-tool-btn:hover {
    background: #f3f4f6;
}

.flowchart-main {
    position: relative;
    overflow: auto;
    background: #f9fafb;
}

.flowchart-main svg {
    display: block;
}

.flowchart-minimap {
    position: absolute;
    bottom: 1rem;
    right: 1rem;
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 0.375rem;
    padding: 0.25rem;
}

.flowchart-minimap-canvas {
    display: block;
}

.flowchart-help {
    padding: 0.75rem 1rem;
    margin: 0;
    font-size: 0.875rem;
    color: #6b7280;
    border-top: 1px solid #e5e7eb;
}

.flowchart-node:hover {
    filter: brightness(1.1);
}

.flowchart-edge:hover {
    stroke-width: 3;
}
"""
