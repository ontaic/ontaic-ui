"""Data grid component with sorting, filtering, and pagination."""
from typing import Any, Callable, Dict, List, Optional, Union
from dataclasses import dataclass, field
from enum import Enum


class GridSortDirection(str, Enum):
    """Sort direction."""
    ASC = "asc"
    DESC = "desc"


class GridFilterType(str, Enum):
    """Filter type."""
    TEXT = "text"
    NUMBER = "number"
    DATE = "date"
    SELECT = "select"
    BOOLEAN = "boolean"
    CUSTOM = "custom"


class GridAlign(str, Enum):
    """Column alignment."""
    LEFT = "left"
    CENTER = "center"
    RIGHT = "right"


@dataclass
class GridColumn:
    """Grid column definition."""
    field: str
    header: str = ""
    width: int = 0
    minWidth: int = 80
    maxWidth: int = 0
    sortable: bool = True
    filterable: bool = True
    resizable: bool = True
    visible: bool = True
    frozen: bool = False
    align: GridAlign = GridAlign.LEFT
    format: str = ""
    cell_renderer: str = ""
    header_renderer: str = ""
    filter_type: GridFilterType = GridFilterType.TEXT
    filter_options: List[Dict[str, Any]] = field(default_factory=list)
    editable: bool = False
    editor_type: str = "text"
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> dict:
        return {
            "field": self.field,
            "header": self.header or self.field,
            "width": self.width,
            "minWidth": self.minWidth,
            "maxWidth": self.maxWidth,
            "sortable": self.sortable,
            "filterable": self.filterable,
            "resizable": self.resizable,
            "visible": self.visible,
            "frozen": self.frozen,
            "align": self.align.value,
            "format": self.format,
            "filterType": self.filter_type.value,
            "filterOptions": self.filter_options,
            "editable": self.editable,
        }


@dataclass
class GridSort:
    """Grid sort state."""
    column: str
    direction: GridSortDirection = GridSortDirection.ASC
    
    def to_dict(self) -> dict:
        return {"column": self.column, "direction": self.direction.value}


@dataclass
class GridFilter:
    """Grid filter state."""
    column: str
    value: Any
    type: GridFilterType = GridFilterType.TEXT
    
    def to_dict(self) -> dict:
        return {"column": self.column, "value": self.value, "type": self.type.value}


@dataclass
class GridPagination:
    """Grid pagination state."""
    page: int = 1
    page_size: int = 25
    total: int = 0
    
    @property
    def total_pages(self) -> int:
        if self.page_size <= 0:
            return 0
        return (self.total + self.page_size - 1) // self.page_size
    
    @property
    def has_next(self) -> bool:
        return self.page < self.total_pages
    
    @property
    def has_prev(self) -> bool:
        return self.page > 1
    
    def to_dict(self) -> dict:
        return {
            "page": self.page,
            "pageSize": self.page_size,
            "total": self.total,
            "totalPages": self.total_pages,
            "hasNext": self.has_next,
            "hasPrev": self.has_prev,
        }


