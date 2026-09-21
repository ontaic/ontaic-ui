"""Animation support for ontaic."""
import json
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field


@dataclass
class Keyframe:
    """Animation keyframe."""
    offset: float  # 0-100
    properties: Dict[str, str]
    
    def to_dict(self) -> Dict[str, Any]:
        return {f"{self.offset}%": self.properties}


@dataclass
class Animation:
    """Animation definition."""
    name: str
    duration: str = "0.3s"
    timing_function: str = "ease"
    delay: str = "0s"
    iteration_count: str = "1"
    direction: str = "normal"
    fill_mode: str = "forwards"
    play_state: str = "running"
    keyframes: List[Keyframe] = field(default_factory=list)
    
    def to_css(self) -> str:
        """Generate CSS for this animation."""
        # Keyframes
        keyframes_css = f"@keyframes {self.name} {{\n"
        for kf in self.keyframes:
            for offset, props in kf.to_dict().items():
                keyframes_css += f"  {offset} {{\n"
                for prop, value in props.items():
                    keyframes_css += f"    {prop}: {value};\n"
                keyframes_css += "  }\n"
        keyframes_css += "}\n"
        
        return keyframes_css
    
    def to_animation_property(self) -> str:
        """Generate the animation CSS property value."""
        return f"{self.name} {self.duration} {self.timing_function} {self.delay} {self.iteration_count} {self.direction} {self.fill_mode} {self.play_state}"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "duration": self.duration,
            "timingFunction": self.timing_function,
            "delay": self.delay,
            "iterationCount": self.iteration_count,
            "direction": self.direction,
            "fillMode": self.fill_mode,
            "playState": self.play_state,
        }


# Predefined animations
FADE_IN = Animation(
    name="fadeIn",
    duration="0.3s",
    keyframes=[
        Keyframe(0, {"opacity": "0"}),
        Keyframe(100, {"opacity": "1"}),
    ],
)

FADE_OUT = Animation(
    name="fadeOut",
    duration="0.3s",
    keyframes=[
        Keyframe(0, {"opacity": "1"}),
        Keyframe(100, {"opacity": "0"}),
    ],
)

SLIDE_IN_UP = Animation(
    name="slideInUp",
    duration="0.3s",
    keyframes=[
        Keyframe(0, {"transform": "translateY(20px)", "opacity": "0"}),
        Keyframe(100, {"transform": "translateY(0)", "opacity": "1"}),
    ],
)

SLIDE_IN_DOWN = Animation(
    name="slideInDown",
    duration="0.3s",
    keyframes=[
        Keyframe(0, {"transform": "translateY(-20px)", "opacity": "0"}),
        Keyframe(100, {"transform": "translateY(0)", "opacity": "1"}),
    ],
)

SLIDE_IN_LEFT = Animation(
    name="slideInLeft",
    duration="0.3s",
    keyframes=[
        Keyframe(0, {"transform": "translateX(-20px)", "opacity": "0"}),
        Keyframe(100, {"transform": "translateX(0)", "opacity": "1"}),
    ],
)

SLIDE_IN_RIGHT = Animation(
    name="slideInRight",
    duration="0.3s",
    keyframes=[
        Keyframe(0, {"transform": "translateX(20px)", "opacity": "0"}),
        Keyframe(100, {"transform": "translateX(0)", "opacity": "1"}),
    ],
)

SCALE_IN = Animation(
    name="scaleIn",
    duration="0.3s",
    keyframes=[
        Keyframe(0, {"transform": "scale(0.9)", "opacity": "0"}),
        Keyframe(100, {"transform": "scale(1)", "opacity": "1"}),
    ],
)

SCALE_OUT = Animation(
    name="scaleOut",
    duration="0.3s",
    keyframes=[
        Keyframe(0, {"transform": "scale(1)", "opacity": "1"}),
        Keyframe(100, {"transform": "scale(0.9)", "opacity": "0"}),
    ],
)

BOUNCE = Animation(
    name="bounce",
    duration="1s",
    iteration_count="infinite",
    keyframes=[
        Keyframe(0, {"transform": "translateY(0)"}),
        Keyframe(50, {"transform": "translateY(-10px)"}),
        Keyframe(100, {"transform": "translateY(0)"}),
    ],
)

SPIN = Animation(
    name="spin",
    duration="1s",
    iteration_count="infinite",
    timing_function="linear",
    keyframes=[
        Keyframe(0, {"transform": "rotate(0deg)"}),
        Keyframe(100, {"transform": "rotate(360deg)"}),
    ],
)

