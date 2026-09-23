"""Signature pad component for capturing handwritten signatures."""
from typing import Any, Callable, Dict, Optional
from dataclasses import dataclass
from enum import Enum


class SignaturePenColor(str, Enum):
    """Signature pen colors."""
    BLACK = "#000000"
    BLUE = "#0000ff"
    RED = "#ff0000"
    GREEN = "#00ff00"
    CUSTOM = "custom"


class SignatureFormat(str, Enum):
    """Signature output format."""
    SVG = "svg"
    PNG = "png"
    JPG = "jpg"
    DATA_URL = "data_url"


@dataclass
class SignatureStyle:
    """Signature pad style."""
    pen_color: str = "#000000"
    pen_width: int = 2
    background_color: str = "#ffffff"
    border_color: str = "#d1d5db"
    border_width: int = 1
    border_radius: str = "0.5rem"
    
    def to_dict(self) -> dict:
        return {
            "penColor": self.pen_color,
            "penWidth": self.pen_width,
            "backgroundColor": self.background_color,
            "borderColor": self.border_color,
            "borderWidth": self.border_width,
            "borderRadius": self.border_radius,
        }


class SignaturePad:
    """Signature pad component for capturing handwritten signatures."""
    
    def __init__(self):
        self._width: int = 400
        self._height: int = 200
        self._style: SignatureStyle = SignatureStyle()
        self._format: SignatureFormat = SignatureFormat.SVG
        self._label: str = "Signature"
        self._placeholder: str = "Sign here"
        self._clear_button: bool = True
        self._save_button: bool = True
        self._undo_button: bool = True
        self._required: bool = False
        self._disabled: bool = False
        self._max_points: int = 1000
        self._velocity_filter_weight: float = 0.7
        self._min_distance: int = 5
        self._on_sign: Optional[Callable] = None
        self._on_clear: Optional[Callable] = None
        self._on_save: Optional[Callable] = None
        self._class_name: str = ""
        self._help_text: str = ""
    
    def size(self, width: int, height: int) -> "SignaturePad":
        """Set size."""
        self._width = width
        self._height = height
        return self
    
    def style(self, style: SignatureStyle) -> "SignaturePad":
        """Set style."""
        self._style = style
        return self
    
    def pen_color(self, color: str) -> "SignaturePad":
        """Set pen color."""
        self._style.pen_color = color
        return self
    
    def pen_width(self, width: int) -> "SignaturePad":
        """Set pen width."""
        self._style.pen_width = width
        return self
    
    def format(self, format: SignatureFormat) -> "SignaturePad":
        """Set output format."""
        self._format = format
        return self
    
    def placeholder(self, text: str) -> "SignaturePad":
        """Set placeholder."""
        self._placeholder = text
        return self
    
    def clear_button(self, show: bool = True) -> "SignaturePad":
        """Show clear button."""
        self._clear_button = show
        return self
    
    def save_button(self, show: bool = True) -> "SignaturePad":
        """Show save button."""
        self._save_button = show
        return self
    
    def undo_button(self, show: bool = True) -> "SignaturePad":
        """Show undo button."""
        self._undo_button = show
        return self
    
    def required(self) -> "SignaturePad":
        """Make required."""
        self._required = True
        return self
    
    def disabled(self) -> "SignaturePad":
        """Make disabled."""
        self._disabled = True
        return self
    
    def on_sign(self, callback: Callable) -> "SignaturePad":
        """Set sign handler."""
        self._on_sign = callback
        return self
    
    def on_clear(self, callback: Callable) -> "SignaturePad":
        """Set clear handler."""
        self._on_clear = callback
        return self
    
    def on_save(self, callback: Callable) -> "SignaturePad":
        """Set save handler."""
        self._on_save = callback
        return self
    
    def class_name(self, class_name: str) -> "SignaturePad":
        """Set CSS class."""
        self._class_name = class_name
        return self
    
    def help_text(self, text: str) -> "SignaturePad":
        """Set help text."""
        self._help_text = text
        return self
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "width": self._width,
            "height": self._height,
            "style": self._style.to_dict(),
            "format": self._format.value,
            "placeholder": self._placeholder,
            "clearButton": self._clear_button,
            "saveButton": self._save_button,
            "undoButton": self._undo_button,
            "required": self._required,
            "disabled": self._disabled,
        }
    
    def to_html(self) -> str:
        """Generate HTML."""
        class_attr = f" {self._class_name}" if self._class_name else ""
        disabled_class = " disabled" if self._disabled else ""
        required_attr = ' <span class="signature-required">*</span>' if self._required else ""
        help_html = f'<p class="signature-help">{self._help_text}</p>' if self._help_text else ""
        
        buttons = ""
        if self._undo_button:
            buttons += '<button type="button" class="signature-btn signature-undo" title="Undo">&#8617;</button>'
        if self._clear_button:
            buttons += '<button type="button" class="signature-btn signature-clear" title="Clear">&#10005;</button>'
        if self._save_button:
            buttons += '<button type="button" class="signature-btn signature-save" title="Save">&#128190;</button>'
        
        return f'''<div class="signature-container{class_attr}{disabled_class}">
            <label class="signature-label">{self._label}{required_attr}</label>
            <div class="signature-wrapper">
                <canvas id="signature-canvas" class="signature-canvas" width="{self._width}" height="{self._height}"></canvas>
                <div class="signature-placeholder">{self._placeholder}</div>
            </div>
            <div class="signature-actions">
                <div class="signature-buttons">{buttons}</div>
                <input type="hidden" class="signature-data" name="signature">
            </div>
            {help_html}
        </div>'''
    
    def generate_js_code(self) -> str:
        """Generate JavaScript."""
        config = self.to_dict()
        return f"""
        // Signature Pad
        (function() {{
            const config = {str(config).replace("'", '"')};
            
            const canvas = document.getElementById('signature-canvas');
            if (!canvas) return;
            
            const ctx = canvas.getContext('2d');
            let isDrawing = false;
            let lastX = 0;
            let lastY = 0;
            let points = [];
            let history = [];
            
            // Style
            ctx.strokeStyle = config.style.penColor;
            ctx.lineWidth = config.style.penWidth;
            ctx.lineCap = 'round';
            ctx.lineJoin = 'round';
            
            // Background
            ctx.fillStyle = config.style.backgroundColor;
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            
            // Placeholder
            const placeholder = canvas.parentElement.querySelector('.signature-placeholder');
            
            function updatePlaceholder() {{
                if (placeholder) {{
                    placeholder.style.display = points.length === 0 ? 'block' : 'none';
                }}
            }}
            
            function getPos(e) {{
                const rect = canvas.getBoundingClientRect();
                const x = (e.clientX || e.touches[0].clientX) - rect.left;
                const y = (e.clientY || e.touches[0].clientY) - rect.top;
                return [x, y];
            }}
            
            function startDraw(e) {{
                if (config.disabled) return;
                isDrawing = true;
                [lastX, lastY] = getPos(e);
                points.push({{x: lastX, y: lastY}});
                
                ctx.beginPath();
                ctx.moveTo(lastX, lastY);
            }}
            
            function draw(e) {{
                if (!isDrawing) return;
                e.preventDefault();
                
                const [x, y] = getPos(e);
                
                ctx.beginPath();
                ctx.moveTo(lastX, lastY);
                ctx.lineTo(x, y);
                ctx.stroke();
                
                lastX = x;
                lastY = y;
                points.push({{x, y}});
            }}
            
            function stopDraw() {{
                if (!isDrawing) return;
                isDrawing = false;
                
                // Save to history
                history.push(canvas.toDataURL());
                if (history.length > 20) history.shift();
                
                updatePlaceholder();
                updateSignatureData();
            }}
            
            function updateSignatureData() {{
                const dataInput = canvas.parentElement.parentElement.querySelector('.signature-data');
                if (dataInput) {{
                    dataInput.value = points.length > 0 ? canvas.toDataURL() : '';
                }}
            }}
            
            // Mouse events
            canvas.addEventListener('mousedown', startDraw);
            canvas.addEventListener('mousemove', draw);
            canvas.addEventListener('mouseup', stopDraw);
            canvas.addEventListener('mouseleave', stopDraw);
            
            // Touch events
            canvas.addEventListener('touchstart', (e) => {{
                e.preventDefault();
                startDraw(e);
            }});
            canvas.addEventListener('touchmove', (e) => {{
                e.preventDefault();
                draw(e);
            }});
            canvas.addEventListener('touchend', stopDraw);
            
            // Clear button
            canvas.parentElement.parentElement.querySelector('.signature-clear')?.addEventListener('click', () => {{
                ctx.fillStyle = config.style.backgroundColor;
                ctx.fillRect(0, 0, canvas.width, canvas.height);
                points = [];
                history = [];
                updatePlaceholder();
                updateSignatureData();
            }});
            
            // Undo button
            canvas.parentElement.parentElement.querySelector('.signature-undo')?.addEventListener('click', () => {{
                if (history.length > 0) {{
                    history.pop();
                    ctx.fillStyle = config.style.backgroundColor;
                    ctx.fillRect(0, 0, canvas.width, canvas.height);
                    
                    if (history.length > 0) {{
                        const img = new Image();
                        img.onload = () => ctx.drawImage(img, 0, 0);
                        img.src = history[history.length - 1];
                    }}
                    updateSignatureData();
                }}
            }});
            
            // Save button
            canvas.parentElement.parentElement.querySelector('.signature-save')?.addEventListener('click', () => {{
                const link = document.createElement('a');
                link.download = 'signature.png';
                link.href = canvas.toDataURL('image/png');
                link.click();
            }});
            
            updatePlaceholder();
        }})();
        """


