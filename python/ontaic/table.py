"""Table and data display components."""
from typing import Any, Callable, Dict, List, Optional
from ontaic.component import Element


class Table(Element):
    """Data table component."""
    
    def __init__(
        self,
        columns: List[Dict[str, str]],
        data: List[Dict[str, Any]],
        striped: bool = True,
        hover: bool = True,
        compact: bool = False,
        bordered: bool = False,
        class_name: str = "",
        **kwargs,
    ):
        self.columns = columns
        self.data = data
        self.striped = striped
        self.hover = hover
        self.compact = compact
        self.bordered = bordered

        super().__init__("div", class_name=class_name, **kwargs)

    def render(self):
        table_classes = "min-w-full divide-y divide-gray-200"
        if self.striped:
            table_classes += " table-striped"
        if self.hover:
            table_classes += " table-hover"
        if self.bordered:
            table_classes += " border border-gray-200"
        
        cell_classes = "px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
        if self.compact:
            cell_classes = "px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
        
        # Header
        header_html = "<tr>"
        for col in self.columns:
            header_html += f'<th class="{cell_classes}">{col.get("header", col.get("key", ""))}</th>'
        header_html += "</tr>"
        
        # Rows
        rows_html = ""
        for i, row in enumerate(self.data):
            row_class = "bg-white"
            if self.striped and i % 2 == 1:
                row_class = "bg-gray-50"
            
            rows_html += f'<tr class="{row_class}">'
            for col in self.columns:
                key = col.get("key", "")
                value = row.get(key, "")
                
                # Format value if formatter provided
                if "format" in col:
                    value = col["format"](value, row)
                
                cell_class = "px-6 py-4 whitespace-nowrap text-sm text-gray-900"
                if self.compact:
                    cell_class = "px-4 py-2 whitespace-nowrap text-sm text-gray-900"
                
                rows_html += f'<td class="{cell_class}">{value}</td>'
            rows_html += "</tr>"
        
        return f"""<div class="overflow-hidden shadow ring-1 ring-black ring-opacity-5 rounded-lg">
            <table class="{table_classes}">
                <thead class="bg-gray-50">
                    {header_html}
                </thead>
                <tbody class="divide-y divide-gray-200">
                    {rows_html}
                </tbody>
            </table>
        </div>"""


