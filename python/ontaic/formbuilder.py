"""Form builder for creating forms declaratively."""
import json
from typing import Any, Callable, Dict, List, Optional, Union
from dataclasses import dataclass, field
from enum import Enum


class FieldType(str, Enum):
    """Form field types."""
    TEXT = "text"
    EMAIL = "email"
    PASSWORD = "password"
    NUMBER = "number"
    TEL = "tel"
    URL = "url"
    DATE = "date"
    TIME = "time"
    DATETIME_LOCAL = "datetime-local"
    MONTH = "month"
    WEEK = "week"
    COLOR = "color"
    FILE = "file"
    TEXTAREA = "textarea"
    SELECT = "select"
    CHECKBOX = "checkbox"
    RADIO = "radio"
    RANGE = "range"
    HIDDEN = "hidden"
    SEARCH = "search"


@dataclass
class FieldOption:
    """Select/radio/checkbox option."""
    value: str
    label: str
    disabled: bool = False
    
    def to_dict(self) -> dict:
        return {"value": self.value, "label": self.label, "disabled": self.disabled}


@dataclass
class FieldValidation:
    """Field validation rules."""
    required: bool = False
    min_length: Optional[int] = None
    max_length: Optional[int] = None
    min_value: Optional[Union[int, float]] = None
    max_value: Optional[Union[int, float]] = None
    pattern: Optional[str] = None
    custom: Optional[str] = None
    message: Optional[str] = None
    
    def to_dict(self) -> dict:
        return {
            "required": self.required,
            "minLength": self.min_length,
            "maxLength": self.max_length,
            "minValue": self.min_value,
            "maxValue": self.max_value,
            "pattern": self.pattern,
            "custom": self.custom,
            "message": self.message,
        }


