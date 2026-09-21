from ontaic.component import Box, Text


class Skeleton(Box):
    """Loading skeleton placeholder."""

    def __init__(
        self,
        width: str = "w-full",
        height: str = "h-4",
        rounded: str = "rounded",
        class_name: str = "",
        **kwargs,
    ):
        full_class = f"bg-gray-200 animate-pulse {width} {height} {rounded} {class_name}"
        super().__init__(class_name=full_class, **kwargs)
