"""Form handling and validation components."""
from typing import Any, Callable, Dict, List, Optional
from ontaic.component import Component, Element


class FormField(Element):
    """Form field with label, input, and validation."""

    def __init__(
        self,
        name: str,
        label: str = "",
        input_type: str = "text",
        placeholder: str = "",
        value: str = "",
        required: bool = False,
        error: str = "",
        help_text: str = "",
        class_name: str = "",
        **kwargs,
    ):
        self.field_name = name
        self.label = label
        self.input_type = input_type
        self.placeholder = placeholder
        self.value = value
        self.required = required
        self.error = error
        self.help_text = help_text

        full_class = f"mb-4 {class_name}"
        super().__init__("div", class_name=full_class, **kwargs)

    def render(self):
        label_html = ""
        if self.label:
            req = ' <span class="text-red-500">*</span>' if self.required else ""
            label_html = f'<label class="block text-sm font-medium text-gray-700 mb-1">{self.label}{req}</label>'

        input_class = "w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none"
        if self.error:
            input_class += " border-red-500"
        else:
            input_class += " border-gray-300"

        input_html = f'<input type="{self.input_type}" name="{self.field_name}" placeholder="{self.placeholder}" value="{self.value}" class="{input_class}" />'

        error_html = ""
        if self.error:
            error_html = f'<p class="mt-1 text-sm text-red-500">{self.error}</p>'

        help_html = ""
        if self.help_text and not self.error:
            help_html = f'<p class="mt-1 text-sm text-gray-500">{self.help_text}</p>'

        return f"""<div class="mb-4">
            {label_html}
            {input_html}
            {error_html}
            {help_html}
        </div>"""


class Form(Element):
    """Form container with validation."""

    def __init__(
        self,
        *children,
        action: str = "",
        method: str = "POST",
        on_submit: Optional[Callable] = None,
        class_name: str = "",
        **kwargs,
    ):
        self.action = action
        self.method = method
        self.on_submit = on_submit

        full_class = f"space-y-4 {class_name}"
        super().__init__("form", class_name=full_class, **kwargs)
        self.children = list(children)

    def render(self):
        inner = "".join(
            child.render() if hasattr(child, "render") else str(child)
            for child in self.children
        )
        return f"""<form method="{self.method}" action="{self.action}" class="{self.class_name}">
            {inner}
        </form>"""


class Select(Element):
    """Select dropdown with options."""

    def __init__(
        self,
        name: str,
        options: List[Dict[str, str]] = None,
        value: str = "",
        placeholder: str = "Select an option",
        class_name: str = "",
        **kwargs,
    ):
        self.field_name = name
        self.options = options or []
        self.value = value
        self.placeholder = placeholder

        full_class = f"w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent {class_name}"
        super().__init__("select", class_name=full_class, **kwargs)

    def render(self):
        options_html = f'<option value="">{self.placeholder}</option>'
        for opt in self.options:
            selected = "selected" if opt.get("value") == self.value else ""
            options_html += f'<option value="{opt["value"]}" {selected}>{opt.get("label", opt["value"])}</option>'

        return f'<select name="{self.field_name}" class="{self.class_name}">{options_html}</select>'


class Checkbox(Element):
    """Checkbox input."""

    def __init__(
        self,
        name: str,
        label: str = "",
        checked: bool = False,
        class_name: str = "",
        **kwargs,
    ):
        self.field_name = name
        self.label = label
        self.checked = checked

        full_class = f"flex items-center {class_name}"
        super().__init__("div", class_name=full_class, **kwargs)

    def render(self):
        checked = "checked" if self.checked else ""
        return f"""<label class="flex items-center cursor-pointer">
            <input type="checkbox" name="{self.field_name}" {checked} class="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500" />
            <span class="ml-2 text-sm text-gray-700">{self.label}</span>
        </label>"""


class Radio(Element):
    """Radio button input."""

    def __init__(
        self,
        name: str,
        value: str,
        label: str = "",
        checked: bool = False,
        class_name: str = "",
        **kwargs,
    ):
        self.field_name = name
        self.value = value
        self.label = label
        self.checked = checked

        full_class = f"flex items-center {class_name}"
        super().__init__("div", class_name=full_class, **kwargs)

    def render(self):
        checked = "checked" if self.checked else ""
        return f"""<label class="flex items-center cursor-pointer">
            <input type="radio" name="{self.field_name}" value="{self.value}" {checked} class="w-4 h-4 text-blue-600 border-gray-300 focus:ring-blue-500" />
            <span class="ml-2 text-sm text-gray-700">{self.label}</span>
        </label>"""
