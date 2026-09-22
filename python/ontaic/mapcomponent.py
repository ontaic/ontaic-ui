"""Map component using Leaflet."""
from typing import Any, Callable, Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum


class MapTile(str, Enum):
    """Map tile providers."""
    OSM = "osm"
    CARTO = "carto"
    STAMEN_TONER = "stamen_toner"
    STAMEN_TERRAIN = "stamen_terrain"
    ESRI = "esri"
    CARTO_DARK = "carto_dark"
    CARTO_LIGHT = "carto_light"


class MarkerIcon(str, Enum):
    """Marker icons."""
    DEFAULT = "default"
    RED = "red"
    BLUE = "blue"
    GREEN = "green"
    YELLOW = "yellow"
    PURPLE = "purple"
    CUSTOM = "custom"


@dataclass
class LatLng:
    """Latitude/Longitude."""
    lat: float
    lng: float
    
    def to_dict(self) -> dict:
        return {"lat": self.lat, "lng": self.lng}


@dataclass
class Marker:
    """Map marker."""
    id: str
    position: LatLng
    title: str = ""
    description: str = ""
    icon: MarkerIcon = MarkerIcon.DEFAULT
    icon_url: str = ""
    draggable: bool = False
    popup: bool = True
    tooltip: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "position": self.position.to_dict(),
            "title": self.title,
            "description": self.description,
            "icon": self.icon.value,
            "iconUrl": self.icon_url,
            "draggable": self.draggable,
            "popup": self.popup,
            "tooltip": self.tooltip,
        }


@dataclass
class Polyline:
    """Map polyline."""
    id: str
    points: List[LatLng]
    color: str = "#3b82f6"
    weight: int = 3
    opacity: float = 1.0
    dashed: bool = False
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "points": [p.to_dict() for p in self.points],
            "color": self.color,
            "weight": self.weight,
            "opacity": self.opacity,
            "dashed": self.dashed,
        }


@dataclass
class Polygon:
    """Map polygon."""
    id: str
    points: List[LatLng]
    color: str = "#3b82f6"
    fill_color: str = "#3b82f6"
    fill_opacity: float = 0.2
    weight: int = 3
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "points": [p.to_dict() for p in self.points],
            "color": self.color,
            "fillColor": self.fill_color,
            "fillOpacity": self.fill_opacity,
            "weight": self.weight,
        }


@dataclass
class Circle:
    """Map circle."""
    id: str
    center: LatLng
    radius: float
    color: str = "#3b82f6"
    fill_color: str = "#3b82f6"
    fill_opacity: float = 0.2
    weight: int = 2
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "center": self.center.to_dict(),
            "radius": self.radius,
            "color": self.color,
            "fillColor": self.fill_color,
            "fillOpacity": self.fill_opacity,
            "weight": self.weight,
        }


