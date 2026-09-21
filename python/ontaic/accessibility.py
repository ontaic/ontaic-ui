"""Accessibility features for ontaic."""
from typing import Any, Dict, List, Optional
from dataclasses import dataclass


@dataclass
class AriaAttributes:
    """ARIA attributes for accessibility."""
    label: str = ""
    labelledby: str = ""
    describedby: str = ""
    hidden: bool = False
    expanded: bool = False
    selected: bool = False
    checked: str = ""  # "true", "false", "mixed"
    disabled: bool = False
    required: bool = False
    invalid: bool = False
    live: str = ""  # "polite", "assertive", "off"
    atomic: bool = False
    busy: bool = False
    relevant: str = ""
    controls: str = ""
    owns: str = ""
    flowto: str = ""
    level: int = 0
    valuemin: float = 0
    valuemax: float = 0
    valuenow: float = 0
    orientation: str = ""  # "horizontal", "vertical"
    autocomplete: str = ""  # "inline", "list", "both", "none"
    multiSelectable: bool = False
    readOnly: bool = False
    
    def to_dict(self) -> Dict[str, str]:
        """Convert to HTML attributes."""
        attrs = {}
        
        if self.label:
            attrs["aria-label"] = self.label
        if self.labelledby:
            attrs["aria-labelledby"] = self.labelledby
        if self.describedby:
            attrs["aria-describedby"] = self.describedby
        if self.hidden:
            attrs["aria-hidden"] = "true"
        if self.expanded:
            attrs["aria-expanded"] = "true"
        if self.selected:
            attrs["aria-selected"] = "true"
        if self.checked:
            attrs["aria-checked"] = self.checked
        if self.disabled:
            attrs["aria-disabled"] = "true"
        if self.required:
            attrs["aria-required"] = "true"
        if self.invalid:
            attrs["aria-invalid"] = "true"
        if self.live:
            attrs["aria-live"] = self.live
        if self.atomic:
            attrs["aria-atomic"] = "true"
        if self.busy:
            attrs["aria-busy"] = "true"
        if self.relevant:
            attrs["aria-relevant"] = self.relevant
        if self.controls:
            attrs["aria-controls"] = self.controls
        if self.owns:
            attrs["aria-owns"] = self.owns
        if self.flowto:
            attrs["aria-flowto"] = self.flowto
        if self.level:
            attrs["aria-level"] = str(self.level)
        if self.valuemin:
            attrs["aria-valuemin"] = str(self.valuemin)
        if self.valuemax:
            attrs["aria-valuemax"] = str(self.valuemax)
        if self.valuenow:
            attrs["aria-valuenow"] = str(self.valuenow)
        if self.orientation:
            attrs["aria-orientation"] = self.orientation
        if self.autocomplete:
            attrs["aria-autocomplete"] = self.autocomplete
        if self.multiSelectable:
            attrs["aria-multiselectable"] = "true"
        if self.readOnly:
            attrs["aria-readonly"] = "true"
        
        return attrs
    
    def to_html(self) -> str:
        """Convert to HTML attribute string."""
        attrs = self.to_dict()
        return " ".join(f'{k}="{v}"' for k, v in attrs.items())


class AccessibleComponent:
    """Base class for accessible components."""
    
    def __init__(self, aria: AriaAttributes = None, role: str = ""):
        self.aria = aria or AriaAttributes()
        self.role = role
    
    def get_accessibility_attrs(self) -> str:
        """Get accessibility HTML attributes."""
        attrs = self.aria.to_dict()
        
        if self.role:
            attrs["role"] = self.role
        
        return " ".join(f'{k}="{v}"' for k, v in attrs.items())


class AccessibleButton(AccessibleComponent):
    """Accessible button component."""
    
    def __init__(
        self,
        text: str,
        onClick: str = "",
        disabled: bool = False,
        ariaLabel: str = "",
        ariaDescribedby: str = "",
        **kwargs,
    ):
        super().__init__(
            aria=AriaAttributes(
                label=ariaLabel,
                describedby=ariaDescribedby,
                disabled=disabled,
            ),
            role="button",
        )
        self.text = text
        self.onClick = onClick
        self.disabled = disabled
        self.kwargs = kwargs
    
    def render(self) -> str:
        disabled_attr = "disabled" if self.disabled else ""
        onclick_attr = f'onclick="{self.onClick}"' if self.onClick else ""
        
        return f"""
        <button 
            {self.get_accessibility_attrs()}
            {disabled_attr}
            {onclick_attr}
            class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed"
        >
            {self.text}
        </button>
        """


