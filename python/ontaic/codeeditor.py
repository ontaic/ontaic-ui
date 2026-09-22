"""Code editor component with syntax highlighting."""
from typing import Any, Callable, Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum


class CodeLanguage(str, Enum):
    """Supported programming languages."""
    JAVASCRIPT = "javascript"
    TYPESCRIPT = "typescript"
    PYTHON = "python"
    HTML = "html"
    CSS = "css"
    JSON = "json"
    MARKDOWN = "markdown"
    SQL = "sql"
    JAVA = "java"
    CPP = "cpp"
    CSHARP = "csharp"
    GO = "go"
    RUST = "rust"
    RUBY = "ruby"
    PHP = "php"
    SWIFT = "swift"
    KOTLIN = "kotlin"
    SHELL = "shell"
    YAML = "yaml"
    XML = "xml"
    PLAINTEXT = "plaintext"


class EditorTheme(str, Enum):
    """Editor themes."""
    LIGHT = "light"
    DARK = "dark"
    VS_DARK = "vs-dark"
    HIGH_CONTRAST = "hc-black"
    MONOKAI = "monokai"
    DRACULA = "dracula"
    SOLARIZED = "solarized"
    NORD = "nord"
    ONE_DARK = "one-dark"
    GITHUB = "github"


class EditorFontSize(int):
    """Editor font size."""
    pass


@dataclass
class EditorKeyBinding:
    """Editor key binding."""
    key: str
    command: str
    when: str = ""
    
    def to_dict(self) -> dict:
        return {"key": self.key, "command": self.command, "when": self.when}


@dataclass
class EditorSnippet:
    """Editor snippet/prefix."""
    prefix: str
    body: str
    description: str = ""
    
    def to_dict(self) -> dict:
        return {"prefix": self.prefix, "body": self.body, "description": self.description}


DEFAULT_SNIPPETS = {
    "javascript": [
        EditorSnippet("fn", "function ${1:name}(${2:params}) {\n\t${3}\n}", "Function declaration"),
        EditorSnippet("afn", "(${1:params}) => {\n\t${2}\n}", "Arrow function"),
        EditorSnippet("cl", "console.log(${1:value});", "Console log"),
        EditorSnippet("for", "for (let ${1:i} = 0; ${1:i} < ${2:array}.length; ${1:i}++) {\n\t${3}\n}", "For loop"),
        EditorSnippet("if", "if (${1:condition}) {\n\t${2}\n}", "If statement"),
    ],
    "python": [
        EditorSnippet("def", "def ${1:name}(${2:params}):\n\t${3}", "Function definition"),
        EditorSnippet("class", "class ${1:Name}:\n\tdef __init__(self${2:}):\n\t\t${3}", "Class definition"),
        EditorSnippet("print", "print(${1:value})", "Print statement"),
        EditorSnippet("for", "for ${1:item} in ${2:iterable}:\n\t${3}", "For loop"),
        EditorSnippet("if", "if ${1:condition}:\n\t${2}", "If statement"),
    ],
    "html": [
        EditorSnippet("div", "<div ${1:class=\"${2}\"}>\n\t${3}\n</div>", "Div element"),
        EditorSnippet("a", "<a href=\"${1:url}\" ${2}>${3}</a>", "Anchor element"),
        EditorSnippet("img", "<img src=\"${1:url}\" alt=\"${2}\" />", "Image element"),
    ],
}


