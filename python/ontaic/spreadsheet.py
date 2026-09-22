"""Spreadsheet component like Excel."""
from typing import Any, Callable, Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum


class CellType(str, Enum):
    """Cell data type."""
    TEXT = "text"
    NUMBER = "number"
    BOOLEAN = "boolean"
    DATE = "date"
    FORMULA = "formula"
    SELECT = "select"
    CURRENCY = "currency"
    PERCENT = "percent"


class CellAlign(str, Enum):
    """Cell alignment."""
    LEFT = "left"
    CENTER = "center"
    RIGHT = "right"


@dataclass
class CellStyle:
    """Cell styling."""
    bold: bool = False
    italic: bool = False
    underline: bool = False
    strikethrough: bool = False
    font_size: int = 14
    font_family: str = ""
    color: str = ""
    background: str = ""
    align: CellAlign = CellAlign.LEFT
    vertical_align: str = "middle"
    wrap: bool = False
    border_top: str = ""
    border_right: str = ""
    border_bottom: str = ""
    border_left: str = ""
    
    def to_dict(self) -> dict:
        return {
            "bold": self.bold,
            "italic": self.italic,
            "underline": self.underline,
            "strikethrough": self.strikethrough,
            "fontSize": self.font_size,
            "fontFamily": self.font_family,
            "color": self.color,
            "background": self.background,
            "align": self.align.value,
            "verticalAlign": self.vertical_align,
            "wrap": self.wrap,
        }


@dataclass
class Cell:
    """Spreadsheet cell."""
    row: int
    col: int
    value: Any = ""
    formula: str = ""
    type: CellType = CellType.TEXT
    style: CellStyle = field(default_factory=CellStyle)
    options: List[Dict[str, Any]] = field(default_factory=list)
    validation: Dict[str, Any] = field(default_factory=dict)
    comment: str = ""
    locked: bool = False
    
    @property
    def address(self) -> str:
        """Get cell address like A1."""
        col_letter = ""
        col = self.col
        while col > 0:
            col -= 1
            col_letter = chr(65 + col % 26) + col_letter
            col //= 26
        return f"{col_letter}{self.row + 1}"
    
    def to_dict(self) -> dict:
        return {
            "row": self.row,
            "col": self.col,
            "value": self.value,
            "formula": self.formula,
            "type": self.type.value,
            "style": self.style.to_dict(),
            "options": self.options,
            "validation": self.validation,
            "comment": self.comment,
            "locked": self.locked,
        }


@dataclass
class SpreadsheetRange:
    """Spreadsheet range."""
    start_row: int
    start_col: int
    end_row: int
    end_col: int
    
    def contains(self, row: int, col: int) -> bool:
        """Check if range contains cell."""
        return (self.start_row <= row <= self.end_row and 
                self.start_col <= col <= self.end_col)
    
    def to_dict(self) -> dict:
        return {
            "startRow": self.start_row,
            "startCol": self.start_col,
            "endRow": self.end_row,
            "endCol": self.end_col,
        }