class DataGrid:
    """Data grid component with advanced features."""
    
    def __init__(self, columns: List[GridColumn] = None, data: List[Dict[str, Any]] = None):
        self._columns = columns or []
        self._data = data or []
        self._sorts: List[GridSort] = []
        self._filters: List[GridFilter] = []
        self._pagination = GridPagination()
        self._selected_rows: List[Dict[str, Any]] = []
        self._selectable: bool = True
        self._multi_select: bool = True
        self._sortable: bool = True
        self._filterable: bool = True
        self._paginated: bool = True
        self._virtual_scroll: bool = False
        self._row_height: int = 48
        self._header_height: int = 56
        self._show_header: bool = True
        self._show_footer: bool = True
        self._show_row_numbers: bool = False
        self._show_checkboxes: bool = True
        self._stripe_rows: bool = True
        self._bordered: bool = True
        self._compact: bool = False
        self._loading: bool = False
        self._empty_text: str = "No data"
        self._on_sort: Optional[Callable] = None
        self._on_filter: Optional[Callable] = None
        self._on_page_change: Optional[Callable] = None
        self._on_row_click: Optional[Callable] = None
        self._on_rowDoubleClick: Optional[Callable] = None
        self._on_select: Optional[Callable] = None
        self._on_cell_edit: Optional[Callable] = None
        self._class_name: str = ""
        self._label: str = ""
        self._height: int = 500
        self._width: str = "100%"
    
    def columns(self, columns: List[GridColumn]) -> "DataGrid":
        """Set columns."""
        self._columns = columns
        return self
    
    def column(self, field: str, header: str = "", **kwargs) -> "DataGrid":
        """Add a column."""
        col = GridColumn(field=field, header=header or field, **kwargs)
        self._columns.append(col)
        return self
    
    def data(self, data: List[Dict[str, Any]]) -> "DataGrid":
        """Set data."""
        self._data = data
        self._pagination.total = len(data)
        return self
    
    def add_row(self, row: Dict[str, Any]):
        """Add a row."""
        self._data.append(row)
        self._pagination.total = len(self._data)
    
    def remove_row(self, index: int):
        """Remove a row."""
        if 0 <= index < len(self._data):
            self._data.pop(index)
            self._pagination.total = len(self._data)
    
    def sort(self, column: str, direction: GridSortDirection = GridSortDirection.ASC) -> "DataGrid":
        """Set sort."""
        self._sorts = [GridSort(column=column, direction=direction)]
        return self
    
    def multi_sort(self, sorts: List[GridSort]) -> "DataGrid":
        """Set multiple sorts."""
        self._sorts = sorts
        return self
    
    def filter(self, column: str, value: Any, filter_type: GridFilterType = GridFilterType.TEXT) -> "DataGrid":
        """Set filter."""
        self._filters = [GridFilter(column=column, value=value, type=filter_type)]
        return self
    
    def page(self, page: int) -> "DataGrid":
        """Set current page."""
        self._pagination.page = page
        return self
    
    def page_size(self, size: int) -> "DataGrid":
        """Set page size."""
        self._pagination.page_size = size
        return self
    
    def selectable(self, selectable: bool = True) -> "DataGrid":
        """Enable selection."""
        self._selectable = selectable
        return self
    
    def multi_select(self, multi: bool = True) -> "DataGrid":
        """Enable multi-select."""
        self._multi_select = multi
        return self
    
    def virtual_scroll(self, virtual: bool = True) -> "DataGrid":
        """Enable virtual scroll."""
        self._virtual_scroll = virtual
        return self
    
    def compact(self, compact: bool = True) -> "DataGrid":
        """Set compact mode."""
        self._compact = compact
        return self
    
    def loading(self, loading: bool = True) -> "DataGrid":
        """Set loading state."""
        self._loading = loading
        return self
    
    def on_sort(self, callback: Callable) -> "DataGrid":
        """Set sort handler."""
        self._on_sort = callback
        return self
    
    def on_filter(self, callback: Callable) -> "DataGrid":
        """Set filter handler."""
        self._on_filter = callback
        return self
    
    def on_page_change(self, callback: Callable) -> "DataGrid":
        """Set page change handler."""
        self._on_page_change = callback
        return self
    
    def on_row_click(self, callback: Callable) -> "DataGrid":
        """Set row click handler."""
        self._on_row_click = callback
        return self
    
    def on_select(self, callback: Callable) -> "DataGrid":
        """Set select handler."""
        self._on_select = callback
        return self
    
    def on_cell_edit(self, callback: Callable) -> "DataGrid":
        """Set cell edit handler."""
        self._on_cell_edit = callback
        return self
    
    def class_name(self, class_name: str) -> "DataGrid":
        """Set CSS class."""
        self._class_name = class_name
        return self
    
    def label(self, label: str) -> "DataGrid":
        """Set label."""
        self._label = label
        return self
    
    def height(self, height: int) -> "DataGrid":
        """Set height."""
        self._height = height
        return self
    
    def get_visible_data(self) -> List[Dict[str, Any]]:
        """Get data with filters and pagination applied."""
        data = self._data.copy()
        
        # Apply filters
        for f in self._filters:
            data = [row for row in data if self._matches_filter(row, f)]
        
        # Apply sort
        for s in reversed(self._sorts):
            data.sort(key=lambda row: row.get(s.column, ""), reverse=s.direction == GridSortDirection.DESC)
        
        # Apply pagination
        if self._paginated:
            start = (self._pagination.page - 1) * self._pagination.page_size
            end = start + self._pagination.page_size
            data = data[start:end]
        
        return data
    
    def _matches_filter(self, row: Dict[str, Any], f: GridFilter) -> bool:
        """Check if row matches filter."""
        value = row.get(f.column, "")
        filter_value = f.value
        
        if not filter_value:
            return True
        
        if f.type == GridFilterType.TEXT:
            return str(filter_value).lower() in str(value).lower()
        elif f.type == GridFilterType.NUMBER:
            try:
                return float(value) == float(filter_value)
            except (ValueError, TypeError):
                return False
        elif f.type == GridFilterType.BOOLEAN:
            return bool(value) == bool(filter_value)
        elif f.type == GridFilterType.SELECT:
            return value == filter_value
        
        return True
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "columns": [c.to_dict() for c in self._columns],
            "data": self.get_visible_data(),
            "sorts": [s.to_dict() for s in self._sorts],
            "filters": [f.to_dict() for f in self._filters],
            "pagination": self._pagination.to_dict(),
            "selectable": self._selectable,
            "multiSelect": self._multi_select,
            "sortable": self._sortable,
            "filterable": self._filterable,
            "paginated": self._paginated,
            "virtualScroll": self._virtual_scroll,
            "rowHeight": self._row_height,
            "showHeader": self._show_header,
            "showFooter": self._show_footer,
            "showRowNumbers": self._show_row_numbers,
            "showCheckboxes": self._show_checkboxes,
            "stripeRows": self._stripe_rows,
            "bordered": self._bordered,
            "compact": self._compact,
            "loading": self._loading,
            "emptyText": self._empty_text,
            "className": self._class_name,
            "label": self._label,
            "height": self._height,
        }
    
    def to_html(self) -> str:
        """Generate HTML."""
        label_html = f'<h3 class="grid-label">{self._label}</h3>' if self._label else ""
        class_attr = f" {self._class_name}" if self._class_name else ""
        compact_class = " grid-compact" if self._compact else ""
        loading_class = " grid-loading" if self._loading else ""
        
        # Header
        header_cells = ""
        if self._show_checkboxes:
            header_cells += '<th class="grid-th grid-th-checkbox"><input type="checkbox" class="grid-select-all"></th>'
        if self._show_row_numbers:
            header_cells += '<th class="grid-th grid-th-num">#</th>'
        
        for col in self._columns:
            if not col.visible:
                continue
            
            sort_icon = ""
            sort_class = ""
            for s in self._sorts:
                if s.column == col.field:
                    sort_class = f" sort-{s.direction.value}"
                    sort_icon = " ▲" if s.direction == GridSortDirection.ASC else " ▼"
            
            frozen_class = " grid-th-frozen" if col.frozen else ""
            width_style = f' style="width: {col.width}px"' if col.width else ""
            
            header_cells += f'<th class="grid-th{sort_class}{frozen_class}" data-field="{col.field}"{width_style}>{col.header}{sort_icon}</th>'
        
        header_html = f'<thead class="grid-thead"><tr>{header_cells}</tr></thead>' if self._show_header else ""
        
        # Body
        visible_data = self.get_visible_data()
        rows_html = ""
        
        if not visible_data:
            rows_html = f'<tr class="grid-empty"><td colspan="{len(self._columns) + 2}">{self._empty_text}</td></tr>'
        else:
            for i, row in enumerate(visible_data):
                row_class = "grid-row"
                if i % 2 == 1 and self._stripe_rows:
                    row_class += " grid-row-stripe"
                
                cells = ""
                if self._show_checkboxes:
                    cells += f'<td class="grid-td grid-td-checkbox"><input type="checkbox" class="grid-row-select" data-index="{i}"></td>'
                if self._show_row_numbers:
                    cells += f'<td class="grid-td grid-td-num">{i + 1}</td>'
                
                for col in self._columns:
                    if not col.visible:
                        continue
                    
                    value = row.get(col.field, "")
                    align_class = f" text-{col.align.value}"
                    frozen_class = " grid-td-frozen" if col.frozen else ""
                    editable_class = " grid-td-editable" if col.editable else ""
                    
                    cells += f'<td class="grid-td{align_class}{frozen_class}{editable_class}" data-field="{col.field}" data-row="{i}">{value}</td>'
                
                rows_html += f'<tr class="{row_class}" data-index="{i}">{cells}</tr>'
        
        body_html = f'<tbody class="grid-tbody">{rows_html}</tbody>'
        
        # Footer/Pagination
        footer_html = ""
        if self._show_footer and self._paginated:
            p = self._pagination
            page_info = f'Showing {(p.page - 1) * p.page_size + 1}-{min(p.page * p.page_size, p.total)} of {p.total}'
            footer_html = f'''<tfoot class="grid-tfoot"><tr>
                <td colspan="{len(self._columns) + 2}">
                    <div class="grid-pagination">
                        <span class="grid-page-info">{page_info}</span>
                        <div class="grid-page-buttons">
                            <button class="grid-page-btn" data-page="1" {"" if p.has_prev else "disabled"}>&laquo;</button>
                            <button class="grid-page-btn" data-page="{p.page - 1}" {"" if p.has_prev else "disabled"}>&lsaquo;</button>
                            <span class="grid-page-current">{p.page} / {p.total_pages}</span>
                            <button class="grid-page-btn" data-page="{p.page + 1}" {"" if p.has_next else "disabled"}>&rsaquo;</button>
                            <button class="grid-page-btn" data-page="{p.total_pages}" {"" if p.has_next else "disabled"}>&raquo;</button>
                        </div>
                    </div>
                </td>
            </tr></tfoot>'''
        
        # Loading overlay
        loading_html = '<div class="grid-loading-overlay"><div class="grid-spinner"></div></div>' if self._loading else ""
        
        return f'''<div class="datagrid{compact_class}{loading_class}{class_attr}" style="height: {self._height}px;">
            {label_html}
            <div class="grid-wrapper">
                <table class="grid-table">
                    {header_html}
                    {body_html}
                    {footer_html}
                </table>
                {loading_html}
            </div>
        </div>'''
    
    def generate_js_code(self) -> str:
        """Generate JavaScript."""
        config = self.to_dict()
        return f"""
        // Data Grid
        (function() {{
            const config = {str(config).replace("'", '"')};
            
            const grid = document.querySelector('.datagrid');
            if (!grid) return;
            
            // Sort
            grid.querySelectorAll('.grid-th[data-field]').forEach(th => {{
                th.addEventListener('click', () => {{
                    const field = th.dataset.field;
                    console.log('Sort by:', field);
                }});
            }});
            
            // Row click
            grid.querySelectorAll('.grid-row').forEach(row => {{
                row.addEventListener('click', () => {{
                    const index = row.dataset.index;
                    console.log('Row clicked:', index);
                }});
                
                row.addEventListener('dblclick', () => {{
                    const index = row.dataset.index;
                    console.log('Row double clicked:', index);
                }});
            }});
            
            // Select all
            const selectAll = grid.querySelector('.grid-select-all');
            if (selectAll) {{
                selectAll.addEventListener('change', () => {{
                    grid.querySelectorAll('.grid-row-select').forEach(cb => {{
                        cb.checked = selectAll.checked;
                    }});
                }});
            }}
            
            // Pagination
            grid.querySelectorAll('.grid-page-btn').forEach(btn => {{
                btn.addEventListener('click', () => {{
                    const page = parseInt(btn.dataset.page);
                    if (!isNaN(page)) {{
                        console.log('Go to page:', page);
                    }}
                }});
            }});
            
            // Cell edit
            grid.querySelectorAll('.grid-td-editable').forEach(td => {{
                td.addEventListener('dblclick', () => {{
                    const field = td.dataset.field;
                    const rowIndex = td.dataset.row;
                    console.log('Edit cell:', field, rowIndex);
                }});
            }});
        }})();
        """