class CodeEditor:
    """Code editor component with syntax highlighting."""
    
    def __init__(self, code: str = "", language: CodeLanguage = CodeLanguage.JAVASCRIPT):
        self.code = code
        self.language = language
        self._theme: EditorTheme = EditorTheme.LIGHT
        self._font_size: int = 14
        self._tab_size: int = 4
        self._minimap: bool = True
        self._line_numbers: bool = True
        self._word_wrap: bool = False
        self._read_only: bool = False
        self._auto_save: bool = False
        self._format_on_save: bool = False
        self._bracket_matching: bool = True
        self._auto_close_brackets: bool = True
        self._auto_close_quotes: bool = True
        self._highlight_active_line: bool = True
        self._show_cursor_blinking: bool = True
        self._cursor_style: str = "line"
        self._padding: Dict[str, int] = field(default_factory=lambda: {"top": 10, "bottom": 10})
        self._scroll_beyond_last_line: bool = False
        self._smooth_scrolling: bool = True
        self._snippets: Dict[str, List[EditorSnippet]] = DEFAULT_SNIPPETS.copy()
        self._key_bindings: List[EditorKeyBinding] = []
        self._on_change: Optional[Callable] = None
        self._on_save: Optional[Callable] = None
        self._on_cursor_change: Optional[Callable] = None
        self._on_selection_change: Optional[Callable] = None
        self._on_scroll: Optional[Callable] = None
        self._height: int = 400
        self._width: str = "100%"
        self._class_name: str = ""
        self._label: str = ""
        self._help_text: str = ""
        self._disabled: bool = False
        self._placeholder: str = ""
        self._language_selector: bool = False
        self._theme_selector: bool = False
        self._export_path: str = ""
        self._linter: bool = False
        self._formatter: bool = False
    
    def theme(self, theme: EditorTheme) -> "CodeEditor":
        """Set editor theme."""
        self._theme = theme
        return self
    
    def font_size(self, size: int) -> "CodeEditor":
        """Set font size."""
        self._font_size = size
        return self
    
    def tab_size(self, size: int) -> "CodeEditor":
        """Set tab size."""
        self._tab_size = size
        return self
    
    def minimap(self, show: bool = True) -> "CodeEditor":
        """Toggle minimap."""
        self._minimap = show
        return self
    
    def line_numbers(self, show: bool = True) -> "CodeEditor":
        """Toggle line numbers."""
        self._line_numbers = show
        return self
    
    def word_wrap(self, wrap: bool = True) -> "CodeEditor":
        """Toggle word wrap."""
        self._word_wrap = wrap
        return self
    
    def read_only(self, readonly: bool = True) -> "CodeEditor":
        """Toggle read-only mode."""
        self._read_only = readonly
        return self
    
    def auto_save(self, auto: bool = True) -> "CodeEditor":
        """Toggle auto-save."""
        self._auto_save = auto
        return self
    
    def format_on_save(self, fmt: bool = True) -> "CodeEditor":
        """Toggle format on save."""
        self._format_on_save = fmt
        return self
    
    def bracket_matching(self, match: bool = True) -> "CodeEditor":
        """Toggle bracket matching."""
        self._bracket_matching = match
        return self
    
    def auto_close_brackets(self, auto: bool = True) -> "CodeEditor":
        """Toggle auto-close brackets."""
        self._auto_close_brackets = auto
        return self
    
    def height(self, height: int) -> "CodeEditor":
        """Set editor height."""
        self._height = height
        return self
    
    def width(self, width: str) -> "CodeEditor":
        """Set editor width."""
        self._width = width
        return self
    
    def on_change(self, callback: Callable) -> "CodeEditor":
        """Set change handler."""
        self._on_change = callback
        return self
    
    def on_save(self, callback: Callable) -> "CodeEditor":
        """Set save handler (Ctrl+S)."""
        self._on_save = callback
        return self
    
    def on_cursor_change(self, callback: Callable) -> "CodeEditor":
        """Set cursor change handler."""
        self._on_cursor_change = callback
        return self
    
    def class_name(self, class_name: str) -> "CodeEditor":
        """Set CSS class."""
        self._class_name = class_name
        return self
    
    def label(self, label: str) -> "CodeEditor":
        """Set label."""
        self._label = label
        return self
    
    def help_text(self, text: str) -> "CodeEditor":
        """Set help text."""
        self._help_text = text
        return self
    
    def disabled(self) -> "CodeEditor":
        """Make disabled."""
        self._disabled = True
        return self
    
    def language_selector(self, show: bool = True) -> "CodeEditor":
        """Show language selector."""
        self._language_selector = show
        return self
    
    def theme_selector(self, show: bool = True) -> "CodeEditor":
        """Show theme selector."""
        self._theme_selector = show
        return self
    
    def add_snippet(self, language: str, snippet: EditorSnippet):
        """Add snippet for language."""
        if language not in self._snippets:
            self._snippets[language] = []
        self._snippets[language].append(snippet)
    
    def add_key_binding(self, binding: EditorKeyBinding):
        """Add key binding."""
        self._key_bindings.append(binding)
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "code": self.code,
            "language": self.language.value,
            "theme": self._theme.value,
            "fontSize": self._font_size,
            "tabSize": self._tab_size,
            "minimap": self._minimap,
            "lineNumbers": self._line_numbers,
            "wordWrap": self._word_wrap,
            "readOnly": self._read_only,
            "autoSave": self._auto_save,
            "formatOnSave": self._format_on_save,
            "bracketMatching": self._bracket_matching,
            "autoCloseBrackets": self._auto_close_brackets,
            "autoCloseQuotes": self._auto_close_quotes,
            "highlightActiveLine": self._highlight_active_line,
            "cursorStyle": self._cursor_style,
            "padding": self._padding,
            "scrollBeyondLastLine": self._scroll_beyond_last_line,
            "smoothScrolling": self._smooth_scrolling,
            "height": self._height,
            "width": self._width,
            "className": self._class_name,
            "label": self._label,
            "helpText": self._help_text,
            "disabled": self._disabled,
            "languageSelector": self._language_selector,
            "themeSelector": self._theme_selector,
            "snippets": {k: [s.to_dict() for s in v] for k, v in self._snippets.items()},
            "keyBindings": [kb.to_dict() for kb in self._key_bindings],
        }
    
    def to_html(self) -> str:
        """Generate HTML."""
        label_html = f'<label class="code-editor-label">{self._label}</label>' if self._label else ""
        help_html = f'<p class="code-editor-help">{self._help_text}</p>' if self._help_text else ""
        disabled_class = " disabled" if self._disabled else ""
        class_attr = f" {self._class_name}" if self._class_name else ""
        
        # Language selector
        lang_selector = ""
        if self._language_selector:
            languages = [lang.value for lang in CodeLanguage]
            options = "".join(f'<option value="{l}"{" selected" if l == self.language.value else ""}>{l}</option>' for l in languages)
            lang_selector = f'<select class="code-editor-lang-select">{options}</select>'
        
        # Theme selector
        theme_selector = ""
        if self._theme_selector:
            themes = [t.value for t in EditorTheme]
            options = "".join(f'<option value="{t}"{" selected" if t == self._theme.value else ""}>{t}</option>' for t in themes)
            theme_selector = f'<select class="code-editor-theme-select">{options}</select>'
        
        toolbar = ""
        if lang_selector or theme_selector:
            toolbar = f'<div class="code-editor-toolbar">{lang_selector}{theme_selector}</div>'
        
        return f'''<div class="code-editor{disabled_class}{class_attr}" style="height: {self._height}px; width: {self._width};">
            {label_html}
            {toolbar}
            <div class="code-editor-wrapper">
                <div class="code-editor-gutter"></div>
                <textarea class="code-editor-textarea" spellcheck="false" placeholder="{self._placeholder}">{self.code}</textarea>
                <pre class="code-editor-highlight"><code></code></pre>
            </div>
            {help_html}
        </div>'''
    
    def generate_js_code(self) -> str:
        """Generate JavaScript."""
        config = self.to_dict()
        return f"""
        // Code Editor
        (function() {{
            const config = {str(config).replace("'", '"')};
            
            const editor = document.querySelector('.code-editor');
            if (!editor) return;
            
            const textarea = editor.querySelector('.code-editor-textarea');
            const highlight = editor.querySelector('.code-editor-highlight code');
            const gutter = editor.querySelector('.code-editor-gutter');
            
            // Syntax highlighting (basic)
            const keywords = {{
                javascript: ['const', 'let', 'var', 'function', 'return', 'if', 'else', 'for', 'while', 'switch', 'case', 'break', 'continue', 'class', 'new', 'this', 'import', 'export', 'default', 'from', 'async', 'await', 'try', 'catch', 'finally', 'throw', 'typeof', 'instanceof', 'in', 'of', 'true', 'false', 'null', 'undefined'],
                python: ['def', 'class', 'return', 'if', 'elif', 'else', 'for', 'while', 'import', 'from', 'as', 'try', 'except', 'finally', 'raise', 'with', 'lambda', 'pass', 'break', 'continue', 'True', 'False', 'None', 'and', 'or', 'not', 'in', 'is', 'self'],
                html: ['html', 'head', 'body', 'div', 'span', 'p', 'a', 'img', 'ul', 'li', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'table', 'tr', 'td', 'th', 'form', 'input', 'button', 'select', 'option', 'textarea'],
                css: ['color', 'background', 'margin', 'padding', 'border', 'display', 'flex', 'grid', 'position', 'width', 'height', 'font-size', 'font-weight', 'text-align', 'justify-content', 'align-items'],
            }};
            
            function highlightCode(code, lang) {{
                let highlighted = code
                    .replace(/&/g, '&amp;')
                    .replace(/</g, '&lt;')
                    .replace(/>/g, '&gt;');
                
                // Strings
                highlighted = highlighted.replace(/(["'`])(?:(?!\\1).|\\.)*\\1/g, '<span class="string">$&</span>');
                
                // Comments
                if (lang === 'python') {{
                    highlighted = highlighted.replace(/(#.*)$/gm, '<span class="comment">$&</span>');
                }} else {{
                    highlighted = highlighted.replace(/(\\/{2}.*$)/gm, '<span class="comment">$&</span>');
                    highlighted = highlighted.replace(/(\\/\\*[\\s\\S]*?\\*\\/)/g, '<span class="comment">$&</span>');
                }}
                
                // Keywords
                const kws = keywords[lang] || keywords['javascript'];
                kws.forEach(kw => {{
                    const regex = new RegExp('\\\\b' + kw + '\\\\b', 'g');
                    highlighted = highlighted.replace(regex, '<span class="keyword">$&</span>');
                }});
                
                // Numbers
                highlighted = highlighted.replace(/\\b(\\d+\\.?\\d*)\\b/g, '<span class="number">$&</span>');
                
                return highlighted;
            }}
            
            function updateHighlight() {{
                if (highlight) {{
                    highlight.innerHTML = highlightCode(textarea.value, config.language);
                }}
                updateGutter();
            }}
            
            function updateGutter() {{
                if (!gutter) return;
                const lines = textarea.value.split('\\n').length;
                let gutterHtml = '';
                for (let i = 1; i <= lines; i++) {{
                    gutterHtml += '<div class="gutter-line">' + i + '</div>';
                }}
                gutter.innerHTML = gutterHtml;
            }}
            
            // Sync scroll
            textarea.addEventListener('scroll', () => {{
                if (highlight) {{
                    highlight.parentElement.scrollTop = textarea.scrollTop;
                    highlight.parentElement.scrollLeft = textarea.scrollLeft;
                }}
                if (gutter) {{
                    gutter.scrollTop = textarea.scrollTop;
                }}
            }});
            
            // Tab handling
            textarea.addEventListener('keydown', (e) => {{
                if (e.key === 'Tab') {{
                    e.preventDefault();
                    const start = textarea.selectionStart;
                    const end = textarea.selectionEnd;
                    textarea.value = textarea.value.substring(0, start) + '    ' + textarea.value.substring(end);
                    textarea.selectionStart = textarea.selectionEnd = start + 4;
                    updateHighlight();
                }}
                
                // Ctrl+S save
                if ((e.ctrlKey || e.metaKey) && e.key === 's') {{
                    e.preventDefault();
                    console.log('Save triggered');
                }}
            }});
            
            textarea.addEventListener('input', updateHighlight);
            
            // Language selector
            const langSelect = editor.querySelector('.code-editor-lang-select');
            if (langSelect) {{
                langSelect.addEventListener('change', (e) => {{
                    config.language = e.target.value;
                    updateHighlight();
                }});
            }}
            
            // Theme selector
            const themeSelect = editor.querySelector('.code-editor-theme-select');
            if (themeSelect) {{
                themeSelect.addEventListener('change', (e) => {{
                    config.theme = e.target.value;
                    editor.className = 'code-editor theme-' + e.target.value;
                }});
            }}
            
            updateHighlight();
        }})();
        """