def create_signature_pad() -> SignaturePad:
    """Create a signature pad."""
    return SignaturePad()


def signature_style(**kwargs) -> SignatureStyle:
    """Create signature style."""
    return SignatureStyle(**kwargs)


SIGNATURE_PAD_CSS = """
.signature-container {
    display: inline-block;
}

.signature-label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: 500;
    color: #374151;
}

.signature-required {
    color: #ef4444;
}

.signature-wrapper {
    position: relative;
    border: 1px solid #d1d5db;
    border-radius: 0.5rem;
    overflow: hidden;
    background: white;
}

.signature-canvas {
    display: block;
    cursor: crosshair;
}

.signature-placeholder {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    color: #9ca3af;
    font-size: 0.875rem;
    pointer-events: none;
}

.signature-actions {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 0.5rem;
}

.signature-buttons {
    display: flex;
    gap: 0.5rem;
}

.signature-btn {
    padding: 0.375rem 0.75rem;
    border: 1px solid #d1d5db;
    background: white;
    border-radius: 0.375rem;
    cursor: pointer;
    font-size: 0.875rem;
}

.signature-btn:hover {
    background: #f3f4f6;
}

.signature-container.disabled .signature-canvas {
    opacity: 0.5;
    cursor: not-allowed;
}

.signature-container.disabled .signature-btn {
    opacity: 0.5;
    cursor: not-allowed;
}

.signature-help {
    margin-top: 0.5rem;
    font-size: 0.875rem;
    color: #6b7280;
}
"""