class Spreadsheet:
    """Spreadsheet component like Excel."""
    
    def __init__(self, rows: int = 100, cols: int = 26):
        self._rows = rows
        self._cols = cols
        self._cells: Dict[Tuple[int, int], Cell] = {}
        self._row_heights: Dict[int, int] = {}
        self._col_widths: Dict[int, int] = {}
        self._default_row_height: int = 32
        self._default_col_width: int = 100
        self._frozen_rows: int = 0
        self._frozen_cols: int = 0
        self._selected_range: Optional[SpreadsheetRange] = None
        self._active_cell: Optional[Tuple[int, int]] = None
        self._selection: List[Tuple[int, int]] = []
        self._clipboard: List[List[Any]] = []
        self._undo_stack: List[Dict] = []
        self._redo_stack: List[Dict] = []
        self._show_grid: bool = True
        self._show_headers: bool = True
        self._show_toolbar: bool = True
        self._show_formulas: bool = False
        self._editable: bool = True
        self._selectable: bool = True
        self._multi_select: bool = True
        self._auto_calc: bool = True
        self._on_change: Optional[Callable] = None
        self._on_select: Optional[Callable] = None
        self._on_cell_click: Optional[Callable] = None
        self._on_cell_edit: Optional[Callable] = None
        self._on_cell_double_click: Optional[Callable] = None
        self._on_context_menu: Optional[Callable] = None
        self._class_name: str = ""
        self._label: str = ""
        self._height: int = 500
        self._width: str = "100%"
    
    def cell(self, row: int, col: int, value: Any = None, **kwargs) -> "Spreadsheet":
        """Set cell value."""
        if (row, col) not in self._cells:
            self._cells[(row, col)] = Cell(row=row, col=col)
        
        cell = self._cells[(row, col)]
        if value is not None:
            cell.value = value
        
        for key, val in kwargs.items():
            if hasattr(cell, key):
                setattr(cell, key, val)
            elif key == "bold":
                cell.style.bold = val
            elif key == "italic":
                cell.style.italic = val
            elif key == "background":
                cell.style.background = val
            elif key == "color":
                cell.style.color = val
        
        return self
    
    def set_data(self, data: List[List[Any]]):
        """Set spreadsheet data from 2D array."""
        self._cells.clear()
        for row_idx, row_data in enumerate(data):
            for col_idx, value in enumerate(row_data):
                self._cells[(row_idx, col_idx)] = Cell(row=row_idx, col=col_idx, value=value)
    
    def get_cell(self, row: int, col: int) -> Optional[Cell]:
        """Get cell."""
        return self._cells.get((row, col))
    
    def get_range(self, range: SpreadsheetRange) -> List[List[Any]]:
        """Get range values."""
        result = []
        for row in range(range.start_row, range.end_row + 1):
            row_data = []
            for col in range(range.start_col, range.end_col + 1):
                cell = self._cells.get((row, col))
                row_data.append(cell.value if cell else "")
            result.append(row_data)
        return result
    
    def set_range(self, range: SpreadsheetRange, data: List[List[Any]]):
        """Set range values."""
        for row_idx, row_data in enumerate(data):
            for col_idx, value in enumerate(row_data):
                row = range.start_row + row_idx
                col = range.start_col + col_idx
                if row <= range.end_row and col <= range.end_col:
                    self.cell(row, col, value)
    
    def row_height(self, row: int, height: int) -> "Spreadsheet":
        """Set row height."""
        self._row_heights[row] = height
        return self
    
    def col_width(self, col: int, width: int) -> "Spreadsheet":
        """Set column width."""
        self._col_widths[col] = width
        return self
    
    def frozen_rows(self, rows: int) -> "Spreadsheet":
        """Set frozen rows."""
        self._frozen_rows = rows
        return self
    
    def frozen_cols(self, cols: int) -> "Spreadsheet":
        """Set frozen columns."""
        self._frozen_cols = cols
        return self
    
    def select(self, range: SpreadsheetRange) -> "Spreadsheet":
        """Select range."""
        self._selected_range = range
        return self
    
    def on_change(self, callback: Callable) -> "Spreadsheet":
        """Set change handler."""
        self._on_change = callback
        return self
    
    def on_select(self, callback: Callable) -> "Spreadsheet":
        """Set select handler."""
        self._on_select = callback
        return self
    
    def on_cell_edit(self, callback: Callable) -> "Spreadsheet":
        """Set cell edit handler."""
        self._on_cell_edit = callback
        return self
    
    def class_name(self, class_name: str) -> "Spreadsheet":
        """Set CSS class."""
        self._class_name = class_name
        return self
    
    def label(self, label: str) -> "Spreadsheet":
        """Set label."""
        self._label = label
        return self
    
    def height(self, height: int) -> "Spreadsheet":
        """Set height."""
        self._height = height
        return self
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "rows": self._rows,
            "cols": self._cols,
            "cells": {f"{k[0]},{k[1]}": v.to_dict() for k, v in self._cells.items()},
            "rowHeights": self._row_heights,
            "colWidths": self._col_widths,
            "defaultRowHeight": self._default_row_height,
            "defaultColWidth": self._default_col_width,
            "frozenRows": self._frozen_rows,
            "frozenCols": self._frozen_cols,
            "showGrid": self._show_grid,
            "showHeaders": self._show_headers,
            "showToolbar": self._show_toolbar,
            "editable": self._editable,
            "className": self._class_name,
            "label": self._label,
            "height": self._height,
        }
    
    def to_html(self) -> str:
        """Generate HTML."""
        label_html = f'<h3 class="sheet-label">{self._label}</h3>' if self._label else ""
        class_attr = f" {self._class_name}" if self._class_name else ""
        
        # Toolbar
        toolbar_html = ""
        if self._show_toolbar:
            toolbar_html = '''<div class="sheet-toolbar">
                <button class="sheet-tool-btn" data-action="undo" title="Undo">↶</button>
                <button class="sheet-tool-btn" data-action="redo" title="Redo">↷</button>
                <span class="sheet-separator"></span>
                <button class="sheet-tool-btn" data-action="bold" title="Bold"><strong>B</strong></button>
                <button class="sheet-tool-btn" data-action="italic" title="Italic"><em>I</em></button>
                <button class="sheet-tool-btn" data-action="underline" title="Underline"><u>U</u></button>
                <span class="sheet-separator"></span>
                <button class="sheet-tool-btn" data-action="align-left" title="Align Left">≡</button>
                <button class="sheet-tool-btn" data-action="align-center" title="Align Center">≡</button>
                <button class="sheet-tool-btn" data-action="align-right" title="Align Right">≡</button>
                <span class="sheet-separator"></span>
                <button class="sheet-tool-btn" data-action="merge" title="Merge Cells">⊞</button>
                <button class="sheet-tool-btn" data-action="formula" title="Insert Formula">fx</button>
            </div>'''
        
        # Column headers
        col_headers = '<th class="sheet-corner"></th>'
        for col in range(min(self._cols, 26)):
            col_letter = chr(65 + col)
            width = self._col_widths.get(col, self._default_col_width)
            col_headers += f'<th class="sheet-col-header" data-col="{col}" style="width: {width}px">{col_letter}</th>'
        
        # Rows
        rows_html = ""
        for row in range(min(self._rows, 100)):
            height = self._row_heights.get(row, self._default_row_height)
            cells = f'<td class="sheet-row-header" data-row="{row}">{row + 1}</td>'
            
            for col in range(min(self._cols, 26)):
                cell = self._cells.get((row, col))
                value = cell.value if cell else ""
                cell_class = "sheet-cell"
                style = ""
                
                if cell and cell.style:
                    if cell.style.bold:
                        style += "font-weight: bold;"
                    if cell.style.italic:
                        style += "font-style: italic;"
                    if cell.style.background:
                        style += f"background: {cell.style.background};"
                    if cell.style.color:
                        style += f"color: {cell.style.color};"
                    style += f"text-align: {cell.style.align.value};"
                
                cells += f'<td class="{cell_class}" data-row="{row}" data-col="{col}" style="{style}">{value}</td>'
            
            rows_html += f'<tr class="sheet-row" style="height: {height}px">{cells}</tr>'
        
        help_html = f'<p class="sheet-help">{self._help_text}</p>' if hasattr(self, '_help_text') and self._help_text else ""
        
        return f'''<div class="spreadsheet{class_attr}" style="height: {self._height}px;">
            {label_html}
            {toolbar_html}
            <div class="sheet-formula-bar">
                <span class="sheet-cell-address">A1</span>
                <input type="text" class="sheet-formula-input" placeholder="Enter value or formula">
            </div>
            <div class="sheet-wrapper">
                <table class="sheet-table">
                    <thead><tr>{col_headers}</tr></thead>
                    <tbody>{rows_html}</tbody>
                </table>
            </div>
            {help_html}
        </div>'''
    
    def generate_js_code(self) -> str:
        """Generate JavaScript."""
        config = self.to_dict()
        return f"""
        // Spreadsheet
        (function() {{
            const config = {str(config).replace("'", '"')};
            
            const sheet = document.querySelector('.spreadsheet');
            if (!sheet) return;
            
            let activeCell = null;
            
            // Cell click
            sheet.querySelectorAll('.sheet-cell').forEach(cell => {{
                cell.addEventListener('click', () => {{
                    sheet.querySelectorAll('.sheet-cell.selected').forEach(c => c.classList.remove('selected'));
                    cell.classList.add('selected');
                    
                    const row = cell.dataset.row;
                    const col = cell.dataset.col;
                    const address = sheet.querySelector('.sheet-cell-address');
                    if (address) {{
                        const colLetter = String.fromCharCode(65 + parseInt(col));
                        address.textContent = colLetter + (parseInt(row) + 1);
                    }}
                    
                    activeCell = cell;
                    console.log('Cell selected:', row, col);
                }});
                
                cell.addEventListener('dblclick', () => {{
                    cell.contentEditable = true;
                    cell.focus();
                }});
                
                cell.addEventListener('blur', () => {{
                    cell.contentEditable = false;
                    console.log('Cell edited:', cell.textContent);
                }});
                
                cell.addEventListener('keydown', (e) => {{
                    if (e.key === 'Enter') {{
                        cell.blur();
                    }}
                }});
            }});
            
            // Toolbar
            sheet.querySelectorAll('.sheet-tool-btn').forEach(btn => {{
                btn.addEventListener('click', () => {{
                    const action = btn.dataset.action;
                    console.log('Toolbar action:', action);
                    
                    if (activeCell) {{
                        switch (action) {{
                            case 'bold':
                                activeCell.style.fontWeight = activeCell.style.fontWeight === 'bold' ? 'normal' : 'bold';
                                break;
                            case 'italic':
                                activeCell.style.fontStyle = activeCell.style.fontStyle === 'italic' ? 'normal' : 'italic';
                                break;
                        }}
                    }}
                }});
            }});
            
            // Formula bar
            const formulaInput = sheet.querySelector('.sheet-formula-input');
            if (formulaInput && activeCell) {{
                formulaInput.addEventListener('input', (e) => {{
                    activeCell.textContent = e.target.value;
                }});
            }}
            
            // Keyboard navigation
            sheet.addEventListener('keydown', (e) => {{
                if (!activeCell || activeCell.contentEditable === 'true') return;
                
                const row = parseInt(activeCell.dataset.row);
                const col = parseInt(activeCell.dataset.col);
                
                let newRow = row;
                let newCol = col;
                
                switch (e.key) {{
                    case 'ArrowUp': newRow = Math.max(0, row - 1); break;
                    case 'ArrowDown': newRow = row + 1; break;
                    case 'ArrowLeft': newCol = Math.max(0, col - 1); break;
                    case 'ArrowRight': newCol = col + 1; break;
                    case 'Tab':
                        e.preventDefault();
                        newCol = e.shiftKey ? Math.max(0, col - 1) : col + 1;
                        break;
                }}
                
                if (newRow !== row || newCol !== col) {{
                    const newCell = sheet.querySelector(`.sheet-cell[data-row="${{newRow}}"][data-col="${{newCol}}"]`);
                    if (newCell) {{
                        newCell.click();
                    }}
                }}
            }});
        }})();
        """