@dataclass
class FormField:
    """Form field definition."""
    name: str
    field_type: FieldType = FieldType.TEXT
    label: str = ""
    placeholder: str = ""
    default_value: Any = None
    options: List[FieldOption] = field(default_factory=list)
    validation: FieldValidation = field(default_factory=FieldValidation)
    disabled: bool = False
    readonly: bool = False
    help_text: str = ""
    class_name: str = ""
    wrapper_class: str = ""
    attributes: Dict[str, str] = field(default_factory=dict)
    
    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "type": self.field_type.value,
            "label": self.label,
            "placeholder": self.placeholder,
            "defaultValue": self.default_value,
            "options": [o.to_dict() for o in self.options],
            "validation": self.validation.to_dict(),
            "disabled": self.disabled,
            "readonly": self.readonly,
            "helpText": self.help_text,
            "className": self.class_name,
            "wrapperClass": self.wrapper_class,
            "attributes": self.attributes,
        }
    
    def to_html(self) -> str:
        """Generate HTML for this field."""
        name = self.name
        field_id = f"field-{name}"
        label_html = f'<label for="{field_id}" class="form-label">{self.label}</label>' if self.label else ""
        help_html = f'<p class="form-help">{self.help_text}</p>' if self.help_text else ""
        wrapper_class = f" {self.wrapper_class}" if self.wrapper_class else ""
        field_class = f" form-input {self.class_name}" if self.class_name else " form-input"
        
        attrs = ""
        if self.disabled:
            attrs += ' disabled'
        if self.readonly:
            attrs += ' readonly'
        if self.validation.required:
            attrs += ' required'
        if self.validation.min_length:
            attrs += f' minlength="{self.validation.min_length}"'
        if self.validation.max_length:
            attrs += f' maxlength="{self.validation.max_length}"'
        if self.validation.pattern:
            attrs += f' pattern="{self.validation.pattern}"'
        
        if self.field_type == FieldType.TEXTAREA:
            value = self.default_value or ""
            return f'''<div class="form-field{wrapper_class}">
                {label_html}
                <textarea id="{field_id}" name="{name}" class="form-textarea{field_class}" placeholder="{self.placeholder}"{attrs}>{value}</textarea>
                {help_html}
            </div>'''
        
        elif self.field_type == FieldType.SELECT:
            options_html = ""
            for opt in self.options:
                selected = " selected" if opt.value == self.default_value else ""
                disabled = " disabled" if opt.disabled else ""
                options_html += f'<option value="{opt.value}"{selected}{disabled}>{opt.label}</option>'
            
            return f'''<div class="form-field{wrapper_class}">
                {label_html}
                <select id="{field_id}" name="{name}" class="form-select{field_class}"{attrs}>
                    {options_html}
                </select>
                {help_html}
            </div>'''
        
        elif self.field_type == FieldType.CHECKBOX:
            checked = " checked" if self.default_value else ""
            return f'''<div class="form-field form-field-checkbox{wrapper_class}">
                <label>
                    <input type="checkbox" id="{field_id}" name="{name}" value="true"{checked}{attrs}>
                    {self.label}
                </label>
                {help_html}
            </div>'''
        
        elif self.field_type == FieldType.RADIO:
            options_html = ""
            for i, opt in enumerate(self.options):
                checked = " checked" if opt.value == self.default_value else ""
                radio_id = f"{field_id}-{i}"
                options_html += f'''<label class="form-radio-label">
                    <input type="radio" id="{radio_id}" name="{name}" value="{opt.value}"{checked}{attrs}>
                    {opt.label}
                </label>'''
            
            return f'''<div class="form-field form-field-radio{wrapper_class}">
                {label_html}
                <div class="form-radio-group">{options_html}</div>
                {help_html}
            </div>'''
        
        elif self.field_type == FieldType.RANGE:
            value = self.default_value or 50
            min_val = self.validation.min_value or 0
            max_val = self.validation.max_value or 100
            return f'''<div class="form-field{wrapper_class}">
                {label_html}
                <input type="range" id="{field_id}" name="{name}" class="form-range{field_class}" value="{value}" min="{min_val}" max="{max_val}"{attrs}>
                {help_html}
            </div>'''
        
        else:
            value = self.default_value or ""
            input_type = self.field_type.value
            return f'''<div class="form-field{wrapper_class}">
                {label_html}
                <input type="{input_type}" id="{field_id}" name="{name}" class="{field_class}" value="{value}" placeholder="{self.placeholder}"{attrs}>
                {help_html}
            </div>'''


