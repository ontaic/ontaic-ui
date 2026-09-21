from ontaic.component import Box, Text, Button


class Badge(Box):
    """Badge/tag component."""

    def __init__(
        self,
        text: str = "",
        variant: str = "default",
        size: str = "md",
        class_name: str = "",
        **kwargs,
    ):
        self.badge_text = text

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
        super().__init__(class_name=full_class, **kwargs)

    def render(self):
        return Box(
            Text(self.badge_text),
            class_name=self.class_name,
        )
