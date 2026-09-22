"""Date and time utilities for ontaic."""
import time
from datetime import datetime, timedelta, timezone
from typing import Optional, Union
from dataclasses import dataclass
from enum import Enum


class DateFormat(str, Enum):
    """Common date formats."""
    SHORT = "MM/DD/YYYY"
    LONG = "MMMM D, YYYY"
    ISO = "YYYY-MM-DD"
    ISO_DATETIME = "YYYY-MM-DD HH:mm:ss"
    TIME_12 = "h:mm A"
    TIME_24 = "HH:mm"
    DATETIME_SHORT = "MM/DD/YY h:mm A"
    DATETIME_LONG = "MMMM D, YYYY h:mm A"


MONTHS = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

MONTHS_SHORT = [
    "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
]

WEEKDAYS = [
    "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"
]

WEEKDAYS_SHORT = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]

WEEKDAYS_MIN = ["Su", "Mo", "Tu", "We", "Th", "Fr", "Sa"]


@dataclass
class DateInfo:
    """Date information."""
    year: int
    month: int
    day: int
    hour: int = 0
    minute: int = 0
    second: int = 0
    weekday: int = 0
    timestamp: float = 0
    
    def to_datetime(self) -> datetime:
        """Convert to datetime."""
        return datetime(self.year, self.month, self.day, self.hour, self.minute, self.second)
    
    @classmethod
    def from_datetime(cls, dt: datetime) -> "DateInfo":
        """Create from datetime."""
        return cls(
            year=dt.year,
            month=dt.month,
            day=dt.day,
            hour=dt.hour,
            minute=dt.minute,
            second=dt.second,
            weekday=dt.weekday(),
            timestamp=dt.timestamp(),
        )
    
    @classmethod
    def now(cls) -> "DateInfo":
        """Get current date/time."""
        return cls.from_datetime(datetime.now())


