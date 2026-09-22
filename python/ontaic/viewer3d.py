"""3D viewer component using Three.js."""
from typing import Any, Callable, Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum


class SceneType(str, Enum):
    """Scene type."""
    PERSPECTIVE = "perspective"
    ORTHOGRAPHIC = "orthographic"


class ObjectType(str, Enum):
    """3D object type."""
    BOX = "box"
    SPHERE = "sphere"
    CYLINDER = "cylinder"
    CONE = "cone"
    TORUS = "torus"
    PLANE = "plane"
    CUSTOM = "custom"


class ViewMode(str, Enum):
    """View mode."""
    ORBIT = "orbit"
    FLY = "fly"
    LOCKED = "locked"


@dataclass
class Material:
    """Material definition."""
    color: str = "#ffffff"
    opacity: float = 1.0
    metalness: float = 0.5
    roughness: float = 0.5
    wireframe: bool = False
    texture_url: str = ""
    normal_map: str = ""
    
    def to_dict(self) -> dict:
        return {
            "color": self.color,
            "opacity": self.opacity,
            "metalness": self.metalness,
            "roughness": self.roughness,
            "wireframe": self.wireframe,
            "textureUrl": self.texture_url,
            "normalMap": self.normal_map,
        }


@dataclass
class Position:
    """3D position."""
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0
    
    def to_dict(self) -> dict:
        return {"x": self.x, "y": self.y, "z": self.z}


@dataclass
class Rotation:
    """3D rotation in degrees."""
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0
    
    def to_dict(self) -> dict:
        return {"x": self.x, "y": self.y, "z": self.z}


@dataclass
class Scale:
    """3D scale."""
    x: float = 1.0
    y: float = 1.0
    z: float = 1.0
    
    def to_dict(self) -> dict:
        return {"x": self.x, "y": self.y, "z": self.z}


@dataclass
class SceneObject:
    """A 3D object in the scene."""
    object_type: ObjectType
    name: str = ""
    position: Position = field(default_factory=Position)
    rotation: Rotation = field(default_factory=Rotation)
    scale: Scale = field(default_factory=Scale)
    material: Material = field(default_factory=Material)
    geometry_params: Dict[str, Any] = field(default_factory=dict)
    visible: bool = True
    cast_shadow: bool = True
    receive_shadow: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> dict:
        return {
            "type": self.object_type.value,
            "name": self.name,
            "position": self.position.to_dict(),
            "rotation": self.rotation.to_dict(),
            "scale": self.scale.to_dict(),
            "material": self.material.to_dict(),
            "geometryParams": self.geometry_params,
            "visible": self.visible,
            "castShadow": self.cast_shadow,
            "receiveShadow": self.receive_shadow,
        }


@dataclass
class CameraConfig:
    """Camera configuration."""
    scene_type: SceneType = SceneType.PERSPECTIVE
    fov: float = 75.0
    near: float = 0.1
    far: float = 1000.0
    position: Position = field(default_factory=lambda: Position(0, 5, 10))
    look_at: Position = field(default_factory=Position)
    zoom: float = 1.0
    
    def to_dict(self) -> dict:
        return {
            "type": self.scene_type.value,
            "fov": self.fov,
            "near": self.near,
            "far": self.far,
            "position": self.position.to_dict(),
            "lookAt": self.look_at.to_dict(),
            "zoom": self.zoom,
        }


@dataclass
class LightConfig:
    """Light configuration."""
    light_type: str = "ambient"
    color: str = "#ffffff"
    intensity: float = 1.0
    position: Position = field(default_factory=Position)
    cast_shadow: bool = False
    
    def to_dict(self) -> dict:
        return {
            "type": self.light_type,
            "color": self.color,
            "intensity": self.intensity,
            "position": self.position.to_dict(),
            "castShadow": self.cast_shadow,
        }


