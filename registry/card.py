from ontaic.component import Box


class Card(Box):
    """Content card with padding and shadow."""

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
