"""Tree view component for hierarchical data."""
from typing import Any, Callable, Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum


class TreeSelectionMode(str, Enum):
    """Tree selection modes."""
    NONE = "none"
    SINGLE = "single"
    MULTIPLE = "multiple"


@dataclass
class TreeNode:
    """Tree node."""
    id: str
    label: str
    icon: str = ""
    children: List["TreeNode"] = field(default_factory=list)
    expanded: bool = True
    selected: bool = False
    disabled: bool = False
    checkbox: bool = False
    checked: bool = False
    indeterminate: bool = False
    data: Any = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    @property
    def is_leaf(self) -> bool:
        """Check if node is a leaf."""
        return len(self.children) == 0
    
    @property
    def depth(self) -> int:
        """Get node depth."""
        return 0
    
    def find_node(self, node_id: str) -> Optional["TreeNode"]:
        """Find a node by ID."""
        if self.id == node_id:
            return self
        
        for child in self.children:
            found = child.find_node(node_id)
            if found:
                return found
        
        return None
    
    def add_child(self, child: "TreeNode"):
        """Add a child node."""
        self.children.append(child)
    
    def remove_child(self, node_id: str):
        """Remove a child node."""
        self.children = [c for c in self.children if c.id != node_id]
    
    def get_all_nodes(self) -> List["TreeNode"]:
        """Get all nodes recursively."""
        nodes = [self]
        for child in self.children:
            nodes.extend(child.get_all_nodes())
        return nodes
    
    def get_selected_nodes(self) -> List["TreeNode"]:
        """Get selected nodes."""
        nodes = []
        if self.selected:
            nodes.append(self)
        for child in self.children:
            nodes.extend(child.get_selected_nodes())
        return nodes
    
    def toggle_expanded(self):
        """Toggle expanded state."""
        self.expanded = not self.expanded
    
    def expand_all(self):
        """Expand all nodes."""
        self.expanded = True
        for child in self.children:
            child.expand_all()
    
    def collapse_all(self):
        """Collapse all nodes."""
        self.expanded = False
        for child in self.children:
            child.collapse_all()
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "label": self.label,
            "icon": self.icon,
            "children": [c.to_dict() for c in self.children],
            "expanded": self.expanded,
            "selected": self.selected,
            "disabled": self.disabled,
            "checkbox": self.checkbox,
            "checked": self.checked,
            "indeterminate": self.indeterminate,
            "data": self.data,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "TreeNode":
        """Create from dictionary."""
        children = [cls.from_dict(c) for c in data.get("children", [])]
        return cls(
            id=data["id"],
            label=data["label"],
            icon=data.get("icon", ""),
            children=children,
            expanded=data.get("expanded", True),
            selected=data.get("selected", False),
            disabled=data.get("disabled", False),
            checkbox=data.get("checkbox", False),
            checked=data.get("checked", False),
            data=data.get("data"),
        )