class DateTime:
    """DateTime utility class."""
    
    def __init__(self, year: int = None, month: int = None, day: int = None, hour: int = None, minute: int = None, second: int = None):
        if year is None:
            now = datetime.now()
            year = now.year
            month = month or now.month
            day = day or now.day
            hour = hour if hour is not None else now.hour
            minute = minute if minute is not None else now.minute
            second = second if second is not None else now.second
        
        self._dt = datetime(year, month or 1, day or 1, hour or 0, minute or 0, second or 0)
    
    @property
    def year(self) -> int:
        return self._dt.year
    
    @property
    def month(self) -> int:
        return self._dt.month
    
    @property
    def day(self) -> int:
        return self._dt.day
    
    @property
    def hour(self) -> int:
        return self._dt.hour
    
    @property
    def minute(self) -> int:
        return self._dt.minute
    
    @property
    def second(self) -> int:
        return self._dt.second
    
    @property
    def weekday(self) -> int:
        return self._dt.weekday()
    
    @property
    def timestamp(self) -> float:
        return self._dt.timestamp()
    
    @property
    def days_in_month(self) -> int:
        """Get number of days in current month."""
        if self.month == 12:
            next_month = datetime(self.year + 1, 1, 1)
        else:
            next_month = datetime(self.year, self.month + 1, 1)
        return (next_month - datetime(self.year, self.month, 1)).days
    
    @property
    def is_leap_year(self) -> bool:
        """Check if year is a leap year."""
        return self.year % 4 == 0 and (self.year % 100 != 0 or self.year % 400 == 0)
    
    @property
    def day_of_year(self) -> int:
        """Get day of year."""
        return (self._dt - datetime(self.year, 1, 1)).days + 1
    
    def format(self, fmt: str) -> str:
        """Format date using format string."""
        replacements = {
            "YYYY": str(self.year),
            "YY": str(self.year)[-2:],
            "MMMM": MONTHS[self.month - 1],
            "MMM": MONTHS_SHORT[self.month - 1],
            "MM": f"{self.month:02d}",
            "M": str(self.month),
            "DD": f"{self.day:02d}",
            "D": str(self.day),
            "HH": f"{self.hour:02d}",
            "H": str(self.hour),
            "hh": f"{(self.hour % 12) or 12:02d}",
            "h": str((self.hour % 12) or 12),
            "mm": f"{self.minute:02d}",
            "m": str(self.minute),
            "ss": f"{self.second:02d}",
            "s": str(self.second),
            "A": "AM" if self.hour < 12 else "PM",
            "a": "am" if self.hour < 12 else "pm",
            "dddd": WEEKDAYS[self._dt.weekday()],
            "ddd": WEEKDAYS_SHORT[self._dt.weekday()],
            "dd": WEEKDAYS_MIN[self._dt.weekday()],
            "d": str(self._dt.weekday()),
        }
        
        result = fmt
        for key, value in replacements.items():
            result = result.replace(key, value)
        
        return result
    
    def to_iso(self) -> str:
        """Convert to ISO format."""
        return self._dt.isoformat()
    
    def to_timestamp(self) -> int:
        """Convert to Unix timestamp."""
        return int(self._dt.timestamp())
    
    def to_date_string(self) -> str:
        """Convert to date string (YYYY-MM-DD)."""
        return self._dt.strftime("%Y-%m-%d")
    
    def to_time_string(self) -> str:
        """Convert to time string (HH:MM:SS)."""
        return self._dt.strftime("%H:%M:%S")
    
    def to_datetime_string(self) -> str:
        """Convert to datetime string (YYYY-MM-DD HH:MM:SS)."""
        return self._dt.strftime("%Y-%m-%d %H:%M:%S")
    
    def add(self, days: int = 0, hours: int = 0, minutes: int = 0, seconds: int = 0) -> "DateTime":
        """Add time to date."""
        delta = timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)
        new_dt = self._dt + delta
        return DateTime.from_datetime(new_dt)
    
    def subtract(self, days: int = 0, hours: int = 0, minutes: int = 0, seconds: int = 0) -> "DateTime":
        """Subtract time from date."""
        delta = timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)
        new_dt = self._dt - delta
        return DateTime.from_datetime(new_dt)
    
    def diff(self, other: "DateTime") -> timedelta:
        """Calculate difference between dates."""
        return self._dt - other._dt
    
    def is_before(self, other: "DateTime") -> bool:
        """Check if date is before another."""
        return self._dt < other._dt
    
    def is_after(self, other: "DateTime") -> bool:
        """Check if date is after another."""
        return self._dt > other._dt
    
    def is_same_day(self, other: "DateTime") -> bool:
        """Check if dates are the same day."""
        return self._dt.date() == other._dt.date()
    
    def is_same_month(self, other: "DateTime") -> bool:
        """Check if dates are in the same month."""
        return self._dt.year == other._dt.year and self._dt.month == other._dt.month
    
    def start_of_day(self) -> "DateTime":
        """Get start of day."""
        return DateTime(self.year, self.month, self.day)
    
    def end_of_day(self) -> "DateTime":
        """Get end of day."""
        return DateTime(self.year, self.month, self.day, 23, 59, 59)
    
    def start_of_month(self) -> "DateTime":
        """Get start of month."""
        return DateTime(self.year, self.month, 1)
    
    def end_of_month(self) -> "DateTime":
        """Get end of month."""
        return DateTime(self.year, self.month, self.days_in_month, 23, 59, 59)
    
    def start_of_year(self) -> "DateTime":
        """Get start of year."""
        return DateTime(self.year, 1, 1)
    
    def end_of_year(self) -> "DateTime":
        """Get end of year."""
        return DateTime(self.year, 12, 31, 23, 59, 59)
    
    def is_weekend(self) -> bool:
        """Check if date is a weekend."""
        return self._dt.weekday() >= 5
    
    def is_workday(self) -> bool:
        """Check if date is a workday."""
        return self._dt.weekday() < 5
    
    def week_of_year(self) -> int:
        """Get week of year."""
        return self._dt.isocalendar()[1]
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "year": self.year,
            "month": self.month,
            "day": self.day,
            "hour": self.hour,
            "minute": self.minute,
            "second": self.second,
            "weekday": self.weekday,
            "timestamp": self.timestamp,
        }
    
    @classmethod
    def from_timestamp(cls, timestamp: float) -> "DateTime":
        """Create from timestamp."""
        dt = datetime.fromtimestamp(timestamp)
        return cls.from_datetime(dt)
    
    @classmethod
    def from_string(cls, date_string: str, fmt: str = None) -> "DateTime":
        """Create from string."""
        if fmt:
            dt = datetime.strptime(date_string, fmt)
        else:
            dt = datetime.fromisoformat(date_string)
        return cls.from_datetime(dt)
    
    @classmethod
    def from_dict(cls, data: dict) -> "DateTime":
        """Create from dictionary."""
        return cls(
            year=data.get("year"),
            month=data.get("month"),
            day=data.get("day"),
            hour=data.get("hour"),
            minute=data.get("minute"),
            second=data.get("second"),
        )
    
    @classmethod
    def now(cls) -> "DateTime":
        """Get current date/time."""
        return cls.from_datetime(datetime.now())
    
    @classmethod
    def today(cls) -> "DateTime":
        """Get today's date."""
        now = datetime.now()
        return cls(now.year, now.month, now.day)
    
    def __str__(self) -> str:
        return self.to_datetime_string()
    
    def __repr__(self) -> str:
        return f"DateTime({self.year}, {self.month}, {self.day}, {self.hour}, {self.minute}, {self.second})"


