"""Navigation and routing components."""
from typing import Any, Callable, Dict, List, Optional
from ontaic.component import Element


class Router(Element):
    """Client-side router container."""

    def __init__(
        self,
        routes: Dict[str, Any],
        initial_route: str = "/",
        class_name: str = "",
        **kwargs,
    ):
        self.routes = routes
        self.initial_route = initial_route

        super().__init__("div", class_name=class_name, **kwargs)

    def render(self):
        routes_html = []
        for path, component in self.routes.items():
            if hasattr(component, "render"):
                content = component.render()
            else:
                content = str(component)
            routes_html.append(
                f'<div data-route="{path}" class="route-page" style="display:none;">{content}</div>'
            )

        return f"""<div id="ontaic-router" class="{self.class_name}">
            {"".join(routes_html)}
            <script>
            (function() {{
                const router = document.getElementById('ontaic-router');
                const pages = router.querySelectorAll('.route-page');
                const initialRoute = '{self.initial_route}';
                
                function navigate(path) {{
                    pages.forEach(p => p.style.display = 'none');
                    const page = router.querySelector('[data-route="' + path + '"]');
                    if (page) page.style.display = 'block';
                    window.history.pushState({{}}, '', path);
                }}
                
                window.addEventListener('popstate', () => {{
                    navigate(window.location.pathname);
                }});
                
                router.querySelectorAll('a[data-link]').forEach(link => {{
                    link.addEventListener('click', (e) => {{
                        e.preventDefault();
                        navigate(link.getAttribute('href'));
                    }});
                }});
                
                navigate(window.location.pathname || initialRoute);
            }})();
            </script>
        </div>"""


class NavLink(Element):
    """Navigation link with active state."""

    def __init__(
        self,
        href: str,
        text: str = "",
        active_class: str = "text-blue-600 font-medium",
        inactive_class: str = "text-gray-600 hover:text-gray-900",
        class_name: str = "",
        **kwargs,
    ):
        self.href = href
        self.link_text = text
        self.active_class = active_class
        self.inactive_class = inactive_class

        full_class = f"px-3 py-2 text-sm font-medium transition-colors {class_name}"
        super().__init__("a", class_name=full_class, **kwargs)

    def render(self):
        is_active = "window.location.pathname === '" + self.href + "'"
        return f"""<a href="{self.href}" data-link class="{self.class_name}"
            x-bind:class="{is_active} ? '{self.active_class}' : '{self.inactive_class}'"
        >{self.link_text}</a>"""


class Navbar(Element):
    """Navigation bar container."""

    def __init__(
        self,
        *children,
        brand: str = "",
        brand_href: str = "/",
        class_name: str = "",
        **kwargs,
    ):
        self.brand = brand
        self.brand_href = brand_href

        super().__init__("nav", class_name=class_name, **kwargs)
        self.children = list(children)

    def render(self):
        brand_html = ""
        if self.brand:
            brand_html = f"""<a href="{self.brand_href}" data-link class="text-xl font-bold text-gray-900">
                {self.brand}
            </a>"""

        links_html = "".join(
            child.render() if hasattr(child, "render") else str(child)
            for child in self.children
        )

        return f"""<nav class="flex items-center justify-between {self.class_name}">
            {brand_html}
            <div class="flex items-center space-x-1">
                {links_html}
            </div>
        </nav>"""


class Sidebar(Element):
    """Sidebar navigation."""

    def __init__(
        self,
        *children,
        width: str = "w-64",
        class_name: str = "",
        **kwargs,
    ):
        super().__init__("aside", class_name=f"{width} {class_name}", **kwargs)
        self.children = list(children)

    def render(self):
        links_html = "".join(
            child.render() if hasattr(child, "render") else str(child)
            for child in self.children
        )

        return f"""<aside class="{self.class_name}">
            <div class="space-y-1">
                {links_html}
            </div>
        </aside>"""


class SidebarLink(Element):
    """Sidebar navigation link."""

    def __init__(
        self,
        href: str,
        text: str = "",
        icon: str = "",
        class_name: str = "",
        **kwargs,
    ):
        self.href = href
        self.link_text = text
        self.icon = icon

        full_class = f"flex items-center px-3 py-2 text-sm font-medium rounded-lg transition-colors hover:bg-gray-100 {class_name}"
        super().__init__("a", class_name=full_class, **kwargs)

    def render(self):
        icon_html = f'<span class="mr-3">{self.icon}</span>' if self.icon else ""
        return f"""<a href="{self.href}" data-link class="{self.class_name}">
            {icon_html}{self.link_text}
        </a>"""
