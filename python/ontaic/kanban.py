"""Kanban board component for task management."""
from typing import Any, Callable, Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum


class KanbanCardSize(str, Enum):
    """Kanban card size."""
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"


class KanbanPriority(str, Enum):
    """Kanban priority."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


@dataclass
class KanbanCard:
    """Kanban card/task."""
    id: str
    title: str
    description: str = ""
    column_id: str = ""
    priority: KanbanPriority = KanbanPriority.MEDIUM
    tags: List[str] = field(default_factory=list)
    assignee: str = ""
    avatar: str = ""
    due_date: str = ""
    estimate: str = ""
    checklist: List[Dict[str, Any]] = field(default_factory=list)
    attachments: List[Dict[str, Any]] = field(default_factory=list)
    color: str = ""
    size: KanbanCardSize = KanbanCardSize.MEDIUM
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    @property
    def checklist_progress(self) -> float:
        """Get checklist completion percentage."""
        if not self.checklist:
            return 0
        completed = sum(1 for item in self.checklist if item.get("completed", False))
        return completed / len(self.checklist) * 100
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "columnId": self.column_id,
            "priority": self.priority.value,
            "tags": self.tags,
            "assignee": self.assignee,
            "avatar": self.avatar,
            "dueDate": self.due_date,
            "estimate": self.estimate,
            "checklist": self.checklist,
            "attachments": self.attachments,
            "color": self.color,
            "size": self.size.value,
            "metadata": self.metadata,
        }


@dataclass
class KanbanColumn:
    """Kanban column."""
    id: str
    title: str
    cards: List[KanbanCard] = field(default_factory=list)
    color: str = ""
    limit: int = 0
    collapsed: bool = False
    
    @property
    def card_count(self) -> int:
        return len(self.cards)
    
    @property
    def is_over_limit(self) -> bool:
        if self.limit <= 0:
            return False
        return self.card_count > self.limit
    
    def add_card(self, card: KanbanCard):
        """Add a card."""
        card.column_id = self.id
        self.cards.append(card)
    
    def remove_card(self, card_id: str):
        """Remove a card."""
        self.cards = [c for c in self.cards if c.id != card_id]
    
    def move_card(self, card_id: str, position: int):
        """Move a card to a position."""
        card = next((c for c in self.cards if c.id == card_id), None)
        if card:
            self.cards.remove(card)
            self.cards.insert(position, card)
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "cards": [c.to_dict() for c in self.cards],
            "color": self.color,
            "limit": self.limit,
            "collapsed": self.collapsed,
        }


class KanbanBoard:
    """Kanban board component."""
    
    def __init__(self, columns: List[KanbanColumn] = None):
        self._columns = columns or []
        self._card_size: KanbanCardSize = KanbanCardSize.MEDIUM
        self._draggable: bool = True
        self._collapsible: bool = True
        self._editable: bool = True
        self._searchable: bool = False
        self._filterable: bool = False
        self._search_value: str = ""
        self._filter_tags: List[str] = []
        self._on_card_click: Optional[Callable] = None
        self._on_card_move: Optional[Callable] = None
        self._on_card_add: Optional[Callable] = None
        self._on_card_delete: Optional[Callable] = None
        self._on_column_add: Optional[Callable] = None
        self._on_column_delete: Optional[Callable] = None
        self._class_name: str = ""
        self._label: str = ""
        self._help_text: str = ""
        self._height: int = 600
        self._show_avatar: bool = True
        self._show_tags: bool = True
        self._show_due_date: bool = True
        self._show_estimate: bool = True
        self._show_checklist_progress: bool = True
    
    def add_column(self, column: KanbanColumn) -> "KanbanBoard":
        """Add a column."""
        self._columns.append(column)
        return self
    
    def column(self, id: str, title: str, **kwargs) -> "KanbanBoard":
        """Add a column."""
        col = KanbanColumn(id=id, title=title, **kwargs)
        self._columns.append(col)
        return self
    
    def add_card(self, column_id: str, card: KanbanCard):
        """Add a card to a column."""
        for col in self._columns:
            if col.id == column_id:
                col.add_card(card)
                break
    
    def card(self, column_id: str, id: str, title: str, **kwargs) -> "KanbanBoard":
        """Add a card."""
        c = KanbanCard(id=id, title=title, **kwargs)
        self.add_card(column_id, c)
        return self
    
    def move_card(self, card_id: str, from_column: str, to_column: str, position: int = -1):
        """Move a card between columns."""
        source_col = next((c for c in self._columns if c.id == from_column), None)
        target_col = next((c for c in self._columns if c.id == to_column), None)
        
        if source_col and target_col:
            card = next((c for c in source_col.cards if c.id == card_id), None)
            if card:
                source_col.remove_card(card_id)
                card.column_id = to_column
                if position >= 0:
                    target_col.cards.insert(position, card)
                else:
                    target_col.add_card(card)
    
    def get_card(self, card_id: str) -> Optional[KanbanCard]:
        """Get a card by ID."""
        for col in self._columns:
            for card in col.cards:
                if card.id == card_id:
                    return card
        return None
    
    def card_size(self, size: KanbanCardSize) -> "KanbanBoard":
        """Set card size."""
        self._card_size = size
        return self
    
    def draggable(self, draggable: bool = True) -> "KanbanBoard":
        """Enable drag and drop."""
        self._draggable = draggable
        return self
    
    def searchable(self, searchable: bool = True) -> "KanbanBoard":
        """Enable search."""
        self._searchable = searchable
        return self
    
    def filterable(self, filterable: bool = True) -> "KanbanBoard":
        """Enable filtering."""
        self._filterable = filterable
        return self
    
    def on_card_click(self, callback: Callable) -> "KanbanBoard":
        """Set card click handler."""
        self._on_card_click = callback
        return self
    
    def on_card_move(self, callback: Callable) -> "KanbanBoard":
        """Set card move handler."""
        self._on_card_move = callback
        return self
    
    def on_card_add(self, callback: Callable) -> "KanbanBoard":
        """Set card add handler."""
        self._on_card_add = callback
        return self
    
    def class_name(self, class_name: str) -> "KanbanBoard":
        """Set CSS class."""
        self._class_name = class_name
        return self
    
    def label(self, label: str) -> "KanbanBoard":
        """Set label."""
        self._label = label
        return self
    
    def height(self, height: int) -> "KanbanBoard":
        """Set height."""
        self._height = height
        return self
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "columns": [c.to_dict() for c in self._columns],
            "cardSize": self._card_size.value,
            "draggable": self._draggable,
            "collapsible": self._collapsible,
            "editable": self._editable,
            "searchable": self._searchable,
            "filterable": self._filterable,
            "showAvatar": self._show_avatar,
            "showTags": self._show_tags,
            "showDueDate": self._show_due_date,
            "showEstimate": self._show_estimate,
            "showChecklistProgress": self._show_checklist_progress,
            "className": self._class_name,
            "label": self._label,
            "height": self._height,
        }
    
    def to_html(self) -> str:
        """Generate HTML."""
        label_html = f'<h3 class="kanban-label">{self._label}</h3>' if self._label else ""
        class_attr = f" {self._class_name}" if self._class_name else ""
        size_class = f" kanban-{self._card_size.value}"
        
        # Search
        search_html = ""
        if self._searchable:
            search_html = '<div class="kanban-search"><input type="text" class="kanban-search-input" placeholder="Search cards..."></div>'
        
        # Columns
        columns_html = ""
        for col in self._columns:
            # Column header
            limit_badge = ""
            if col.limit > 0:
                limit_badge = f'<span class="column-limit{" over-limit" if col.is_over_limit else ""}">{col.card_count}/{col.limit}</span>'
            
            header_html = f'''<div class="kanban-column-header" style="border-top-color: {col.color or '#3b82f6'}">
                <span class="column-title">{col.title}</span>
                {limit_badge}
                <span class="column-count">{col.card_count}</span>
            </div>'''
            
            # Cards
            cards_html = ""
            for card in col.cards:
                # Priority indicator
                priority_html = f'<span class="card-priority priority-{card.priority.value}"></span>' if card.priority != KanbanPriority.MEDIUM else ""
                
                # Tags
                tags_html = ""
                if self._show_tags and card.tags:
                    tags = "".join(f'<span class="card-tag">{t}</span>' for t in card.tags[:3])
                    tags_html = f'<div class="card-tags">{tags}</div>'
                
                # Assignee
                assignee_html = ""
                if self._show_avatar and card.assignee:
                    avatar = card.avatar or card.assignee[0].upper()
                    assignee_html = f'<div class="card-avatar">{avatar}</div>'
                
                # Due date
                due_html = ""
                if self._show_due_date and card.due_date:
                    due_html = f'<span class="card-due">{card.due_date}</span>'
                
                # Estimate
                estimate_html = ""
                if self._show_estimate and card.estimate:
                    estimate_html = f'<span class="card-estimate">{card.estimate}</span>'
                
                # Checklist progress
                checklist_html = ""
                if self._show_checklist_progress and card.checklist:
                    progress = card.checklist_progress
                    checklist_html = f'''<div class="card-checklist">
                        <div class="checklist-progress">
                            <div class="checklist-bar" style="width: {progress}%"></div>
                        </div>
                        <span class="checklist-text">{int(progress)}%</span>
                    </div>'''
                
                # Color accent
                color_style = f" border-left: 3px solid {card.color};" if card.color else ""
                
                cards_html += f'''<div class="kanban-card" data-id="{card.id}" data-column="{col.id}" style="{color_style}">
                    {priority_html}
                    <h4 class="card-title">{card.title}</h4>
                    <p class="card-description">{card.description}</p>
                    {tags_html}
                    <div class="card-footer">
                        {assignee_html}
                        {due_html}
                        {estimate_html}
                        {checklist_html}
                    </div>
                </div>'''
            
            # Add card button
            add_btn = '<button type="button" class="kanban-add-card">+ Add Card</button>' if self._editable else ""
            
            columns_html += f'''<div class="kanban-column" data-column="{col.id}">
                {header_html}
                <div class="kanban-cards">{cards_html}</div>
                {add_btn}
            </div>'''
        
        help_html = f'<p class="kanban-help">{self._help_text}</p>' if hasattr(self, '_help_text') and self._help_text else ""
        
        return f'''<div class="kanban-board{size_class}{class_attr}" style="height: {self._height}px;">
            {label_html}
            {search_html}
            <div class="kanban-columns">{columns_html}</div>
            {help_html}
        </div>'''
    
    def generate_js_code(self) -> str:
        """Generate JavaScript."""
        config = self.to_dict()
        return f"""
        // Kanban Board
        (function() {{
            const config = {str(config).replace("'", '"')};
            
            const board = document.querySelector('.kanban-board');
            if (!board) return;
            
            let draggedCard = null;
            
            // Card drag and drop
            board.querySelectorAll('.kanban-card').forEach(card => {{
                card.setAttribute('draggable', 'true');
                
                card.addEventListener('dragstart', (e) => {{
                    draggedCard = card;
                    card.classList.add('dragging');
                    e.dataTransfer.effectAllowed = 'move';
                }});
                
                card.addEventListener('dragend', () => {{
                    card.classList.remove('dragging');
                    draggedCard = null;
                    board.querySelectorAll('.kanban-column').forEach(col => {{
                        col.classList.remove('drag-over');
                    }});
                }});
                
                card.addEventListener('click', () => {{
                    console.log('Card clicked:', card.dataset.id);
                }});
            }});
            
            // Column drop zones
            board.querySelectorAll('.kanban-column').forEach(column => {{
                column.addEventListener('dragover', (e) => {{
                    e.preventDefault();
                    column.classList.add('drag-over');
                }});
                
                column.addEventListener('dragleave', () => {{
                    column.classList.remove('drag-over');
                }});
                
                column.addEventListener('drop', (e) => {{
                    e.preventDefault();
                    column.classList.remove('drag-over');
                    
                    if (draggedCard) {{
                        const cards = column.querySelector('.kanban-cards');
                        cards.appendChild(draggedCard);
                        console.log('Card moved to:', column.dataset.column);
                    }}
                }});
            }});
            
            // Add card buttons
            board.querySelectorAll('.kanban-add-card').forEach(btn => {{
                btn.addEventListener('click', () => {{
                    const column = btn.closest('.kanban-column');
                    console.log('Add card to:', column.dataset.column);
                }});
            }});
            
            // Search
            const searchInput = board.querySelector('.kanban-search-input');
            if (searchInput) {{
                searchInput.addEventListener('input', (e) => {{
                    const query = e.target.value.toLowerCase();
                    board.querySelectorAll('.kanban-card').forEach(card => {{
                        const title = card.querySelector('.card-title')?.textContent.toLowerCase() || '';
                        const desc = card.querySelector('.card-description')?.textContent.toLowerCase() || '';
                        const visible = !query || title.includes(query) || desc.includes(query);
                        card.style.display = visible ? '' : 'none';
                    }});
                }});
            }}
        }})();
        """


def create_kanban(columns: List[KanbanColumn] = None) -> KanbanBoard:
    """Create a kanban board."""
    return KanbanBoard(columns)


def kanban_column(id: str, title: str, **kwargs) -> KanbanColumn:
    """Create a kanban column."""
    return KanbanColumn(id=id, title=title, **kwargs)


def kanban_card(id: str, title: str, **kwargs) -> KanbanCard:
    """Create a kanban card."""
    return KanbanCard(id=id, title=title, **kwargs)


KANBAN_CSS = """
.kanban-board {
    display: flex;
    flex-direction: column;
    background: #f3f4f6;
    border-radius: 0.5rem;
    overflow: hidden;
}