class AccessibleInput(AccessibleComponent):
    """Accessible input component."""
    
    def __init__(
        self,
        type: str = "text",
        name: str = "",
        value: str = "",
        placeholder: str = "",
        label: str = "",
        required: bool = False,
        disabled: bool = False,
        readOnly: bool = False,
        ariaDescribedby: str = "",
        ariaInvalid: bool = False,
        **kwargs,
    ):
        super().__init__(
            aria=AriaAttributes(
                label=label,
                describedby=ariaDescribedby,
                required=required,
                disabled=disabled,
                readOnly=readOnly,
                invalid=ariaInvalid,
            ),
        )
        self.type = type
        self.name = name
        self.value = value
        self.placeholder = placeholder
        self.label = label
        self.required = required
        self.disabled = disabled
        self.readOnly = readOnly
        self.kwargs = kwargs
    
    def render(self) -> str:
        input_id = f"input-{self.name or id(self)}"
        required_attr = "required" if self.required else ""
        disabled_attr = "disabled" if self.disabled else ""
        readonly_attr = "readonly" if self.readOnly else ""
        
        label_html = f'<label for="{input_id}" class="block text-sm font-medium text-gray-700 mb-1">{self.label}</label>' if self.label else ""
        
        return f"""
        <div>
            {label_html}
            <input 
                type="{self.type}"
                id="{input_id}"
                name="{self.name}"
                value="{self.value}"
                placeholder="{self.placeholder}"
                {self.get_accessibility_attrs()}
                {required_attr}
                {disabled_attr}
                {readonly_attr}
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none disabled:opacity-50 disabled:cursor-not-allowed"
            />
        </div>
        """


class AccessibleSelect(AccessibleComponent):
    """Accessible select component."""
    
    def __init__(
        self,
        name: str = "",
        options: List[Dict[str, str]] = None,
        value: str = "",
        label: str = "",
        required: bool = False,
        disabled: bool = False,
        ariaDescribedby: str = "",
        **kwargs,
    ):
        super().__init__(
            aria=AriaAttributes(
                label=label,
                describedby=ariaDescribedby,
                required=required,
                disabled=disabled,
            ),
        )
        self.name = name
        self.options = options or []
        self.value = value
        self.label = label
        self.required = required
        self.disabled = disabled
        self.kwargs = kwargs
    
    def render(self) -> str:
        select_id = f"select-{self.name or id(self)}"
        required_attr = "required" if self.required else ""
        disabled_attr = "disabled" if self.disabled else ""
        
        options_html = ""
        for opt in self.options:
            selected = "selected" if opt.get("value") == self.value else ""
            options_html += f'<option value="{opt.get("value", "")}" {selected}>{opt.get("label", opt.get("value", ""))}</option>'
        
        label_html = f'<label for="{select_id}" class="block text-sm font-medium text-gray-700 mb-1">{self.label}</label>' if self.label else ""
        
        return f"""
        <div>
            {label_html}
            <select 
                id="{select_id}"
                name="{self.name}"
                {self.get_accessibility_attrs()}
                {required_attr}
                {disabled_attr}
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none disabled:opacity-50 disabled:cursor-not-allowed"
            >
                {options_html}
            </select>
        </div>
        """


class AccessibleCheckbox(AccessibleComponent):
    """Accessible checkbox component."""
    
    def __init__(
        self,
        name: str = "",
        checked: bool = False,
        label: str = "",
        disabled: bool = False,
        ariaDescribedby: str = "",
        **kwargs,
    ):
        super().__init__(
            aria=AriaAttributes(
                label=label,
                describedby=ariaDescribedby,
                checked="true" if checked else "false",
                disabled=disabled,
            ),
            role="checkbox",
        )
        self.name = name
        self.checked = checked
        self.label = label
        self.disabled = disabled
        self.kwargs = kwargs
    
    def render(self) -> str:
        input_id = f"checkbox-{self.name or id(self)}"
        checked_attr = "checked" if self.checked else ""
        disabled_attr = "disabled" if self.disabled else ""
        
        return f"""
        <label class="flex items-center cursor-pointer">
            <input 
                type="checkbox"
                id="{input_id}"
                name="{self.name}"
                {self.get_accessibility_attrs()}
                {checked_attr}
                {disabled_attr}
                class="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
            />
            <span class="ml-2 text-sm text-gray-700">{self.label}</span>
        </label>
        """


