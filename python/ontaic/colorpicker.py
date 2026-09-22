"""Color picker component."""
from typing import Any, Callable, Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum


class ColorFormat(str, Enum):
    """Color format."""
    HEX = "hex"
    RGB = "rgb"
    RGBA = "rgba"
    HSL = "hsl"
    HSLA = "hsla"


@dataclass
class ColorPreset:
    """Color preset."""
    name: str
    value: str
    
    def to_dict(self) -> dict:
        return {"name": self.name, "value": self.value}


DEFAULT_PRESETS = [
    ColorPreset("Red", "#ef4444"),
    ColorPreset("Orange", "#f97316"),
    ColorPreset("Amber", "#f59e0b"),
    ColorPreset("Yellow", "#eab308"),
    ColorPreset("Lime", "#84cc16"),
    ColorPreset("Green", "#22c55e"),
    ColorPreset("Emerald", "#10b981"),
    ColorPreset("Teal", "#14b8a6"),
    ColorPreset("Cyan", "#06b6d4"),
    ColorPreset("Sky", "#0ea5e9"),
    ColorPreset("Blue", "#3b82f6"),
    ColorPreset("Indigo", "#6366f1"),
    ColorPreset("Violet", "#8b5cf6"),
    ColorPreset("Purple", "#a855f7"),
    ColorPreset("Fuchsia", "#d946ef"),
    ColorPreset("Pink", "#ec4899"),
    ColorPreset("Rose", "#f43f5e"),
    ColorPreset("White", "#ffffff"),
    ColorPreset("Gray", "#6b7280"),
    ColorPreset("Black", "#000000"),
]


