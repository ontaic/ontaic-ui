"""Calendar and scheduler component."""
import calendar
from datetime import datetime, timedelta
from typing import Any, Callable, Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum


class CalendarView(str, Enum):
    """Calendar view modes."""
    MONTH = "month"
    WEEK = "week"
    DAY = "day"
    YEAR = "year"
    AGENDA = "agenda"


class EventColor(str, Enum):
    """Event colors."""
    BLUE = "blue"
    GREEN = "green"
    RED = "red"
    YELLOW = "yellow"
    PURPLE = "purple"
    PINK = "pink"
    GRAY = "gray"


@dataclass
class CalendarEvent:
    """Calendar event."""
    id: str
    title: str
    start: datetime
    end: datetime
    description: str = ""
    location: str = ""
    color: EventColor = EventColor.BLUE
    all_day: bool = False
    recurring: bool = False
    recurrence_rule: str = ""
    attendees: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    @property
    def duration_hours(self) -> float:
        """Get duration in hours."""
        delta = self.end - self.start
        return delta.total_seconds() / 3600
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "start": self.start.isoformat(),
            "end": self.end.isoformat(),
            "description": self.description,
            "location": self.location,
            "color": self.color.value,
            "allDay": self.all_day,
            "recurring": self.recurring,
            "recurrenceRule": self.recurrence_rule,
            "attendees": self.attendees,
            "metadata": self.metadata,
        }


@dataclass
class CalendarSlot:
    """Time slot for scheduling."""
    start: datetime
    end: datetime
    available: bool = True
    event: Optional[CalendarEvent] = None
    
    def to_dict(self) -> dict:
        return {
            "start": self.start.isoformat(),
            "end": self.end.isoformat(),
            "available": self.available,
            "event": self.event.to_dict() if self.event else None,
        }


