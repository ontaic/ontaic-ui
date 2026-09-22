"""Advanced notification and toast system."""
import time
import uuid
from typing import Any, Callable, Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum


class NotificationType(str, Enum):
    """Notification types."""
    SUCCESS = "success"
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


class NotificationPosition(str, Enum):
    """Notification position."""
    TOP_RIGHT = "top-right"
    TOP_LEFT = "top-left"
    TOP_CENTER = "top-center"
    BOTTOM_RIGHT = "bottom-right"
    BOTTOM_LEFT = "bottom-left"
    BOTTOM_CENTER = "bottom-center"
    TOP_FULL = "top-full"
    BOTTOM_FULL = "bottom-full"


class NotificationSize(str, Enum):
    """Notification size."""
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"


@dataclass
class NotificationAction:
    """Notification action button."""
    label: str
    onClick: Optional[Callable] = None
    url: Optional[str] = None
    style: str = ""
    
    def to_dict(self) -> dict:
        return {
            "label": self.label,
            "url": self.url,
            "style": self.style,
        }


@dataclass
class Notification:
    """Notification message."""
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    type: NotificationType = NotificationType.INFO
    title: str = ""
    message: str = ""
    duration: float = 5000
    position: NotificationPosition = NotificationPosition.TOP_RIGHT
    size: NotificationSize = NotificationSize.MEDIUM
    icon: str = ""
    actions: List[NotificationAction] = field(default_factory=list)
    closable: bool = True
    progress: bool = False
    pause_on_hover: bool = True
    show_icon: bool = True
    show_close: bool = True
    show_progress: bool = False
    custom_class: str = ""
    data: Dict[str, Any] = field(default_factory=dict)
    created_at: float = field(default_factory=time.time)
    _timeout: Optional[float] = None
    _paused: bool = False
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "type": self.type.value,
            "title": self.title,
            "message": self.message,
            "duration": self.duration,
            "position": self.position.value,
            "size": self.size.value,
            "icon": self.icon,
            "actions": [a.to_dict() for a in self.actions],
            "closable": self.closable,
            "progress": self.progress,
            "pauseOnHover": self.pause_on_hover,
            "showIcon": self.show_icon,
            "showClose": self.show_close,
            "showProgress": self.show_progress,
            "customClass": self.custom_class,
            "data": self.data,
        }
    
    @classmethod
    def success(cls, message: str, title: str = "", **kwargs) -> "Notification":
        """Create success notification."""
        return cls(type=NotificationType.SUCCESS, message=message, title=title or "Success", **kwargs)
    
    @classmethod
    def error(cls, message: str, title: str = "", **kwargs) -> "Notification":
        """Create error notification."""
        return cls(type=NotificationType.ERROR, message=message, title=title or "Error", duration=0, **kwargs)
    
    @classmethod
    def warning(cls, message: str, title: str = "", **kwargs) -> "Notification":
        """Create warning notification."""
        return cls(type=NotificationType.WARNING, message=message, title=title or "Warning", **kwargs)
    
    @classmethod
    def info(cls, message: str, title: str = "", **kwargs) -> "Notification":
        """Create info notification."""
        return cls(type=NotificationType.INFO, message=message, title=title or "Info", **kwargs)


