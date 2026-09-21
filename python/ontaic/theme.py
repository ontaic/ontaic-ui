"""Theming system for ontaic."""
import json
from typing import Any, Callable, Dict, List, Optional
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class ThemeColors:
    """Color palette for a theme."""
    primary: str = "#3B82F6"
    primary_hover: str = "#2563EB"
    primary_active: str = "#1D4ED8"
    secondary: str = "#6B7280"
    secondary_hover: str = "#4B5563"
    success: str = "#10B981"
    success_hover: str = "#059669"
    warning: str = "#F59E0B"
    warning_hover: str = "#D97706"
    danger: str = "#EF4444"
    danger_hover: str = "#DC2626"
    info: str = "#3B82F6"
    info_hover: str = "#2563EB"
    
    # Background colors
    background: str = "#FFFFFF"
    background_secondary: str = "#F9FAFB"
    background_tertiary: str = "#F3F4F6"
    
    # Text colors
    text_primary: str = "#111827"
    text_secondary: str = "#6B7280"
    text_tertiary: str = "#9CA3AF"
    text_inverse: str = "#FFFFFF"
    
    # Border colors
    border: str = "#E5E7EB"
    border_hover: str = "#D1D5DB"
    border_focus: str = "#3B82F6"
    
    # Shadow
    shadow: str = "0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)"
    shadow_md: str = "0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)"
    shadow_lg: str = "0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)"
    
    def to_dict(self) -> Dict[str, str]:
        return {k: v for k, v in self.__dict__.items()}


@dataclass
class ThemeSpacing:
    """Spacing scale for a theme."""
    xs: str = "0.25rem"
    sm: str = "0.5rem"
    md: str = "1rem"
    lg: str = "1.5rem"
    xl: str = "2rem"
    xxl: str = "3rem"
    
    def to_dict(self) -> Dict[str, str]:
        return {k: v for k, v in self.__dict__.items()}


@dataclass
class ThemeTypography:
    """Typography scale for a theme."""
    font_family: str = "Inter, system-ui, -apple-system, sans-serif"
    font_family_mono: str = "Fira Code, monospace"
    
    font_size_xs: str = "0.75rem"
    font_size_sm: str = "0.875rem"
    font_size_base: str = "1rem"
    font_size_lg: str = "1.125rem"
    font_size_xl: str = "1.25rem"
    font_size_2xl: str = "1.5rem"
    font_size_3xl: str = "1.875rem"
    font_size_4xl: str = "2.25rem"
    
    font_weight_normal: str = "400"
    font_weight_medium: str = "500"
    font_weight_semibold: str = "600"
    font_weight_bold: str = "700"
    
    line_height_tight: str = "1.25"
    line_height_normal: str = "1.5"
    line_height_relaxed: str = "1.75"
    
    def to_dict(self) -> Dict[str, str]:
        return {k: v for k, v in self.__dict__.items()}


@dataclass
class ThemeBorderRadius:
    """Border radius scale for a theme."""
    none: str = "0"
    sm: str = "0.25rem"
    md: str = "0.375rem"
    lg: str = "0.5rem"
    xl: str = "0.75rem"
    xxl: str = "1rem"
    full: str = "9999px"
    
    def to_dict(self) -> Dict[str, str]:
        return {k: v for k, v in self.__dict__.items()}


@dataclass
class Theme:
    """Complete theme definition."""
    name: str
    colors: ThemeColors = field(default_factory=ThemeColors)
    spacing: ThemeSpacing = field(default_factory=ThemeSpacing)
    typography: ThemeTypography = field(default_factory=ThemeTypography)
    border_radius: ThemeBorderRadius = field(default_factory=ThemeBorderRadius)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "colors": self.colors.to_dict(),
            "spacing": self.spacing.to_dict(),
            "typography": self.typography.to_dict(),
            "border_radius": self.border_radius.to_dict(),
        }
    
    def to_css_variables(self) -> str:
        """Generate CSS variables from theme."""
        css = ":root {\n"
        
        # Colors
        for key, value in self.colors.to_dict().items():
            css_var = key.replace("_", "-")
            css += f"  --color-{css_var}: {value};\n"
        
        # Spacing
        for key, value in self.spacing.to_dict().items():
            css_var = key.replace("_", "-")
            css += f"  --spacing-{css_var}: {value};\n"
        
        # Typography
        for key, value in self.typography.to_dict().items():
            css_var = key.replace("_", "-")
            css += f"  --font-{css_var}: {value};\n"
        
        # Border radius
        for key, value in self.border_radius.to_dict().items():
            css_var = key.replace("_", "-")
            css += f"  --radius-{css_var}: {value};\n"
        
        css += "}"
        return css