PULSE = Animation(
    name="pulse",
    duration="2s",
    iteration_count="infinite",
    keyframes=[
        Keyframe(0, {"opacity": "1"}),
        Keyframe(50, {"opacity": "0.5"}),
        Keyframe(100, {"opacity": "1"}),
    ],
)

SHAKE = Animation(
    name="shake",
    duration="0.5s",
    keyframes=[
        Keyframe(0, {"transform": "translateX(0)"}),
        Keyframe(25, {"transform": "translateX(-5px)"}),
        Keyframe(50, {"transform": "translateX(5px)"}),
        Keyframe(75, {"transform": "translateX(-5px)"}),
        Keyframe(100, {"transform": "translateX(0)"}),
    ],
)

# Predefined transitions
TRANSITION_FADE = "opacity 0.3s ease"
TRANSITION_SLIDE_UP = "transform 0.3s ease, opacity 0.3s ease"
TRANSITION_SLIDE_DOWN = "transform 0.3s ease, opacity 0.3s ease"
TRANSITION_SCALE = "transform 0.3s ease, opacity 0.3s ease"
TRANSITION_ALL = "all 0.3s ease"


class AnimationManager:
    """Animation manager for ontaic."""
    
    def __init__(self):
        self.animations: Dict[str, Animation] = {
            "fadeIn": FADE_IN,
            "fadeOut": FADE_OUT,
            "slideInUp": SLIDE_IN_UP,
            "slideInDown": SLIDE_IN_DOWN,
            "slideInLeft": SLIDE_IN_LEFT,
            "slideInRight": SLIDE_IN_RIGHT,
            "scaleIn": SCALE_IN,
            "scaleOut": SCALE_OUT,
            "bounce": BOUNCE,
            "spin": SPIN,
            "pulse": PULSE,
            "shake": SHAKE,
        }
        self._custom_keyframes: List[str] = []
    
    def register(self, animation: Animation):
        """Register a custom animation."""
        self.animations[animation.name] = animation
    
    def get(self, name: str) -> Optional[Animation]:
        """Get an animation by name."""
        return self.animations.get(name)
    
    def generate_css(self) -> str:
        """Generate all animation CSS."""
        css = ""
        for animation in self.animations.values():
            css += animation.to_css() + "\n"
        return css
    
    def generate_keyframes_js(self) -> str:
        """Generate JavaScript keyframes."""
        keyframes = {}
        for name, animation in self.animations.items():
            keyframes[name] = [kf.to_dict() for kf in animation.keyframes]
        return json.dumps(keyframes, indent=2)


class AnimatedElement:
    """Element with animation support."""
    
    def __init__(
        self,
        animation: str = None,
        duration: str = "0.3s",
        delay: str = "0s",
        trigger: str = "hover",  # hover, click, load, scroll
    ):
        self.animation = animation
        self.duration = duration
        self.delay = delay
        self.trigger = trigger
    
    def get_animation_style(self) -> str:
        """Get CSS style for animation."""
        if not self.animation:
            return ""
        
        animation_manager = AnimationManager()
        anim = animation_manager.get(self.animation)
        if not anim:
            return ""
        
        anim.duration = self.duration
        anim.delay = self.delay
        
        return f"animation: {anim.to_animation_property()}"
    
    def get_transition_style(self) -> str:
        """Get CSS transition style."""
        return f"transition: {TRANSITION_ALL}"


# Animated components
class FadeIn:
    """Fade in animation wrapper."""
    
    def __init__(self, duration: str = "0.3s", delay: str = "0s"):
        self.duration = duration
        self.delay = delay
    
    def render(self, content: str) -> str:
        return f'<div style="animation: fadeIn {self.duration} ease {delay} forwards">{content}</div>'


class SlideIn:
    """Slide in animation wrapper."""
    
    def __init__(self, direction: str = "up", duration: str = "0.3s", delay: str = "0s"):
        self.direction = direction
        self.duration = duration
        self.delay = delay
    
    def render(self, content: str) -> str:
        animation_map = {
            "up": "slideInUp",
            "down": "slideInDown",
            "left": "slideInLeft",
            "right": "slideInRight",
        }
        animation = animation_map.get(self.direction, "slideInUp")
        return f'<div style="animation: {animation} {self.duration} ease {self.delay} forwards">{content}</div>'