class TreeView:
    """Tree view component."""
    
    def __init__(self, nodes: List[TreeNode] = None):
        self._nodes = nodes or []
        self._selection_mode: TreeSelectionMode = TreeSelectionMode.SINGLE
        self._show_icons: bool = True
        self._show_checkbox: bool = False
        self._show_lines: bool = True
        self._show_root: bool = True
        self._draggable: bool = False
        self._droppable: bool = False
        self._lazy_load: bool = False
        self._searchable: bool = False
        self._search_value: str = ""
        self._filter: Optional[Callable] = None
        self._on_select: Optional[Callable] = None
        self._on_expand: Optional[Callable] = None
        self._on_collapse: Optional[Callable] = None
        self._on_check: Optional[Callable] = None
        self._on_drop: Optional[Callable] = None
        self._on_double_click: Optional[Callable] = None
        self._on_context_menu: Optional[Callable] = None
        self._class_name: str = ""
        self._label: str = ""
        self._help_text: str = ""
        self._disabled: bool = False
        self._height: int = 400
        self._indent: int = 24
    
    def add_node(self, node: TreeNode, parent_id: str = None) -> "TreeView":
        """Add a node."""
        if parent_id:
            parent = self._find_node(parent_id, self._nodes)
            if parent:
                parent.add_child(node)
        else:
            self._nodes.append(node)
        return self
    
    def remove_node(self, node_id: str):
        """Remove a node."""
        self._remove_node(node_id, self._nodes)
    
    def _find_node(self, node_id: str, nodes: List[TreeNode]) -> Optional[TreeNode]:
        """Find a node in list."""
        for node in nodes:
            if node.id == node_id:
                return node
            found = self._find_node(node_id, node.children)
            if found:
                return found
        return None
    
    def _remove_node(self, node_id: str, nodes: List[TreeNode]):
        """Remove a node from list."""
        for i, node in enumerate(nodes):
            if node.id == node_id:
                nodes.pop(i)
                return True
            if self._remove_node(node_id, node.children):
                return True
        return False
    
    def get_node(self, node_id: str) -> Optional[TreeNode]:
        """Get a node by ID."""
        return self._find_node(node_id, self._nodes)
    
    def get_all_nodes(self) -> List[TreeNode]:
        """Get all nodes."""
        nodes = []
        for node in self._nodes:
            nodes.extend(node.get_all_nodes())
        return nodes
    
    def get_selected_nodes(self) -> List[TreeNode]:
        """Get selected nodes."""
        nodes = []
        for node in self._nodes:
            nodes.extend(node.get_selected_nodes())
        return nodes
    
    def expand_all(self):
        """Expand all nodes."""
        for node in self._nodes:
            node.expand_all()
    
    def collapse_all(self):
        """Collapse all nodes."""
        for node in self._nodes:
            node.collapse_all()
    
    def select_node(self, node_id: str):
        """Select a node."""
        for node in self._nodes:
            self._deselect_all(node)
        
        node = self._find_node(node_id, self._nodes)
        if node:
            node.selected = True
    
    def _deselect_all(self, node: TreeNode):
        """Deselect all nodes."""
        node.selected = False
        for child in node.children:
            self._deselect_all(child)
    
    def selection_mode(self, mode: TreeSelectionMode) -> "TreeView":
        """Set selection mode."""
        self._selection_mode = mode
        return self
    
    def show_icons(self, show: bool = True) -> "TreeView":
        """Show icons."""
        self._show_icons = show
        return self
    
    def show_checkbox(self, show: bool = True) -> "TreeView":
        """Show checkboxes."""
        self._show_checkbox = show
        return self
    
    def show_lines(self, show: bool = True) -> "TreeView":
        """Show tree lines."""
        self._show_lines = show
        return self
    
    def show_root(self, show: bool = True) -> "TreeView":
        """Show root node."""
        self._show_root = show
        return self
    
    def draggable(self, draggable: bool = True) -> "TreeView":
        """Make draggable."""
        self._draggable = draggable
        return self
    
    def droppable(self, droppable: bool = True) -> "TreeView":
        """Make droppable."""
        self._droppable = droppable
        return self
    
    def searchable(self, searchable: bool = True) -> "TreeView":
        """Enable search."""
        self._searchable = searchable
        return self
    
    def on_select(self, callback: Callable) -> "TreeView":
        """Set select handler."""
        self._on_select = callback
        return self
    
    def on_expand(self, callback: Callable) -> "TreeView":
        """Set expand handler."""
        self._on_expand = callback
        return self
    
    def on_check(self, callback: Callable) -> "TreeView":
        """Set check handler."""
        self._on_check = callback
        return self
    
    def on_double_click(self, callback: Callable) -> "TreeView":
        """Set double click handler."""
        self._on_double_click = callback
        return self
    
    def class_name(self, class_name: str) -> "TreeView":
        """Set CSS class."""
        self._class_name = class_name
        return self
    
    def label(self, label: str) -> "TreeView":
        """Set label."""
        self._label = label
        return self
    
    def disabled(self) -> "TreeView":
        """Make disabled."""
        self._disabled = True
        return self
    
    def height(self, height: int) -> "TreeView":
        """Set height."""
        self._height = height
        return self
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "nodes": [n.to_dict() for n in self._nodes],
            "selectionMode": self._selection_mode.value,
            "showIcons": self._show_icons,
            "showCheckbox": self._show_checkbox,
            "showLines": self._show_lines,
            "showRoot": self._show_root,
            "draggable": self._draggable,
            "droppable": self._droppable,
            "searchable": self._searchable,
            "disabled": self._disabled,
            "height": self._height,
            "indent": self._indent,
            "className": self._class_name,
            "label": self._label,
        }
    
    def to_html(self) -> str:
        """Generate HTML."""
        label_html = f'<h3 class="tree-label">{self._label}</h3>' if self._label else ""
        disabled_class = " disabled" if self._disabled else ""
        class_attr = f" {self._class_name}" if self._class_name else ""
        
        # Search
        search_html = ""
        if self._searchable:
            search_html = '<div class="tree-search"><input type="text" class="tree-search-input" placeholder="Search..."></div>'
        
        # Render nodes
        nodes_html = ""
        for node in self._nodes:
            if self._show_root or node != self._nodes[0]:
                nodes_html += self._render_node(node, 0)
        
        help_html = f'<p class="tree-help">{self._help_text}</p>' if hasattr(self, '_help_text') and self._help_text else ""
        
        return f'''<div class="tree-view{disabled_class}{class_attr}" style="height: {self._height}px;">
            {label_html}
            {search_html}
            <div class="tree-content">{nodes_html}</div>
            {help_html}
        </div>'''
    
    def _render_node(self, node: TreeNode, depth: int) -> str:
        """Render a node."""
        classes = ["tree-node"]
        if node.expanded:
            classes.append("expanded")
        if node.selected:
            classes.append("selected")
        if node.disabled:
            classes.append("disabled")
        if node.is_leaf:
            classes.append("leaf")
        
        indent = depth * self._indent
        
        # Toggle icon
        toggle = ""
        if not node.is_leaf:
            toggle = f'<span class="tree-toggle"></span>'
        
        # Icon
        icon = ""
        if self._show_icons and node.icon:
            icon = f'<span class="tree-icon">{node.icon}</span>'
        
        # Checkbox
        checkbox = ""
        if self._show_checkbox or node.checkbox:
            checked = " checked" if node.checked else ""
            indeterminate = " data-indeterminate" if node.indeterminate else ""
            checkbox = f'<input type="checkbox" class="tree-checkbox"{checked}{indeterminate}>'
        
        # Children
        children_html = ""
        if not node.is_leaf:
            children = "".join(self._render_node(child, depth + 1) for child in node.children)
            children_html = f'<div class="tree-children">{children}</div>'
        
        return f'''<div class="{' '.join(classes)}" data-id="{node.id}" style="padding-left: {indent}px;">
            {toggle}
            {checkbox}
            {icon}
            <span class="tree-label">{node.label}</span>
            {children_html}
        </div>'''
    
    def generate_js_code(self) -> str:
        """Generate JavaScript."""
        config = self.to_dict()
        return f"""
        // Tree View
        (function() {{
            const config = {str(config).replace("'", '"')};
            
            const tree = document.querySelector('.tree-view');
            if (!tree) return;
            
            // Toggle expand/collapse
            tree.querySelectorAll('.tree-node:not(.leaf)').forEach(node => {{
                const toggle = node.querySelector('.tree-toggle');
                const children = node.querySelector('.tree-children');
                
                if (toggle) {{
                    toggle.addEventListener('click', (e) => {{
                        e.stopPropagation();
                        node.classList.toggle('expanded');
                        if (children) {{
                            children.style.display = node.classList.contains('expanded') ? 'block' : 'none';
                        }}
                    }});
                }}
            }});
            
            // Node selection
            tree.querySelectorAll('.tree-node').forEach(node => {{
                node.addEventListener('click', (e) => {{
                    if (e.target.classList.contains('tree-checkbox')) return;
                    
                    tree.querySelectorAll('.tree-node.selected').forEach(n => n.classList.remove('selected'));
                    node.classList.add('selected');
                    console.log('Node selected:', node.dataset.id);
                }});
                
                node.addEventListener('dblclick', () => {{
                    console.log('Node double clicked:', node.dataset.id);
                }});
            }});
            
            // Checkbox
            tree.querySelectorAll('.tree-checkbox').forEach(checkbox => {{
                checkbox.addEventListener('change', (e) => {{
                    e.stopPropagation();
                    const node = checkbox.closest('.tree-node');
                    console.log('Checkbox changed:', node.dataset.id, checkbox.checked);
                }});
            }});
            
            // Search
            const searchInput = tree.querySelector('.tree-search-input');
            if (searchInput) {{
                searchInput.addEventListener('input', (e) => {{
                    const query = e.target.value.toLowerCase();
                    tree.querySelectorAll('.tree-node').forEach(node => {{
                        const label = node.querySelector('.tree-label')?.textContent.toLowerCase() || '';
                        const visible = !query || label.includes(query);
                        node.style.display = visible ? '' : 'none';
                    }});
                }});
            }}
        }})();
        """