# Predefined themes
LIGHT_THEME = Theme(
    name="light",
    colors=ThemeColors(),
)

DARK_THEME = Theme(
    name="dark",
    colors=ThemeColors(
        background="#111827",
        background_secondary="#1F2937",
        background_tertiary="#374151",
        text_primary="#F9FAFB",
        text_secondary="#9CA3AF",
        text_tertiary="#6B7280",
        text_inverse="#111827",
        border="#374151",
        border_hover="#4B5563",
        border_focus="#3B82F6",
        shadow="0 1px 3px 0 rgba(0, 0, 0, 0.3), 0 1px 2px 0 rgba(0, 0, 0, 0.2)",
        shadow_md="0 4px 6px -1px rgba(0, 0, 0, 0.3), 0 2px 4px -1px rgba(0, 0, 0, 0.2)",
        shadow_lg="0 10px 15px -3px rgba(0, 0, 0, 0.3), 0 4px 6px -2px rgba(0, 0, 0, 0.2)",
    ),
)

BLUE_THEME = Theme(
    name="blue",
    colors=ThemeColors(
        primary="#2563EB",
        primary_hover="#1D4ED8",
        primary_active="#1E40AF",
    ),
)

GREEN_THEME = Theme(
    name="green",
    colors=ThemeColors(
        primary="#059669",
        primary_hover="#047857",
        primary_active="#065F46",
        success="#10B981",
        success_hover="#059669",
    ),
)

PURPLE_THEME = Theme(
    name="purple",
    colors=ThemeColors(
        primary="#7C3AED",
        primary_hover="#6D28D9",
        primary_active="#5B21B6",
    ),
)


