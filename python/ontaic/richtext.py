"""Rich text editor component."""
from typing import Any, Callable, Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum


class EditorToolbar(str, Enum):
    """Editor toolbar options."""
    BASIC = "basic"
    FULL = "full"
    MINIMAL = "minimal"
    CUSTOM = "custom"


class EditorFormat(str, Enum):
    """Editor output formats."""
    HTML = "html"
    TEXT = "text"
    MARKDOWN = "markdown"


@dataclass
class ToolbarButton:
    """Toolbar button definition."""
    name: str
    icon: str = ""
    tooltip: str = ""
    action: str = ""
    group: str = ""
    
    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "icon": self.icon,
            "tooltip": self.tooltip,
            "action": self.action,
            "group": self.group,
        }


TOOLBAR_GROUPS = {
    "history": ["undo", "redo"],
    "format": ["bold", "italic", "underline", "strikethrough"],
    "heading": ["h1", "h2", "h3", "h4", "h5", "h6"],
    "list": ["unordered-list", "ordered-list", "indent", "outdent"],
    "alignment": ["align-left", "align-center", "align-right", "align-justify"],
    "link": ["link", "unlink", "image"],
    "table": ["table"],
    "code": ["code", "code-block", "blockquote"],
    "clear": ["clear-formatting"],
}


