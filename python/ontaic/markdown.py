"""Markdown editor with live preview."""
from typing import Any, Callable, Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum


class MarkdownViewMode(str, Enum):
    """Markdown view mode."""
    EDIT = "edit"
    PREVIEW = "preview"
    SPLIT = "split"


@dataclass
class MarkdownToolbarItem:
    """Markdown toolbar item."""
    name: str
    icon: str
    action: str
    tooltip: str = ""
    group: str = ""
    
    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "icon": self.icon,
            "action": self.action,
            "tooltip": self.tooltip,
            "group": self.group,
        }


DEFAULT_TOOLBAR = [
    MarkdownToolbarItem("bold", "<strong>B</strong>", "bold", "Bold", "format"),
    MarkdownToolbarItem("italic", "<em>I</em>", "italic", "Italic", "format"),
    MarkdownToolbarItem("strikethrough", "<s>S</s>", "strikethrough", "Strikethrough", "format"),
    MarkdownToolbarItem("h1", "<strong>H1</strong>", "heading1", "Heading 1", "heading"),
    MarkdownToolbarItem("h2", "<strong>H2</strong>", "heading2", "Heading 2", "heading"),
    MarkdownToolbarItem("h3", "<strong>H3</strong>", "heading3", "Heading 3", "heading"),
    MarkdownToolbarItem("ul", "&#8226;", "unorderedList", "Unordered List", "list"),
    MarkdownToolbarItem("ol", "1.", "orderedList", "Ordered List", "list"),
    MarkdownToolbarItem("checklist", "&#9745;", "checklist", "Checklist", "list"),
    MarkdownToolbarItem("quote", "&#8220;", "blockquote", "Quote", "block"),
    MarkdownToolbarItem("code", "&lt;/&gt;", "code", "Inline Code", "block"),
    MarkdownToolbarItem("codeblock", "&#9618;", "codeBlock", "Code Block", "block"),
    MarkdownToolbarItem("link", "&#128279;", "link", "Link", "insert"),
    MarkdownToolbarItem("image", "&#128247;", "image", "Image", "insert"),
    MarkdownToolbarItem("table", "&#9638;", "table", "Table", "insert"),
    MarkdownToolbarItem("hr", "&#8212;", "horizontalRule", "Horizontal Rule", "insert"),
]