def create_datagrid(columns: List[GridColumn] = None, data: List[Dict[str, Any]] = None) -> DataGrid:
    """Create a data grid."""
    return DataGrid(columns, data)


def grid_column(field: str, header: str = "", **kwargs) -> GridColumn:
    """Create a grid column."""
    return GridColumn(field=field, header=header or field, **kwargs)


def grid_sort(column: str, direction: GridSortDirection = GridSortDirection.ASC) -> GridSort:
    """Create a grid sort."""
    return GridSort(column=column, direction=direction)


def grid_filter(column: str, value: Any, filter_type: GridFilterType = GridFilterType.TEXT) -> GridFilter:
    """Create a grid filter."""
    return GridFilter(column=column, value=value, type=filter_type)


DATA_GRID_CSS = """
.datagrid {
    border: 1px solid #e5e7eb;
    border-radius: 0.5rem;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    background: white;
}

.grid-label {
    padding: 1rem;
    margin: 0;
    font-size: 1.25rem;
    font-weight: 600;
    color: #111827;
    border-bottom: 1px solid #e5e7eb;
}

.grid-wrapper {
    flex: 1;
    overflow: auto;
    position: relative;
}

.grid-table {
    width: 100%;
    border-collapse: collapse;
}

.grid-thead {
    position: sticky;
    top: 0;
    z-index: 10;
}

.grid-th {
    padding: 0.75rem 1rem;
    text-align: left;
    font-weight: 600;
    color: #374151;
    background: #f9fafb;
    border-bottom: 2px solid #e5e7eb;
    white-space: nowrap;
    cursor: pointer;
    user-select: none;
}

.grid-th:hover {
    background: #f3f4f6;
}

.grid-th.sort-asc::after {
    content: ' ▲';
}

.grid-th.sort-desc::after {
    content: ' ▼';
}

.grid-th-checkbox,
.grid-td-checkbox {
    width: 40px;
    text-align: center;
}

.grid-th-num,
.grid-td-num {
    width: 50px;
    text-align: center;
    color: #6b7280;
}

.grid-tbody {
    overflow: auto;
}

.grid-row {
    border-bottom: 1px solid #f3f4f6;
}

.grid-row:hover {
    background: #f9fafb;
}

.grid-row-stripe {
    background: #fafafa;
}

.grid-row-stripe:hover {
    background: #f3f4f6;
}

.grid-td {
    padding: 0.75rem 1rem;
    color: #374151;
}

.grid-td-editable {
    cursor: pointer;
}

.grid-td-editable:hover {
    background: #eff6ff;
}

.text-left { text-align: left; }
.text-center { text-align: center; }
.text-right { text-align: right; }

.grid-tfoot {
    border-top: 2px solid #e5e7eb;
    background: #f9fafb;
}

.grid-pagination {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.75rem 1rem;
}

.grid-page-info {
    font-size: 0.875rem;
    color: #6b7280;
}

.grid-page-buttons {
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.grid-page-btn {
    padding: 0.375rem 0.625rem;
    border: 1px solid #d1d5db;
    background: white;
    border-radius: 0.25rem;
    cursor: pointer;
}

.grid-page-btn:hover:not(:disabled) {
    background: #f9fafb;
}

.grid-page-btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

.grid-page-current {
    font-size: 0.875rem;
    color: #374151;
}

.grid-empty {
    text-align: center;
    padding: 3rem;
    color: #9ca3af;
}

.grid-loading-overlay {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(255, 255, 255, 0.8);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 20;
}

.grid-spinner {
    width: 40px;
    height: 40px;
    border: 3px solid #e5e7eb;
    border-top-color: #3b82f6;
    border-radius: 50%;
    animation: spin 1s linear infinite;
}

@keyframes spin {
    to { transform: rotate(360deg); }
}

.grid-compact .grid-th,
.grid-compact .grid-td {
    padding: 0.5rem 0.75rem;
}

.grid-th-frozen,
.grid-td-frozen {
    position: sticky;
    left: 0;
    background: inherit;
    z-index: 5;
}

.grid-th-frozen {
    z-index: 15;
}
"""