class NotificationManager:
    """Notification manager for handling toasts and notifications."""
    
    def __init__(self, position: NotificationPosition = NotificationPosition.TOP_RIGHT, max_notifications: int = 10):
        self.position = position
        self.max_notifications = max_notifications
        self._notifications: List[Notification] = []
        self._on_add: List[Callable] = []
        self._on_remove: List[Callable] = []
        self._on_clear: List[Callable] = []
    
    def add(self, notification: Notification) -> Notification:
        """Add a notification."""
        if len(self._notifications) >= self.max_notifications:
            oldest = self._notifications.pop(0)
            self._trigger_remove(oldest)
        
        notification.position = notification.position or self.position
        self._notifications.append(notification)
        self._trigger_add(notification)
        
        return notification
    
    def remove(self, notification_id: str):
        """Remove a notification."""
        for i, n in enumerate(self._notifications):
            if n.id == notification_id:
                removed = self._notifications.pop(i)
                self._trigger_remove(removed)
                break
    
    def clear(self):
        """Clear all notifications."""
        self._notifications.clear()
        self._trigger_clear()
    
    def success(self, message: str, title: str = "", **kwargs) -> Notification:
        """Show success notification."""
        return self.add(Notification.success(message, title, **kwargs))
    
    def error(self, message: str, title: str = "", **kwargs) -> Notification:
        """Show error notification."""
        return self.add(Notification.error(message, title, **kwargs))
    
    def warning(self, message: str, title: str = "", **kwargs) -> Notification:
        """Show warning notification."""
        return self.add(Notification.warning(message, title, **kwargs))
    
    def info(self, message: str, title: str = "", **kwargs) -> Notification:
        """Show info notification."""
        return self.add(Notification.info(message, title, **kwargs))
    
    def on_add(self, callback: Callable):
        """Register add callback."""
        self._on_add.append(callback)
    
    def on_remove(self, callback: Callable):
        """Register remove callback."""
        self._on_remove.append(callback)
    
    def on_clear(self, callback: Callable):
        """Register clear callback."""
        self._on_clear.append(callback)
    
    def _trigger_add(self, notification: Notification):
        """Trigger add callbacks."""
        for cb in self._on_add:
            cb(notification)
    
    def _trigger_remove(self, notification: Notification):
        """Trigger remove callbacks."""
        for cb in self._on_remove:
            cb(notification)
    
    def _trigger_clear(self):
        """Trigger clear callbacks."""
        for cb in self._on_clear:
            cb()
    
    def get_notifications(self) -> List[Notification]:
        """Get all notifications."""
        return self._notifications.copy()
    
    def get_count(self) -> int:
        """Get notification count."""
        return len(self._notifications)
    
    def generate_js_code(self) -> str:
        """Generate JavaScript for notification system."""
        return """
        // Notification Manager
        const notificationManager = {
            notifications: [],
            position: 'top-right',
            maxNotifications: 10,
            
            init(config = {}) {
                this.position = config.position || 'top-right';
                this.maxNotifications = config.maxNotifications || 10;
                this.createContainer();
            },
            
            createContainer() {
                const existing = document.querySelector('.notification-container');
                if (existing) return;
                
                const container = document.createElement('div');
                container.className = 'notification-container notification-' + this.position;
                document.body.appendChild(container);
            },
            
            show(options) {
                const id = 'notif-' + Math.random().toString(36).substr(2, 9);
                const notification = {
                    id,
                    type: options.type || 'info',
                    title: options.title || '',
                    message: options.message || '',
                    duration: options.duration !== undefined ? options.duration : 5000,
                    closable: options.closable !== false,
                    icon: options.icon || '',
                    actions: options.actions || [],
                    progress: options.progress || false,
                    pauseOnHover: options.pauseOnHover !== false,
                };
                
                this.notifications.push(notification);
                
                if (this.notifications.length > this.maxNotifications) {
                    this.remove(this.notifications[0].id);
                }
                
                this.render(notification);
                
                if (notification.duration > 0) {
                    this.startTimer(notification);
                }
                
                return id;
            },
            
            render(notification) {
                const container = document.querySelector('.notification-container');
                if (!container) return;
                
                const el = document.createElement('div');
                el.className = 'notification notification-' + notification.type;
                el.id = notification.id;
                
                const icon = this.getIcon(notification.type);
                
                el.innerHTML = `
                    <div class="notification-content">
                        ${notification.showIcon !== false ? `<div class="notification-icon">${notification.icon || icon}</div>` : ''}
                        <div class="notification-body">
                            ${notification.title ? `<div class="notification-title">${notification.title}</div>` : ''}
                            <div class="notification-message">${notification.message}</div>
                        </div>
                        ${notification.closable ? '<button class="notification-close">&times;</button>' : ''}
                    </div>
                    ${notification.duration > 0 ? '<div class="notification-progress"></div>' : ''}
                `;
                
                if (notification.closable) {
                    el.querySelector('.notification-close').addEventListener('click', () => {
                        this.remove(notification.id);
                    });
                }
                
                if (notification.pauseOnHover && notification.duration > 0) {
                    el.addEventListener('mouseenter', () => this.pauseTimer(notification));
                    el.addEventListener('mouseleave', () => this.resumeTimer(notification));
                }
                
                container.appendChild(el);
                
                requestAnimationFrame(() => el.classList.add('show'));
            },
            
            getIcon(type) {
                const icons = {
                    success: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>',
                    error: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><line x1="15" y1="9" x2="9" y2="15"></line><line x1="9" y1="9" x2="15" y2="15"></line></svg>',
                    warning: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path><line x1="12" y1="9" x2="12" y2="13"></line><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>',
                    info: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="16" x2="12" y2="12"></line><line x1="12" y1="8" x2="12.01" y2="8"></line></svg>',
                };
                return icons[type] || icons.info;
            },
            
            remove(id) {
                const el = document.getElementById(id);
                if (el) {
                    el.classList.remove('show');
                    el.classList.add('hide');
                    setTimeout(() => el.remove(), 300);
                }
                this.notifications = this.notifications.filter(n => n.id !== id);
            },
            
            clear() {
                document.querySelectorAll('.notification').forEach(el => {
                    el.classList.remove('show');
                    el.classList.add('hide');
                    setTimeout(() => el.remove(), 300);
                });
                this.notifications = [];
            },
            
            startTimer(notification) {
                const el = document.getElementById(notification.id);
                if (!el) return;
                
                const progressBar = el.querySelector('.notification-progress');
                if (progressBar) {
                    progressBar.style.transition = 'width ' + notification.duration + 'ms linear';
                    requestAnimationFrame(() => progressBar.style.width = '0%');
                }
                
                notification._timeout = setTimeout(() => {
                    this.remove(notification.id);
                }, notification.duration);
            },
            
            pauseTimer(notification) {
                if (notification._timeout) {
                    clearTimeout(notification._timeout);
                    notification._timeout = null;
                    const el = document.getElementById(notification.id);
                    if (el) {
                        el.classList.add('paused');
                    }
                }
            },
            
            resumeTimer(notification) {
                const el = document.getElementById(notification.id);
                if (el) {
                    el.classList.remove('paused');
                }
                if (notification.duration > 0 && !notification._timeout) {
                    this.startTimer(notification);
                }
            },
            
            success(message, options = {}) {
                return this.show({ ...options, type: 'success', message });
            },
            
            error(message, options = {}) {
                return this.show({ ...options, type: 'error', message, duration: 0 });
            },
            
            warning(message, options = {}) {
                return this.show({ ...options, type: 'warning', message });
            },
            
            info(message, options = {}) {
                return this.show({ ...options, type: 'info', message });
            }
        };
        
        notificationManager.init();
        """


