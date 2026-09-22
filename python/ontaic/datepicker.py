"""Date picker component."""
import calendar
from datetime import datetime, timedelta
from typing import Any, Callable, Dict, List, Optional, Union
from dataclasses import dataclass, field
from enum import Enum


class PickerMode(str, Enum):
    """Date picker mode."""
    DATE = "date"
    TIME = "time"
    DATETIME = "datetime"
    MONTH = "month"
    YEAR = "year"


class PickerSize(str, Enum):
    """Date picker size."""
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"


@dataclass
class PickerPreset:
    """Date picker preset."""
    label: str
    value: Any
    
    def to_dict(self) -> dict:
        return {"label": self.label, "value": str(self.value)}


PRESETS = [
    PickerPreset("Today", "today"),
    PickerPreset("Yesterday", "yesterday"),
    PickerPreset("Last 7 days", "last_7_days"),
    PickerPreset("Last 30 days", "last_30_days"),
    PickerPreset("This month", "this_month"),
    PickerPreset("Last month", "last_month"),
]


class DatePicker:
    """Date picker component."""
    
    def __init__(self, name: str = "date", placeholder: str = "Select date", mode: PickerMode = PickerMode.DATE):
        self.name = name
        self.placeholder = placeholder
        self.mode = mode
        self._value: Optional[datetime] = None
        self._min_date: Optional[datetime] = None
        self._max_date: Optional[datetime] = None
        self._disabled_dates: List[datetime] = []
        self._disabled_days_of_week: List[int] = []
        self._first_day_of_week: int = 0
        self._show_presets: bool = False
        self._presets: List[PickerPreset] = PRESETS
        self._on_change: Optional[Callable] = None
        self._on_open: Optional[Callable] = None
        self._on_close: Optional[Callable] = None
        self._inline: bool = False
        self._size: PickerSize = PickerSize.MEDIUM
        self._class_name: str = ""
        self._label: str = ""
        self._help_text: str = ""
        self._error: str = ""
        self._required: bool = False
        self._disabled: bool = False
        self._readonly: bool = False
    
    def value(self, value: Union[datetime, str, None]) -> "DatePicker":
        """Set value."""
        if isinstance(value, str):
            try:
                value = datetime.fromisoformat(value)
            except ValueError:
                value = None
        self._value = value
        return self
    
    def min_date(self, value: Union[datetime, str]) -> "DatePicker":
        """Set minimum date."""
        if isinstance(value, str):
            value = datetime.fromisoformat(value)
        self._min_date = value
        return self
    
    def max_date(self, value: Union[datetime, str]) -> "DatePicker":
        """Set maximum date."""
        if isinstance(value, str):
            value = datetime.fromisoformat(value)
        self._max_date = value
        return self
    
    def disabled_dates(self, dates: List[Union[datetime, str]]) -> "DatePicker":
        """Set disabled dates."""
        self._disabled_dates = []
        for d in dates:
            if isinstance(d, str):
                d = datetime.fromisoformat(d)
            self._disabled_dates.append(d)
        return self
    
    def disabled_days_of_week(self, days: List[int]) -> "DatePicker":
        """Set disabled days of week (0=Sunday, 6=Saturday)."""
        self._disabled_days_of_week = days
        return self
    
    def first_day_of_week(self, day: int) -> "DatePicker":
        """Set first day of week (0=Sunday, 1=Monday)."""
        self._first_day_of_week = day
        return self
    
    def show_presets(self, show: bool = True, presets: List[PickerPreset] = None) -> "DatePicker":
        """Show presets panel."""
        self._show_presets = show
        if presets:
            self._presets = presets
        return self
    
    def on_change(self, callback: Callable) -> "DatePicker":
        """Set change handler."""
        self._on_change = callback
        return self
    
    def on_open(self, callback: Callable) -> "DatePicker":
        """Set open handler."""
        self._on_open = callback
        return self
    
    def on_close(self, callback: Callable) -> "DatePicker":
        """Set close handler."""
        self._on_close = callback
        return self
    
    def inline(self) -> "DatePicker":
        """Make picker inline."""
        self._inline = True
        return self
    
    def size(self, size: PickerSize) -> "DatePicker":
        """Set size."""
        self._size = size
        return self
    
    def class_name(self, class_name: str) -> "DatePicker":
        """Set CSS class."""
        self._class_name = class_name
        return self
    
    def label(self, label: str) -> "DatePicker":
        """Set label."""
        self._label = label
        return self
    
    def help_text(self, text: str) -> "DatePicker":
        """Set help text."""
        self._help_text = text
        return self
    
    def error(self, error: str) -> "DatePicker":
        """Set error message."""
        self._error = error
        return self
    
    def required(self) -> "DatePicker":
        """Make required."""
        self._required = True
        return self
    
    def disabled(self) -> "DatePicker":
        """Make disabled."""
        self._disabled = True
        return self
    
    def readonly(self) -> "DatePicker":
        """Make readonly."""
        self._readonly = True
        return self
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "placeholder": self.placeholder,
            "mode": self.mode.value,
            "value": self._value.isoformat() if self._value else None,
            "minDate": self._min_date.isoformat() if self._min_date else None,
            "maxDate": self._max_date.isoformat() if self._max_date else None,
            "disabledDates": [d.isoformat() for d in self._disabled_dates],
            "disabledDaysOfWeek": self._disabled_days_of_week,
            "firstDayOfWeek": self._first_day_of_week,
            "showPresets": self._show_presets,
            "presets": [p.to_dict() for p in self._presets],
            "inline": self._inline,
            "size": self._size.value,
            "className": self._class_name,
            "label": self._label,
            "helpText": self._help_text,
            "error": self._error,
            "required": self._required,
            "disabled": self._disabled,
            "readonly": self._readonly,
        }
    
    def to_html(self) -> str:
        """Generate HTML for date picker."""
        label_html = f'<label class="date-picker-label">{self._label}</label>' if self._label else ""
        help_html = f'<p class="date-picker-help">{self._help_text}</p>' if self._help_text else ""
        error_html = f'<p class="date-picker-error">{self._error}</p>' if self._error else ""
        
        size_class = f" date-picker-{self._size.value}" if self._size != PickerSize.MEDIUM else ""
        error_class = " date-picker-error-state" if self._error else ""
        disabled_class = " disabled" if self._disabled else ""
        class_attr = f" {self._class_name}" if self._class_name else ""
        
        display_value = ""
        if self._value:
            if self.mode == PickerMode.DATE:
                display_value = self._value.strftime("%Y-%m-%d")
            elif self.mode == PickerMode.TIME:
                display_value = self._value.strftime("%H:%M")
            elif self.mode == PickerMode.DATETIME:
                display_value = self._value.strftime("%Y-%m-%d %H:%M")
            elif self.mode == PickerMode.MONTH:
                display_value = self._value.strftime("%Y-%m")
            elif self.mode == PickerMode.YEAR:
                display_value = self._value.strftime("%Y")
        
        input_readonly = " readonly" if self._readonly else ""
        input_disabled = " disabled" if self._disabled else ""
        input_required = " required" if self._required else ""
        
        presets_html = ""
        if self._show_presets:
            presets = "".join(f'<button type="button" class="preset-btn" data-value="{p.value}">{p.label}</button>' for p in self._presets)
            presets_html = f'<div class="date-picker-presets">{presets}</div>'
        
        if self._inline:
            calendar_html = self._render_calendar()
            return f'''<div class="date-picker-container{size_class}{error_class}{disabled_class}{class_attr}">
                {label_html}
                <div class="date-picker-inline">
                    {calendar_html}
                </div>
                {presets_html}
                {help_html}
                {error_html}
            </div>'''
        
        return f'''<div class="date-picker-container{size_class}{error_class}{disabled_class}{class_attr}">
            {label_html}
            <div class="date-picker-input-wrapper">
                <input type="text" class="date-picker-input" name="{self.name}" value="{display_value}" placeholder="{self.placeholder}" data-mode="{self.mode.value}"{input_readonly}{input_disabled}{input_required}>
                <button type="button" class="date-picker-toggle" aria-label="Open date picker">
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line></svg>
                </button>
            </div>
            <div class="date-picker-dropdown">
                {self._render_calendar()}
            </div>
            {presets_html}
            {help_html}
            {error_html}
        </div>'''
    
    def _render_calendar(self) -> str:
        """Render calendar HTML."""
        now = datetime.now()
        year = self._value.year if self._value else now.year
        month = self._value.month if self._value else now.month
        
        month_name = calendar.month_name[month]
        
        prev_month = month - 1 if month > 1 else 12
        prev_year = year if month > 1 else year - 1
        next_month = month + 1 if month < 12 else 1
        next_year = year if month < 12 else year + 1
        
        days_header = ["Su", "Mo", "Tu", "We", "Th", "Fr", "Sa"]
        if self._first_day_of_week == 1:
            days_header = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]
        
        days_html = "".join(f'<th class="calendar-weekday">{d}</th>' for d in days_header)
        
        cal = calendar.monthcalendar(year, month)
        weeks_html = ""
        for week in cal:
            days = ""
            for i, day in enumerate(week):
                if day == 0:
                    days += '<td class="calendar-day empty"></td>'
                    continue
                
                day_date = datetime(year, month, day)
                is_today = day_date.date() == now.date()
                is_selected = self._value and day_date.date() == self._value.date()
                is_disabled = day_date in self._disabled_dates
                is_weekend = (i + self._first_day_of_week) % 7 >= 5
                is_disabled_day = (i + self._first_day_of_week) % 7 in self._disabled_days_of_week
                is_before_min = self._min_date and day_date < self._min_date
                is_after_max = self._max_date and day_date > self._max_date
                
                classes = ["calendar-day"]
                if is_today:
                    classes.append("today")
                if is_selected:
                    classes.append("selected")
                if is_disabled or is_disabled_day or is_before_min or is_after_max:
                    classes.append("disabled")
                if is_weekend:
                    classes.append("weekend")
                
                days += f'<td class="{" ".join(classes)}" data-date="{day_date.isoformat()}">{day}</td>'
            
            weeks_html += f"<tr>{days}</tr>"
        
        return f'''<div class="calendar">
            <div class="calendar-header">
                <button type="button" class="calendar-nav" data-direction="prev" data-month="{prev_month}" data-year="{prev_year}">&lt;</button>
                <span class="calendar-title">{month_name} {year}</span>
                <button type="button" class="calendar-nav" data-direction="next" data-month="{next_month}" data-year="{next_year}">&gt;</button>
            </div>
            <table class="calendar-table">
                <thead><tr>{days_html}</tr></thead>
                <tbody>{weeks_html}</tbody>
            </table>
        </div>'''
    
    def generate_js_code(self) -> str:
        """Generate JavaScript for date picker."""
        config = self.to_dict()
        return f"""
        // Date Picker
        (function() {{
            const config = {str(config).replace("'", '"')};
            
            const container = document.querySelector('.date-picker-container');
            if (!container) return;
            
            const input = container.querySelector('.date-picker-input');
            const toggle = container.querySelector('.date-picker-toggle');
            const dropdown = container.querySelector('.date-picker-dropdown');
            
            if (toggle && dropdown) {{
                toggle.addEventListener('click', () => {{
                    dropdown.classList.toggle('open');
                }});
                
                document.addEventListener('click', (e) => {{
                    if (!container.contains(e.target)) {{
                        dropdown.classList.remove('open');
                    }}
                }});
            }}
            
            // Calendar navigation
            container.querySelectorAll('.calendar-nav').forEach(btn => {{
                btn.addEventListener('click', () => {{
                    const month = parseInt(btn.dataset.month);
                    const year = parseInt(btn.dataset.year);
                    console.log('Navigate to:', year, month);
                }});
            }});
            
            // Day selection
            container.querySelectorAll('.calendar-day:not(.disabled):not(.empty)').forEach(day => {{
                day.addEventListener('click', () => {{
                    const date = day.dataset.date;
                    if (input) {{
                        input.value = date;
                    }}
                    container.querySelectorAll('.calendar-day.selected').forEach(d => d.classList.remove('selected'));
                    day.classList.add('selected');
                    dropdown.classList.remove('open');
                    console.log('Selected:', date);
                }});
            }});
            
            // Preset selection
            container.querySelectorAll('.preset-btn').forEach(btn => {{
                btn.addEventListener('click', () => {{
                    const value = btn.dataset.value;
                    console.log('Preset selected:', value);
                }});
            }});
        }})();
        """