class ThemeManager:
    """Theme manager for ontaic applications."""
    
    def __init__(self):
        self.themes: Dict[str, Theme] = {
            "light": LIGHT_THEME,
            "dark": DARK_THEME,
            "blue": BLUE_THEME,
            "green": GREEN_THEME,
            "purple": PURPLE_THEME,
        }
        self.current_theme: str = "light"
        self._listeners: list = []
    
    def get_theme(self, name: str = None) -> Theme:
        """Get a theme by name."""
        theme_name = name or self.current_theme
        return self.themes.get(theme_name, LIGHT_THEME)
    
    def set_theme(self, name: str):
        """Set the current theme."""
        if name in self.themes:
            self.current_theme = name
            # Notify listeners
            for listener in self._listeners:
                listener(name, self.themes[name])
    
    def register_theme(self, theme: Theme):
        """Register a custom theme."""
        self.themes[theme.name] = theme
    
    def on_theme_change(self, listener: Callable):
        """Register a theme change listener."""
        self._listeners.append(listener)
    
    def get_available_themes(self) -> List[str]:
        """Get list of available theme names."""
        return list(self.themes.keys())
    
    def toggle_dark_mode(self):
        """Toggle between light and dark themes."""
        if self.current_theme == "light":
            self.set_theme("dark")
        else:
            self.set_theme("light")
    
    def generate_css(self) -> str:
        """Generate CSS for the current theme."""
        theme = self.get_theme()
        return theme.to_css_variables()
    
    def generate_js_code(self) -> str:
        """Generate JavaScript code for theme management."""
        themes_json = {name: theme.to_dict() for name, theme in self.themes.items()}
        
        return f"""
        // Theme Manager
        const themeManager = {{
            currentTheme: '{self.current_theme}',
            themes: {json.dumps(themes_json)},
            
            setTheme(name) {{
                if (this.themes[name]) {{
                    this.currentTheme = name;
                    localStorage.setItem('ontaic-theme', name);
                    this.applyTheme(name);
                    document.dispatchEvent(new CustomEvent('themechange', {{ detail: name }}));
                }}
            }},
            
            getTheme(name) {{
                return this.themes[name || this.currentTheme];
            }},
            
            toggleDarkMode() {{
                this.setTheme(this.currentTheme === 'light' ? 'dark' : 'light');
            }},
            
            applyTheme(name) {{
                const theme = this.themes[name];
                if (!theme) return;
                
                const root = document.documentElement;
                
                // Apply colors
                Object.entries(theme.colors).forEach(([key, value]) => {{
                    const cssVar = '--color-' + key.replace(/_/g, '-');
                    root.style.setProperty(cssVar, value);
                }});
                
                // Apply spacing
                Object.entries(theme.spacing).forEach(([key, value]) => {{
                    const cssVar = '--spacing-' + key.replace(/_/g, '-');
                    root.style.setProperty(cssVar, value);
                }});
                
                // Apply typography
                Object.entries(theme.typography).forEach(([key, value]) => {{
                    const cssVar = '--font-' + key.replace(/_/g, '-');
                    root.style.setProperty(cssVar, value);
                }});
                
                // Apply border radius
                Object.entries(theme.border_radius).forEach(([key, value]) => {{
                    const cssVar = '--radius-' + key.replace(/_/g, '-');
                    root.style.setProperty(cssVar, value);
                }});
            }},
            
            init() {{
                const savedTheme = localStorage.getItem('ontaic-theme') || '{self.current_theme}';
                this.setTheme(savedTheme);
            }}
        }};
        
        // Initialize theme
        themeManager.init();
        """
    
    def save_to_file(self, file_path: str):
        """Save theme configuration to a file."""
        config = {
            "current_theme": self.current_theme,
            "themes": {name: theme.to_dict() for name, theme in self.themes.items()},
        }
        Path(file_path).write_text(json.dumps(config, indent=2))
    
    def load_from_file(self, file_path: str):
        """Load theme configuration from a file."""
        try:
            config = json.loads(Path(file_path).read_text())
            self.current_theme = config.get("current_theme", "light")
            for name, theme_data in config.get("themes", {}).items():
                theme = Theme(
                    name=name,
                    colors=ThemeColors(**theme_data.get("colors", {})),
                    spacing=ThemeSpacing(**theme_data.get("spacing", {})),
                    typography=ThemeTypography(**theme_data.get("typography", {})),
                    border_radius=ThemeBorderRadius(**theme_data.get("border_radius", {})),
                )
                self.register_theme(theme)
        except Exception as e:
            print(f"[ontaic] Failed to load theme: {e}")


# Theme toggle component
class ThemeToggle:
    """Theme toggle button component."""
    
    def __init__(self, theme_manager: ThemeManager = None):
        self.theme_manager = theme_manager or ThemeManager()
    
    def render(self) -> str:
        return f"""
        <button 
            onclick="themeManager.toggleDarkMode()"
            class="p-2 rounded-lg bg-gray-100 hover:bg-gray-200 dark:bg-gray-800 dark:hover:bg-gray-700 transition-colors"
            aria-label="Toggle theme"
        >
            <svg class="w-5 h-5 text-gray-600 dark:text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                    d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z">
                </path>
            </svg>
        </button>
        """


# Theme selector component
class ThemeSelector:
    """Theme selector dropdown component."""
    
    def __init__(self, theme_manager: ThemeManager = None):
        self.theme_manager = theme_manager or ThemeManager()
    
    def render(self) -> str:
        themes = self.theme_manager.get_available_themes()
        options_html = "\n".join([
            f'<option value="{name}" {"selected" if name == self.theme_manager.current_theme else ""}>{name.title()}</option>'
            for name in themes
        ])
        
        return f"""
        <select 
            onchange="themeManager.setTheme(this.value)"
            class="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        >
            {options_html}
        </select>
        """