def create_notification_manager(position: NotificationPosition = NotificationPosition.TOP_RIGHT, max_notifications: int = 10) -> NotificationManager:
    """Create a notification manager."""
    return NotificationManager(position, max_notifications)


def notify_success(message: str, title: str = "", **kwargs) -> Notification:
    """Show success notification."""
    return Notification.success(message, title, **kwargs)


def notify_error(message: str, title: str = "", **kwargs) -> Notification:
    """Show error notification."""
    return Notification.error(message, title, **kwargs)


def notify_warning(message: str, title: str = "", **kwargs) -> Notification:
    """Show warning notification."""
    return Notification.warning(message, title, **kwargs)


def notify_info(message: str, title: str = "", **kwargs) -> Notification:
    """Show info notification."""
    return Notification.info(message, title, **kwargs)


NOTIFICATION_CSS = """
.notification-container {
    position: fixed;
    z-index: 9999;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    max-height: 100vh;
    overflow: hidden;
    pointer-events: none;
}

.notification-container > * {
    pointer-events: auto;
}

.notification-top-right {
    top: 1rem;
    right: 1rem;
    align-items: flex-end;
}

.notification-top-left {
    top: 1rem;
    left: 1rem;
    align-items: flex-start;
}

.notification-top-center {
    top: 1rem;
    left: 50%;
    transform: translateX(-50%);
    align-items: center;
}

.notification-bottom-right {
    bottom: 1rem;
    right: 1rem;
    align-items: flex-end;
    flex-direction: column-reverse;
}

.notification-bottom-left {
    bottom: 1rem;
    left: 1rem;
    align-items: flex-start;
    flex-direction: column-reverse;
}

.notification-bottom-center {
    bottom: 1rem;
    left: 50%;
    transform: translateX(-50%);
    align-items: center;
    flex-direction: column-reverse;
}

.notification {
    display: flex;
    flex-direction: column;
    min-width: 320px;
    max-width: 450px;
    background: white;
    border-radius: 0.5rem;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    overflow: hidden;
    transform: translateX(100%);
    opacity: 0;
    transition: all 0.3s ease;
}

.notification-top-left .notification,
.notification-bottom-left .notification {
    transform: translateX(-100%);
}

.notification-top-center .notification,
.notification-bottom-center .notification {
    transform: translateY(-100%);
}

.notification.show {
    transform: translateX(0) translateY(0);
    opacity: 1;
}

.notification.hide {
    transform: translateX(100%);
    opacity: 0;
}

.notification-top-left .notification.hide,
.notification-bottom-left .notification.hide {
    transform: translateX(-100%);
}

.notification-content {
    display: flex;
    align-items: flex-start;
    padding: 1rem;
    gap: 0.75rem;
}

.notification-icon {
    flex-shrink: 0;
    width: 24px;
    height: 24px;
}

.notification-icon svg {
    width: 100%;
    height: 100%;
}

.notification-success .notification-icon {
    color: #10b981;
}

.notification-error .notification-icon {
    color: #ef4444;
}

.notification-warning .notification-icon {
    color: #f59e0b;
}

.notification-info .notification-icon {
    color: #3b82f6;
}

.notification-body {
    flex: 1;
    min-width: 0;
}

.notification-title {
    font-weight: 600;
    color: #111827;
    margin-bottom: 0.25rem;
}

.notification-message {
    color: #6b7280;
    font-size: 0.875rem;
    line-height: 1.5;
}

.notification-close {
    flex-shrink: 0;
    width: 24px;
    height: 24px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: transparent;
    border: none;
    color: #9ca3af;
    cursor: pointer;
    font-size: 1.25rem;
    line-height: 1;
    border-radius: 0.25rem;
}

.notification-close:hover {
    background: #f3f4f6;
    color: #374151;
}

.notification-progress {
    height: 3px;
    background: currentColor;
    opacity: 0.2;
    width: 100%;
}

.notification-success .notification-progress {
    color: #10b981;
}

.notification-error .notification-progress {
    color: #ef4444;
}

.notification-warning .notification-progress {
    color: #f59e0b;
}

.notification-info .notification-progress {
    color: #3b82f6;
}

.notification.paused .notification-progress {
    transition: none !important;
}

/* Small size */
.notification-small .notification-content {
    padding: 0.75rem;
}

.notification-small .notification-title {
    font-size: 0.875rem;
}

.notification-small .notification-message {
    font-size: 0.8125rem;
}

/* Large size */
.notification-large .notification-content {
    padding: 1.25rem;
}

.notification-large .notification-title {
    font-size: 1rem;
}

.notification-large .notification-message {
    font-size: 0.9375rem;
}
"""
