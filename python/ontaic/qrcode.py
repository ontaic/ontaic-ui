"""QR Code component."""
from typing import Any, Callable, Dict, Optional
from dataclasses import dataclass
from enum import Enum


class QRLevel(str, Enum):
    """QR code error correction level."""
    L = "L"  # 7%
    M = "M"  # 15%
    Q = "Q"  # 25%
    H = "H"  # 30%


class QRFormat(str, Enum):
    """QR code output format."""
    SVG = "svg"
    CANVAS = "canvas"
    DATA_URL = "data_url"


@dataclass
class QRStyle:
    """QR code style options."""
    foreground: str = "#000000"
    background: str = "#ffffff"
    size: int = 200
    margin: int = 4
    dot_style: str = "square"  # square, rounded, dots
    corner_style: str = "square"  # square, rounded, extra-rounded
    
    def to_dict(self) -> dict:
        return {
            "foreground": self.foreground,
            "background": self.background,
            "size": self.size,
            "margin": self.margin,
            "dotStyle": self.dot_style,
            "cornerStyle": self.corner_style,
        }


class QRCode:
    """QR Code component."""
    
    def __init__(self, data: str = ""):
        self._data = data
        self._level: QRLevel = QRLevel.M
        self._format: QRFormat = QRFormat.SVG
        self._style: QRStyle = QRStyle()
        self._logo_url: str = ""
        self._logo_size: int = 40
        self._class_name: str = ""
        self._label: str = ""
        self._on_click: Optional[Callable] = None
        self._downloadable: bool = False
    
    def data(self, data: str) -> "QRCode":
        """Set QR data."""
        self._data = data
        return self
    
    def level(self, level: QRLevel) -> "QRCode":
        """Set error correction level."""
        self._level = level
        return self
    
    def format(self, format: QRFormat) -> "QRCode":
        """Set output format."""
        self._format = format
        return self
    
    def style(self, style: QRStyle) -> "QRCode":
        """Set style."""
        self._style = style
        return self
    
    def foreground(self, color: str) -> "QRCode":
        """Set foreground color."""
        self._style.foreground = color
        return self
    
    def background(self, color: str) -> "QRCode":
        """Set background color."""
        self._style.background = color
        return self
    
    def size(self, size: int) -> "QRCode":
        """Set size."""
        self._style.size = size
        return self
    
    def logo(self, url: str, size: int = 40) -> "QRCode":
        """Set logo."""
        self._logo_url = url
        self._logo_size = size
        return self
    
    def downloadable(self, downloadable: bool = True) -> "QRCode":
        """Make downloadable."""
        self._downloadable = downloadable
        return self
    
    def on_click(self, callback: Callable) -> "QRCode":
        """Set click handler."""
        self._on_click = callback
        return self
    
    def class_name(self, class_name: str) -> "QRCode":
        """Set CSS class."""
        self._class_name = class_name
        return self
    
    def label(self, label: str) -> "QRCode":
        """Set label."""
        self._label = label
        return self
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "data": self._data,
            "level": self._level.value,
            "format": self._format.value,
            "style": self._style.to_dict(),
            "logoUrl": self._logo_url,
            "logoSize": self._logo_size,
            "downloadable": self._downloadable,
        }
    
    def to_html(self) -> str:
        """Generate HTML."""
        label_html = f'<h4 class="qr-label">{self._label}</h4>' if self._label else ""
        class_attr = f" {self._class_name}" if self._class_name else ""
        size = self._style.size
        
        download_btn = ""
        if self._downloadable:
            download_btn = '<button type="button" class="qr-download-btn" onclick="downloadQR()">Download</button>'
        
        logo_html = f'<div class="qr-logo" style="width:{self._logo_size}px;height:{self._logo_size}px;"><img src="{self._logo_url}" alt="Logo"></div>' if self._logo_url else ""
        
        return f'''<div class="qr-container{class_attr}">
            {label_html}
            <div class="qr-wrapper">
                <canvas id="qr-canvas" width="{size}" height="{size}" style="display:none;"></canvas>
                <svg id="qr-svg" class="qr-code" width="{size}" height="{size}" viewBox="0 0 {size} {size}">
                    <rect width="{size}" height="{size}" fill="{self._style.background}"/>
                    <text x="50%" y="50%" text-anchor="middle" dominant-baseline="middle" fill="{self._style.foreground}" font-size="12" font-family="system-ui">QR Code</text>
                </svg>
                {logo_html}
            </div>
            {download_btn}
        </div>'''
    
    def generate_js_code(self) -> str:
        """Generate JavaScript."""
        config = self.to_dict()
        return f"""
        // QR Code
        (function() {{
            const config = {str(config).replace("'", '"')};
            
            function generateQR() {{
                const data = config.data;
                if (!data) return;
                
                // Simple QR pattern generation
                const canvas = document.getElementById('qr-canvas');
                const svg = document.getElementById('qr-svg');
                if (!canvas || !svg) return;
                
                const size = config.style.size;
                const moduleSize = Math.floor(size / 25);
                const margin = config.style.margin;
                
                // Generate pseudo-random pattern based on data
                let seed = 0;
                for (let i = 0; i < data.length; i++) {{
                    seed = ((seed << 5) - seed) + data.charCodeAt(i);
                    seed |= 0;
                }}
                
                function random() {{
                    seed = (seed * 16807) % 2147483647;
                    return (seed - 1) / 2147483646;
                }}
                
                let svgContent = '<rect width="' + size + '" height="' + size + '" fill="' + config.style.background + '"/>';
                
                // Position detection patterns
                function drawFinder(x, y) {{
                    for (let i = 0; i < 7; i++) {{
                        for (let j = 0; j < 7; j++) {{
                            if (i === 0 || i === 6 || j === 0 || j === 6 || (i >= 2 && i <= 4 && j >= 2 && j <= 4)) {{
                                svgContent += '<rect x="' + (x + i * moduleSize) + '" y="' + (y + j * moduleSize) + '" width="' + moduleSize + '" height="' + moduleSize + '" fill="' + config.style.foreground + '"/>';
                            }}
                        }}
                    }}
                }}
                
                drawFinder(margin, margin);
                drawFinder(margin, size - margin - 7 * moduleSize);
                drawFinder(size - margin - 7 * moduleSize, margin);
                
                // Data modules
                for (let i = 9; i < 25; i++) {{
                    for (let j = 9; j < 25; j++) {{
                        if (random() > 0.55) {{
                            svgContent += '<rect x="' + (margin + i * moduleSize) + '" y="' + (margin + j * moduleSize) + '" width="' + moduleSize + '" height="' + moduleSize + '" fill="' + config.style.foreground + '"/>';
                        }}
                    }}
                }}
                
                svg.innerHTML = svgContent;
            }}
            
            generateQR();
            
            // Download
            window.downloadQR = function() {{
                const svg = document.getElementById('qr-svg');
                const svgData = new XMLSerializer().serializeToString(svg);
                const canvas = document.getElementById('qr-canvas');
                const ctx = canvas.getContext('2d');
                const img = new Image();
                img.onload = function() {{
                    ctx.drawImage(img, 0, 0);
                    const link = document.createElement('a');
                    link.download = 'qrcode.png';
                    link.href = canvas.toDataURL('image/png');
                    link.click();
                }};
                img.src = 'data:image/svg+xml;base64,' + btoa(svgData);
            }};
        }})();
        """


def create_qr_code(data: str = "") -> QRCode:
    """Create a QR code."""
    return QRCode(data)


def qr_style(**kwargs) -> QRStyle:
    """Create QR style."""
    return QRStyle(**kwargs)


QR_CODE_CSS = """
.qr-container {
    display: inline-block;
    text-align: center;
}

.qr-label {
    margin: 0 0 0.5rem;
    font-size: 0.875rem;
    font-weight: 500;
    color: #374151;
}

.qr-wrapper {
    position: relative;
    display: inline-block;
    border: 1px solid #e5e7eb;
    border-radius: 0.5rem;
    overflow: hidden;
    background: white;
}

.qr-code {
    display: block;
}

.qr-logo {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background: white;
    border-radius: 0.25rem;
    padding: 4px;
}

.qr-logo img {
    width: 100%;
    height: 100%;
    object-fit: contain;
}

.qr-download-btn {
    margin-top: 0.5rem;
    padding: 0.375rem 0.75rem;
    border: 1px solid #d1d5db;
    background: white;
    border-radius: 0.375rem;
    cursor: pointer;
    font-size: 0.875rem;
}

.qr-download-btn:hover {
    background: #f3f4f6;
}
"""
