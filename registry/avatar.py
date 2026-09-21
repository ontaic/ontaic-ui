from ontaic.component import Box, Text


class Avatar(Box):
    """Avatar component with image or initials."""

    def __init__(
        self,
        src: str = "",
        alt: str = "",
        initials: str = "",
        size: str = "md",
        class_name: str = "",
        **kwargs,
    ):
        self.src = src
        self.alt = alt
        self.initials = initials

        size_classes = {
            "sm": "h-8 w-8 text-xs",
            "md": "h-10 w-10 text-sm",
            "lg": "h-12 w-12 text-base",
            "xl": "h-16 w-16 text-lg",
        }

        full_class = f"inline-flex items-center justify-center rounded-full bg-gray-300 {size_classes.get(size, size_classes['md'])} {class_name}"
        super().__init__(class_name=full_class, **kwargs)

    def render(self):
        if self.src:
            return Box(
                f'<img src="{self.src}" alt="{self.alt}" class="h-full w-full rounded-full" />',
                class_name=self.class_name,
            )
        else:
            return Box(
                Text(self.initials, class_name="font-medium text-gray-700"),
                class_name=self.class_name,
            )