def now() -> DateTime:
    """Get current date/time."""
    return DateTime.now()


def today() -> DateTime:
    """Get today's date."""
    return DateTime.today()


def from_timestamp(timestamp: float) -> DateTime:
    """Create DateTime from timestamp."""
    return DateTime.from_timestamp(timestamp)


def from_string(date_string: str, fmt: str = None) -> DateTime:
    """Create DateTime from string."""
    return DateTime.from_string(date_string, fmt)


def format_date(dt: DateTime, fmt: str) -> str:
    """Format a DateTime."""
    return dt.format(fmt)


def format_relative(dt: DateTime) -> str:
    """Format date relative to now (e.g., '2 hours ago')."""
    now = DateTime.now()
    diff = now.diff(dt)
    
    seconds = int(diff.total_seconds())
    
    if seconds < 0:
        return "in the future"
    
    if seconds < 60:
        return "just now"
    
    minutes = seconds // 60
    if minutes < 60:
        return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
    
    hours = minutes // 60
    if hours < 24:
        return f"{hours} hour{'s' if hours > 1 else ''} ago"
    
    days = hours // 24
    if days < 7:
        return f"{days} day{'s' if days > 1 else ''} ago"
    
    if days < 30:
        weeks = days // 7
        return f"{weeks} week{'s' if weeks > 1 else ''} ago"
    
    if days < 365:
        months = days // 30
        return f"{months} month{'s' if months > 1 else ''} ago"
    
    years = days // 365
    return f"{years} year{'s' if years > 1 else ''} ago"


def time_ago(seconds: int) -> str:
    """Convert seconds to relative time string."""
    if seconds < 60:
        return "just now"
    
    minutes = seconds // 60
    if minutes < 60:
        return f"{minutes}m ago"
    
    hours = minutes // 60
    if hours < 24:
        return f"{hours}h ago"
    
    days = hours // 24
    if days < 7:
        return f"{days}d ago"
    
    weeks = days // 7
    if weeks < 4:
        return f"{weeks}w ago"
    
    months = days // 30
    if months < 12:
        return f"{months}mo ago"
    
    years = days // 365
    return f"{years}y ago"


def generate_calendar(year: int, month: int) -> list:
    """Generate a month calendar grid."""
    first_day = datetime(year, month, 1)
    last_day = datetime(year, month + 1, 1) - timedelta(days=1) if month < 12 else datetime(year, 12, 31)
    
    start_weekday = first_day.weekday()
    days_in_month = last_day.day
    
    calendar = []
    week = [None] * start_weekday
    
    for day in range(1, days_in_month + 1):
        week.append(day)
        if len(week) == 7:
            calendar.append(week)
            week = []
    
    if week:
        while len(week) < 7:
            week.append(None)
        calendar.append(week)
    
    return calendar


DATE_CSS = """
.date-picker {
    font-family: system-ui, -apple-system, sans-serif;
    border: 1px solid #e5e7eb;
    border-radius: 0.5rem;
    padding: 0.5rem;
    background: white;
}

.date-picker-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.5rem;
}

.date-picker-title {
    font-weight: 600;
    color: #111827;
}

.date-picker-nav {
    display: flex;
    gap: 0.25rem;
}

.date-picker-btn {
    padding: 0.25rem 0.5rem;
    border: none;
    background: #f3f4f6;
    border-radius: 0.25rem;
    cursor: pointer;
}

.date-picker-btn:hover {
    background: #e5e7eb;
}

.date-picker-weekdays {
    display: grid;
    grid-template-columns: repeat(7, 1fr);
    gap: 0.25rem;
    margin-bottom: 0.25rem;
}

.date-picker-weekday {
    text-align: center;
    font-size: 0.75rem;
    color: #6b7280;
    padding: 0.25rem;
}

.date-picker-days {
    display: grid;
    grid-template-columns: repeat(7, 1fr);
    gap: 0.25rem;
}

.date-picker-day {
    text-align: center;
    padding: 0.5rem;
    border-radius: 0.25rem;
    cursor: pointer;
}

.date-picker-day:hover {
    background: #f3f4f6;
}

.date-picker-day.selected {
    background: #3b82f6;
    color: white;
}

.date-picker-day.today {
    border: 2px solid #3b82f6;
}

.date-picker-day.other-month {
    color: #9ca3af;
}
"""
