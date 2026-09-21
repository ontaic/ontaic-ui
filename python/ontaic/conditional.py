"""Conditional rendering and loop components."""
from typing import Any, Callable, List, Optional
from ontaic.component import Element


class If(Element):
    """Conditional rendering - renders children if condition is true."""

    def __init__(
        self,
        condition: Any,
        *children,
        else_content: Any = None,
        class_name: str = "",
        **kwargs,
    ):
        self.condition = condition
        self.else_content = else_content

        super().__init__("div", class_name=class_name, **kwargs)
        self.children = list(children)

    def render(self):
        if self.condition:
            return "".join(
                child.render() if hasattr(child, "render") else str(child)
                for child in self.children
            )
        elif self.else_content:
            if hasattr(self.else_content, "render"):
                return self.else_content.render()
            return str(self.else_content)
        return ""


class Show(Element):
    """Show/hide based on state value."""

    def __init__(
        self,
        state_key: str,
        *children,
        when: str = "truthy",
        class_name: str = "",
        **kwargs,
    ):
        self.state_key = state_key
        self.when = when

        super().__init__("div", class_name=class_name, **kwargs)
        self.children = list(children)

    def render(self):
        node_id = f"show-{self.state_key}"
        return f"""<div id="{node_id}" data-show="{self.state_key}" data-when="{self.when}" class="{self.class_name}">
            {"".join(c.render() if hasattr(c, "render") else str(c) for c in self.children)}
        </div>"""


class ForEach(Element):
    """Loop rendering over a list."""

    def __init__(
        self,
        items: List[Any],
        render_item: Callable,
        key_field: str = "id",
        class_name: str = "",
        **kwargs,
    ):
        self.items = items
        self.render_item = render_item
        self.key_field = key_field

        super().__init__("div", class_name=class_name, **kwargs)

    def render(self):
        if not self.items:
            return ""

        items_html = []
        for item in self.items:
            rendered = self.render_item(item)
            if hasattr(rendered, "render"):
                items_html.append(rendered.render())
            else:
                items_html.append(str(rendered))

        return f'<div class="{self.class_name}">{"".join(items_html)}</div>'


class Switch(Element):
    """Switch/case rendering."""

    def __init__(
        self,
        value: Any,
        cases: dict,
        default: Any = None,
        class_name: str = "",
        **kwargs,
    ):
        self.value = value
        self.cases = cases
        self.default = default

        super().__init__("div", class_name=class_name, **kwargs)

    def render(self):
        content = self.cases.get(self.value, self.default)
        if content is None:
            return ""
        if hasattr(content, "render"):
            return content.render()
        return str(content)


class Unless(Element):
    """Render children only if condition is falsy."""

    def __init__(
        self,
        condition: Any,
        *children,
        class_name: str = "",
        **kwargs,
    ):
        self.condition = condition

        super().__init__("div", class_name=class_name, **kwargs)
        self.children = list(children)

    def render(self):
        if not self.condition:
            return "".join(
                child.render() if hasattr(child, "render") else str(child)
                for child in self.children
            )
        return ""


class Fragment(Element):
    """Fragment - renders children without a wrapper element."""

    def __init__(self, *children, **kwargs):
        super().__init__("fragment", **kwargs)
        self.children = list(children)

    def render(self):
        return "".join(
            child.render() if hasattr(child, "render") else str(child)
            for child in self.children
        )