class DataTable(Element):
    """Advanced data table with sorting, filtering, and pagination."""
    
    def __init__(
        self,
        columns: List[Dict[str, str]],
        data: List[Dict[str, Any]],
        page_size: int = 10,
        sortable: bool = True,
        filterable: bool = True,
        selectable: bool = False,
        class_name: str = "",
        **kwargs,
    ):
        self.columns = columns
        self.data = data
        self.page_size = page_size
        self.sortable = sortable
        self.filterable = filterable
        self.selectable = selectable

        super().__init__("div", class_name=class_name, **kwargs)

    def render(self):
        table_id = f"datatable-{id(self)}"
        
        # Build columns JSON for JavaScript
        columns_json = str([
            {"key": col.get("key", ""), "header": col.get("header", ""), "sortable": col.get("sortable", self.sortable)}
            for col in self.columns
        ]).replace("'", '"')
        
        return f"""<div id="{table_id}" class="datatable">
            {"" if not self.filterable else '''
            <div class="mb-4">
                <input type="text" placeholder="Search..." 
                    class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    oninput="filterTable(this.value)">
            </div>
            '''}
            <div class="overflow-hidden shadow ring-1 ring-black ring-opacity-5 rounded-lg">
                <table class="min-w-full divide-y divide-gray-200">
                    <thead class="bg-gray-50">
                        <tr>
                            {"".join(f'<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100" onclick="sortTable(&#39;{col.get("key", "")}&#39;)">{col.get("header", col.get("key", ""))}</th>' if col.get("sortable", self.sortable) else f'<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">{col.get("header", col.get("key", ""))}</th>' for col in self.columns)}
                        </tr>
                    </thead>
                    <tbody id="{table_id}-body" class="divide-y divide-gray-200">
                    </tbody>
                </table>
            </div>
            <div class="flex items-center justify-between mt-4">
                <div class="text-sm text-gray-700">
                    Showing <span id="{table_id}-showing">1-10</span> of <span id="{table_id}-total">{len(self.data)}</span> results
                </div>
                <div class="flex gap-2">
                    <button onclick="prevPage()" class="px-3 py-1 text-sm bg-gray-100 rounded hover:bg-gray-200">Previous</button>
                    <button onclick="nextPage()" class="px-3 py-1 text-sm bg-gray-100 rounded hover:bg-gray-200">Next</button>
                </div>
            </div>
            <script>
            const {table_id}_data = {str(self.data).replace("'", '"')};
            const {table_id}_columns = {columns_json};
            let {table_id}_page = 0;
            let {table_id}_sort = {{ key: '', asc: true }};
            let {table_id}_filter = '';
            
            function renderTable() {{
                let data = [...{table_id}_data];
                
                // Filter
                if ({table_id}_filter) {{
                    const filter = {table_id}_filter.toLowerCase();
                    data = data.filter(row => 
                        Object.values(row).some(val => 
                            String(val).toLowerCase().includes(filter)
                        )
                    );
                }}
                
                // Sort
                if ({table_id}_sort.key) {{
                    data.sort((a, b) => {{
                        const aVal = a[{table_id}_sort.key] || '';
                        const bVal = b[{table_id}_sort.key] || '';
                        const cmp = String(aVal).localeCompare(String(bVal));
                        return {table_id}_sort.asc ? cmp : -cmp;
                    }});
                }}
                
                // Paginate
                const start = {table_id}_page * {self.page_size};
                const pageData = data.slice(start, start + {self.page_size});
                
                // Render rows
                const tbody = document.getElementById('{table_id}-body');
                tbody.innerHTML = pageData.map(row => {{
                    return '<tr class="bg-white hover:bg-gray-50">' + 
                        {table_id}_columns.map(col => 
                            '<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">' + (row[col.key] || '') + '</td>'
                        ).join('') + 
                    '</tr>';
                }}).join('');
                
                // Update pagination info
                document.getElementById('{table_id}-showing').textContent = 
                    (start + 1) + '-' + Math.min(start + {self.page_size}, data.length);
                document.getElementById('{table_id}-total').textContent = data.length;
            }}
            
            function sortTable(key) {{
                if ({table_id}_sort.key === key) {{
                    {table_id}_sort.asc = !{table_id}_sort.asc;
                }} else {{
                    {table_id}_sort = {{ key, asc: true }};
                }}
                renderTable();
            }}
            
            function filterTable(value) {{
                {table_id}_filter = value;
                {table_id}_page = 0;
                renderTable();
            }}
            
            function nextPage() {{
                const totalPages = Math.ceil({table_id}_data.length / {self.page_size});
                if ({table_id}_page < totalPages - 1) {{
                    {table_id}_page++;
                    renderTable();
                }}
            }}
            
            function prevPage() {{
                if ({table_id}_page > 0) {{
                    {table_id}_page--;
                    renderTable();
                }}
            }}
            
            // Initial render
            renderTable();
            </script>
        </div>"""


class DataGrid(Element):
    """Grid layout for data display."""
    
    def __init__(
        self,
        items: List[Any],
        render_item: Callable,
        columns: int = 3,
        gap: int = 4,
        class_name: str = "",
        **kwargs,
    ):
        self.items = items
        self.render_item = render_item
        self.columns = columns
        self.gap = gap

        super().__init__("div", class_name=class_name, **kwargs)

    def render(self):
        grid_classes = f"grid grid-cols-{self.columns} gap-{self.gap}"
        
        items_html = ""
        for item in self.items:
            rendered = self.render_item(item)
            if hasattr(rendered, "render"):
                items_html += rendered.render()
            else:
                items_html += str(rendered)
        
        return f'<div class="{grid_classes}">{items_html}</div>'


class CardList(Element):
    """List of cards."""
    
    def __init__(
        self,
        items: List[Dict[str, Any]],
        title_key: str = "title",
        description_key: str = "description",
        class_name: str = "",
        **kwargs,
    ):
        self.items = items
        self.title_key = title_key
        self.description_key = description_key

        super().__init__("div", class_name=class_name, **kwargs)

    def render(self):
        cards_html = ""
        for item in self.items:
            title = item.get(self.title_key, "")
            description = item.get(self.description_key, "")
            
            cards_html += f"""<div class="bg-white rounded-lg shadow p-4 mb-4">
                <h3 class="text-lg font-semibold text-gray-900">{title}</h3>
                <p class="text-gray-600 mt-2">{description}</p>
            </div>"""
        
        return f'<div class="space-y-4">{cards_html}</div>'
