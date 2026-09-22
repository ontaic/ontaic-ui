"""Image cropper component with zoom and rotation."""
from typing import Any, Callable, Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum


class CropShape(str, Enum):
    """Crop shape."""
    RECTANGLE = "rectangle"
    SQUARE = "square"
    CIRCLE = "circle"


class CropAspect(str, Enum):
    """Crop aspect ratio."""
    FREE = "free"
    ORIGINAL = "original"
    SQUARE = "1:1"
    LANDSCAPE_16_9 = "16:9"
    LANDSCAPE_4_3 = "4:3"
    PORTRAIT_9_16 = "9:16"
    PORTRAIT_3_4 = "3:4"


@dataclass
class CropArea:
    """Crop area coordinates."""
    x: int = 0
    y: int = 0
    width: int = 0
    height: int = 0
    
    def to_dict(self) -> dict:
        return {"x": self.x, "y": self.y, "width": self.width, "height": self.height}
    
    @classmethod
    def from_dict(cls, data: dict) -> "CropArea":
        return cls(x=data.get("x", 0), y=data.get("y", 0), width=data.get("width", 0), height=data.get("height", 0))


class ImageCropper:
    """Image cropper component with zoom and rotation."""
    
    def __init__(self, image_url: str = ""):
        self.image_url = image_url
        self._shape: CropShape = CropShape.RECTANGLE
        self._aspect: CropAspect = CropAspect.FREE
        self._aspect_ratio: float = 0
        self._min_width: int = 50
        self._min_height: int = 50
        self._max_width: int = 0
        self._max_height: int = 0
        self._output_width: int = 0
        self._output_height: int = 0
        self._output_format: str = "png"
        self._output_quality: float = 0.92
        self._zoom: float = 1
        self._min_zoom: float = 0.5
        self._max_zoom: float = 3
        self._rotation: int = 0
        self._flip_horizontal: bool = False
        self._flip_vertical: bool = False
        self._crop_area: CropArea = CropArea()
        self._show_grid: bool = True
        self._show_controls: bool = True
        self._show_zoom: bool = True
        self._show_rotate: bool = True
        self._show_flip: bool = True
        self._show_reset: bool = True
        self._show_preview: bool = True
        self._preview_size: int = 150
        self._movable: bool = True
        self._resizable: bool = True
        self._on_crop: Optional[Callable] = None
        self._on_zoom: Optional[Callable] = None
        self._on_rotate: Optional[Callable] = None
        self._on_ready: Optional[Callable] = None
        self._class_name: str = ""
        self._label: str = ""
        self._help_text: str = ""
        self._disabled: bool = False
    
    def shape(self, shape: CropShape) -> "ImageCropper":
        """Set crop shape."""
        self._shape = shape
        return self
    
    def aspect(self, aspect: CropAspect) -> "ImageCropper":
        """Set aspect ratio."""
        self._aspect = aspect
        if aspect == CropAspect.SQUARE:
            self._aspect_ratio = 1
        elif aspect == CropAspect.LANDSCAPE_16_9:
            self._aspect_ratio = 16 / 9
        elif aspect == CropAspect.LANDSCAPE_4_3:
            self._aspect_ratio = 4 / 3
        elif aspect == CropAspect.PORTRAIT_9_16:
            self._aspect_ratio = 9 / 16
        elif aspect == CropAspect.PORTRAIT_3_4:
            self._aspect_ratio = 3 / 4
        else:
            self._aspect_ratio = 0
        return self
    
    def output_size(self, width: int, height: int) -> "ImageCropper":
        """Set output size."""
        self._output_width = width
        self._output_height = height
        return self
    
    def output_format(self, fmt: str, quality: float = 0.92) -> "ImageCropper":
        """Set output format."""
        self._output_format = fmt
        self._output_quality = quality
        return self
    
    def zoom(self, zoom: float) -> "ImageCropper":
        """Set zoom level."""
        self._zoom = max(self._min_zoom, min(self._max_zoom, zoom))
        return self
    
    def rotation(self, degrees: int) -> "ImageCropper":
        """Set rotation in degrees."""
        self._rotation = degrees % 360
        return self
    
    def on_crop(self, callback: Callable) -> "ImageCropper":
        """Set crop handler."""
        self._on_crop = callback
        return self
    
    def on_zoom(self, callback: Callable) -> "ImageCropper":
        """Set zoom handler."""
        self._on_zoom = callback
        return self
    
    def on_rotate(self, callback: Callable) -> "ImageCropper":
        """Set rotate handler."""
        self._on_rotate = callback
        return self
    
    def on_ready(self, callback: Callable) -> "ImageCropper":
        """Set ready handler."""
        self._on_ready = callback
        return self
    
    def class_name(self, class_name: str) -> "ImageCropper":
        """Set CSS class."""
        self._class_name = class_name
        return self
    
    def label(self, label: str) -> "ImageCropper":
        """Set label."""
        self._label = label
        return self
    
    def help_text(self, text: str) -> "ImageCropper":
        """Set help text."""
        self._help_text = text
        return self
    
    def disabled(self) -> "ImageCropper":
        """Make disabled."""
        self._disabled = True
        return self
    
    def get_cropped_data(self) -> Dict[str, Any]:
        """Get cropped image data."""
        return {
            "imageUrl": self.image_url,
            "cropArea": self._crop_area.to_dict(),
            "zoom": self._zoom,
            "rotation": self._rotation,
            "flipHorizontal": self._flip_horizontal,
            "flipVertical": self._flip_vertical,
            "outputWidth": self._output_width,
            "outputHeight": self._output_height,
            "outputFormat": self._output_format,
        }
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "imageUrl": self.image_url,
            "shape": self._shape.value,
            "aspect": self._aspect.value,
            "aspectRatio": self._aspect_ratio,
            "minWidth": self._min_width,
            "minHeight": self._min_height,
            "outputWidth": self._output_width,
            "outputHeight": self._output_height,
            "outputFormat": self._output_format,
            "outputQuality": self._output_quality,
            "zoom": self._zoom,
            "minZoom": self._min_zoom,
            "maxZoom": self._max_zoom,
            "rotation": self._rotation,
            "flipHorizontal": self._flip_horizontal,
            "flipVertical": self._flip_vertical,
            "showGrid": self._show_grid,
            "showControls": self._show_controls,
            "showZoom": self._show_zoom,
            "showRotate": self._show_rotate,
            "showFlip": self._show_flip,
            "showReset": self._show_reset,
            "showPreview": self._show_preview,
            "previewSize": self._preview_size,
            "movable": self._movable,
            "resizable": self._resizable,
            "disabled": self._disabled,
            "className": self._class_name,
            "label": self._label,
        }
    
    def to_html(self) -> str:
        """Generate HTML."""
        label_html = f'<label class="cropper-label">{self._label}</label>' if self._label else ""
        help_html = f'<p class="cropper-help">{self._help_text}</p>' if self._help_text else ""
        disabled_class = " disabled" if self._disabled else ""
        class_attr = f" {self._class_name}" if self._class_name else ""
        shape_class = f" cropper-{self._shape.value}"
        
        # Preview
        preview_html = ""
        if self._show_preview:
            preview_html = f'''<div class="cropper-preview">
                <div class="cropper-preview-image" style="background-image: url('{self.image_url}')"></div>
            </div>'''
        
        # Controls
        controls_html = ""
        if self._show_controls:
            zoom_html = ""
            if self._show_zoom:
                zoom_html = f'''<div class="cropper-control">
                    <label>Zoom</label>
                    <input type="range" class="cropper-zoom" min="{self._min_zoom}" max="{self._max_zoom}" step="0.1" value="{self._zoom}">
                    <span class="cropper-zoom-value">{self._zoom}x</span>
                </div>'''
            
            rotate_html = ""
            if self._show_rotate:
                rotate_html = f'''<div class="cropper-control">
                    <label>Rotate</label>
                    <button type="button" class="cropper-btn" data-action="rotate-left">&#8634;</button>
                    <button type="button" class="cropper-btn" data-action="rotate-right">&#8635;</button>
                    <span class="cropper-rotation-value">{self._rotation}°</span>
                </div>'''
            
            flip_html = ""
            if self._show_flip:
                flip_html = f'''<div class="cropper-control">
                    <label>Flip</label>
                    <button type="button" class="cropper-btn" data-action="flip-h">↔</button>
                    <button type="button" class="cropper-btn" data-action="flip-v">↕</button>
                </div>'''
            
            reset_html = ""
            if self._show_reset:
                reset_html = '<button type="button" class="cropper-btn cropper-reset">Reset</button>'
            
            controls_html = f'''<div class="cropper-controls">
                {zoom_html}
                {rotate_html}
                {flip_html}
                {reset_html}
                <button type="button" class="cropper-btn cropper-crop-btn">Crop</button>
            </div>'''
        
        return f'''<div class="image-cropper{shape_class}{disabled_class}{class_attr}">
            {label_html}
            <div class="cropper-container">
                <div class="cropper-wrapper">
                    <img src="{self.image_url}" class="cropper-image" style="transform: scale({self._zoom}) rotate({self._rotation}deg) scaleX({-1 if self._flip_horizontal else 1}) scaleY({-1 if self._flip_vertical else 1});">
                    <div class="cropper-crop-area"></div>
                    {f'<div class="cropper-grid"></div>' if self._show_grid else ''}
                </div>
                {preview_html}
            </div>
            {controls_html}
            <input type="hidden" name="crop_data" value="">
            {help_html}
        </div>'''
    
    def generate_js_code(self) -> str:
        """Generate JavaScript."""
        config = self.to_dict()
        return f"""
        // Image Cropper
        (function() {{
            const config = {str(config).replace("'", '"')};
            
            const cropper = document.querySelector('.image-cropper');
            if (!cropper) return;
            
            const image = cropper.querySelector('.cropper-image');
            const cropArea = cropper.querySelector('.cropper-crop-area');
            const zoomInput = cropper.querySelector('.cropper-zoom');
            const hidden = cropper.querySelector('input[type="hidden"]');
            
            let zoom = config.zoom;
            let rotation = config.rotation;
            let flipH = false;
            let flipV = false;
            
            // Zoom
            if (zoomInput) {{
                zoomInput.addEventListener('input', (e) => {{
                    zoom = parseFloat(e.target.value);
                    updateTransform();
                    const zoomValue = cropper.querySelector('.cropper-zoom-value');
                    if (zoomValue) zoomValue.textContent = zoom.toFixed(1) + 'x';
                }});
            }}
            
            // Rotate
            cropper.querySelectorAll('[data-action="rotate-left"]').forEach(btn => {{
                btn.addEventListener('click', () => {{
                    rotation = (rotation - 90) % 360;
                    updateTransform();
                    updateRotationDisplay();
                }});
            }});
            
            cropper.querySelectorAll('[data-action="rotate-right"]').forEach(btn => {{
                btn.addEventListener('click', () => {{
                    rotation = (rotation + 90) % 360;
                    updateTransform();
                    updateRotationDisplay();
                }});
            }});
            
            // Flip
            cropper.querySelectorAll('[data-action="flip-h"]').forEach(btn => {{
                btn.addEventListener('click', () => {{
                    flipH = !flipH;
                    updateTransform();
                }});
            }});
            
            cropper.querySelectorAll('[data-action="flip-v"]').forEach(btn => {{
                btn.addEventListener('click', () => {{
                    flipV = !flipV;
                    updateTransform();
                }});
            }});
            
            // Reset
            cropper.querySelector('.cropper-reset')?.addEventListener('click', () => {{
                zoom = 1;
                rotation = 0;
                flipH = false;
                flipV = false;
                updateTransform();
                if (zoomInput) zoomInput.value = 1;
                updateRotationDisplay();
            }});
            
            // Crop
            cropper.querySelector('.cropper-crop-btn')?.addEventListener('click', () => {{
                const data = {{
                    zoom,
                    rotation,
                    flipHorizontal: flipH,
                    flipVertical: flipV,
                    cropArea: {{ x: 0, y: 0, width: image.naturalWidth, height: image.naturalHeight }}
                }};
                
                if (hidden) hidden.value = JSON.stringify(data);
                console.log('Crop data:', data);
            }});
            
            function updateTransform() {{
                if (image) {{
                    image.style.transform = `scale(${{zoom}}) rotate(${{rotation}}deg) scaleX(${{flipH ? -1 : 1}}) scaleY(${{flipV ? -1 : 1}})`;
                }}
            }}
            
            function updateRotationDisplay() {{
                const rotValue = cropper.querySelector('.cropper-rotation-value');
                if (rotValue) rotValue.textContent = ((rotation % 360) + 360) % 360 + '°';
            }}
        }})();
        """


