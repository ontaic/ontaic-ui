from ontaic.component import Box, Text


class Separator(Box):
    """Horizontal/vertical separator/divider."""

    def __init__(
        self,
        orientation: str = "horizontal",
        class_name: str = "",
        **kwargs,
    ):
        if orientation == "vertical":
            full_class = f"w-px h-full bg-gray-200 {class_name}"
        else:
            full_class = f"w-full h-px bg-gray-200 {class_name}"

        super().__init__(class_name=full_class, **kwargs)