class Viewer3D:
    """3D viewer component using Three.js."""
    
    def __init__(self):
        self._objects: List[SceneObject] = []
        self._camera: CameraConfig = CameraConfig()
        self._lights: List[LightConfig] = [
            LightConfig(light_type="ambient", intensity=0.5),
            LightConfig(light_type="directional", position=Position(5, 10, 7.5), cast_shadow=True),
        ]
        self._view_mode: ViewMode = ViewMode.ORBIT
        self._show_grid: bool = True
        self._show_axes: bool = True
        self._show_controls: bool = True
        self._auto_rotate: bool = False
        self._auto_rotate_speed: float = 2.0
        self._background_color: str = "#1a1a1a"
        self._width: int = 800
        self._height: int = 600
        self._antialias: bool = True
        self._on_object_click: Optional[Callable] = None
        self._on_scene_ready: Optional[Callable] = None
        self._on_camera_change: Optional[Callable] = None
        self._selected_object: Optional[str] = None
        self._class_name: str = ""
        self._label: str = ""
        self._help_text: str = ""
    
    def add_object(self, obj: SceneObject) -> "Viewer3D":
        """Add object to scene."""
        self._objects.append(obj)
        return self
    
    def add_box(self, name: str = "", size: tuple = (1, 1, 1), **kwargs) -> "Viewer3D":
        """Add a box."""
        obj = SceneObject(
            object_type=ObjectType.BOX,
            name=name,
            geometry_params={"width": size[0], "height": size[1], "depth": size[2]},
            **kwargs,
        )
        self._objects.append(obj)
        return self
    
    def add_sphere(self, name: str = "", radius: float = 0.5, **kwargs) -> "Viewer3D":
        """Add a sphere."""
        obj = SceneObject(
            object_type=ObjectType.SPHERE,
            name=name,
            geometry_params={"radius": radius},
            **kwargs,
        )
        self._objects.append(obj)
        return self
    
    def add_cylinder(self, name: str = "", radius: float = 0.5, height: float = 1, **kwargs) -> "Viewer3D":
        """Add a cylinder."""
        obj = SceneObject(
            object_type=ObjectType.CYLINDER,
            name=name,
            geometry_params={"radius": radius, "height": height},
            **kwargs,
        )
        self._objects.append(obj)
        return self
    
    def add_cone(self, name: str = "", radius: float = 0.5, height: float = 1, **kwargs) -> "Viewer3D":
        """Add a cone."""
        obj = SceneObject(
            object_type=ObjectType.CONE,
            name=name,
            geometry_params={"radius": radius, "height": height},
            **kwargs,
        )
        self._objects.append(obj)
        return self
    
    def add_torus(self, name: str = "", radius: float = 0.5, tube: float = 0.2, **kwargs) -> "Viewer3D":
        """Add a torus."""
        obj = SceneObject(
            object_type=ObjectType.TORUS,
            name=name,
            geometry_params={"radius": radius, "tube": tube},
            **kwargs,
        )
        self._objects.append(obj)
        return self
    
    def add_plane(self, name: str = "", width: float = 10, height: float = 10, **kwargs) -> "Viewer3D":
        """Add a plane."""
        obj = SceneObject(
            object_type=ObjectType.PLANE,
            name=name,
            geometry_params={"width": width, "height": height},
            **kwargs,
        )
        self._objects.append(obj)
        return self
    
    def camera(self, config: CameraConfig) -> "Viewer3D":
        """Set camera configuration."""
        self._camera = config
        return self
    
    def add_light(self, light: LightConfig) -> "Viewer3D":
        """Add a light."""
        self._lights.append(light)
        return self
    
    def view_mode(self, mode: ViewMode) -> "Viewer3D":
        """Set view mode."""
        self._view_mode = mode
        return self
    
    def show_grid(self, show: bool = True) -> "Viewer3D":
        """Toggle grid."""
        self._show_grid = show
        return self
    
    def show_axes(self, show: bool = True) -> "Viewer3D":
        """Toggle axes."""
        self._show_axes = show
        return self
    
    def show_controls(self, show: bool = True) -> "Viewer3D":
        """Toggle controls."""
        self._show_controls = show
        return self
    
    def auto_rotate(self, enabled: bool = True, speed: float = 2.0) -> "Viewer3D":
        """Enable auto-rotation."""
        self._auto_rotate = enabled
        self._auto_rotate_speed = speed
        return self
    
    def background_color(self, color: str) -> "Viewer3D":
        """Set background color."""
        self._background_color = color
        return self
    
    def size(self, width: int, height: int) -> "Viewer3D":
        """Set viewer size."""
        self._width = width
        self._height = height
        return self
    
    def on_object_click(self, callback: Callable) -> "Viewer3D":
        """Set object click handler."""
        self._on_object_click = callback
        return self
    
    def on_scene_ready(self, callback: Callable) -> "Viewer3D":
        """Set scene ready handler."""
        self._on_scene_ready = callback
        return self
    
    def class_name(self, class_name: str) -> "Viewer3D":
        """Set CSS class."""
        self._class_name = class_name
        return self
    
    def label(self, label: str) -> "Viewer3D":
        """Set label."""
        self._label = label
        return self
    
    def help_text(self, text: str) -> "Viewer3D":
        """Set help text."""
        self._help_text = text
        return self
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "objects": [o.to_dict() for o in self._objects],
            "camera": self._camera.to_dict(),
            "lights": [l.to_dict() for l in self._lights],
            "viewMode": self._view_mode.value,
            "showGrid": self._show_grid,
            "showAxes": self._show_axes,
            "showControls": self._show_controls,
            "autoRotate": self._auto_rotate,
            "autoRotateSpeed": self._auto_rotate_speed,
            "backgroundColor": self._background_color,
            "width": self._width,
            "height": self._height,
            "antialias": self._antialias,
        }
    
    def to_html(self) -> str:
        """Generate HTML."""
        label_html = f'<h3 class="viewer3d-label">{self._label}</h3>' if self._label else ""
        help_html = f'<p class="viewer3d-help">{self._help_text}</p>' if self._help_text else ""
        class_attr = f" {self._class_name}" if self._class_name else ""
        
        controls_html = ""
        if self._show_controls:
            controls_html = f'''<div class="viewer3d-controls">
                <button type="button" class="viewer3d-btn" data-action="rotate-left">&#8634;</button>
                <button type="button" class="viewer3d-btn" data-action="rotate-right">&#8635;</button>
                <button type="button" class="viewer3d-btn" data-action="zoom-in">+</button>
                <button type="button" class="viewer3d-btn" data-action="zoom-out">-</button>
                <button type="button" class="viewer3d-btn" data-action="reset">Reset</button>
                <button type="button" class="viewer3d-btn" data-action="fullscreen">Fullscreen</button>
            </div>'''
        
        object_list = ""
        if self._objects:
            items = "".join(f'<li class="viewer3d-obj-item" data-name="{o.name}">{o.name or o.object_type.value}</li>' for o in self._objects)
            object_list = f'''<div class="viewer3d-objects">
                <h4>Objects ({len(self._objects)})</h4>
                <ul>{items}</ul>
            </div>'''
        
        return f'''<div class="viewer3d-container{class_attr}">
            {label_html}
            <div class="viewer3d-main">
                <canvas id="viewer3d-canvas" width="{self._width}" height="{self._height}"></canvas>
                {controls_html}
            </div>
            {object_list}
            {help_html}
        </div>'''
    
    def generate_js_code(self) -> str:
        """Generate JavaScript."""
        config = self.to_dict()
        objects_json = str(config["objects"]).replace("'", '"')
        camera_json = str(config["camera"]).replace("'", '"')
        lights_json = str(config["lights"]).replace("'", '"')
        
        return f"""
        // 3D Viewer
        (function() {{
            const config = {{
                objects: {objects_json},
                camera: {camera_json},
                lights: {lights_json},
                showGrid: {str(config["showGrid"]).lower()},
                showAxes: {str(config["showAxes"]).lower()},
                autoRotate: {str(config["autoRotate"]).lower()},
                autoRotateSpeed: {config["autoRotateSpeed"]},
                backgroundColor: "{config['backgroundColor']}",
            }};
            
            const canvas = document.getElementById('viewer3d-canvas');
            if (!canvas) return;
            
            const ctx = canvas.getContext('2d');
            ctx.fillStyle = config.backgroundColor;
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            
            ctx.fillStyle = '#ffffff';
            ctx.font = '14px system-ui';
            ctx.textAlign = 'center';
            ctx.fillText('3D Viewer (requires Three.js)', canvas.width / 2, canvas.height / 2 - 10);
            ctx.fillText(config.objects.length + ' objects in scene', canvas.width / 2, canvas.height / 2 + 15);
            
            // Grid
            if (config.showGrid) {{
                ctx.strokeStyle = 'rgba(255,255,255,0.1)';
                ctx.lineWidth = 1;
                for (let i = 0; i <= canvas.width; i += 40) {{
                    ctx.beginPath();
                    ctx.moveTo(i, 0);
                    ctx.lineTo(i, canvas.height);
                    ctx.stroke();
                }}
                for (let j = 0; j <= canvas.height; j += 40) {{
                    ctx.beginPath();
                    ctx.moveTo(0, j);
                    ctx.lineTo(canvas.width, j);
                    ctx.stroke();
                }}
            }}
            
            // Axes
            if (config.showAxes) {{
                ctx.lineWidth = 2;
                ctx.strokeStyle = '#ff4444';
                ctx.beginPath();
                ctx.moveTo(canvas.width / 2, canvas.height / 2);
                ctx.lineTo(canvas.width / 2 + 60, canvas.height / 2);
                ctx.stroke();
                ctx.fillStyle = '#ff4444';
                ctx.fillText('X', canvas.width / 2 + 70, canvas.height / 2);
                
                ctx.strokeStyle = '#44ff44';
                ctx.beginPath();
                ctx.moveTo(canvas.width / 2, canvas.height / 2);
                ctx.lineTo(canvas.width / 2, canvas.height / 2 - 60);
                ctx.stroke();
                ctx.fillStyle = '#44ff44';
                ctx.fillText('Y', canvas.width / 2, canvas.height / 2 - 70);
                
                ctx.strokeStyle = '#4444ff';
                ctx.beginPath();
                ctx.moveTo(canvas.width / 2, canvas.height / 2);
                ctx.lineTo(canvas.width / 2 + 40, canvas.height / 2 + 40);
                ctx.stroke();
                ctx.fillStyle = '#4444ff';
                ctx.fillText('Z', canvas.width / 2 + 55, canvas.height / 2 + 55);
            }}
            
            // Object labels
            config.objects.forEach((obj, i) => {{
                const x = canvas.width / 2 + (i - config.objects.length / 2) * 80;
                const y = canvas.height / 2;
                
                ctx.fillStyle = obj.material.color;
                ctx.globalAlpha = obj.material.opacity;
                
                switch (obj.type) {{
                    case 'box':
                        ctx.fillRect(x - 20, y - 20, 40, 40);
                        break;
                    case 'sphere':
                        ctx.beginPath();
                        ctx.arc(x, y, 20, 0, Math.PI * 2);
                        ctx.fill();
                        break;
                    default:
                        ctx.fillRect(x - 15, y - 25, 30, 50);
                }}
                
                ctx.globalAlpha = 1;
                ctx.fillStyle = '#ffffff';
                ctx.font = '10px system-ui';
                ctx.fillText(obj.name || obj.type, x, y + 35);
            }});
            
            // Controls
            document.querySelectorAll('.viewer3d-btn').forEach(btn => {{
                btn.addEventListener('click', () => {{
                    console.log('Action:', btn.dataset.action);
                }});
            }});
            
            // Object list click
            document.querySelectorAll('.viewer3d-obj-item').forEach(item => {{
                item.addEventListener('click', () => {{
                    console.log('Selected:', item.dataset.name);
                }});
            }});
        }})();
        """