def create_tree_view(nodes: List[TreeNode] = None) -> TreeView:
    """Create a tree view."""
    return TreeView(nodes)


def tree_node(id: str, label: str, **kwargs) -> TreeNode:
    """Create a tree node."""
    return TreeNode(id=id, label=label, **kwargs)


TREE_VIEW_CSS = """
.tree-view {
    border: 1px solid #e5e7eb;
    border-radius: 0.5rem;
    overflow: auto;
    background: white;
}

.tree-label {
    padding: 1rem;
    margin: 0;
    font-size: 1rem;
    font-weight: 600;
    color: #111827;
    border-bottom: 1px solid #e5e7eb;
}

.tree-search {
    padding: 0.75rem 1rem;
    border-bottom: 1px solid #e5e7eb;
}

.tree-search-input {
    width: 100%;
    padding: 0.5rem;
    border: 1px solid #d1d5db;
    border-radius: 0.375rem;
    font-size: 0.875rem;
}

.tree-search-input:focus {
    outline: none;
    border-color: #3b82f6;
}

.tree-content {
    padding: 0.5rem;
}

.tree-node {
    display: flex;
    align-items: center;
    padding: 0.5rem;
    border-radius: 0.375rem;
    cursor: pointer;
    user-select: none;
}

.tree-node:hover {
    background: #f9fafb;
}

.tree-node.selected {
    background: #eff6ff;
}

.tree-node.disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

.tree-toggle {
    width: 20px;
    height: 20px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-right: 0.25rem;
    color: #6b7280;
    transition: transform 0.2s;
}

.tree-toggle::before {
    content: '▶';
    font-size: 0.625rem;
}

.tree-node.expanded > .tree-toggle {
    transform: rotate(90deg);
}

.tree-checkbox {
    margin-right: 0.5rem;
    width: 16px;
    height: 16px;
}

.tree-icon {
    margin-right: 0.5rem;
    color: #6b7280;
}

.tree-label {
    flex: 1;
    color: #374151;
}

.tree-children {
    display: block;
}

.tree-node.leaf > .tree-toggle {
    visibility: hidden;
}

.tree-help {
    padding: 0.75rem 1rem;
    margin: 0;
    font-size: 0.875rem;
    color: #6b7280;
    border-top: 1px solid #e5e7eb;
}
"""