class MapComponent:
    """Map component using Leaflet."""
    
    def __init__(self, center: LatLng = None, zoom: int = 13):
        self._center = center or LatLng(51.505, -0.09)
        self._zoom = zoom
        self._tile: MapTile = MapTile.OSM
        self._markers: List[Marker] = []
        self._polylines: List[Polyline] = []
        self._polygons: List[Polygon] = []
        self._circles: List[Circle] = []
        self._show_controls: bool = True
        self._show_zoom: bool = True
        self._show_scale: bool = True
        self._show_attribution: bool = True
        self._draggable: bool = True
        self._scroll_wheel_zoom: bool = True
        self._double_click_zoom: bool = True
        self._keyboard: bool = True
        self._width: int = 800
        self._height: int = 600
        self._min_zoom: int = 1
        self._max_zoom: int = 18
        self._on_marker_click: Optional[Callable] = None
        self._on_map_click: Optional[Callable] = None
        self._on_marker_drag: Optional[Callable] = None
        self._class_name: str = ""
        self._label: str = ""
        self._help_text: str = ""
    
    def center(self, lat: float, lng: float) -> "MapComponent":
        """Set map center."""
        self._center = LatLng(lat, lng)
        return self
    
    def zoom(self, zoom: int) -> "MapComponent":
        """Set zoom level."""
        self._zoom = zoom
        return self
    
    def tile(self, tile: MapTile) -> "MapComponent":
        """Set tile provider."""
        self._tile = tile
        return self
    
    def add_marker(self, marker: Marker) -> "MapComponent":
        """Add a marker."""
        self._markers.append(marker)
        return self
    
    def marker(self, lat: float, lng: float, title: str = "", **kwargs) -> "MapComponent":
        """Add a marker."""
        id = f"marker_{len(self._markers)}"
        m = Marker(id=id, position=LatLng(lat, lng), title=title, **kwargs)
        self._markers.append(m)
        return self
    
    def add_polyline(self, polyline: Polyline) -> "MapComponent":
        """Add a polyline."""
        self._polylines.append(polyline)
        return self
    
    def polyline(self, points: List[tuple], color: str = "#3b82f6", **kwargs) -> "MapComponent":
        """Add a polyline."""
        id = f"poly_{len(self._polylines)}"
        latlngs = [LatLng(p[0], p[1]) for p in points]
        p = Polyline(id=id, points=latlngs, color=color, **kwargs)
        self._polylines.append(p)
        return self
    
    def add_polygon(self, polygon: Polygon) -> "MapComponent":
        """Add a polygon."""
        self._polygons.append(polygon)
        return self
    
    def add_circle(self, circle: Circle) -> "MapComponent":
        """Add a circle."""
        self._circles.append(circle)
        return self
    
    def circle(self, lat: float, lng: float, radius: float, color: str = "#3b82f6", **kwargs) -> "MapComponent":
        """Add a circle."""
        id = f"circle_{len(self._circles)}"
        c = Circle(id=id, center=LatLng(lat, lng), radius=radius, color=color, **kwargs)
        self._circles.append(c)
        return self
    
    def show_controls(self, show: bool = True) -> "MapComponent":
        """Toggle controls."""
        self._show_controls = show
        return self
    
    def show_scale(self, show: bool = True) -> "MapComponent":
        """Toggle scale."""
        self._show_scale = show
        return self
    
    def draggable(self, draggable: bool = True) -> "MapComponent":
        """Toggle draggable."""
        self._draggable = draggable
        return self
    
    def scroll_wheel_zoom(self, enabled: bool = True) -> "MapComponent":
        """Toggle scroll wheel zoom."""
        self._scroll_wheel_zoom = enabled
        return self
    
    def size(self, width: int, height: int) -> "MapComponent":
        """Set size."""
        self._width = width
        self._height = height
        return self
    
    def zoom_range(self, min_zoom: int, max_zoom: int) -> "MapComponent":
        """Set zoom range."""
        self._min_zoom = min_zoom
        self._max_zoom = max_zoom
        return self
    
    def on_marker_click(self, callback: Callable) -> "MapComponent":
        """Set marker click handler."""
        self._on_marker_click = callback
        return self
    
    def on_map_click(self, callback: Callable) -> "MapComponent":
        """Set map click handler."""
        self._on_map_click = callback
        return self
    
    def class_name(self, class_name: str) -> "MapComponent":
        """Set CSS class."""
        self._class_name = class_name
        return self
    
    def label(self, label: str) -> "MapComponent":
        """Set label."""
        self._label = label
        return self
    
    def help_text(self, text: str) -> "MapComponent":
        """Set help text."""
        self._help_text = text
        return self
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "center": self._center.to_dict(),
            "zoom": self._zoom,
            "tile": self._tile.value,
            "markers": [m.to_dict() for m in self._markers],
            "polylines": [p.to_dict() for p in self._polylines],
            "polygons": [p.to_dict() for p in self._polygons],
            "circles": [c.to_dict() for c in self._circles],
            "showControls": self._show_controls,
            "showZoom": self._show_zoom,
            "showScale": self._show_scale,
            "draggable": self._draggable,
            "scrollWheelZoom": self._scroll_wheel_zoom,
            "width": self._width,
            "height": self._height,
            "minZoom": self._min_zoom,
            "maxZoom": self._max_zoom,
        }
    
    def to_html(self) -> str:
        """Generate HTML."""
        label_html = f'<h3 class="map-label">{self._label}</h3>' if self._label else ""
        help_html = f'<p class="map-help">{self._help_text}</p>' if self._help_text else ""
        class_attr = f" {self._class_name}" if self._class_name else ""
        
        return f'''<div class="map-container{class_attr}">
            {label_html}
            <div class="map-wrapper">
                <div id="leaflet-map" class="leaflet-map" style="width: {self._width}px; height: {self._height}px;"></div>
            </div>
            {help_html}
        </div>'''
    
    def generate_js_code(self) -> str:
        """Generate JavaScript."""
        config = self.to_dict()
        markers_json = str(config["markers"]).replace("'", '"')
        polylines_json = str(config["polylines"]).replace("'", '"')
        polygons_json = str(config["polygons"]).replace("'", '"')
        circles_json = str(config["circles"]).replace("'", '"')
        
        tile_urls = {
            "osm": "https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png",
            "carto": "https://{{s}}.basemaps.cartocdn.com/light_all/{{z}}/{{x}}/{{y}}@2x.png",
            "carto_dark": "https://{{s}}.basemaps.cartocdn.com/dark_all/{{z}}/{{x}}/{{y}}@2x.png",
            "carto_light": "https://{{s}}.basemaps.cartocdn.com/light_all/{{z}}/{{x}}/{{y}}@2x.png",
        }
        tile_url = tile_urls.get(config["tile"], tile_urls["osm"])
        
        return f"""
        // Map Component
        (function() {{
            const config = {{
                center: [{config['center']['lat']}, {config['center']['lng']}],
                zoom: {config['zoom']},
                markers: {markers_json},
                polylines: {polylines_json},
                polygons: {polygons_json},
                circles: {circles_json},
                scrollWheelZoom: {str(config['scrollWheelZoom']).lower()},
                minZoom: {config['minZoom']},
                maxZoom: {config['maxZoom']},
            }};
            
            // Initialize map (placeholder - requires Leaflet)
            const mapContainer = document.getElementById('leaflet-map');
            if (!mapContainer) return;
            
            mapContainer.style.background = '#e5e7eb';
            mapContainer.style.display = 'flex';
            mapContainer.style.alignItems = 'center';
            mapContainer.style.justifyContent = 'center';
            mapContainer.style.fontFamily = 'system-ui';
            mapContainer.style.color = '#374151';
            mapContainer.innerHTML = '<div style="text-align:center"><div style="font-size:48px;margin-bottom:16px">&#x1F5FA;</div><div style="font-size:16px;font-weight:600">Map Component</div><div style="font-size:14px;margin-top:8px">Requires Leaflet.js</div><div style="font-size:12px;margin-top:4px;color:#6b7280">Center: ' + config.center[0].toFixed(4) + ', ' + config.center[1].toFixed(4) + '</div><div style="font-size:12px;margin-top:4px;color:#6b7280">Markers: ' + config.markers.length + ' | Shapes: ' + (config.polylines.length + config.polygons.length + config.circles.length) + '</div></div>';
            
            // Marker list
            if (config.markers.length > 0) {{
                const markerList = document.createElement('div');
                markerList.className = 'map-marker-list';
                markerList.innerHTML = config.markers.map(m => 
                    '<div class="map-marker-item" data-id="' + m.id + '">' +
                    '<span class="map-marker-dot" style="background:' + (m.icon === 'red' ? '#ef4444' : m.icon === 'blue' ? '#3b82f6' : m.icon === 'green' ? '#22c55e' : '#6b7280') + '"></span>' +
                    '<span class="map-marker-title">' + (m.title || m.id) + '</span>' +
                    (m.description ? '<span class="map-marker-desc">' + m.description + '</span>' : '') +
                    '</div>'
                ).join('');
                mapContainer.appendChild(markerList);
            }}
            
            // In real implementation, use Leaflet:
            // const map = L.map('leaflet-map').setView(config.center, config.zoom);
            // L.tileLayer('{tile_url}').addTo(map);
            // config.markers.forEach(m => L.marker([m.position.lat, m.position.lng]).addTo(map));
        }})();
        """