class Calendar:
    """Calendar component with event support."""
    
    def __init__(self, name: str = "calendar"):
        self.name = name
        self._view: CalendarView = CalendarView.MONTH
        self._date: datetime = datetime.now()
        self._events: List[CalendarEvent] = []
        self._selected_date: Optional[datetime] = None
        self._selected_dates: List[datetime] = []
        self._first_day_of_week: int = 0
        self._show_other_months: bool = True
        self._show_week_numbers: bool = False
        self._min_date: Optional[datetime] = None
        self._max_date: Optional[datetime] = None
        self._disabled_dates: List[datetime] = []
        self._on_date_select: Optional[Callable] = None
        self._on_event_click: Optional[Callable] = None
        self._on_event_create: Optional[Callable] = None
        self._on_event_update: Optional[Callable] = None
        self._on_event_delete: Optional[Callable] = None
        self._on_view_change: Optional[Callable] = None
        self._class_name: str = ""
        self._label: str = ""
        self._help_text: str = ""
        self._selectable: bool = True
        self._multi_select: bool = False
        self._readonly: bool = False
        self._height: int = 600
        self._slot_duration: int = 30
        self._business_hours: Tuple[int, int] = (9, 17)
        self._weekends: bool = True
    
    @property
    def current_date(self) -> datetime:
        return self._date
    
    def view(self, view: CalendarView) -> "Calendar":
        """Set calendar view."""
        self._view = view
        return self
    
    def date(self, date: datetime) -> "Calendar":
        """Set current date."""
        self._date = date
        return self
    
    def add_event(self, event: CalendarEvent) -> "Calendar":
        """Add an event."""
        self._events.append(event)
        return self
    
    def event(self, id: str, title: str, start: datetime, end: datetime, **kwargs) -> "Calendar":
        """Add an event."""
        e = CalendarEvent(id=id, title=title, start=start, end=end, **kwargs)
        self._events.append(e)
        return self
    
    def remove_event(self, event_id: str):
        """Remove an event."""
        self._events = [e for e in self._events if e.id != event_id]
    
    def on_date_select(self, callback: Callable) -> "Calendar":
        """Set date select handler."""
        self._on_date_select = callback
        return self
    
    def on_event_click(self, callback: Callable) -> "Calendar":
        """Set event click handler."""
        self._on_event_click = callback
        return self
    
    def on_event_create(self, callback: Callable) -> "Calendar":
        """Set event create handler."""
        self._on_event_create = callback
        return self
    
    def class_name(self, class_name: str) -> "Calendar":
        """Set CSS class."""
        self._class_name = class_name
        return self
    
    def label(self, label: str) -> "Calendar":
        """Set label."""
        self._label = label
        return self
    
    def selectable(self, selectable: bool = True) -> "Calendar":
        """Make selectable."""
        self._selectable = selectable
        return self
    
    def multi_select(self, multi: bool = True) -> "Calendar":
        """Enable multi-select."""
        self._multi_select = multi
        return self
    
    def readonly(self) -> "Calendar":
        """Make readonly."""
        self._readonly = True
        return self
    
    def height(self, height: int) -> "Calendar":
        """Set height."""
        self._height = height
        return self
    
    def slot_duration(self, minutes: int) -> "Calendar":
        """Set slot duration in minutes."""
        self._slot_duration = minutes
        return self
    
    def business_hours(self, start: int, end: int) -> "Calendar":
        """Set business hours."""
        self._business_hours = (start, end)
        return self
    
    def weekends(self, show: bool = True) -> "Calendar":
        """Toggle weekends."""
        self._weekends = show
        return self
    
    def get_events_for_date(self, date: datetime) -> List[CalendarEvent]:
        """Get events for a specific date."""
        return [e for e in self._events if e.start.date() == date.date()]
    
    def get_events_for_range(self, start: datetime, end: datetime) -> List[CalendarEvent]:
        """Get events for a date range."""
        return [e for e in self._events if e.start >= start and e.start <= end]
    
    def get_slots_for_date(self, date: datetime) -> List[CalendarSlot]:
        """Get time slots for a date."""
        slots = []
        current = datetime(date.year, date.month, date.day, self._business_hours[0])
        end_time = datetime(date.year, date.month, date.day, self._business_hours[1])
        
        while current < end_time:
            slot_end = current + timedelta(minutes=self._slot_duration)
            events = [e for e in self._events if e.start <= current < e.end or e.start < slot_end <= e.end]
            
            slots.append(CalendarSlot(
                start=current,
                end=slot_end,
                available=len(events) == 0,
                event=events[0] if events else None,
            ))
            
            current = slot_end
        
        return slots
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "view": self._view.value,
            "date": self._date.isoformat(),
            "events": [e.to_dict() for e in self._events],
            "selectedDate": self._selected_date.isoformat() if self._selected_date else None,
            "firstDayOfWeek": self._first_day_of_week,
            "showOtherMonths": self._show_other_months,
            "showWeekNumbers": self._show_week_numbers,
            "minDate": self._min_date.isoformat() if self._min_date else None,
            "maxDate": self._max_date.isoformat() if self._max_date else None,
            "selectable": self._selectable,
            "multiSelect": self._multi_select,
            "readonly": self._readonly,
            "height": self._height,
            "slotDuration": self._slot_duration,
            "businessHours": self._business_hours,
            "weekends": self._weekends,
            "className": self._class_name,
            "label": self._label,
        }
    
    def to_html(self) -> str:
        """Generate HTML."""
        label_html = f'<h3 class="calendar-label">{self._label}</h3>' if self._label else ""
        class_attr = f" {self._class_name}" if self._class_name else ""
        
        # View buttons
        views_html = f'''<div class="calendar-views">
            <button type="button" class="calendar-view-btn{' active' if self._view == CalendarView.MONTH else ''}" data-view="month">Month</button>
            <button type="button" class="calendar-view-btn{' active' if self._view == CalendarView.WEEK else ''}" data-view="week">Week</button>
            <button type="button" class="calendar-view-btn{' active' if self._view == CalendarView.DAY else ''}" data-view="day">Day</button>
            <button type="button" class="calendar-view-btn{' active' if self._view == CalendarView.AGENDA else ''}" data-view="agenda">Agenda</button>
        </div>'''
        
        # Navigation
        nav_html = f'''<div class="calendar-nav">
            <button type="button" class="calendar-nav-btn" data-action="prev">&lt;</button>
            <span class="calendar-title">{self._date.strftime("%B %Y")}</span>
            <button type="button" class="calendar-nav-btn" data-action="next">&gt;</button>
            <button type="button" class="calendar-today-btn">Today</button>
        </div>'''
        
        # Calendar grid
        if self._view == CalendarView.MONTH:
            calendar_html = self._render_month_view()
        elif self._view == CalendarView.WEEK:
            calendar_html = self._render_week_view()
        elif self._view == CalendarView.DAY:
            calendar_html = self._render_day_view()
        else:
            calendar_html = self._render_agenda_view()
        
        help_html = f'<p class="calendar-help">{self._help_text}</p>' if hasattr(self, '_help_text') and self._help_text else ""
        
        return f'''<div class="calendar{class_attr}" style="height: {self._height}px;">
            {label_html}
            <div class="calendar-header">
                {nav_html}
                {views_html}
            </div>
            <div class="calendar-body">
                {calendar_html}
            </div>
            {help_html}
        </div>'''
    
    def _render_month_view(self) -> str:
        """Render month view."""
        year = self._date.year
        month = self._date.month
        
        # Header
        days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
        header = "".join(f'<div class="calendar-weekday">{d}</div>' for d in days)
        
        # Calendar days
        cal = calendar.monthcalendar(year, month)
        cells = ""
        
        for week in cal:
            for day in week:
                if day == 0:
                    cells += '<div class="calendar-day empty"></div>'
                    continue
                
                date = datetime(year, month, day)
                is_today = date.date() == datetime.now().date()
                is_selected = self._selected_date and date.date() == self._selected_date.date()
                events = self.get_events_for_date(date)
                
                classes = ["calendar-day"]
                if is_today:
                    classes.append("today")
                if is_selected:
                    classes.append("selected")
                
                events_html = ""
                for e in events[:3]:
                    events_html += f'<div class="calendar-event event-{e.color.value}" data-event-id="{e.id}">{e.title}</div>'
                if len(events) > 3:
                    events_html += f'<div class="calendar-more">+{len(events) - 3} more</div>'
                
                cells += f'''<div class="{' '.join(classes)}" data-date="{date.isoformat()}">
                    <span class="day-number">{day}</span>
                    <div class="day-events">{events_html}</div>
                </div>'''
        
        return f'<div class="calendar-month"><div class="calendar-weekdays">{header}</div><div class="calendar-days">{cells}</div></div>'
    
    def _render_week_view(self) -> str:
        """Render week view."""
        # Week header
        start_of_week = self._date - timedelta(days=self._date.weekday())
        header = ""
        for i in range(7):
            day = start_of_week + timedelta(days=i)
            is_today = day.date() == datetime.now().date()
            header += f'<div class="calendar-week-header{" today" if is_today else ""}"><span class="day-name">{day.strftime("%a")}</span><span class="day-num">{day.day}</span></div>'
        
        # Time slots
        slots = ""
        for hour in range(self._business_hours[0], self._business_hours[1]):
            slots += f'<div class="calendar-time-slot"><span class="time-label">{hour}:00</span></div>'
        
        return f'<div class="calendar-week"><div class="calendar-week-header-row">{header}</div><div class="calendar-time-grid">{slots}</div></div>'
    
    def _render_day_view(self) -> str:
        """Render day view."""
        slots = ""
        for hour in range(self._business_hours[0], self._business_hours[1]):
            events = [e for e in self._events if e.start.hour == hour]
            events_html = ""
            for e in events:
                events_html += f'<div class="calendar-event event-{e.color.value}" data-event-id="{e.id}">{e.title}</div>'
            slots += f'<div class="calendar-time-slot"><span class="time-label">{hour}:00</span><div class="slot-events">{events_html}</div></div>'
        
        return f'<div class="calendar-day-view"><div class="calendar-day-title">{self._date.strftime("%A, %B %d, %Y")}</div><div class="calendar-time-grid">{slots}</div></div>'
    
    def _render_agenda_view(self) -> str:
        """Render agenda view."""
        events = sorted(self._events, key=lambda e: e.start)
        
        if not events:
            return '<div class="calendar-agenda empty">No events scheduled</div>'
        
        items = ""
        current_date = None
        
        for e in events:
            if current_date != e.start.date():
                current_date = e.start.date()
                items += f'<div class="agenda-date">{current_date.strftime("%A, %B %d, %Y")}</div>'
            
            time_str = "All Day" if e.all_day else e.start.strftime("%I:%M %p")
            items += f'''<div class="agenda-event event-{e.color.value}" data-event-id="{e.id}">
                <span class="event-time">{time_str}</span>
                <span class="event-title">{e.title}</span>
                {f'<span class="event-location">{e.location}</span>' if e.location else ''}
            </div>'''
        
        return f'<div class="calendar-agenda">{items}</div>'
    
    def generate_js_code(self) -> str:
        """Generate JavaScript."""
        config = self.to_dict()
        return f"""
        // Calendar
        (function() {{
            const config = {str(config).replace("'", '"')};
            
            const calendar = document.querySelector('.calendar');
            if (!calendar) return;
            
            let currentDate = new Date(config.date);
            let currentView = config.view;
            
            // Navigation
            calendar.querySelectorAll('.calendar-nav-btn').forEach(btn => {{
                btn.addEventListener('click', () => {{
                    const action = btn.dataset.action;
                    if (action === 'prev') {{
                        currentDate.setMonth(currentDate.getMonth() - 1);
                    }} else if (action === 'next') {{
                        currentDate.setMonth(currentDate.getMonth() + 1);
                    }}
                    updateCalendar();
                }});
            }});
            
            calendar.querySelector('.calendar-today-btn')?.addEventListener('click', () => {{
                currentDate = new Date();
                updateCalendar();
            }});
            
            // View switching
            calendar.querySelectorAll('.calendar-view-btn').forEach(btn => {{
                btn.addEventListener('click', () => {{
                    calendar.querySelectorAll('.calendar-view-btn').forEach(b => b.classList.remove('active'));
                    btn.classList.add('active');
                    currentView = btn.dataset.view;
                    updateCalendar();
                }});
            }});
            
            // Day click
            calendar.querySelectorAll('.calendar-day:not(.empty)').forEach(day => {{
                day.addEventListener('click', () => {{
                    const date = day.dataset.date;
                    console.log('Date selected:', date);
                }});
            }});
            
            // Event click
            calendar.querySelectorAll('.calendar-event').forEach(event => {{
                event.addEventListener('click', (e) => {{
                    e.stopPropagation();
                    const eventId = event.dataset.eventId;
                    console.log('Event clicked:', eventId);
                }});
            }});
            
            function updateCalendar() {{
                console.log('Calendar updated:', currentDate, currentView);
            }}
        }})();
        """


