from ontaic.component import Box, Text


class Alert(Box):
    """Alert/notification component."""

    def __init__(
        self,
        message: str = "",
        variant: str = "info",
        dismissible: bool = False,
        class_name: str = "",
        **kwargs,
    ):
        self.message = message
        self.variant = variant
        self.dismissible = dismissible

        variant_classes = {
            "info": "bg-blue-50 border-blue-200 text-blue-800",
            "success": "bg-green-50 border-green-200 text-green-800",
            "warning": "bg-yellow-50 border-yellow-200 text-yellow-800",
            "error": "bg-red-50 border-red-200 text-red-800",
        }

        full_class = f"border rounded-lg p-4 {variant_classes.get(variant, variant_classes['info'])} {class_name}"
        super().__init__(class_name=full_class, **kwargs)

    def render(self):
        return Box(
            Text(self.message, class_name="text-sm font-medium"),
            class_name=self.class_name,
        )
