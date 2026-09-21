from ontaic.component import Box, Text, Button


class Modal(Box):
    """Modal dialog overlay."""

    def __init__(
        self,
        title: str = "",
        children=None,
        on_close=None,
        class_name: str = "",
        **kwargs,
    ):
        self.title = title
        self.on_close = on_close

        full_class = f"fixed inset-0 z-50 flex items-center justify-center {class_name}"
        super().__init__(class_name=full_class, **kwargs)

    def render(self):
        overlay = Box(
            class_name="absolute inset-0 bg-black/50 backdrop-blur-sm",
        )

        content = Box(
            Box(
                Text(self.title, tag="h2", class_name="text-xl font-semibold text-gray-900"),
                Button(
                    "x",
                    class_name="text-gray-400 hover:text-gray-600",
                    on_click=self.on_close,
                ),
                class_name="flex items-center justify-between p-4 border-b",
            ),
            Box(
                class_name="p-4",
            ),
            class_name="relative bg-white rounded-xl shadow-2xl max-w-lg w-full mx-4",
        )

        return Box(overlay, content, class_name="relative")