class RichTextEditor:
    """Rich text editor component."""
    
    def __init__(self, content: str = "", placeholder: str = "Type here...", toolbar: EditorToolbar = EditorToolbar.FULL):
        self.content = content
        self.placeholder = placeholder
        self.toolbar = toolbar
        self._on_change: Optional[Callable] = None
        self._on_focus: Optional[Callable] = None
        self._on_blur: Optional[Callable] = None
        self._format: EditorFormat = EditorFormat.HTML
        self._height: int = 300
        self._min_height: int = 150
        self._max_height: int = 500
        self._readonly: bool = False
        self._custom_toolbar: List[str] = []
        self._class_name: str = ""
    
    def on_change(self, callback: Callable) -> "RichTextEditor":
        """Set change handler."""
        self._on_change = callback
        return self
    
    def on_focus(self, callback: Callable) -> "RichTextEditor":
        """Set focus handler."""
        self._on_focus = callback
        return self
    
    def on_blur(self, callback: Callable) -> "RichTextEditor":
        """Set blur handler."""
        self._on_blur = callback
        return self
    
    def format(self, fmt: EditorFormat) -> "RichTextEditor":
        """Set output format."""
        self._format = fmt
        return self
    
    def height(self, height: int) -> "RichTextEditor":
        """Set editor height."""
        self._height = height
        return self
    
    def min_height(self, height: int) -> "RichTextEditor":
        """Set minimum height."""
        self._min_height = height
        return self
    
    def max_height(self, height: int) -> "RichTextEditor":
        """Set maximum height."""
        self._max_height = height
        return self
    
    def readonly(self) -> "RichTextEditor":
        """Make editor readonly."""
        self._readonly = True
        return self
    
    def custom_toolbar(self, buttons: List[str]) -> "RichTextEditor":
        """Set custom toolbar buttons."""
        self.toolbar = EditorToolbar.CUSTOM
        self._custom_toolbar = buttons
        return self
    
    def class_name(self, class_name: str) -> "RichTextEditor":
        """Set CSS class name."""
        self._class_name = class_name
        return self
    
    def _get_toolbar_buttons(self) -> List[str]:
        """Get toolbar buttons based on toolbar type."""
        if self.toolbar == EditorToolbar.MINIMAL:
            return ["bold", "italic", "underline", "link"]
        elif self.toolbar == EditorToolbar.BASIC:
            return ["bold", "italic", "underline", "unordered-list", "ordered-list", "link"]
        elif self.toolbar == EditorToolbar.CUSTOM:
            return self._custom_toolbar
        else:  # FULL
            buttons = []
            for group_buttons in TOOLBAR_GROUPS.values():
                buttons.extend(group_buttons)
            return buttons
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "content": self.content,
            "placeholder": self.placeholder,
            "toolbar": self.toolbar.value,
            "format": self._format.value,
            "height": self._height,
            "minHeight": self._min_height,
            "maxHeight": self._max_height,
            "readonly": self._readonly,
            "buttons": self._get_toolbar_buttons(),
            "className": self._class_name,
        }
    
    def to_html(self) -> str:
        """Generate HTML for editor."""
        readonly = " contenteditable='false'" if self._readonly else " contenteditable='true'"
        class_attr = f" class='rich-editor {self._class_name}'" if self._class_name else " class='rich-editor'"
        
        toolbar_html = self._render_toolbar()
        
        return f'''<div class="rich-editor-container">
            {toolbar_html}
            <div id="rich-editor"{class_attr} style="min-height: {self._min_height}px; max-height: {self._max_height}px; height: {self._height}px;"{readonly}>
                {self.content or f'<p class="placeholder">{self.placeholder}</p>'}
            </div>
        </div>'''
    
    def _render_toolbar(self) -> str:
        """Render toolbar HTML."""
        if self.toolbar == EditorToolbar.MINIMAL:
            return self._render_toolbar_group(["bold", "italic", "underline", "link"])
        
        groups = []
        for group_name, buttons in TOOLBAR_GROUPS.items():
            if self.toolbar == EditorToolbar.BASIC:
                if group_name in ["history", "format", "list", "link"]:
                    groups.append(self._render_toolbar_group(buttons))
            elif self.toolbar == EditorToolbar.CUSTOM:
                if any(b in buttons for b in self._custom_toolbar):
                    groups.append(self._render_toolbar_group([b for b in buttons if b in self._custom_toolbar]))
            else:  # FULL
                groups.append(self._render_toolbar_group(buttons))
        
        return f'<div class="rich-editor-toolbar">{"".join(groups)}</div>'
    
    def _render_toolbar_group(self, buttons: List[str]) -> str:
        """Render a toolbar button group."""
        button_html = []
        for btn in buttons:
            icon = self._get_button_icon(btn)
            button_html.append(f'<button type="button" class="toolbar-btn" data-action="{btn}" title="{btn.replace("-", " ").title()}">{icon}</button>')
        
        return f'<div class="toolbar-group">{"".join(button_html)}</div>'
    
    def _get_button_icon(self, button: str) -> str:
        """Get icon for toolbar button."""
        icons = {
            "bold": "<strong>B</strong>",
            "italic": "<em>I</em>",
            "underline": "<u>U</u>",
            "strikethrough": "<s>S</s>",
            "h1": "<strong>H1</strong>",
            "h2": "<strong>H2</strong>",
            "h3": "<strong>H3</strong>",
            "h4": "<strong>H4</strong>",
            "h5": "<strong>H5</strong>",
            "h6": "<strong>H6</strong>",
            "unordered-list": "&#8226;",
            "ordered-list": "1.",
            "indent": "&#8677;",
            "outdent": "&#8676;",
            "align-left": "&#8676;",
            "align-center": "&#8596;",
            "align-right": "&#8677;",
            "align-justify": "&#9776;",
            "link": "&#128279;",
            "unlink": "&#128279;",
            "image": "&#128247;",
            "table": "&#9638;",
            "code": "&lt;/&gt;",
            "code-block": "&#9618;",
            "blockquote": "&#8220;",
            "undo": "&#8630;",
            "redo": "&#8631;",
            "clear-formatting": "&#10006;",
        }
        return icons.get(button, button)
    
    def generate_js_code(self) -> str:
        """Generate JavaScript for editor."""
        config = self.to_dict()
        return f"""
        // Rich Text Editor
        (function() {{
            const config = {str(config).replace("'", '"')};
            
            const editor = document.getElementById('rich-editor');
            if (!editor) return;
            
            // Toolbar actions
            document.querySelectorAll('.toolbar-btn').forEach(btn => {{
                btn.addEventListener('click', () => {{
                    const action = btn.dataset.action;
                    
                    switch (action) {{
                        case 'bold':
                            document.execCommand('bold');
                            break;
                        case 'italic':
                            document.execCommand('italic');
                            break;
                        case 'underline':
                            document.execCommand('underline');
                            break;
                        case 'strikethrough':
                            document.execCommand('strikeThrough');
                            break;
                        case 'h1':
                            document.execCommand('formatBlock', false, '<h1>');
                            break;
                        case 'h2':
                            document.execCommand('formatBlock', false, '<h2>');
                            break;
                        case 'h3':
                            document.execCommand('formatBlock', false, '<h3>');
                            break;
                        case 'h4':
                            document.execCommand('formatBlock', false, '<h4>');
                            break;
                        case 'h5':
                            document.execCommand('formatBlock', false, '<h5>');
                            break;
                        case 'h6':
                            document.execCommand('formatBlock', false, '<h6>');
                            break;
                        case 'unordered-list':
                            document.execCommand('insertUnorderedList');
                            break;
                        case 'ordered-list':
                            document.execCommand('insertOrderedList');
                            break;
                        case 'indent':
                            document.execCommand('indent');
                            break;
                        case 'outdent':
                            document.execCommand('outdent');
                            break;
                        case 'align-left':
                            document.execCommand('justifyLeft');
                            break;
                        case 'align-center':
                            document.execCommand('justifyCenter');
                            break;
                        case 'align-right':
                            document.execCommand('justifyRight');
                            break;
                        case 'align-justify':
                            document.execCommand('justifyFull');
                            break;
                        case 'link':
                            const url = prompt('Enter URL:');
                            if (url) {{
                                document.execCommand('createLink', false, url);
                            }}
                            break;
                        case 'unlink':
                            document.execCommand('unlink');
                            break;
                        case 'code':
                            document.execCommand('formatBlock', false, '<code>');
                            break;
                        case 'blockquote':
                            document.execCommand('formatBlock', false, '<blockquote>');
                            break;
                        case 'clear-formatting':
                            document.execCommand('removeFormat');
                            break;
                    }}
                    
                    btn.classList.toggle('active');
                    editor.focus();
                }});
            }});
            
            // Content change detection
            editor.addEventListener('input', () => {{
                const content = editor.innerHTML;
                console.log('Content changed:', content);
            }});
            
            // Placeholder handling
            editor.addEventListener('focus', () => {{
                if (editor.innerHTML === '<p class="placeholder">' + config.placeholder + '</p>') {{
                    editor.innerHTML = '';
                }}
            }});
            
            editor.addEventListener('blur', () => {{
                if (editor.innerHTML.trim() === '') {{
                    editor.innerHTML = '<p class="placeholder">' + config.placeholder + '</p>';
                }}
            }});
        }})();
        """