def create_calendar(name: str = "calendar") -> Calendar:
    """Create a calendar."""
    return Calendar(name)


def calendar_event(id: str, title: str, start: datetime, end: datetime, **kwargs) -> CalendarEvent:
    """Create a calendar event."""
    return CalendarEvent(id=id, title=title, start=start, end=end, **kwargs)


CALENDAR_CSS = """
.calendar {
    border: 1px solid #e5e7eb;
    border-radius: 0.5rem;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    background: white;
}

.calendar-label {
    padding: 1rem;
    margin: 0;
    font-size: 1.25rem;
    font-weight: 600;
    color: #111827;
}

.calendar-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem;
    border-bottom: 1px solid #e5e7eb;
}

.calendar-nav {
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.calendar-nav-btn {
    width: 32px;
    height: 32px;
    display: flex;
    align-items: center;
    justify-content: center;
    border: 1px solid #d1d5db;
    background: white;
    border-radius: 0.375rem;
    cursor: pointer;
}

.calendar-nav-btn:hover {
    background: #f9fafb;
}

.calendar-title {
    font-weight: 600;
    color: #111827;
    min-width: 150px;
    text-align: center;
}

.calendar-today-btn {
    padding: 0.375rem 0.75rem;
    border: 1px solid #d1d5db;
    background: white;
    border-radius: 0.375rem;
    cursor: pointer;
}

.calendar-today-btn:hover {
    background: #f9fafb;
}

.calendar-views {
    display: flex;
    gap: 0.25rem;
}

.calendar-view-btn {
    padding: 0.375rem 0.75rem;
    border: 1px solid #d1d5db;
    background: white;
    border-radius: 0.375rem;
    cursor: pointer;
}

.calendar-view-btn.active {
    background: #3b82f6;
    color: white;
    border-color: #3b82f6;
}

.calendar-body {
    flex: 1;
    overflow: auto;
}

.calendar-weekdays {
    display: grid;
    grid-template-columns: repeat(7, 1fr);
    border-bottom: 1px solid #e5e7eb;
}

.calendar-weekday {
    padding: 0.75rem;
    text-align: center;
    font-weight: 500;
    color: #6b7280;
    font-size: 0.875rem;
}

.calendar-days {
    display: grid;
    grid-template-columns: repeat(7, 1fr);
}

.calendar-day {
    min-height: 100px;
    padding: 0.5rem;
    border: 1px solid #e5e7eb;
    cursor: pointer;
}

.calendar-day:hover {
    background: #f9fafb;
}

.calendar-day.today {
    background: #eff6ff;
}

.calendar-day.selected {
    background: #dbeafe;
}

.calendar-day.empty {
    background: #f9fafb;
    cursor: default;
}

.day-number {
    font-weight: 500;
    color: #374151;
}

.calendar-event {
    padding: 0.125rem 0.375rem;
    margin-top: 0.25rem;
    border-radius: 0.25rem;
    font-size: 0.75rem;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    cursor: pointer;
}

.event-blue { background: #dbeafe; color: #1e40af; }
.event-green { background: #d1fae5; color: #065f46; }
.event-red { background: #fee2e2; color: #991b1b; }
.event-yellow { background: #fef3c7; color: #92400e; }
.event-purple { background: #ede9fe; color: #5b21b6; }
.event-pink { background: #fce7f3; color: #9d174d; }
.event-gray { background: #f3f4f6; color: #374151; }

.calendar-more {
    font-size: 0.75rem;
    color: #6b7280;
    padding: 0.125rem 0.375rem;
}

.calendar-agenda {
    padding: 1rem;
}

.calendar-agenda.empty {
    text-align: center;
    color: #9ca3af;
}

.agenda-date {
    font-weight: 600;
    color: #374151;
    padding: 0.5rem 0;
    border-bottom: 1px solid #e5e7eb;
}

.agenda-event {
    display: flex;
    gap: 1rem;
    padding: 0.75rem;
    border-radius: 0.375rem;
    margin: 0.5rem 0;
    cursor: pointer;
}

.agenda-event:hover {
    opacity: 0.9;
}

.event-time {
    color: #6b7280;
    font-size: 0.875rem;
}

.event-title {
    font-weight: 500;
}

.event-location {
    color: #6b7280;
    font-size: 0.875rem;
}

.calendar-week-header-row {
    display: grid;
    grid-template-columns: repeat(7, 1fr);
    border-bottom: 1px solid #e5e7eb;
}

.calendar-week-header {
    padding: 0.75rem;
    text-align: center;
}

.calendar-week-header.today {
    background: #eff6ff;
}

.day-name {
    display: block;
    font-size: 0.75rem;
    color: #6b7280;
}

.day-num {
    display: block;
    font-size: 1.25rem;
    font-weight: 600;
    color: #111827;
}

.calendar-time-grid {
    display: flex;
    flex-direction: column;
}

.calendar-time-slot {
    display: flex;
    align-items: flex-start;
    min-height: 60px;
    border-bottom: 1px solid #e5e7eb;
}

.time-label {
    width: 60px;
    padding: 0.5rem;
    font-size: 0.75rem;
    color: #6b7280;
}

.slot-events {
    flex: 1;
    padding: 0.25rem;
}

.calendar-day-view {
    padding: 1rem;
}

.calendar-day-title {
    font-weight: 600;
    color: #111827;
    margin-bottom: 1rem;
}
"""