def create_spreadsheet(rows: int = 100, cols: int = 26) -> Spreadsheet:
    """Create a spreadsheet."""
    return Spreadsheet(rows, cols)


def cell_style(**kwargs) -> CellStyle:
    """Create cell style."""
    return CellStyle(**kwargs)


SPREADSHEET_CSS = """
.spreadsheet {
    border: 1px solid #e5e7eb;
    border-radius: 0.5rem;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    background: white;
}

.sheet-label {
    padding: 1rem;
    margin: 0;
    font-size: 1.25rem;
    font-weight: 600;
    color: #111827;
    border-bottom: 1px solid #e5e7eb;
}

.sheet-toolbar {
    display: flex;
    align-items: center;
    gap: 0.25rem;
    padding: 0.5rem 1rem;
    background: #f9fafb;
    border-bottom: 1px solid #e5e7eb;
}

.sheet-tool-btn {
    width: 32px;
    height: 32px;
    display: flex;
    align-items: center;
    justify-content: center;
    border: none;
    background: transparent;
    border-radius: 0.25rem;
    cursor: pointer;
    font-size: 0.875rem;
}

.sheet-tool-btn:hover {
    background: #e5e7eb;
}

.sheet-separator {
    width: 1px;
    height: 20px;
    background: #d1d5db;
    margin: 0 0.25rem;
}

.sheet-formula-bar {
    display: flex;
    align-items: center;
    padding: 0.5rem 1rem;
    border-bottom: 1px solid #e5e7eb;
    background: white;
}

.sheet-cell-address {
    width: 60px;
    font-weight: 500;
    color: #374151;
    font-family: monospace;
}

.sheet-formula-input {
    flex: 1;
    padding: 0.375rem 0.5rem;
    border: 1px solid #d1d5db;
    border-radius: 0.25rem;
    font-family: monospace;
    font-size: 0.875rem;
}

.sheet-formula-input:focus {
    outline: none;
    border-color: #3b82f6;
}

.sheet-wrapper {
    flex: 1;
    overflow: auto;
}

.sheet-table {
    border-collapse: collapse;
    table-layout: fixed;
}

.sheet-corner {
    width: 50px;
    background: #f9fafb;
    border: 1px solid #e5e7eb;
}

.sheet-col-header {
    padding: 0.5rem;
    background: #f9fafb;
    border: 1px solid #e5e7eb;
    font-weight: 500;
    color: #6b7280;
    text-align: center;
    user-select: none;
}

.sheet-row-header {
    width: 50px;
    padding: 0.5rem;
    background: #f9fafb;
    border: 1px solid #e5e7eb;
    font-weight: 500;
    color: #6b7280;
    text-align: center;
    user-select: none;
}

.sheet-cell {
    padding: 0.375rem 0.5rem;
    border: 1px solid #e5e7eb;
    min-width: 100px;
    height: 32px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.sheet-cell:hover {
    background: #f9fafb;
}

.sheet-cell.selected {
    outline: 2px solid #3b82f6;
    outline-offset: -2px;
    background: #eff6ff;
}

.sheet-cell[contenteditable="true"] {
    outline: 2px solid #2563eb;
    outline-offset: -2px;
    background: white;
}

.sheet-help {
    padding: 0.75rem 1rem;
    margin: 0;
    font-size: 0.875rem;
    color: #6b7280;
    border-top: 1px solid #e5e7eb;
}
"""