def create_viewer_3d() -> Viewer3D:
    """Create a 3D viewer."""
    return Viewer3D()


def scene_object(obj_type: ObjectType, name: str = "", **kwargs) -> SceneObject:
    """Create a scene object."""
    return SceneObject(object_type=obj_type, name=name, **kwargs)


def camera_config(**kwargs) -> CameraConfig:
    """Create camera configuration."""
    return CameraConfig(**kwargs)


def light_config(light_type: str = "ambient", **kwargs) -> LightConfig:
    """Create light configuration."""
    return LightConfig(light_type=light_type, **kwargs)


VIEWER_3D_CSS = """
.viewer3d-container {
    border: 1px solid #374151;
    border-radius: 0.5rem;
    overflow: hidden;
    background: #0f0f0f;
}

.viewer3d-label {
    padding: 0.75rem 1rem;
    margin: 0;
    font-size: 1.125rem;
    font-weight: 600;
    color: #f9fafb;
    background: #1f2937;
    border-bottom: 1px solid #374151;
}

.viewer3d-main {
    position: relative;
}

.viewer3d-main canvas {
    display: block;
    width: 100%;
}

.viewer3d-controls {
    position: absolute;
    bottom: 1rem;
    left: 50%;
    transform: translateX(-50%);
    display: flex;
    gap: 0.5rem;
    padding: 0.5rem;
    background: rgba(0, 0, 0, 0.7);
    border-radius: 0.5rem;
}

.viewer3d-btn {
    padding: 0.375rem 0.75rem;
    border: 1px solid #4b5563;
    background: #1f2937;
    color: #f9fafb;
    border-radius: 0.25rem;
    cursor: pointer;
    font-size: 0.875rem;
}

.viewer3d-btn:hover {
    background: #374151;
}

.viewer3d-objects {
    padding: 0.75rem 1rem;
    background: #1f2937;
    border-top: 1px solid #374151;
}

.viewer3d-objects h4 {
    margin: 0 0 0.5rem;
    font-size: 0.875rem;
    color: #9ca3af;
}

.viewer3d-objects ul {
    margin: 0;
    padding: 0;
    list-style: none;
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
}

.viewer3d-obj-item {
    padding: 0.25rem 0.5rem;
    background: #374151;
    color: #f9fafb;
    border-radius: 0.25rem;
    font-size: 0.75rem;
    cursor: pointer;
}

.viewer3d-obj-item:hover {
    background: #4b5563;
}

.viewer3d-help {
    padding: 0.75rem 1rem;
    margin: 0;
    font-size: 0.875rem;
    color: #9ca3af;
    background: #1f2937;
    border-top: 1px solid #374151;
}
"""