class MarkdownEditor:
    """Markdown editor with live preview."""
    
    def __init__(self, content: str = "", placeholder: str = "Write your markdown here..."):
        self.content = content
        self.placeholder = placeholder
        self._view_mode: MarkdownViewMode = MarkdownViewMode.SPLIT
        self._toolbar: List[MarkdownToolbarItem] = DEFAULT_TOOLBAR
        self._on_change: Optional[Callable] = None
        self._on_save: Optional[Callable] = None
        self._height: int = 400
        self._disabled: bool = False
        self._class_name: str = ""
        self._label: str = ""
        self._help_text: str = ""
        self._syntax_highlight: bool = True
        self._line_numbers: bool = False
        self._word_wrap: bool = True
        self._tab_size: int = 4
        self._auto_preview: bool = True
        self._preview_debounce: int = 300
        self._theme: str = "light"
    
    def view_mode(self, mode: MarkdownViewMode) -> "MarkdownEditor":
        """Set view mode."""
        self._view_mode = mode
        return self
    
    def toolbar(self, items: List[MarkdownToolbarItem]) -> "MarkdownEditor":
        """Set toolbar items."""
        self._toolbar = items
        return self
    
    def on_change(self, callback: Callable) -> "MarkdownEditor":
        """Set change handler."""
        self._on_change = callback
        return self
    
    def on_save(self, callback: Callable) -> "MarkdownEditor":
        """Set save handler."""
        self._on_save = callback
        return self
    
    def height(self, height: int) -> "MarkdownEditor":
        """Set height."""
        self._height = height
        return self
    
    def disabled(self) -> "MarkdownEditor":
        """Make disabled."""
        self._disabled = True
        return self
    
    def class_name(self, class_name: str) -> "MarkdownEditor":
        """Set CSS class."""
        self._class_name = class_name
        return self
    
    def label(self, label: str) -> "MarkdownEditor":
        """Set label."""
        self._label = label
        return self
    
    def help_text(self, text: str) -> "MarkdownEditor":
        """Set help text."""
        self._help_text = text
        return self
    
    def syntax_highlight(self, highlight: bool = True) -> "MarkdownEditor":
        """Enable syntax highlighting."""
        self._syntax_highlight = highlight
        return self
    
    def line_numbers(self, show: bool = True) -> "MarkdownEditor":
        """Show line numbers."""
        self._line_numbers = show
        return self
    
    def word_wrap(self, wrap: bool = True) -> "MarkdownEditor":
        """Enable word wrap."""
        self._word_wrap = wrap
        return self
    
    def theme(self, theme: str) -> "MarkdownEditor":
        """Set theme (light, dark)."""
        self._theme = theme
        return self
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "content": self.content,
            "placeholder": self.placeholder,
            "viewMode": self._view_mode.value,
            "toolbar": [item.to_dict() for item in self._toolbar],
            "height": self._height,
            "disabled": self._disabled,
            "className": self._class_name,
            "label": self._label,
            "helpText": self._help_text,
            "syntaxHighlight": self._syntax_highlight,
            "lineNumbers": self._line_numbers,
            "wordWrap": self._word_wrap,
            "tabSize": self._tab_size,
            "autoPreview": self._auto_preview,
            "theme": self._theme,
        }
    
    def to_html(self) -> str:
        """Generate HTML."""
        label_html = f'<label class="md-editor-label">{self._label}</label>' if self._label else ""
        help_html = f'<p class="md-editor-help">{self._help_text}</p>' if self._help_text else ""
        disabled_class = " disabled" if self._disabled else ""
        class_attr = f" {self._class_name}" if self._class_name else ""
        theme_class = f" md-theme-{self._theme}"
        
        # Toolbar
        toolbar_html = ""
        if self._toolbar:
            buttons = []
            for item in self._toolbar:
                buttons.append(f'<button type="button" class="md-toolbar-btn" data-action="{item.action}" title="{item.tooltip}">{item.icon}</button>')
            toolbar_html = f'<div class="md-toolbar">{"".join(buttons)}</div>'
        
        # View mode buttons
        view_buttons = f'''<div class="md-view-buttons">
            <button type="button" class="md-view-btn" data-mode="edit">Edit</button>
            <button type="button" class="md-view-btn active" data-mode="split">Split</button>
            <button type="button" class="md-view-btn" data-mode="preview">Preview</button>
        </div>'''
        
        # Editor and preview
        editor_class = f"md-editor-pane{' active' if self._view_mode in [MarkdownViewMode.EDIT, MarkdownViewMode.SPLIT] else ''}"
        preview_class = f"md-preview-pane{' active' if self._view_mode in [MarkdownViewMode.PREVIEW, MarkdownViewMode.SPLIT] else ''}"
        
        editor_html = f'''<div class="md-editor-area">
            <textarea class="md-textarea" placeholder="{self.placeholder}" style="height: {self._height}px">{'{' + '}' if not self.content else self.content}</textarea>
        </div>'''
        
        preview_html = f'''<div class="md-preview-area">
            <div class="md-preview-content" style="min-height: {self._height}px"></div>
        </div>'''
        
        return f'''<div class="md-editor{disabled_class}{class_attr}{theme_class}">
            {label_html}
            <div class="md-header">
                {toolbar_html}
                {view_buttons}
            </div>
            <div class="md-body">
                <div class="{editor_class}">{editor_html}</div>
                <div class="{preview_class}">{preview_html}</div>
            </div>
            <input type="hidden" name="markdown_content" value="{self.content}">
            {help_html}
        </div>'''
    
    def generate_js_code(self) -> str:
        """Generate JavaScript."""
        config = self.to_dict()
        return f"""
        // Markdown Editor
        (function() {{
            const config = {str(config).replace("'", '"')};
            
            const editor = document.querySelector('.md-editor');
            if (!editor) return;
            
            const textarea = editor.querySelector('.md-textarea');
            const preview = editor.querySelector('.md-preview-content');
            const hidden = editor.querySelector('input[type="hidden"]');
            
            // Markdown parser
            function parseMarkdown(md) {{
                let html = md;
                
                // Headers
                html = html.replace(/^### (.+)$/gm, '<h3>$1</h3>');
                html = html.replace(/^## (.+)$/gm, '<h2>$1</h2>');
                html = html.replace(/^# (.+)$/gm, '<h1>$1</h1>');
                
                // Bold and italic
                html = html.replace(/\\*\\*(.+?)\\*\\*/g, '<strong>$1</strong>');
                html = html.replace(/\\*(.+?)\\*/g, '<em>$1</em>');
                html = html.replace(/~~(.+?)~~/g, '<del>$1</del>');
                
                // Code
                html = html.replace(/`([^`]+)`/g, '<code>$1</code>');
                html = html.replace(/^```(\\w*)\\n([\\s\\S]*?)^```/gm, '<pre><code class="language-$1">$2</code></pre>');
                
                // Lists
                html = html.replace(/^\\* (.+)$/gm, '<li>$1</li>');
                html = html.replace(/^\\d+\\. (.+)$/gm, '<li>$1</li>');
                
                // Blockquote
                html = html.replace(/^> (.+)$/gm, '<blockquote>$1</blockquote>');
                
                // Links and images
                html = html.replace(/\\[(.+)\\]\\((.+)\\)/g, '<a href="$2">$1</a>');
                html = html.replace(/!\\[(.+)\\]\\((.+)\\)/g, '<img src="$2" alt="$1">');
                
                // Horizontal rule
                html = html.replace(/^---$/gm, '<hr>');
                html = html.replace(/^\\*\\*\\*$/gm, '<hr>');
                
                // Paragraphs
                html = html.replace(/\\n\\n/g, '</p><p>');
                html = '<p>' + html + '</p>';
                
                // Line breaks
                html = html.replace(/\\n/g, '<br>');
                
                return html;
            }}
            
            // Update preview
            function updatePreview() {{
                if (textarea && preview) {{
                    preview.innerHTML = parseMarkdown(textarea.value);
                    if (hidden) hidden.value = textarea.value;
                }}
            }}
            
            // Toolbar actions
            editor.querySelectorAll('.md-toolbar-btn').forEach(btn => {{
                btn.addEventListener('click', () => {{
                    const action = btn.dataset.action;
                    const start = textarea.selectionStart;
                    const end = textarea.selectionEnd;
                    const selected = textarea.value.substring(start, end);
                    
                    let replacement = selected;
                    
                    switch (action) {{
                        case 'bold':
                            replacement = '**' + selected + '**';
                            break;
                        case 'italic':
                            replacement = '*' + selected + '*';
                            break;
                        case 'strikethrough':
                            replacement = '~~' + selected + '~~';
                            break;
                        case 'heading1':
                            replacement = '# ' + selected;
                            break;
                        case 'heading2':
                            replacement = '## ' + selected;
                            break;
                        case 'heading3':
                            replacement = '### ' + selected;
                            break;
                        case 'unorderedList':
                            replacement = '- ' + selected;
                            break;
                        case 'orderedList':
                            replacement = '1. ' + selected;
                            break;
                        case 'link':
                            replacement = '[' + selected + '](url)';
                            break;
                        case 'image':
                            replacement = '![' + selected + '](url)';
                            break;
                        case 'code':
                            replacement = '`' + selected + '`';
                            break;
                        case 'blockquote':
                            replacement = '> ' + selected;
                            break;
                    }}
                    
                    textarea.value = textarea.value.substring(0, start) + replacement + textarea.value.substring(end);
                    updatePreview();
                    textarea.focus();
                }});
            }});
            
            // View mode buttons
            editor.querySelectorAll('.md-view-btn').forEach(btn => {{
                btn.addEventListener('click', () => {{
                    editor.querySelectorAll('.md-view-btn').forEach(b => b.classList.remove('active'));
                    btn.classList.add('active');
                    
                    const mode = btn.dataset.mode;
                    const editorPane = editor.querySelector('.md-editor-pane');
                    const previewPane = editor.querySelector('.md-preview-pane');
                    
                    editorPane.classList.toggle('active', mode === 'edit' || mode === 'split');
                    previewPane.classList.toggle('active', mode === 'preview' || mode === 'split');
                }});
            }});
            
            // Text input
            if (textarea) {{
                textarea.addEventListener('input', updatePreview);
                updatePreview();
            }}
        }})();
        """