.kanban-label {
    padding: 1rem;
    margin: 0;
    font-size: 1.25rem;
    font-weight: 600;
    color: #111827;
    background: white;
    border-bottom: 1px solid #e5e7eb;
}

.kanban-search {
    padding: 0.75rem 1rem;
    background: white;
    border-bottom: 1px solid #e5e7eb;
}

.kanban-search-input {
    width: 100%;
    padding: 0.5rem;
    border: 1px solid #d1d5db;
    border-radius: 0.375rem;
    font-size: 0.875rem;
}

.kanban-columns {
    display: flex;
    flex: 1;
    overflow-x: auto;
    padding: 1rem;
    gap: 1rem;
}

.kanban-column {
    flex: 0 0 300px;
    background: white;
    border-radius: 0.5rem;
    display: flex;
    flex-direction: column;
    max-height: 100%;
}

.kanban-column.drag-over {
    background: #eff6ff;
}

.kanban-column-header {
    padding: 0.75rem 1rem;
    border-top: 3px solid #3b82f6;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.column-title {
    flex: 1;
    font-weight: 600;
    color: #374151;
}

.column-count {
    background: #e5e7eb;
    padding: 0.125rem 0.5rem;
    border-radius: 1rem;
    font-size: 0.75rem;
    color: #6b7280;
}