def create_date_picker(name: str = "date", placeholder: str = "Select date", mode: PickerMode = PickerMode.DATE) -> DatePicker:
    """Create a date picker."""
    return DatePicker(name, placeholder, mode)


def create_date_range_picker(start_name: str = "start_date", end_name: str = "end_date") -> tuple:
    """Create a date range picker pair."""
    start = DatePicker(start_name, "Start date")
    end = DatePicker(end_name, "End date")
    return start, end


DATE_PICKER_CSS = """
.date-picker-container {
    position: relative;
    display: inline-block;
    width: 100%;
}

.date-picker-label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: 500;
    color: #374151;
}

.date-picker-input-wrapper {
    position: relative;
    display: flex;
}

.date-picker-input {
    width: 100%;
    padding: 0.5rem 2.5rem 0.5rem 0.75rem;
    border: 1px solid #d1d5db;
    border-radius: 0.375rem;
    font-size: 1rem;
    background-color: white;
}

.date-picker-input:focus {
    outline: none;
    border-color: #3b82f6;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.date-picker-input:disabled {
    background-color: #f3f4f6;
    cursor: not-allowed;
}

.date-picker-toggle {
    position: absolute;
    right: 0;
    top: 0;
    bottom: 0;
    padding: 0 0.75rem;
    background: transparent;
    border: none;
    border-left: 1px solid #e5e7eb;
    cursor: pointer;
    color: #6b7280;
}

.date-picker-toggle:hover {
    color: #374151;
    background-color: #f9fafb;
}

.date-picker-dropdown {
    display: none;
    position: absolute;
    top: 100%;
    left: 0;
    z-index: 50;
    margin-top: 0.25rem;
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 0.5rem;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.date-picker-dropdown.open {
    display: block;
}

.date-picker-help {
    margin-top: 0.25rem;
    font-size: 0.875rem;
    color: #6b7280;
}

.date-picker-error {
    margin-top: 0.25rem;
    font-size: 0.875rem;
    color: #dc2626;
}

.date-picker-error-state .date-picker-input {
    border-color: #dc2626;
}

.calendar {
    padding: 1rem;
    min-width: 280px;
}

.calendar-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;
}

.calendar-title {
    font-weight: 600;
    color: #111827;
}

.calendar-nav {
    padding: 0.25rem 0.5rem;
    border: none;
    background: #f3f4f6;
    border-radius: 0.25rem;
    cursor: pointer;
    color: #374151;
}

.calendar-nav:hover {
    background: #e5e7eb;
}

.calendar-table {
    width: 100%;
    border-collapse: collapse;
}

.calendar-weekday {
    padding: 0.5rem;
    text-align: center;
    font-size: 0.75rem;
    color: #6b7280;
    font-weight: 500;
}

.calendar-day {
    padding: 0.5rem;
    text-align: center;
    cursor: pointer;
    border-radius: 0.375rem;
}

.calendar-day:hover:not(.disabled):not(.empty) {
    background-color: #f3f4f6;
}

.calendar-day.today {
    font-weight: 600;
    color: #3b82f6;
}

.calendar-day.selected {
    background-color: #3b82f6;
    color: white;
}

.calendar-day.selected:hover {
    background-color: #2563eb;
}

.calendar-day.disabled {
    color: #d1d5db;
    cursor: not-allowed;
}

.calendar-day.weekend {
    color: #6b7280;
}

.date-picker-presets {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin-top: 0.5rem;
}

.preset-btn {
    padding: 0.375rem 0.75rem;
    border: 1px solid #d1d5db;
    background: white;
    border-radius: 0.375rem;
    font-size: 0.875rem;
    cursor: pointer;
}

.preset-btn:hover {
    background: #f9fafb;
    border-color: #9ca3af;
}

.preset-btn.active {
    background: #3b82f6;
    color: white;
    border-color: #3b82f6;
}

.date-picker-small .date-picker-input {
    padding: 0.375rem 2rem 0.375rem 0.5rem;
    font-size: 0.875rem;
}

.date-picker-large .date-picker-input {
    padding: 0.625rem 3rem 0.625rem 1rem;
    font-size: 1.125rem;
}

.date-picker-inline .date-picker-dropdown {
    display: block;
    position: static;
    box-shadow: none;
    border: none;
}
"""