class FormBuilder:
    """Builder for creating forms."""
    
    def __init__(self, action: str = "", method: str = "POST"):
        self.action = action
        self.method = method
        self._fields: List[FormField] = []
        self._submit_text: str = "Submit"
        self._submit_class: str = "form-submit"
        self._form_class: str = ""
        self._on_submit: Optional[Callable] = None
        self._validate: bool = True
    
    def field(self, name: str, field_type: FieldType = FieldType.TEXT, **kwargs) -> "FormBuilder":
        """Add a field."""
        options = kwargs.pop("options", [])
        if options and not isinstance(options[0], FieldOption):
            options = [FieldOption(value=str(o), label=str(o)) for o in options]
        
        validation = kwargs.pop("validation", None)
        if validation and not isinstance(validation, FieldValidation):
            validation = FieldValidation(**validation)
        
        form_field = FormField(
            name=name,
            field_type=field_type,
            options=options or [],
            validation=validation or FieldValidation(),
            **kwargs,
        )
        self._fields.append(form_field)
        return self
    
    def text(self, name: str, **kwargs) -> "FormBuilder":
        """Add a text field."""
        return self.field(name, FieldType.TEXT, **kwargs)
    
    def email(self, name: str, **kwargs) -> "FormBuilder":
        """Add an email field."""
        return self.field(name, FieldType.EMAIL, **kwargs)
    
    def password(self, name: str, **kwargs) -> "FormBuilder":
        """Add a password field."""
        return self.field(name, FieldType.PASSWORD, **kwargs)
    
    def number(self, name: str, **kwargs) -> "FormBuilder":
        """Add a number field."""
        return self.field(name, FieldType.NUMBER, **kwargs)
    
    def textarea(self, name: str, **kwargs) -> "FormBuilder":
        """Add a textarea field."""
        return self.field(name, FieldType.TEXTAREA, **kwargs)
    
    def select(self, name: str, options: List[Union[str, FieldOption]], **kwargs) -> "FormBuilder":
        """Add a select field."""
        return self.field(name, FieldType.SELECT, options=options, **kwargs)
    
    def checkbox(self, name: str, **kwargs) -> "FormBuilder":
        """Add a checkbox field."""
        return self.field(name, FieldType.CHECKBOX, **kwargs)
    
    def radio(self, name: str, options: List[Union[str, FieldOption]], **kwargs) -> "FormBuilder":
        """Add a radio field."""
        return self.field(name, FieldType.RADIO, options=options, **kwargs)
    
    def date(self, name: str, **kwargs) -> "FormBuilder":
        """Add a date field."""
        return self.field(name, FieldType.DATE, **kwargs)
    
    def time(self, name: str, **kwargs) -> "FormBuilder":
        """Add a time field."""
        return self.field(name, FieldType.TIME, **kwargs)
    
    def range(self, name: str, min_value: int = 0, max_value: int = 100, **kwargs) -> "FormBuilder":
        """Add a range field."""
        validation = kwargs.pop("validation", FieldValidation(min_value=min_value, max_value=max_value))
        return self.field(name, FieldType.RANGE, validation=validation, **kwargs)
    
    def hidden(self, name: str, value: Any = None, **kwargs) -> "FormBuilder":
        """Add a hidden field."""
        return self.field(name, FieldType.HIDDEN, default_value=value, **kwargs)
    
    def file(self, name: str, **kwargs) -> "FormBuilder":
        """Add a file field."""
        return self.field(name, FieldType.FILE, **kwargs)
    
    def color(self, name: str, **kwargs) -> "FormBuilder":
        """Add a color field."""
        return self.field(name, FieldType.COLOR, **kwargs)
    
    def submit(self, text: str = "Submit", class_name: str = "form-submit") -> "FormBuilder":
        """Set submit button."""
        self._submit_text = text
        self._submit_class = class_name
        return self
    
    def action(self, url: str) -> "FormBuilder":
        """Set form action."""
        self.action = url
        return self
    
    def method(self, method: str) -> "FormBuilder":
        """Set form method."""
        self.method = method.upper()
        return self
    
    def class_name(self, class_name: str) -> "FormBuilder":
        """Set form class."""
        self._form_class = class_name
        return self
    
    def on_submit(self, callback: Callable) -> "FormBuilder":
        """Set submit handler."""
        self._on_submit = callback
        return self
    
    def no_validate(self) -> "FormBuilder":
        """Disable browser validation."""
        self._validate = False
        return self
    
    def build(self) -> Dict[str, Any]:
        """Build form configuration."""
        return {
            "action": self.action,
            "method": self.method,
            "fields": [f.to_dict() for f in self._fields],
            "submitText": self._submit_text,
            "submitClass": self._submit_class,
            "formClass": self._form_class,
            "validate": self._validate,
        }
    
    def to_html(self) -> str:
        """Generate HTML form."""
        form_class = f' class="{self._form_class}"' if self._form_class else ""
        no_validate = " novalidate" if not self._validate else ""
        action = f' action="{self.action}"' if self.action else ""
        
        fields_html = "\n".join(f.to_html() for f in self._fields)
        
        return f'''<form{action} method="{self.method}"{form_class}{no_validate}>
            {fields_html}
            <button type="submit" class="{self._submit_class}">{self._submit_text}</button>
        </form>'''
    
    def generate_js_code(self) -> str:
        """Generate JavaScript for form."""
        config = json.dumps(self.build())
        return f"""
        // Form Builder
        (function() {{
            const config = {config};
            
            const form = document.querySelector('form');
            if (!form) return;
            
            form.addEventListener('submit', (e) => {{
                e.preventDefault();
                
                const formData = new FormData(form);
                const data = {{}};
                
                config.fields.forEach(field => {{
                    if (field.type === 'checkbox') {{
                        data[field.name] = formData.has(field.name);
                    }} else if (field.type === 'number' || field.type === 'range') {{
                        data[field.name] = parseFloat(formData.get(field.name)) || 0;
                    }} else {{
                        data[field.name] = formData.get(field.name) || '';
                    }}
                }});
                
                console.log('Form submitted:', data);
            }});
        }})();
        """