.column-limit {
    font-size: 0.75rem;
    color: #6b7280;
}

.column-limit.over-limit {
    color: #ef4444;
    font-weight: 600;
}

.kanban-cards {
    flex: 1;
    overflow-y: auto;
    padding: 0.5rem;
    min-height: 100px;
}

.kanban-card {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 0.5rem;
    padding: 0.75rem;
    margin-bottom: 0.5rem;
    cursor: pointer;
    transition: box-shadow 0.2s;
}

.kanban-card:hover {
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.kanban-card.dragging {
    opacity: 0.5;
}

.card-priority {
    display: inline-block;
    width: 8px;
    height: 8px;
    border-radius: 50%;
    margin-right: 0.5rem;
}

.priority-low { background: #10b981; }
.priority-medium { background: #f59e0b; }
.priority-high { background: #f97316; }
.priority-urgent { background: #ef4444; }

.card-title {
    margin: 0 0 0.5rem;
    font-size: 0.875rem;
    font-weight: 500;
    color: #111827;
}

.card-description {
    margin: 0 0 0.5rem;
    font-size: 0.75rem;
    color: #6b7280;
    line-height: 1.4;
}

.card-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 0.25rem;
    margin-bottom: 0.5rem;
}

.card-tag {
    padding: 0.125rem 0.375rem;
    background: #f3f4f6;
    border-radius: 0.25rem;
    font-size: 0.625rem;
    color: #6b7280;
}

.card-footer {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.75rem;
    color: #6b7280;
}

.card-avatar {
    width: 24px;
    height: 24px;
    border-radius: 50%;
    background: #3b82f6;
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.625rem;
    font-weight: 600;
}

.card-due {
    color: #f59e0b;
}

.card-checklist {
    display: flex;
    align-items: center;
    gap: 0.25rem;
    margin-left: auto;
}

.checklist-progress {
    width: 40px;
    height: 4px;
    background: #e5e7eb;
    border-radius: 2px;
    overflow: hidden;
}

.checklist-bar {
    height: 100%;
    background: #10b981;
}

.checklist-text {
    font-size: 0.625rem;
}

.kanban-add-card {
    padding: 0.75rem;
    background: transparent;
    border: none;
    border-top: 1px solid #e5e7eb;
    color: #6b7280;
    cursor: pointer;
    text-align: left;
}

.kanban-add-card:hover {
    background: #f9fafb;
    color: #374151;
}

.kanban-help {
    padding: 0.75rem 1rem;
    margin: 0;
    font-size: 0.875rem;
    color: #6b7280;
    background: white;
    border-top: 1px solid #e5e7eb;
}

/* Small cards */
.kanban-small .kanban-card {
    padding: 0.5rem;
}

.kanban-small .card-title {
    font-size: 0.8125rem;
}

.kanban-small .card-description {
    display: none;
}

/* Large cards */
.kanban-large .kanban-card {
    padding: 1rem;
}

.kanban-large .card-title {
    font-size: 1rem;
}
"""