def create_map(center_lat: float = 51.505, center_lng: float = -0.09, zoom: int = 13) -> MapComponent:
    """Create a map component."""
    return MapComponent(center=LatLng(center_lat, center_lng), zoom=zoom)


def lat_lng(lat: float, lng: float) -> LatLng:
    """Create a LatLng."""
    return LatLng(lat=lat, lng=lng)


def map_marker(lat: float, lng: float, title: str = "", **kwargs) -> Marker:
    """Create a map marker."""
    return Marker(id=f"marker_{id(lat)}_{id(lng)}", position=LatLng(lat, lng), title=title, **kwargs)


MAP_CSS = """
.map-container {
    border: 1px solid #e5e7eb;
    border-radius: 0.5rem;
    overflow: hidden;
    background: white;
}

.map-label {
    padding: 0.75rem 1rem;
    margin: 0;
    font-size: 1.125rem;
    font-weight: 600;
    color: #111827;
    border-bottom: 1px solid #e5e7eb;
}

.map-wrapper {
    position: relative;
}

.leaflet-map {
    background: #e5e7eb;
}

.map-marker-list {
    padding: 0.5rem;
    max-height: 150px;
    overflow-y: auto;
    border-top: 1px solid #e5e7eb;
}

.map-marker-item {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.375rem 0.5rem;
    border-radius: 0.25rem;
    cursor: pointer;
}

.map-marker-item:hover {
    background: #f3f4f6;
}

.map-marker-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    flex-shrink: 0;
}

.map-marker-title {
    font-size: 0.875rem;
    font-weight: 500;
    color: #111827;
}

.map-marker-desc {
    font-size: 0.75rem;
    color: #6b7280;
    margin-left: auto;
}

.map-help {
    padding: 0.75rem 1rem;
    margin: 0;
    font-size: 0.875rem;
    color: #6b7280;
    border-top: 1px solid #e5e7eb;
}
"""
