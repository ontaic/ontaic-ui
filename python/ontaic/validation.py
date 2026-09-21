"""Form validation with patterns and custom validators."""
import re
from typing import Any, Callable, Dict, List, Optional
from dataclasses import dataclass


@dataclass
class ValidationError:
    """Validation error."""
    field: str
    message: str
    code: str


class Validator:
    """Base validator class."""
    
    def __init__(self, message: str = "Invalid value"):
        self.message = message
    
    def validate(self, value: Any) -> Optional[str]:
        """Validate a value. Returns error message or None."""
        raise NotImplementedError


class Required(Validator):
    """Required field validator."""
    
    def __init__(self, message: str = "This field is required"):
        super().__init__(message)
    
    def validate(self, value: Any) -> Optional[str]:
        if value is None or value == "":
            return self.message
        return None


class MinLength(Validator):
    """Minimum length validator."""
    
    def __init__(self, min_length: int, message: str = None):
        self.min_length = min_length
        super().__init__(message or f"Must be at least {min_length} characters")
    
    def validate(self, value: Any) -> Optional[str]:
        if value and len(str(value)) < self.min_length:
            return self.message
        return None


class MaxLength(Validator):
    """Maximum length validator."""
    
    def __init__(self, max_length: int, message: str = None):
        self.max_length = max_length
        super().__init__(message or f"Must be at most {max_length} characters")
    
    def validate(self, value: Any) -> Optional[str]:
        if value and len(str(value)) > self.max_length:
            return self.message
        return None


class Pattern(Validator):
    """Regex pattern validator."""
    
    def __init__(self, pattern: str, message: str = "Invalid format"):
        self.pattern = pattern
        super().__init__(message)
    
    def validate(self, value: Any) -> Optional[str]:
        if value and not re.match(self.pattern, str(value)):
            return self.message
        return None


class Email(Validator):
    """Email validator."""
    
    def __init__(self, message: str = "Invalid email address"):
        super().__init__(message)
        self.pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    def validate(self, value: Any) -> Optional[str]:
        if value and not re.match(self.pattern, str(value)):
            return self.message
        return None


class URL(Validator):
    """URL validator."""
    
    def __init__(self, message: str = "Invalid URL"):
        super().__init__(message)
        self.pattern = r'^https?://[^\s/$.?#].[^\s]*$'
    
    def validate(self, value: Any) -> Optional[str]:
        if value and not re.match(self.pattern, str(value)):
            return self.message
        return None


class Phone(Validator):
    """Phone number validator."""
    
    def __init__(self, message: str = "Invalid phone number"):
        super().__init__(message)
        self.pattern = r'^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$'
    
    def validate(self, value: Any) -> Optional[str]:
        if value and not re.match(self.pattern, str(value)):
            return self.message
        return None


class Numeric(Validator):
    """Numeric validator."""
    
    def __init__(self, message: str = "Must be a number"):
        super().__init__(message)
    
    def validate(self, value: Any) -> Optional[str]:
        if value:
            try:
                float(value)
            except (ValueError, TypeError):
                return self.message
        return None


class Integer(Validator):
    """Integer validator."""
    
    def __init__(self, message: str = "Must be an integer"):
        super().__init__(message)
    
    def validate(self, value: Any) -> Optional[str]:
        if value:
            try:
                int(value)
            except (ValueError, TypeError):
                return self.message
        return None


class Min(Validator):
    """Minimum value validator."""
    
    def __init__(self, min_value: float, message: str = None):
        self.min_value = min_value
        super().__init__(message or f"Must be at least {min_value}")
    
    def validate(self, value: Any) -> Optional[str]:
        if value:
            try:
                if float(value) < self.min_value:
                    return self.message
            except (ValueError, TypeError):
                return "Invalid number"
        return None


class Max(Validator):
    """Maximum value validator."""
    
    def __init__(self, max_value: float, message: str = None):
        self.max_value = max_value
        super().__init__(message or f"Must be at most {max_value}")
    
    def validate(self, value: Any) -> Optional[str]:
        if value:
            try:
                if float(value) > self.max_value:
                    return self.message
            except (ValueError, TypeError):
                return "Invalid number"
        return None


class Custom(Validator):
    """Custom validator with a function."""
    
    def __init__(self, validator_func: Callable[[Any], bool], message: str = "Invalid value"):
        self.validator_func = validator_func
        super().__init__(message)
    
    def validate(self, value: Any) -> Optional[str]:
        if value and not self.validator_func(value):
            return self.message
        return None


class MatchField(Validator):
    """Match another field validator."""
    
    def __init__(self, field_name: str, message: str = None):
        self.field_name = field_name
        super().__init__(message or f"Must match {field_name}")
    
    def validate(self, value: Any, other_values: Dict[str, Any] = None) -> Optional[str]:
        if other_values and value != other_values.get(self.field_name):
            return self.message
        return None