def create_markdown_editor(content: str = "", placeholder: str = "Write your markdown here...") -> MarkdownEditor:
    """Create a markdown editor."""
    return MarkdownEditor(content, placeholder)


MARKDOWN_EDITOR_CSS = """
.md-editor {
    border: 1px solid #d1d5db;
    border-radius: 0.5rem;
    overflow: hidden;
}

.md-editor-label {
    display: block;
    padding: 0.75rem 1rem 0;
    font-weight: 500;
    color: #374151;
}

.md-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.5rem;
    background: #f9fafb;
    border-bottom: 1px solid #e5e7eb;
}

.md-toolbar {
    display: flex;
    gap: 0.25rem;
}

.md-toolbar-btn {
    padding: 0.375rem 0.625rem;
    background: transparent;
    border: none;
    border-radius: 0.25rem;
    cursor: pointer;
    color: #374151;
    font-size: 0.875rem;
}

.md-toolbar-btn:hover {
    background: #e5e7eb;
}

.md-view-buttons {
    display: flex;
    gap: 0.25rem;
}

.md-view-btn {
    padding: 0.375rem 0.75rem;
    background: transparent;
    border: 1px solid #d1d5db;
    border-radius: 0.25rem;
    cursor: pointer;
    font-size: 0.875rem;
}

.md-view-btn.active {
    background: #3b82f6;
    color: white;
    border-color: #3b82f6;
}

.md-body {
    display: flex;
}

.md-editor-pane,
.md-preview-pane {
    display: none;
}

.md-editor-pane.active {
    flex: 1;
    display: block;
}

.md-preview-pane.active {
    flex: 1;
    display: block;
    border-left: 1px solid #e5e7eb;
}

.md-textarea {
    width: 100%;
    padding: 1rem;
    border: none;
    resize: none;
    font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
    font-size: 0.875rem;
    line-height: 1.6;
    outline: none;
}

.md-textarea:focus {
    outline: none;
}

.md-preview-area {
    padding: 1rem;
}

.md-preview-content h1 { font-size: 2rem; font-weight: bold; margin: 1rem 0; }
.md-preview-content h2 { font-size: 1.5rem; font-weight: bold; margin: 1rem 0; }
.md-preview-content h3 { font-size: 1.25rem; font-weight: bold; margin: 1rem 0; }

.md-preview-content p {
    margin: 0.5rem 0;
    line-height: 1.6;
}

.md-preview-content strong {
    font-weight: 600;
}

.md-preview-content em {
    font-style: italic;
}

.md-preview-content del {
    text-decoration: line-through;
}

.md-preview-content code {
    font-family: monospace;
    background: #f3f4f6;
    padding: 0.125rem 0.375rem;
    border-radius: 0.25rem;
    font-size: 0.875em;
}

.md-preview-content pre {
    background: #1f2937;
    color: #f9fafb;
    padding: 1rem;
    border-radius: 0.375rem;
    overflow-x: auto;
}

.md-preview-content pre code {
    background: transparent;
    padding: 0;
    color: inherit;
}

.md-preview-content blockquote {
    border-left: 4px solid #e5e7eb;
    margin: 1rem 0;
    padding: 0.5rem 1rem;
    background: #f9fafb;
    color: #6b7280;
}

.md-preview-content img {
    max-width: 100%;
    border-radius: 0.375rem;
}

.md-preview-content a {
    color: #3b82f6;
    text-decoration: underline;
}

.md-preview-content hr {
    border: none;
    border-top: 1px solid #e5e7eb;
    margin: 1.5rem 0;
}

.md-preview-content ul,
.md-preview-content ol {
    margin: 0.5rem 0;
    padding-left: 2rem;
}

.md-preview-content li {
    margin: 0.25rem 0;
}

.md-editor-help {
    padding: 0 1rem 0.75rem;
    font-size: 0.875rem;
    color: #6b7280;
}

/* Dark theme */
.md-theme-dark .md-editor {
    background: #1f2937;
    border-color: #374151;
}

.md-theme-dark .md-header {
    background: #111827;
    border-color: #374151;
}

.md-theme-dark .md-textarea {
    color: #f9fafb;
    background: #1f2937;
}

.md-theme-dark .md-preview-content {
    color: #f9fafb;
}

.md-theme-dark .md-preview-content code {
    background: #374151;
}

.md-theme-dark .md-preview-content pre {
    background: #111827;
}

.md-theme-dark .md-preview-content blockquote {
    background: #374151;
    color: #d1d5db;
}
"""
