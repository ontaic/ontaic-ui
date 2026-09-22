"""Timeline component for displaying events in chronological order."""
from typing import Any, Callable, Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum


class TimelineOrientation(str, Enum):
    """Timeline orientation."""
    VERTICAL = "vertical"
    HORIZONTAL = "horizontal"


class TimelineAlign(str, Enum):
    """Timeline alignment."""
    LEFT = "left"
    RIGHT = "right"
    ALTERNATE = "alternate"
    CENTER = "center"


class TimelineSize(str, Enum):
    """Timeline size."""
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"


@dataclass
class TimelineDot:
    """Timeline dot/icon."""
    icon: str = ""
    color: str = "blue"
    size: str = ""
    
    def to_dict(self) -> dict:
        return {"icon": self.icon, "color": self.color, "size": self.size}


@dataclass
class TimelineItem:
    """Timeline item."""
    id: str
    title: str
    description: str = ""
    date: str = ""
    time: str = ""
    dot: TimelineDot = field(default_factory=TimelineDot)
    content: str = ""
    tags: List[str] = field(default_factory=list)
    link: str = ""
    link_text: str = ""
    image: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "date": self.date,
            "time": self.time,
            "dot": self.dot.to_dict(),
            "content": self.content,
            "tags": self.tags,
            "link": self.link,
            "linkText": self.link_text,
            "image": self.image,
            "metadata": self.metadata,
        }


