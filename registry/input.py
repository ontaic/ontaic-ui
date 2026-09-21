from ontaic.component import Input as BaseInput


class Input(BaseInput):
    """Configurable input field with label and validation."""

    def __init__(
        self,
        label: str = "",
        placeholder: str = "",
        value: str = "",
        error: str = "",
        on_change=None,
        **kwargs,
    ):
        size = kwargs.pop("size", "md")
        size_classes = {
            "sm": "px-3 py-1.5 text-sm",
            "md": "px-4 py-2 text-base",
            "lg": "px-4 py-3 text-lg",
        }

        input_class = f"w-full rounded-lg border border-gray-300 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 outline-none transition-all {size_classes.get(size, size_classes['md'])}"

        super().__init__(
            placeholder=placeholder,
            value=value,
            class_name=input_class,
            on_change=on_change,
            **kwargs,
        )
        self.label = label
        self.error = error
