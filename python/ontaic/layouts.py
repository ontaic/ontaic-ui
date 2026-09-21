from ontaic.component import Box, Text, Element
from typing import Optional, List


class Container(Box):
    """Responsive container with max-width."""

    def __init__(
        self,
        *children,
        max_width: str = "max-w-7xl",
        padding: str = "px-4",
        class_name: str = "",
        **kwargs,
    ):
        full_class = f"mx-auto {max_width} {padding} {class_name}"
        super().__init__(*children, class_name=full_class, **kwargs)


class Flex(Box):
    """Flexbox layout container."""

    def __init__(
        self,
        *children,
        direction: str = "row",
        justify: str = "start",
        align: str = "start",
        wrap: bool = False,
        gap: str = "0",
        class_name: str = "",
        **kwargs,
    ):
        direction_class = {
            "row": "flex-row",
            "col": "flex-col",
            "row-reverse": "flex-row-reverse",
            "col-reverse": "flex-col-reverse",
        }.get(direction, "flex-row")

        justify_class = {
            "start": "justify-start",
            "end": "justify-end",
            "center": "justify-center",
            "between": "justify-between",
            "around": "justify-around",
            "evenly": "justify-evenly",
        }.get(justify, "justify-start")

        align_class = {
            "start": "items-start",
            "end": "items-end",
            "center": "items-center",
            "stretch": "items-stretch",
            "baseline": "items-baseline",
        }.get(align, "items-start")

        wrap_class = "flex-wrap" if wrap else "flex-nowrap"

        full_class = f"flex {direction_class} {justify_class} {align_class} {wrap_class} gap-{gap} {class_name}"
        super().__init__(*children, class_name=full_class, **kwargs)


class Grid(Box):
    """CSS Grid layout container."""

    def __init__(
        self,
        *children,
        columns: int = 1,
        rows: int = 0,
        gap: str = "4",
        class_name: str = "",
        **kwargs,
    ):
        cols_class = f"grid-cols-{columns}"

        full_class = f"grid {cols_class} gap-{gap} {class_name}"
        super().__init__(*children, class_name=full_class, **kwargs)


class Stack(Box):
    """Vertical stack with consistent spacing."""

    def __init__(
        self,
        *children,
        spacing: str = "4",
        class_name: str = "",
        **kwargs,
    ):
        full_class = f"flex flex-col space-y-{spacing} {class_name}"
        super().__init__(*children, class_name=full_class, **kwargs)


class Center(Box):
    """Center content horizontally and vertically."""

    def __init__(
        self,
        *children,
        class_name: str = "",
        **kwargs,
    ):
        full_class = f"flex items-center justify-center {class_name}"
        super().__init__(*children, class_name=full_class, **kwargs)


class Spacer(Box):
    """Flexible spacer element."""

    def __init__(
        self,
        size: str = "flex-1",
        class_name: str = "",
        **kwargs,
    ):
        full_class = f"{size} {class_name}"
        super().__init__(class_name=full_class, **kwargs)


class Card(Box):
    """Card with padding, shadow, and rounded corners."""

    def __init__(
        self,
        *children,
        padding: str = "p-6",
        shadow: str = "shadow-md",
        rounded: str = "rounded-xl",
        class_name: str = "",
        **kwargs,
    ):
        full_class = f"bg-white {padding} {shadow} {rounded} {class_name}"
        super().__init__(*children, class_name=full_class, **kwargs)


class Divider(Element):
    """Horizontal divider line."""

    def __init__(
        self,
        class_name: str = "",
        **kwargs,
    ):
        full_class = f"w-full h-px bg-gray-200 {class_name}"
        super().__init__("div", class_name=full_class, **kwargs)


class Badge(Text):
    """Badge/tag element."""

    def __init__(
        self,
        text: str = "",
        variant: str = "default",
        size: str = "md",
        class_name: str = "",
        **kwargs,
    ):
        variant_classes = {
            "default": "bg-gray-100 text-gray-800",
            "primary": "bg-blue-100 text-blue-800",
            "success": "bg-green-100 text-green-800",
            "warning": "bg-yellow-100 text-yellow-800",
            "danger": "bg-red-100 text-red-800",
        }

        size_classes = {
            "sm": "px-2 py-0.5 text-xs",
            "md": "px-2.5 py-0.5 text-sm",
            "lg": "px-3 py-1 text-sm",
        }

        full_class = f"inline-flex items-center font-medium rounded-full {size_classes.get(size, size_classes['md'])} {variant_classes.get(variant, variant_classes['default'])} {class_name}"
        super().__init__(text, class_name=full_class, **kwargs)


class Heading(Text):
    """Heading element with proper sizing."""

    def __init__(
        self,
        text: str = "",
        level: int = 1,
        class_name: str = "",
        **kwargs,
    ):
        tag = f"h{level}"
        size_classes = {
            1: "text-4xl font-bold",
            2: "text-3xl font-semibold",
            3: "text-2xl font-semibold",
            4: "text-xl font-medium",
            5: "text-lg font-medium",
            6: "text-base font-medium",
        }

        full_class = f"{size_classes.get(level, size_classes['1'])} {class_name}"
        super().__init__(text, tag=tag, class_name=full_class, **kwargs)


class Paragraph(Text):
    """Paragraph element."""

    def __init__(
        self,
        text: str = "",
        size: str = "base",
        class_name: str = "",
        **kwargs,
    ):
        size_classes = {
            "sm": "text-sm",
            "base": "text-base",
            "lg": "text-lg",
            "xl": "text-xl",
        }

        full_class = f"{size_classes.get(size, size_classes['base'])} {class_name}"
        super().__init__(text, tag="p", class_name=full_class, **kwargs)
