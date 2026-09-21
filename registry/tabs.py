from ontaic.component import Box, Text


class Tabs(Box):
    """Tabs component for content switching."""

    def __init__(
        self,
        tabs: list = None,
        active_tab: str = "",
        class_name: str = "",
        **kwargs,
    ):
        self.tabs = tabs or []
        self.active_tab = active_tab or (self.tabs[0] if self.tabs else "")

        full_class = f"border-b border-gray-200 {class_name}"
        super().__init__(class_name=full_class, **kwargs)

    def render(self):
        tab_items = ""
        for tab in self.tabs:
            is_active = tab == self.active_tab
            tab_class = "px-4 py-2 text-sm font-medium border-b-2 -mb-px "
            if is_active:
                tab_class += "border-blue-500 text-blue-600"
            else:
                tab_class += "border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300"

            tab_items += f'<button class="{tab_class}" data-tab="{tab}">{tab}</button>'

        return Box(
            f'<nav class="flex space-x-8">{tab_items}</nav>',
            class_name=self.class_name,
        )
