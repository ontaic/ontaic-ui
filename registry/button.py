from ontaic.component import Button as BaseButton


class Button(BaseButton):
    """Configurable button component with theme support."""

    def __init__(
        self,
        text: str = "Click me",
        variant: str = "primary",
        size: str = "md",
        on_click=None,
        **kwargs,
    ):
        size_classes = {
            "sm": "px-3 py-1.5 text-sm",
            "md": "px-4 py-2 text-base",
            "lg": "px-6 py-3 text-lg",
        }

        variant_classes = {
            "primary": "bg-blue-600 hover:bg-blue-700 text-white",
            "secondary": "bg-gray-200 hover:bg-gray-300 text-gray-800",
            "danger": "bg-red-600 hover:bg-red-700 text-white",
            "success": "bg-green-600 hover:bg-green-700 text-white",
            "ghost": "bg-transparent hover:bg-gray-100 text-gray-800",
        }

        class_name = f"rounded-lg font-medium transition-colors {size_classes.get(size, size_classes['md'])} {variant_classes.get(variant, variant_classes['primary'])} {kwargs.pop('class_name', '')}"

        super().__init__(text=text, class_name=class_name, on_click=on_click, **kwargs)