class ColorPicker:
    """Color picker component."""
    
    def __init__(self, name: str = "color", value: str = "#3b82f6"):
        self.name = name
        self._value = value
        self._format: ColorFormat = ColorFormat.HEX
        self._presets: List[ColorPreset] = DEFAULT_PRESETS
        self._show_presets: bool = True
        self._show_input: bool = True
        self._show_preview: bool = True
        self._show_tabs: bool = True
        self._on_change: Optional[Callable] = None
        self._disabled: bool = False
        self._class_name: str = ""
        self._label: str = ""
        self._help_text: str = ""
        self._size: str = "medium"
        self._inline: bool = False
    
    @property
    def value(self) -> str:
        return self._value
    
    @value.setter
    def value(self, value: str):
        self._value = value
    
    def format(self, fmt: ColorFormat) -> "ColorPicker":
        """Set color format."""
        self._format = fmt
        return self
    
    def presets(self, presets: List[ColorPreset]) -> "ColorPicker":
        """Set color presets."""
        self._presets = presets
        return self
    
    def show_presets(self, show: bool = True) -> "ColorPicker":
        """Show presets."""
        self._show_presets = show
        return self
    
    def show_input(self, show: bool = True) -> "ColorPicker":
        """Show input."""
        self._show_input = show
        return self
    
    def show_preview(self, show: bool = True) -> "ColorPicker":
        """Show preview."""
        self._show_preview = show
        return self
    
    def show_tabs(self, show: bool = True) -> "ColorPicker":
        """Show tabs."""
        self._show_tabs = show
        return self
    
    def on_change(self, callback: Callable) -> "ColorPicker":
        """Set change handler."""
        self._on_change = callback
        return self
    
    def disabled(self) -> "ColorPicker":
        """Make disabled."""
        self._disabled = True
        return self
    
    def class_name(self, class_name: str) -> "ColorPicker":
        """Set CSS class."""
        self._class_name = class_name
        return self
    
    def label(self, label: str) -> "ColorPicker":
        """Set label."""
        self._label = label
        return self
    
    def help_text(self, text: str) -> "ColorPicker":
        """Set help text."""
        self._help_text = text
        return self
    
    def size(self, size: str) -> "ColorPicker":
        """Set size (small, medium, large)."""
        self._size = size
        return self
    
    def inline(self) -> "ColorPicker":
        """Make inline."""
        self._inline = True
        return self
    
    def hex_to_rgb(self, hex_color: str) -> Tuple[int, int, int]:
        """Convert hex to RGB."""
        hex_color = hex_color.lstrip("#")
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def rgb_to_hex(self, r: int, g: int, b: int) -> str:
        """Convert RGB to hex."""
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def hex_to_hsl(self, hex_color: str) -> Tuple[int, int, int]:
        """Convert hex to HSL."""
        r, g, b = self.hex_to_rgb(hex_color)
        r, g, b = r / 255, g / 255, b / 255
        max_val = max(r, g, b)
        min_val = min(r, g, b)
        l = (max_val + min_val) / 2
        
        if max_val == min_val:
            h = s = 0
        else:
            d = max_val - min_val
            s = d / (2 - max_val - min_val) if l > 0.5 else d / (max_val + min_val)
            if max_val == r:
                h = (g - b) / d + (6 if g < b else 0)
            elif max_val == g:
                h = (b - r) / d + 2
            else:
                h = (r - g) / d + 4
            h /= 6
        
        return int(h * 360), int(s * 100), int(l * 100)
    
    def get_formatted_value(self) -> str:
        """Get value in current format."""
        if self._format == ColorFormat.HEX:
            return self._value
        
        r, g, b = self.hex_to_rgb(self._value)
        
        if self._format == ColorFormat.RGB:
            return f"rgb({r}, {g}, {b})"
        elif self._format == ColorFormat.RGBA:
            return f"rgba({r}, {g}, {b}, 1)"
        elif self._format == ColorFormat.HSL:
            h, s, l = self.hex_to_hsl(self._value)
            return f"hsl({h}, {s}%, {l}%)"
        elif self._format == ColorFormat.HSLA:
            h, s, l = self.hex_to_hsl(self._value)
            return f"hsla({h}, {s}%, {l}%, 1)"
        
        return self._value
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "value": self._value,
            "format": self._format.value,
            "presets": [p.to_dict() for p in self._presets],
            "showPresets": self._show_presets,
            "showInput": self._show_input,
            "showPreview": self._show_preview,
            "showTabs": self._show_tabs,
            "disabled": self._disabled,
            "className": self._class_name,
            "label": self._label,
            "helpText": self._help_text,
            "size": self._size,
            "inline": self._inline,
            "formattedValue": self.get_formatted_value(),
        }
    
    def to_html(self) -> str:
        """Generate HTML."""
        label_html = f'<label class="color-picker-label">{self._label}</label>' if self._label else ""
        help_html = f'<p class="color-picker-help">{self._help_text}</p>' if self._help_text else ""
        disabled_class = " disabled" if self._disabled else ""
        class_attr = f" {self._class_name}" if self._class_name else ""
        size_class = f" color-picker-{self._size}" if self._size != "medium" else ""
        
        presets_html = ""
        if self._show_presets:
            preset_items = "".join(
                f'<button type="button" class="color-preset" data-color="{p.value}" title="{p.name}" style="background: {p.value}"></button>'
                for p in self._presets
            )
            presets_html = f'<div class="color-presets">{preset_items}</div>'
        
        input_html = ""
        if self._show_input:
            input_html = f'''<div class="color-input-group">
                <input type="text" class="color-input" value="{self._value}" maxlength="7" placeholder="#000000">
            </div>'''
        
        preview_html = ""
        if self._show_preview:
            preview_html = f'<div class="color-preview" style="background: {self._value}"></div>'
        
        tabs_html = ""
        if self._show_tabs:
            tabs_html = f'''<div class="color-tabs">
                <button type="button" class="color-tab active" data-format="hex">HEX</button>
                <button type="button" class="color-tab" data-format="rgb">RGB</button>
                <button type="button" class="color-tab" data-format="hsl">HSL</button>
            </div>'''
        
        if self._inline:
            return f'''<div class="color-picker{disabled_class}{class_attr}{size_class}">
                {label_html}
                {preview_html}
                {tabs_html}
                <div class="color-picker-body">
                    <div class="color-spectrum"></div>
                    <div class="color-hue"></div>
                </div>
                {presets_html}
                {input_html}
                <input type="hidden" name="{self.name}" value="{self._value}">
                {help_html}
            </div>'''
        
        return f'''<div class="color-picker{disabled_class}{class_attr}{size_class}">
            {label_html}
            <div class="color-picker-trigger">
                <div class="color-trigger-swatch" style="background: {self._value}"></div>
                <input type="text" class="color-trigger-input" value="{self.get_formatted_value()}" readonly>
            </div>
            <div class="color-picker-dropdown">
                {preview_html}
                {tabs_html}
                <div class="color-picker-body">
                    <div class="color-spectrum"></div>
                    <div class="color-hue"></div>
                </div>
                {presets_html}
                {input_html}
                <input type="hidden" name="{self.name}" value="{self._value}">
            </div>
            {help_html}
        </div>'''
    
    def generate_js_code(self) -> str:
        """Generate JavaScript."""
        config = self.to_dict()
        return f"""
        // Color Picker
        (function() {{
            const config = {str(config).replace("'", '"')};
            
            const container = document.querySelector('.color-picker');
            if (!container) return;
            
            const trigger = container.querySelector('.color-picker-trigger');
            const dropdown = container.querySelector('.color-picker-dropdown');
            const spectrum = container.querySelector('.color-spectrum');
            const hue = container.querySelector('.color-hue');
            const input = container.querySelector('.color-input');
            const hidden = container.querySelector('input[type="hidden"]');
            
            // Toggle dropdown
            if (trigger) {{
                trigger.addEventListener('click', () => {{
                    dropdown.classList.toggle('open');
                }});
                
                document.addEventListener('click', (e) => {{
                    if (!container.contains(e.target)) {{
                        dropdown.classList.remove('open');
                    }}
                }});
            }}
            
            // Spectrum interaction
            if (spectrum) {{
                let isDragging = false;
                
                spectrum.addEventListener('mousedown', (e) => {{
                    isDragging = true;
                    updateColor(e);
                }});
                
                document.addEventListener('mousemove', (e) => {{
                    if (isDragging) updateColor(e);
                }});
                
                document.addEventListener('mouseup', () => {{
                    isDragging = false;
                }});
                
                function updateColor(e) {{
                    const rect = spectrum.getBoundingClientRect();
                    const x = Math.max(0, Math.min(e.clientX - rect.left, rect.width));
                    const y = Math.max(0, Math.min(e.clientY - rect.top, rect.height));
                    
                    const s = (x / rect.width) * 100;
                    const l = 100 - (y / rect.height) * 100;
                    
                    const hueVal = hue ? parseInt(hue.querySelector('input')?.value || 0) : 0;
                    const hex = hslToHex(hueVal, s, l);
                    
                    setColor(hex);
                }}
            }}
            
            // Hue interaction
            if (hue) {{
                let isDraggingHue = false;
                
                hue.addEventListener('mousedown', (e) => {{
                    isDraggingHue = true;
                    updateHue(e);
                }});
                
                document.addEventListener('mousemove', (e) => {{
                    if (isDraggingHue) updateHue(e);
                }});
                
                document.addEventListener('mouseup', () => {{
                    isDraggingHue = false;
                }});
                
                function updateHue(e) {{
                    const rect = hue.getBoundingClientRect();
                    const x = Math.max(0, Math.min(e.clientX - rect.left, rect.width));
                    const h = (x / rect.width) * 360;
                    hue.style.setProperty('--hue', h);
                }}
            }}
            
            // Preset selection
            container.querySelectorAll('.color-preset').forEach(preset => {{
                preset.addEventListener('click', () => {{
                    const color = preset.dataset.color;
                    setColor(color);
                }});
            }});
            
            // Input change
            if (input) {{
                input.addEventListener('input', (e) => {{
                    const value = e.target.value;
                    if (/^#[0-9a-f]{{6}}$/i.test(value)) {{
                        setColor(value);
                    }}
                }});
            }}
            
            function setColor(hex) {{
                container.style.setProperty('--selected-color', hex);
                if (hidden) hidden.value = hex;
                if (input) input.value = hex;
                
                const preview = container.querySelector('.color-preview');
                if (preview) preview.style.background = hex;
                
                const swatch = container.querySelector('.color-trigger-swatch');
                if (swatch) swatch.style.background = hex;
            }}
            
            function hslToHex(h, s, l) {{
                s /= 100;
                l /= 100;
                const a = s * Math.min(l, 1 - l);
                const f = n => {{
                    const k = (n + h / 30) % 12;
                    const color = l - a * Math.max(Math.min(k - 3, 9 - k, 1), -1);
                    return Math.round(255 * color).toString(16).padStart(2, '0');
                }};
                return `#${{f(0)}}${{f(8)}}${{f(4)}}`;
            }}
        }})();
        """