class Timeline:
    """Timeline component."""
    
    def __init__(self, items: List[TimelineItem] = None):
        self._items = items or []
        self._orientation: TimelineOrientation = TimelineOrientation.VERTICAL
        self._align: TimelineAlign = TimelineAlign.ALTERNATE
        self._size: TimelineSize = TimelineSize.MEDIUM
        self._show_date: bool = True
        self._show_time: bool = False
        self._show_icon: bool = True
        self._show_line: bool = True
        self._animate: bool = True
        self._on_item_click: Optional[Callable] = None
        self._on_item_hover: Optional[Callable] = None
        self._class_name: str = ""
        self._label: str = ""
        self._help_text: str = ""
    
    def add_item(self, item: TimelineItem) -> "Timeline":
        """Add an item."""
        self._items.append(item)
        return self
    
    def item(self, id: str, title: str, **kwargs) -> "Timeline":
        """Add an item."""
        item = TimelineItem(id=id, title=title, **kwargs)
        self._items.append(item)
        return self
    
    def orientation(self, orientation: TimelineOrientation) -> "Timeline":
        """Set orientation."""
        self._orientation = orientation
        return self
    
    def align(self, align: TimelineAlign) -> "Timeline":
        """Set alignment."""
        self._align = align
        return self
    
    def size(self, size: TimelineSize) -> "Timeline":
        """Set size."""
        self._size = size
        return self
    
    def show_date(self, show: bool = True) -> "Timeline":
        """Show date."""
        self._show_date = show
        return self
    
    def show_time(self, show: bool = True) -> "Timeline":
        """Show time."""
        self._show_time = show
        return self
    
    def show_icon(self, show: bool = True) -> "Timeline":
        """Show icon."""
        self._show_icon = show
        return self
    
    def show_line(self, show: bool = True) -> "Timeline":
        """Show line."""
        self._show_line = show
        return self
    
    def animate(self, animate: bool = True) -> "Timeline":
        """Enable animation."""
        self._animate = animate
        return self
    
    def on_item_click(self, callback: Callable) -> "Timeline":
        """Set item click handler."""
        self._on_item_click = callback
        return self
    
    def class_name(self, class_name: str) -> "Timeline":
        """Set CSS class."""
        self._class_name = class_name
        return self
    
    def label(self, label: str) -> "Timeline":
        """Set label."""
        self._label = label
        return self
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "items": [i.to_dict() for i in self._items],
            "orientation": self._orientation.value,
            "align": self._align.value,
            "size": self._size.value,
            "showDate": self._show_date,
            "showTime": self._show_time,
            "showIcon": self._show_icon,
            "showLine": self._show_line,
            "animate": self._animate,
            "className": self._class_name,
            "label": self._label,
        }
    
    def to_html(self) -> str:
        """Generate HTML."""
        label_html = f'<h3 class="timeline-label">{self._label}</h3>' if self._label else ""
        class_attr = f" {self._class_name}" if self._class_name else ""
        size_class = f" timeline-{self._size.value}" if self._size != TimelineSize.MEDIUM else ""
        orient_class = f" timeline-{self._orientation.value}"
        align_class = f" timeline-{self._align.value}"
        
        items_html = ""
        for i, item in enumerate(self._items):
            side = ""
            if self._align == TimelineAlign.ALTERNATE:
                side = "left" if i % 2 == 0 else "right"
            elif self._align == TimelineAlign.LEFT:
                side = "left"
            elif self._align == TimelineAlign.RIGHT:
                side = "right"
            
            # Dot
            dot_color = item.dot.color or "blue"
            dot_icon = item.dot.icon or str(i + 1)
            dot_html = f'<div class="timeline-dot dot-{dot_color}">{dot_icon}</div>'
            
            # Date/time
            date_html = ""
            if self._show_date and item.date:
                date_html = f'<div class="timeline-date">{item.date}</div>'
            if self._show_time and item.time:
                date_html += f'<div class="timeline-time">{item.time}</div>'
            
            # Content
            content_html = f'<div class="timeline-content">{item.content}</div>' if item.content else ""
            
            # Tags
            tags_html = ""
            if item.tags:
                tags = "".join(f'<span class="timeline-tag">{t}</span>' for t in item.tags)
                tags_html = f'<div class="timeline-tags">{tags}</div>'
            
            # Link
            link_html = ""
            if item.link:
                link_text = item.link_text or "View more"
                link_html = f'<a href="{item.link}" class="timeline-link">{link_text}</a>'
            
            # Image
            image_html = ""
            if item.image:
                image_html = f'<img src="{item.image}" class="timeline-image" alt="">'
            
            items_html += f'''<div class="timeline-item{f' item-{side}' if side else ''}" data-id="{item.id}">
                {dot_html}
                <div class="timeline-body">
                    <div class="timeline-header">
                        <h4 class="timeline-title">{item.title}</h4>
                        {date_html}
                    </div>
                    <div class="timeline-description">{item.description}</div>
                    {content_html}
                    {tags_html}
                    {link_html}
                    {image_html}
                </div>
            </div>'''
        
        help_html = f'<p class="timeline-help">{self._help_text}</p>' if hasattr(self, '_help_text') and self._help_text else ""
        
        return f'''<div class="timeline{orient_class}{align_class}{size_class}{class_attr}">
            {label_html}
            <div class="timeline-track">
                {items_html}
            </div>
            {help_html}
        </div>'''
    
    def generate_js_code(self) -> str:
        """Generate JavaScript."""
        config = self.to_dict()
        return f"""
        // Timeline
        (function() {{
            const config = {str(config).replace("'", '"')};
            
            const timeline = document.querySelector('.timeline');
            if (!timeline) return;
            
            // Item click
            timeline.querySelectorAll('.timeline-item').forEach(item => {{
                item.addEventListener('click', () => {{
                    console.log('Timeline item clicked:', item.dataset.id);
                }});
            }});
            
            // Animation on scroll
            if (config.animate) {{
                const observer = new IntersectionObserver((entries) => {{
                    entries.forEach(entry => {{
                        if (entry.isIntersecting) {{
                            entry.target.classList.add('animate-in');
                        }}
                    }});
                }}, {{ threshold: 0.1 }});
                
                timeline.querySelectorAll('.timeline-item').forEach(item => {{
                    observer.observe(item);
                }});
            }}
        }})();
        """


def create_timeline(items: List[TimelineItem] = None) -> Timeline:
    """Create a timeline."""
    return Timeline(items)


def timeline_item(id: str, title: str, **kwargs) -> TimelineItem:
    """Create a timeline item."""
    return TimelineItem(id=id, title=title, **kwargs)


def timeline_dot(icon: str = "", color: str = "blue") -> TimelineDot:
    """Create a timeline dot."""
    return TimelineDot(icon=icon, color=color)