def create_editor(content: str = "", placeholder: str = "Type here...", toolbar: EditorToolbar = EditorToolbar.FULL) -> RichTextEditor:
    """Create a rich text editor."""
    return RichTextEditor(content, placeholder, toolbar)


def create_markdown_editor(content: str = "", placeholder: str = "Type in markdown...") -> RichTextEditor:
    """Create a markdown editor."""
    return RichTextEditor(content, placeholder, EditorToolbar.MINIMAL).format(EditorFormat.MARKDOWN)


RICH_EDITOR_CSS = """
.rich-editor-container {
    border: 1px solid #d1d5db;
    border-radius: 0.375rem;
    overflow: hidden;
}

.rich-editor-toolbar {
    display: flex;
    flex-wrap: wrap;
    gap: 0.25rem;
    padding: 0.5rem;
    background-color: #f9fafb;
    border-bottom: 1px solid #e5e7eb;
}

.toolbar-group {
    display: flex;
    gap: 0.125rem;
}

.toolbar-group:not(:last-child)::after {
    content: '';
    width: 1px;
    background-color: #e5e7eb;
    margin: 0 0.25rem;
}

.toolbar-btn {
    padding: 0.375rem 0.625rem;
    border: none;
    background: transparent;
    border-radius: 0.25rem;
    cursor: pointer;
    color: #374151;
    font-size: 0.875rem;
    line-height: 1;
    transition: background-color 0.15s ease;
}

.toolbar-btn:hover {
    background-color: #e5e7eb;
}

.toolbar-btn.active {
    background-color: #d1d5db;
}

.rich-editor {
    padding: 1rem;
    outline: none;
    overflow-y: auto;
    font-size: 1rem;
    line-height: 1.5;
}

.rich-editor .placeholder {
    color: #9ca3af;
    pointer-events: none;
}

.rich-editor:focus {
    outline: none;
}

.rich-editor h1 { font-size: 2rem; font-weight: bold; margin: 0.5rem 0; }
.rich-editor h2 { font-size: 1.5rem; font-weight: bold; margin: 0.5rem 0; }
.rich-editor h3 { font-size: 1.25rem; font-weight: bold; margin: 0.5rem 0; }
.rich-editor h4 { font-size: 1rem; font-weight: bold; margin: 0.5rem 0; }
.rich-editor h5 { font-size: 0.875rem; font-weight: bold; margin: 0.5rem 0; }
.rich-editor h6 { font-size: 0.75rem; font-weight: bold; margin: 0.5rem 0; }

.rich-editor ul, .rich-editor ol {
    margin: 0.5rem 0;
    padding-left: 2rem;
}

.rich-editor li {
    margin: 0.25rem 0;
}

.rich-editor blockquote {
    border-left: 4px solid #e5e7eb;
    margin: 1rem 0;
    padding: 0.5rem 1rem;
    background-color: #f9fafb;
    color: #6b7280;
}

.rich-editor code {
    font-family: monospace;
    background-color: #f3f4f6;
    padding: 0.125rem 0.25rem;
    border-radius: 0.25rem;
    font-size: 0.875em;
}

.rich-editor pre {
    background-color: #1f2937;
    color: #f9fafb;
    padding: 1rem;
    border-radius: 0.375rem;
    overflow-x: auto;
    font-family: monospace;
}

.rich-editor a {
    color: #3b82f6;
    text-decoration: underline;
}

.rich-editor img {
    max-width: 100%;
    height: auto;
    border-radius: 0.375rem;
}

.rich-editor table {
    width: 100%;
    border-collapse: collapse;
    margin: 1rem 0;
}

.rich-editor table th,
.rich-editor table td {
    border: 1px solid #e5e7eb;
    padding: 0.5rem;
    text-align: left;
}

.rich-editor table th {
    background-color: #f9fafb;
    font-weight: 600;
}
"""