def create_image_cropper(image_url: str = "") -> ImageCropper:
    """Create an image cropper."""
    return ImageCropper(image_url)


IMAGE_CROPPER_CSS = """
.image-cropper {
    display: inline-block;
}

.cropper-label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: 500;
    color: #374151;
}

.cropper-container {
    display: flex;
    gap: 1rem;
}

.cropper-wrapper {
    position: relative;
    overflow: hidden;
    background: #1f2937;
    border-radius: 0.5rem;
    max-width: 500px;
    max-height: 400px;
}

.cropper-image {
    display: block;
    max-width: 100%;
    max-height: 400px;
    transform-origin: center;
}

.cropper-crop-area {
    position: absolute;
    top: 10%;
    left: 10%;
    width: 80%;
    height: 80%;
    border: 2px dashed white;
    cursor: move;
}

.cropper-grid {
    position: absolute;
    top: 10%;
    left: 10%;
    width: 80%;
    height: 80%;
    background-image: 
        linear-gradient(rgba(255, 255, 255, 0.3) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255, 255, 255, 0.3) 1px, transparent 1px);
    background-size: 33.33% 33.33%;
    pointer-events: none;
}

.cropper-preview {
    width: 150px;
    height: 150px;
    border-radius: 0.5rem;
    overflow: hidden;
    border: 1px solid #e5e7eb;
}

.cropper-preview-image {
    width: 100%;
    height: 100%;
    background-size: cover;
    background-position: center;
}

.cropper-controls {
    margin-top: 1rem;
    display: flex;
    flex-wrap: wrap;
    gap: 1rem;
    align-items: center;
}

.cropper-control {
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.cropper-control label {
    font-size: 0.875rem;
    color: #6b7280;
    min-width: 50px;
}

.cropper-zoom {
    width: 100px;
}

.cropper-zoom-value,
.cropper-rotation-value {
    font-size: 0.875rem;
    color: #374151;
    min-width: 40px;
}

.cropper-btn {
    padding: 0.375rem 0.75rem;
    border: 1px solid #d1d5db;
    background: white;
    border-radius: 0.375rem;
    cursor: pointer;
    font-size: 0.875rem;
}

.cropper-btn:hover {
    background: #f9fafb;
}

.cropper-crop-btn {
    background: #3b82f6;
    color: white;
    border-color: #3b82f6;
}

.cropper-crop-btn:hover {
    background: #2563eb;
}

.cropper-reset {
    color: #6b7280;
}

.cropper-circle .cropper-crop-area {
    border-radius: 50%;
}

.cropper-circle .cropper-grid {
    border-radius: 50%;
}

.cropper-help {
    margin-top: 0.5rem;
    font-size: 0.875rem;
    color: #6b7280;
}

.image-cropper.disabled {
    opacity: 0.5;
    pointer-events: none;
}
"""