TIMELINE_CSS = """
.timeline {
    padding: 1rem 0;
}

.timeline-label {
    font-size: 1.25rem;
    font-weight: 600;
    color: #111827;
    margin-bottom: 1.5rem;
}

.timeline-track {
    position: relative;
    padding: 1rem 0;
}

.timeline-vertical .timeline-track {
    padding-left: 2rem;
}

.timeline-vertical.timeline-left .timeline-track {
    padding-left: 2rem;
}

.timeline-vertical.timeline-right .timeline-track {
    padding-left: 0;
    padding-right: 2rem;
}

.timeline-vertical.timeline-center .timeline-track {
    padding-left: 50%;
}

.timeline-horizontal .timeline-track {
    display: flex;
    overflow-x: auto;
    padding-bottom: 1rem;
}

/* Timeline item */
.timeline-item {
    position: relative;
    margin-bottom: 2rem;
}

.timeline-horizontal .timeline-item {
    flex: 0 0 300px;
    margin-right: 2rem;
    margin-bottom: 0;
}

.timeline-vertical .timeline-item::before {
    content: '';
    position: absolute;
    left: -2rem;
    top: 0;
    bottom: 0;
    width: 2px;
    background: #e5e7eb;
}

.timeline-vertical.timeline-right .timeline-item::before {
    left: auto;
    right: -2rem;
}

.timeline-vertical.timeline-center .timeline-item::before {
    left: 50%;
    transform: translateX(-50%);
}

.timeline-item:last-child::before {
    display: none;
}

/* Dot */
.timeline-dot {
    position: absolute;
    left: -2rem;
    top: 0;
    width: 24px;
    height: 24px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.75rem;
    font-weight: 600;
    color: white;
    z-index: 1;
}

.timeline-vertical.timeline-right .timeline-dot {
    left: auto;
    right: -2rem;
}

.timeline-vertical.timeline-center .timeline-dot {
    left: 50%;
    transform: translateX(-50%);
}

.dot-blue { background: #3b82f6; }
.dot-green { background: #10b981; }
.dot-red { background: #ef4444; }
.dot-yellow { background: #f59e0b; }
.dot-purple { background: #8b5cf6; }
.dot-gray { background: #6b7280; }

/* Body */
.timeline-body {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 0.5rem;
    padding: 1rem;
}

.timeline-item:hover .timeline-body {
    border-color: #d1d5db;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

/* Header */
.timeline-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 0.5rem;
}

.timeline-title {
    margin: 0;
    font-size: 1rem;
    font-weight: 600;
    color: #111827;
}

.timeline-date {
    font-size: 0.875rem;
    color: #6b7280;
}

.timeline-time {
    font-size: 0.75rem;
    color: #9ca3af;
}

/* Description */
.timeline-description {
    color: #6b7280;
    font-size: 0.875rem;
    line-height: 1.5;
}

/* Content */
.timeline-content {
    margin-top: 0.75rem;
    padding-top: 0.75rem;
    border-top: 1px solid #f3f4f6;
}

/* Tags */
.timeline-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin-top: 0.75rem;
}

.timeline-tag {
    padding: 0.25rem 0.5rem;
    background: #f3f4f6;
    border-radius: 0.25rem;
    font-size: 0.75rem;
    color: #6b7280;
}

/* Link */
.timeline-link {
    display: inline-block;
    margin-top: 0.75rem;
    color: #3b82f6;
    font-size: 0.875rem;
    text-decoration: none;
}

.timeline-link:hover {
    text-decoration: underline;
}

/* Image */
.timeline-image {
    margin-top: 0.75rem;
    max-width: 100%;
    border-radius: 0.375rem;
}

/* Animation */
.timeline-item {
    opacity: 0;
    transform: translateY(20px);
    transition: opacity 0.3s ease, transform 0.3s ease;
}

.timeline-item.animate-in {
    opacity: 1;
    transform: translateY(0);
}

.timeline-horizontal .timeline-item {
    transform: translateX(20px);
}

.timeline-horizontal .timeline-item.animate-in {
    transform: translateX(0);
}

/* Size variants */
.timeline-small .timeline-dot {
    width: 20px;
    height: 20px;
    font-size: 0.625rem;
}

.timeline-small .timeline-body {
    padding: 0.75rem;
}

.timeline-small .timeline-title {
    font-size: 0.875rem;
}

.timeline-large .timeline-dot {
    width: 32px;
    height: 32px;
    font-size: 0.875rem;
}

.timeline-large .timeline-body {
    padding: 1.25rem;
}

.timeline-large .timeline-title {
    font-size: 1.125rem;
}

.timeline-help {
    margin-top: 1rem;
    font-size: 0.875rem;
    color: #6b7280;
}
"""