def create_color_picker(name: str = "color", value: str = "#3b82f6") -> ColorPicker:
    """Create a color picker."""
    return ColorPicker(name, value)


def color_preset(name: str, value: str) -> ColorPreset:
    """Create a color preset."""
    return ColorPreset(name, value)


COLOR_PICKER_CSS = """
.color-picker {
    position: relative;
    display: inline-block;
}

.color-picker-label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: 500;
    color: #374151;
}

.color-picker-trigger {
    display: flex;
    align-items: center;
    border: 1px solid #d1d5db;
    border-radius: 0.375rem;
    overflow: hidden;
    cursor: pointer;
}

.color-trigger-swatch {
    width: 40px;
    height: 40px;
    border-right: 1px solid #e5e7eb;
}

.color-trigger-input {
    flex: 1;
    padding: 0.5rem;
    border: none;
    font-family: monospace;
    font-size: 0.875rem;
}

.color-picker-dropdown {
    display: none;
    position: absolute;
    top: 100%;
    left: 0;
    z-index: 50;
    margin-top: 0.5rem;
    padding: 1rem;
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 0.5rem;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    min-width: 280px;
}

.color-picker-dropdown.open {
    display: block;
}

.color-picker-body {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    margin-bottom: 1rem;
}

.color-spectrum {
    width: 100%;
    height: 200px;
    background: linear-gradient(to top, #000, transparent),
                linear-gradient(to right, #fff, hsl(var(--hue, 0), 100%, 50%));
    border-radius: 0.375rem;
    cursor: crosshair;
}

.color-hue {
    width: 100%;
    height: 16px;
    background: linear-gradient(to right, 
        hsl(0, 100%, 50%), 
        hsl(60, 100%, 50%), 
        hsl(120, 100%, 50%), 
        hsl(180, 100%, 50%), 
        hsl(240, 100%, 50%), 
        hsl(300, 100%, 50%), 
        hsl(360, 100%, 50%));
    border-radius: 0.375rem;
    cursor: pointer;
}

.color-preview {
    width: 100%;
    height: 48px;
    border-radius: 0.375rem;
    margin-bottom: 1rem;
}

.color-tabs {
    display: flex;
    gap: 0.25rem;
    margin-bottom: 1rem;
}

.color-tab {
    flex: 1;
    padding: 0.375rem;
    background: #f3f4f6;
    border: none;
    border-radius: 0.25rem;
    font-size: 0.75rem;
    font-weight: 500;
    cursor: pointer;
}

.color-tab.active {
    background: #3b82f6;
    color: white;
}

.color-presets {
    display: flex;
    flex-wrap: wrap;
    gap: 0.375rem;
    margin-bottom: 1rem;
}

.color-preset {
    width: 24px;
    height: 24px;
    border: 2px solid transparent;
    border-radius: 4px;
    cursor: pointer;
    padding: 0;
}

.color-preset:hover {
    border-color: #374151;
    transform: scale(1.1);
}

.color-input-group {
    display: flex;
}

.color-input {
    flex: 1;
    padding: 0.5rem;
    border: 1px solid #d1d5db;
    border-radius: 0.375rem;
    font-family: monospace;
}

.color-input:focus {
    outline: none;
    border-color: #3b82f6;
}

.color-picker-help {
    margin-top: 0.5rem;
    font-size: 0.875rem;
    color: #6b7280;
}

.color-picker-small .color-trigger-swatch {
    width: 32px;
    height: 32px;
}

.color-picker-large .color-trigger-swatch {
    width: 48px;
    height: 48px;
}

.color-picker.disabled {
    opacity: 0.5;
    cursor: not-allowed;
}
"""
