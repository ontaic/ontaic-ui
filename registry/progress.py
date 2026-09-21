from ontaic.component import Box, Text


class Progress(Box):
    """Progress bar component."""

    def __init__(
        self,
        value: int = 0,
        max_value: int = 100,
        variant: str = "primary",
        size: str = "md",
        show_label: bool = False,
        class_name: str = "",
        **kwargs,
    ):
        self.value = value
        self.max_value = max_value
        self.variant = variant
        self.show_label = show_label

        size_classes = {
            "sm": "h-1.5",
            "md": "h-2.5",
            "lg": "h-4",
        }

        full_class = f"w-full bg-gray-200 rounded-full {size_classes.get(size, size_classes['md'])} {class_name}"
        super().__init__(class_name=full_class, **kwargs)

    def render(self):
        percentage = min(100, max(0, int((self.value / self.max_value) * 100))) if self.max_value > 0 else 0

        variant_classes = {
            "primary": "bg-blue-600",
            "success": "bg-green-600",
            "warning": "bg-yellow-500",
            "danger": "bg-red-600",
        }

        bar_class = f"{variant_classes.get(self.variant, variant_classes['primary'])} h-full rounded-full transition-all duration-300"
        inner = f'<div class="{bar_class}" style="width: {percentage}%"></div>'

        if self.show_label:
            inner = f'<div class="flex items-center justify-between mb-1"><span class="text-sm font-medium text-gray-700">{percentage}%</span></div><div class="w-full bg-gray-200 rounded-full h-2.5"><div class="{bar_class}" style="width: {percentage}%"></div></div>'

        return Box(inner, class_name=self.class_name)