class ScaleIn:
    """Scale in animation wrapper."""
    
    def __init__(self, duration: str = "0.3s", delay: str = "0s"):
        self.duration = duration
        self.delay = delay
    
    def render(self, content: str) -> str:
        return f'<div style="animation: scaleIn {self.duration} ease {self.delay} forwards">{content}</div>'


class Spinner:
    """Loading spinner component."""
    
    def __init__(self, size: str = "w-8 h-8", color: str = "text-blue-500"):
        self.size = size
        self.color = color
    
    def render(self) -> str:
        return f"""
        <div class="{self.size} {self.color} animate-spin">
            <svg class="w-full h-full" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
        </div>
        """


class Skeleton:
    """Skeleton loading component."""
    
    def __init__(
        self,
        width: str = "w-full",
        height: str = "h-4",
        rounded: str = "rounded",
        class_name: str = "",
    ):
        self.width = width
        self.height = height
        self.rounded = rounded
        self.class_name = class_name
    
    def render(self) -> str:
        return f"""
        <div class="{self.width} {self.height} {self.rounded} bg-gray-200 animate-pulse {self.class_name}"></div>
        """


class ProgressBar:
    """Animated progress bar."""
    
    def __init__(
        self,
        value: float,
        max_value: float = 100,
        color: str = "bg-blue-500",
        height: str = "h-2",
        animated: bool = True,
    ):
        self.value = value
        self.max_value = max_value
        self.color = color
        self.height = height
        self.animated = animated
    
    def render(self) -> str:
        percentage = min(100, (self.value / self.max_value) * 100)
        animation = "transition: width 0.5s ease" if self.animated else ""
        
        return f"""
        <div class="w-full bg-gray-200 rounded-full {self.height}">
            <div class="{self.color} {self.height} rounded-full" style="width: {percentage}%; {animation}"></div>
        </div>
        """


class Collapse:
    """Collapsible/accordion animation."""
    
    def __init__(self, is_open: bool = False, duration: str = "0.3s"):
        self.is_open = is_open
        self.duration = duration
    
    def render(self, header: str, content: str) -> str:
        max_height = "auto" if self.is_open else "0"
        overflow = "visible" if self.is_open else "hidden"
        opacity = "1" if self.is_open else "0"
        transform = "rotate(180deg)" if self.is_open else "rotate(0deg)"
        
        return f"""
        <div class="border rounded-lg">
            <button class="w-full px-4 py-3 text-left font-medium flex justify-between items-center"
                onclick="this.nextElementSibling.style.maxHeight = this.nextElementSibling.style.maxHeight === '0px' ? this.nextElementSibling.scrollHeight + 'px' : '0px'; this.querySelector('svg').style.transform = this.querySelector('svg').style.transform === 'rotate(180deg)' ? 'rotate(0deg)' : 'rotate(180deg)'">
                {header}
                <svg class="w-5 h-5 transform transition-transform" style="transform: {transform}" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
                </svg>
            </button>
            <div class="overflow-hidden transition-all" style="max-height: {max_height}; transition: max-height {self.duration} ease">
                <div class="px-4 py-3 border-t">
                    {content}
                </div>
            </div>
        </div>
        """


class Tabs:
    """Animated tabs component."""
    
    def __init__(self, tabs: List[Dict[str, str]], active_tab: str = None):
        self.tabs = tabs
        self.active_tab = active_tab or (tabs[0]["id"] if tabs else "")
    
    def render(self) -> str:
        tabs_id = f"tabs-{id(self)}"
        
        tabs_html = ""
        for tab in self.tabs:
            active = "border-b-2 border-blue-500 text-blue-600" if tab["id"] == self.active_tab else "text-gray-500 hover:text-gray-700"
            tabs_html += f"""
            <button class="px-4 py-2 font-medium {active} transition-colors" 
                onclick="switchTab('{tabs_id}', '{tab['id']}')">
                {tab['label']}
            </button>
            """
        
        panels_html = ""
        for tab in self.tabs:
            display = "block" if tab["id"] == self.active_tab else "none"
            panels_html += f"""
            <div id="{tabs_id}-panel-{tab['id']}" class="py-4" style="display: {display}">
                {tab.get('content', '')}
            </div>
            """
        
        return f"""
        <div id="{tabs_id}">
            <div class="flex border-b">
                {tabs_html}
            </div>
            <div class="relative">
                {panels_html}
            </div>
        </div>
        <script>
        function switchTab(tabsId, tabId) {{
            const container = document.getElementById(tabsId);
            const panels = container.querySelectorAll('[id^="' + tabsId + '-panel-"]');
            const buttons = container.querySelectorAll('button');
            
            panels.forEach(panel => {{
                panel.style.display = 'none';
                panel.style.opacity = '0';
            }});
            
            buttons.forEach(btn => {{
                btn.classList.remove('border-b-2', 'border-blue-500', 'text-blue-600');
                btn.classList.add('text-gray-500');
            }});
            
            const activePanel = document.getElementById(tabsId + '-panel-' + tabId);
            if (activePanel) {{
                activePanel.style.display = 'block';
                setTimeout(() => activePanel.style.opacity = '1', 10);
            }}
            
            event.target.classList.add('border-b-2', 'border-blue-500', 'text-blue-600');
            event.target.classList.remove('text-gray-500');
        }}
        </script>
        """