class FormValidator:
    """Form validator that validates multiple fields."""
    
    def __init__(self):
        self.rules: Dict[str, List[Validator]] = {}
        self.errors: Dict[str, str] = {}
    
    def add_rule(self, field: str, validator: Validator):
        """Add a validation rule for a field."""
        if field not in self.rules:
            self.rules[field] = []
        self.rules[field].append(validator)
        return self
    
    def validate(self, data: Dict[str, Any]) -> Dict[str, str]:
        """Validate all fields and return errors."""
        self.errors = {}
        
        for field, validators in self.rules.items():
            value = data.get(field)
            for validator in validators:
                error = validator.validate(value)
                if error:
                    self.errors[field] = error
                    break
        
        return self.errors
    
    def is_valid(self, data: Dict[str, Any]) -> bool:
        """Check if data is valid."""
        errors = self.validate(data)
        return len(errors) == 0
    
    def get_errors(self) -> Dict[str, str]:
        """Get validation errors."""
        return self.errors.copy()
    
    def get_error(self, field: str) -> Optional[str]:
        """Get error for a specific field."""
        return self.errors.get(field)
    
    def generate_js_code(self) -> str:
        """Generate JavaScript validation code."""
        rules_js = {}
        for field, validators in self.rules.items():
            rules_js[field] = []
            for v in validators:
                if isinstance(v, Required):
                    rules_js[field].append({"type": "required", "message": v.message})
                elif isinstance(v, MinLength):
                    rules_js[field].append({"type": "minLength", "min": v.min_length, "message": v.message})
                elif isinstance(v, MaxLength):
                    rules_js[field].append({"type": "maxLength", "max": v.max_length, "message": v.message})
                elif isinstance(v, Pattern):
                    rules_js[field].append({"type": "pattern", "pattern": v.pattern, "message": v.message})
                elif isinstance(v, Email):
                    rules_js[field].append({"type": "email", "message": v.message})
                elif isinstance(v, Numeric):
                    rules_js[field].append({"type": "numeric", "message": v.message})
                elif isinstance(v, Min):
                    rules_js[field].append({"type": "min", "min": v.min_value, "message": v.message})
                elif isinstance(v, Max):
                    rules_js[field].append({"type": "max", "max": v.max_value, "message": v.message})
        
        return f"""
        // Form Validation
        const validationRules = {str(rules_js).replace("'", '"')};
        
        function validateField(field, value) {{
            const rules = validationRules[field];
            if (!rules) return null;
            
            for (const rule of rules) {{
                switch (rule.type) {{
                    case 'required':
                        if (!value) return rule.message;
                        break;
                    case 'minLength':
                        if (value && value.length < rule.min) return rule.message;
                        break;
                    case 'maxLength':
                        if (value && value.length > rule.max) return rule.message;
                        break;
                    case 'pattern':
                        if (value && !new RegExp(rule.pattern).test(value)) return rule.message;
                        break;
                    case 'email':
                        if (value && !/^[^@]+@[^@]+\\.[^@]+$/.test(value)) return rule.message;
                        break;
                    case 'numeric':
                        if (value && isNaN(value)) return rule.message;
                        break;
                    case 'min':
                        if (value && Number(value) < rule.min) return rule.message;
                        break;
                    case 'max':
                        if (value && Number(value) > rule.max) return rule.message;
                        break;
                }}
            }}
            return null;
        }}
        
        function validateForm(formData) {{
            const errors = {{}};
            for (const field in validationRules) {{
                const error = validateField(field, formData[field]);
                if (error) errors[field] = error;
            }}
            return errors;
        }}
        
        function showFieldError(field, message) {{
            const input = document.querySelector(`[name="${{field}}"]`);
            if (input) {{
                input.classList.add('border-red-500');
                let errorEl = input.parentElement.querySelector('.field-error');
                if (!errorEl) {{
                    errorEl = document.createElement('p');
                    errorEl.className = 'field-error mt-1 text-sm text-red-500';
                    input.parentElement.appendChild(errorEl);
                }}
                errorEl.textContent = message;
            }}
        }}
        
        function clearFieldError(field) {{
            const input = document.querySelector(`[name="${{field}}"]`);
            if (input) {{
                input.classList.remove('border-red-500');
                const errorEl = input.parentElement.querySelector('.field-error');
                if (errorEl) errorEl.remove();
            }}
        }}
        """


# Predefined validators
validators = {
    "email": Email(),
    "url": URL(),
    "phone": Phone(),
    "required": Required(),
    "numeric": Numeric(),
    "integer": Integer(),
}


def create_validator(*validator_types: str) -> List[Validator]:
    """Create validators from predefined types."""
    return [validators[vt] for vt in validator_types if vt in validators]
