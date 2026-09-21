from ontaic.component import Box, Text


class DataGrid(Box):
    """Data table with headers and rows."""

    def __init__(
        self,
        columns: list = None,
        rows: list = None,
        striped: bool = True,
        hoverable: bool = True,
        class_name: str = "",
        **kwargs,
    ):
        self.columns = columns or []
        self.rows = rows or []
        self.striped = striped
        self.hoverable = hoverable

        full_class = f"w-full overflow-hidden rounded-lg border border-gray-200 {class_name}"
        super().__init__(class_name=full_class, **kwargs)

    def render(self):
        header_class = "bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
        cell_class = "px-6 py-4 whitespace-nowrap text-sm text-gray-900"

        rows_html = ""
        for i, row in enumerate(self.rows):
            row_class = "bg-white" if i % 2 == 0 else "bg-gray-50" if self.striped else "bg-white"
            if self.hoverable:
                row_class += " hover:bg-gray-100"

            cells = ""
            for cell in row:
                cells += f'<td class="{cell_class}">{cell}</td>'
            rows_html += f'<tr class="{row_class}">{cells}</tr>'

        headers = ""
        for col in self.columns:
            headers += f'<th class="{header_class} px-6 py-3">{col}</th>'

        return Box(
            f"""<table class="min-w-full divide-y divide-gray-200">
                <thead><tr>{headers}</tr></thead>
                <tbody class="divide-y divide-gray-200">{rows_html}</tbody>
            </table>""",
            class_name="overflow-x-auto",
        )