class Carousel:
    """Animated carousel/slider component."""
    
    def __init__(
        self,
        items: List[Dict[str, str]],
        auto_play: bool = True,
        interval: int = 5000,
        show_dots: bool = True,
        show_arrows: bool = True,
    ):
        self.items = items
        self.auto_play = auto_play
        self.interval = interval
        self.show_dots = show_dots
        self.show_arrows = show_arrows
    
    def render(self) -> str:
        carousel_id = f"carousel-{id(self)}"
        
        items_html = ""
        for i, item in enumerate(self.items):
            active = "opacity-100" if i == 0 else "opacity-0"
            items_html += f"""
            <div class="absolute inset-0 transition-opacity duration-500 {active}" data-slide="{i}">
                <div class="w-full h-full bg-gray-200 flex items-center justify-center">
                    <div class="text-center">
                        <h3 class="text-2xl font-bold mb-2">{item.get('title', '')}</h3>
                        <p class="text-gray-600">{item.get('description', '')}</p>
                    </div>
                </div>
            </div>
            """
        
        dots_html = ""
        if self.show_dots:
            for i in range(len(self.items)):
                active = "bg-blue-500" if i == 0 else "bg-gray-300"
                dots_html += f"""
                <button class="w-3 h-3 rounded-full {active} transition-colors" 
                    onclick="goToSlide('{carousel_id}', {i})"></button>
                """
        
        arrows_html = ""
        if self.show_arrows:
            arrows_html = f"""
            <button class="absolute left-4 top-1/2 -translate-y-1/2 w-10 h-10 bg-white/80 rounded-full flex items-center justify-center hover:bg-white transition-colors"
                onclick="prevSlide('{carousel_id}')">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path>
                </svg>
            </button>
            <button class="absolute right-4 top-1/2 -translate-y-1/2 w-10 h-10 bg-white/80 rounded-full flex items-center justify-center hover:bg-white transition-colors"
                onclick="nextSlide('{carousel_id}')">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
                </svg>
            </button>
            """
        
        auto_play_script = ""
        if self.auto_play:
            auto_play_script = f"""
            setInterval(() => nextSlide('{carousel_id}'), {self.interval});
            """
        
        return f"""
        <div id="{carousel_id}" class="relative overflow-hidden rounded-lg">
            <div class="relative h-64">
                {items_html}
            </div>
            {arrows_html}
            <div class="flex justify-center gap-2 mt-4">
                {dots_html}
            </div>
        </div>
        <script>
        let {carousel_id}_current = 0;
        const {carousel_id}_total = {len(self.items)};
        
        function goToSlide(id, index) {{
            const slides = document.querySelectorAll(`#${{id}} [data-slide]`);
            const dots = document.querySelectorAll(`#${{id}} ~ div button`);
            
            slides.forEach((slide, i) => {{
                slide.style.opacity = i === index ? '1' : '0';
            }});
            
            dots.forEach((dot, i) => {{
                dot.classList.toggle('bg-blue-500', i === index);
                dot.classList.toggle('bg-gray-300', i !== index);
            }});
            
            {carousel_id}_current = index;
        }}
        
        function nextSlide(id) {{
            const next = ({carousel_id}_current + 1) % {carousel_id}_total;
            goToSlide(id, next);
        }}
        
        function prevSlide(id) {{
            const prev = ({carousel_id}_current - 1 + {carousel_id}_total) % {carousel_id}_total;
            goToSlide(id, prev);
        }}
        
        {auto_play_script}
        </script>
        """


# Generate animation CSS for inclusion in pages
def generate_animation_css() -> str:
    """Generate all animation CSS."""
    manager = AnimationManager()
    return manager.generate_css()