def create_code_editor(code: str = "", language: CodeLanguage = CodeLanguage.JAVASCRIPT) -> CodeEditor:
    """Create a code editor."""
    return CodeEditor(code, language)


def code_snippet(prefix: str, body: str, description: str = "") -> EditorSnippet:
    """Create a code snippet."""
    return EditorSnippet(prefix, body, description)


def key_binding(key: str, command: str, when: str = "") -> EditorKeyBinding:
    """Create a key binding."""
    return EditorKeyBinding(key, command, when)


CODE_EDITOR_CSS = """
.code-editor {
    border: 1px solid #d1d5db;
    border-radius: 0.5rem;
    overflow: hidden;
    display: flex;
    flex-direction: column;
}

.code-editor-label {
    display: block;
    padding: 0.75rem 1rem 0;
    font-weight: 500;
    color: #374151;
}

.code-editor-toolbar {
    display: flex;
    gap: 0.5rem;
    padding: 0.5rem 1rem;
    background: #f9fafb;
    border-bottom: 1px solid #e5e7eb;
}

.code-editor-lang-select,
.code-editor-theme-select {
    padding: 0.375rem 0.5rem;
    border: 1px solid #d1d5db;
    border-radius: 0.25rem;
    font-size: 0.875rem;
    background: white;
}

.code-editor-wrapper {
    display: flex;
    flex: 1;
    overflow: hidden;
    position: relative;
}

.code-editor-gutter {
    width: 50px;
    background: #f9fafb;
    border-right: 1px solid #e5e7eb;
    overflow: hidden;
    font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
    font-size: 14px;
    line-height: 1.5;
    color: #9ca3af;
    text-align: right;
    padding: 10px 8px 10px 0;
}

.gutter-line {
    height: 21px;
}

.code-editor-textarea {
    flex: 1;
    padding: 10px;
    border: none;
    resize: none;
    font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
    font-size: 14px;
    line-height: 1.5;
    background: transparent;
    color: transparent;
    caret-color: #111827;
    position: absolute;
    top: 0;
    left: 50px;
    right: 0;
    bottom: 0;
    z-index: 1;
    outline: none;
    white-space: pre;
    overflow: auto;
}

.code-editor-highlight {
    flex: 1;
    margin: 0;
    padding: 10px;
    font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
    font-size: 14px;
    line-height: 1.5;
    background: white;
    overflow: auto;
    pointer-events: none;
    position: absolute;
    top: 0;
    left: 50px;
    right: 0;
    bottom: 0;
    z-index: 0;
}

.code-editor-highlight code {
    display: block;
    white-space: pre;
}

/* Syntax highlighting colors */
.code-editor .keyword {
    color: #d73a49;
}

.code-editor .string {
    color: #032f62;
}

.code-editor .comment {
    color: #6a737d;
    font-style: italic;
}

.code-editor .number {
    color: #005cc5;
}

.code-editor-help {
    padding: 0.5rem 1rem;
    font-size: 0.875rem;
    color: #6b7280;
    background: #f9fafb;
    border-top: 1px solid #e5e7eb;
}

/* Dark theme */
.code-editor.theme-dark,
.code-editor.theme-vs-dark {
    background: #1e1e1e;
}

.code-editor.theme-dark .code-editor-gutter,
.code-editor.theme-vs-dark .code-editor-gutter {
    background: #252526;
    border-color: #3c3c3c;
    color: #858585;
}

.code-editor.theme-dark .code-editor-textarea,
.code-editor.theme-vs-dark .code-editor-textarea {
    color: transparent;
    caret-color: #d4d4d4;
}

.code-editor.theme-dark .code-editor-highlight,
.code-editor.theme-vs-dark .code-editor-highlight {
    background: #1e1e1e;
    color: #d4d4d4;
}

.code-editor.theme-dark .keyword,
.code-editor.theme-vs-dark .keyword {
    color: #569cd6;
}

.code-editor.theme-dark .string,
.code-editor.theme-vs-dark .string {
    color: #ce9178;
}

.code-editor.theme-dark .comment,
.code-editor.theme-vs-dark .comment {
    color: #6a9955;
}

.code-editor.theme-dark .number,
.code-editor.theme-vs-dark .number {
    color: #b5cea8;
}

/* Monokai theme */
.code-editor.theme-monokai {
    background: #272822;
}

.code-editor.theme-monokai .keyword {
    color: #f92672;
}

.code-editor.theme-monokai .string {
    color: #e6db74;
}

.code-editor.theme-monokai .comment {
    color: #75715e;
}

/* Dracula theme */
.code-editor.theme-dracula {
    background: #282a36;
}

.code-editor.theme-dracula .keyword {
    color: #ff79c6;
}

.code-editor.theme-dracula .string {
    color: #f1fa8c;
}

.code-editor.theme-dracula .comment {
    color: #6272a4;
}

.code-editor.disabled {
    opacity: 0.5;
    pointer-events: none;
}
"""