class AccessibleRadio(AccessibleComponent):
    """Accessible radio button component."""
    
    def __init__(
        self,
        name: str = "",
        value: str = "",
        checked: bool = False,
        label: str = "",
        disabled: bool = False,
        ariaDescribedby: str = "",
        **kwargs,
    ):
        super().__init__(
            aria=AriaAttributes(
                label=label,
                describedby=ariaDescribedby,
                checked="true" if checked else "false",
                disabled=disabled,
            ),
            role="radio",
        )
        self.name = name
        self.value = value
        self.checked = checked
        self.label = label
        self.disabled = disabled
        self.kwargs = kwargs
    
    def render(self) -> str:
        input_id = f"radio-{self.name}-{self.value}"
        checked_attr = "checked" if self.checked else ""
        disabled_attr = "disabled" if self.disabled else ""
        
        return f"""
        <label class="flex items-center cursor-pointer">
            <input 
                type="radio"
                id="{input_id}"
                name="{self.name}"
                value="{self.value}"
                {self.get_accessibility_attrs()}
                {checked_attr}
                {disabled_attr}
                class="w-4 h-4 text-blue-600 border-gray-300 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
            />
            <span class="ml-2 text-sm text-gray-700">{self.label}</span>
        </label>
        """


class AccessibleModal(AccessibleComponent):
    """Accessible modal dialog component."""
    
    def __init__(
        self,
        title: str,
        content: str,
        isOpen: bool = False,
        onClose: str = "",
        **kwargs,
    ):
        super().__init__(
            aria=AriaAttributes(
                label=title,
                hidden=not isOpen,
            ),
            role="dialog",
        )
        self.title = title
        self.content = content
        self.isOpen = isOpen
        self.onClose = onClose
        self.kwargs = kwargs
    
    def render(self) -> str:
        modal_id = f"modal-{id(self)}"
        display = "flex" if self.isOpen else "none"
        
        return f"""
        <div 
            id="{modal_id}"
            class="fixed inset-0 z-50 overflow-y-auto"
            style="display: {display}"
            {self.get_accessibility_attrs()}
            aria-modal="true"
        >
            <div class="flex items-center justify-center min-h-screen px-4 pt-4 pb-20 text-center sm:block sm:p-0">
                <div class="fixed inset-0 transition-opacity bg-gray-500 bg-opacity-75" onclick="{self.onClose}"></div>
                <span class="hidden sm:inline-block sm:align-middle sm:h-screen">&#8203;</span>
                <div class="inline-block w-full max-w-md p-6 my-8 overflow-hidden text-left align-bottom transition-all transform bg-white shadow-xl rounded-2xl sm:align-middle">
                    <h2 class="text-lg font-semibold text-gray-900 mb-4">{self.title}</h2>
                    <div class="text-gray-700">{self.content}</div>
                    <div class="mt-4 flex justify-end">
                        <button 
                            onclick="{self.onClose}"
                            class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
                        >
                            Close
                        </button>
                    </div>
                </div>
            </div>
        </div>
        """


class AccessibleAlert(AccessibleComponent):
    """Accessible alert component."""
    
    def __init__(
        self,
        message: str,
        type: str = "info",  # info, success, warning, error
        dismissible: bool = False,
        onDismiss: str = "",
        **kwargs,
    ):
        super().__init__(
            aria=AriaAttributes(
                live="polite",
            ),
            role="alert",
        )
        self.message = message
        self.alert_type = type
        self.dismissible = dismissible
        self.onDismiss = onDismiss
        self.kwargs = kwargs
    
    def render(self) -> str:
        type_classes = {
            "info": "bg-blue-50 text-blue-800 border-blue-200",
            "success": "bg-green-50 text-green-800 border-green-200",
            "warning": "bg-yellow-50 text-yellow-800 border-yellow-200",
            "error": "bg-red-50 text-red-800 border-red-200",
        }
        
        dismiss_button = ""
        if self.dismissible:
            dismiss_button = f"""
            <button 
                onclick="{self.onDismiss}"
                class="ml-auto -mx-1.5 -my-1.5 rounded-lg focus:ring-2 focus:ring-offset-2 p-1.5 hover:bg-gray-100"
                aria-label="Dismiss"
            >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                </svg>
            </button>
            """
        
        return f"""
        <div class="flex items-center p-4 rounded-lg border {type_classes.get(self.alert_type, type_classes['info'])}" {self.get_accessibility_attrs()}>
            <span class="flex-1">{self.message}</span>
            {dismiss_button}
        </div>
        """