def create_form(action: str = "", method: str = "POST") -> FormBuilder:
    """Create a form builder."""
    return FormBuilder(action, method)


def form_field(name: str, field_type: FieldType = FieldType.TEXT, **kwargs) -> FormField:
    """Create a form field."""
    options = kwargs.pop("options", [])
    if options and not isinstance(options[0], FieldOption):
        options = [FieldOption(value=str(o), label=str(o)) for o in options]
    
    validation = kwargs.pop("validation", None)
    if validation and not isinstance(validation, FieldValidation):
        validation = FieldValidation(**validation)
    
    return FormField(
        name=name,
        field_type=field_type,
        options=options or [],
        validation=validation or FieldValidation(),
        **kwargs,
    )


def field_option(value: str, label: str, disabled: bool = False) -> FieldOption:
    """Create a field option."""
    return FieldOption(value=value, label=label, disabled=disabled)


def field_validation(**kwargs) -> FieldValidation:
    """Create field validation."""
    return FieldValidation(**kwargs)


FORM_CSS = """
.form-field {
    margin-bottom: 1rem;
}

.form-label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: 500;
    color: #374151;
}

.form-input,
.form-select,
.form-textarea {
    width: 100%;
    padding: 0.5rem 0.75rem;
    border: 1px solid #d1d5db;
    border-radius: 0.375rem;
    font-size: 1rem;
    line-height: 1.5;
    transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
}

.form-input:focus,
.form-select:focus,
.form-textarea:focus {
    outline: none;
    border-color: #3b82f6;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.form-input:disabled,
.form-select:disabled,
.form-textarea:disabled {
    background-color: #f3f4f6;
    cursor: not-allowed;
}

.form-textarea {
    min-height: 100px;
    resize: vertical;
}

.form-select {
    appearance: none;
    background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 20 20'%3e%3cpath stroke='%236b7280' stroke-linecap='round' stroke-linejoin='round' stroke-width='1.5' d='M6 8l4 4 4-4'/%3e%3c/svg%3e");
    background-position: right 0.5rem center;
    background-repeat: no-repeat;
    background-size: 1.5em 1.5em;
    padding-right: 2.5rem;
}

.form-radio-group {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}

.form-radio-label {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    cursor: pointer;
}

.form-field-checkbox label {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    cursor: pointer;
}

.form-help {
    margin-top: 0.25rem;
    font-size: 0.875rem;
    color: #6b7280;
}

.form-submit {
    padding: 0.625rem 1.25rem;
    background-color: #3b82f6;
    color: white;
    font-weight: 500;
    border: none;
    border-radius: 0.375rem;
    cursor: pointer;
    transition: background-color 0.15s ease-in-out;
}

.form-submit:hover {
    background-color: #2563eb;
}

.form-submit:disabled {
    background-color: #93c5fd;
    cursor: not-allowed;
}

.form-range {
    width: 100%;
    height: 0.5rem;
    background: #e5e7eb;
    border-radius: 0.25rem;
    outline: none;
    opacity: 0.7;
    transition: opacity 0.15s;
}

.form-range:hover {
    opacity: 1;
}
"""