class SkipLink(AccessibleComponent):
    """Skip to main content link for keyboard navigation."""
    
    def __init__(self, href: str = "#main", text: str = "Skip to main content"):
        super().__init__(role="navigation")
        self.href = href
        self.text = text
    
    def render(self) -> str:
        return f"""
        <a href="{self.href}" class="sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4 focus:z-50 focus:px-4 focus:py-2 focus:bg-blue-500 focus:text-white focus:rounded-lg">
            {self.text}
        </a>
        """


class LiveRegion(AccessibleComponent):
    """ARIA live region for dynamic content updates."""
    
    def __init__(
        self,
        message: str = "",
        live: str = "polite",  # polite, assertive, off
        atomic: bool = True,
        **kwargs,
    ):
        super().__init__(
            aria=AriaAttributes(
                live=live,
                atomic=atomic,
            ),
        )
        self.message = message
        self.kwargs = kwargs
    
    def render(self) -> str:
        return f"""
        <div {self.get_accessibility_attrs()} class="sr-only">
            {self.message}
        </div>
        """


# Keyboard navigation utilities
def generate_keyboard_nav_js() -> str:
    """Generate JavaScript for keyboard navigation."""
    return """
    // Keyboard Navigation
    const keyboardNav = {
        init() {
            // Focus trap for modals
            document.addEventListener('keydown', (e) => {
                const modal = document.querySelector('[role="dialog"]:not([aria-hidden="true"])');
                if (modal) {
                    this.trapFocus(modal, e);
                }
            });
            
            // Arrow key navigation for lists
            document.addEventListener('keydown', (e) => {
                if (e.target.matches('[role="listbox"] [role="option"]')) {
                    this.handleListNavigation(e);
                }
            });
            
            // Escape key to close
            document.addEventListener('keydown', (e) => {
                if (e.key === 'Escape') {
                    const modal = document.querySelector('[role="dialog"]:not([aria-hidden="true"])');
                    if (modal) {
                        modal.setAttribute('aria-hidden', 'true');
                        modal.style.display = 'none';
                    }
                }
            });
        },
        
        trapFocus(element, event) {
            const focusableElements = element.querySelectorAll(
                'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
            );
            const firstElement = focusableElements[0];
            const lastElement = focusableElements[focusableElements.length - 1];
            
            if (event.key === 'Tab') {
                if (event.shiftKey && document.activeElement === firstElement) {
                    event.preventDefault();
                    lastElement.focus();
                } else if (!event.shiftKey && document.activeElement === lastElement) {
                    event.preventDefault();
                    firstElement.focus();
                }
            }
        },
        
        handleListNavigation(event) {
            const options = Array.from(event.target.parentElement.querySelectorAll('[role="option"]'));
            const currentIndex = options.indexOf(event.target);
            
            let newIndex;
            if (event.key === 'ArrowDown') {
                newIndex = (currentIndex + 1) % options.length;
            } else if (event.key === 'ArrowUp') {
                newIndex = (currentIndex - 1 + options.length) % options.length;
            } else if (event.key === 'Home') {
                newIndex = 0;
            } else if (event.key === 'End') {
                newIndex = options.length - 1;
            }
            
            if (newIndex !== undefined) {
                event.preventDefault();
                options[newIndex].focus();
                options[newIndex].setAttribute('aria-selected', 'true');
                options[currentIndex].setAttribute('aria-selected', 'false');
            }
        }
    };
    
    // Initialize keyboard navigation
    keyboardNav.init();
    """


# Screen reader only utility
def sr_only(text: str) -> str:
    """Generate screen reader only text."""
    return f'<span class="sr-only">{text}</span>'


# Focus visible utility
FOCUS_VISIBLE_CSS = """
/* Focus visible styles */
*:focus-visible {
    outline: 2px solid #3B82F6;
    outline-offset: 2px;
}

/* Screen reader only */
.sr-only {
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    white-space: nowrap;
    border-width: 0;
}

/* Reduced motion */
@media (prefers-reduced-motion: reduce) {
    *,
    *::before,
    *::after {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
    }
}
"""
