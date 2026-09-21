"""AI code generation API for ontaic components."""
import json
from typing import Dict, List, Optional


SCHEMA_PROMPT_TEMPLATE = """You are an expert in the Ontaic Python UI framework. Generate Python code for a component based on the user's description.

Available components:
- Box: Generic container (like div)
- Text: Text element with tag and class_name
- Button: Button with on_click handler
- Input: Text input with placeholder
- Image: Image with src and alt

Available state:
- Define state with type annotations: `count: int = 0`
- Use f-strings with self.xxx for reactive text
- Use lambda for event handlers: `on_click=lambda: self.count + 1`

Available Tailwind CSS classes:
- Layout: flex, grid, block, inline, hidden
- Flexbox: flex-row, flex-col, items-center, justify-center, gap-4
- Spacing: p-4, m-2, px-6, py-3, mb-4
- Colors: bg-blue-500, text-white, border-gray-300
- Typography: text-lg, font-bold, text-center
- Rounded: rounded-lg, rounded-full
- Shadow: shadow-md, shadow-lg

Example component:
```python
from ontaic.component import Component, State, Box, Text, Button

class Counter(Component):
    count: int = 0

    def render(self):
        return Box(
            Text(f"Count: {self.count}", tag="h1", class_name="text-4xl font-bold"),
            Button("+1", on_click=lambda: self.count + 1, class_name="bg-blue-500 text-white px-4 py-2 rounded"),
            class_name="p-8 text-center"
        )
```

User request: {description}

Generate ONLY the Python code. No explanation needed."""


def generate_component_prompt(description: str) -> str:
    """Generate a prompt for AI code generation."""
    return SCHEMA_PROMPT_TEMPLATE.format(description=description)


def generate_schema_prompt(description: str) -> str:
    """Generate a prompt for AI schema generation."""
    return f"""You are an expert in the Ontaic UI framework. Generate a JSON schema for a component.

The schema format is:
{{
  "version": "1.0",
  "html": "<html string>",
  "bindings": {{ "state_key": "node_id" }},
  "events": {{ "node_id": {{ "event": "handler_js" }} }},
  "initialState": {{ "state_key": "default_value" }},
  "components": [{{ "name": "ComponentName", "states": ["state1"] }}]
}}

Available HTML elements:
- <div> for containers
- <span> for inline text
- <button> for buttons
- <input> for inputs
- <img> for images

Tailwind CSS classes are supported inline.

User request: {description}

Generate ONLY the JSON schema. No explanation needed."""


def validate_generated_code(code: str) -> Dict[str, any]:
    """Validate generated Python code for common errors."""
    errors = []
    warnings = []

    # Check for imports
    if "from ontaic.component import" not in code:
        errors.append("Missing ontaic.component import")

    # Check for Component class
    if "class " not in code:
        errors.append("No class definition found")

    # Check for render method
    if "def render" not in code:
        errors.append("No render method found")

    # Check for state annotations
    if ": int = " in code or ": str = " in code or ": bool = " in code:
        pass  # Good, has state
    elif "State(" in code:
        pass  # Good, uses State class
    else:
        warnings.append("No state fields found - component will be static")

    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
    }


# Example prompts for common patterns
EXAMPLE_PROMPTS = {
    "counter": "A counter with increment, decrement, and reset buttons showing the current count",
    "todo_list": "A todo list with input field, add button, and list of items with delete buttons",
    "login_form": "A login form with email and password fields, remember me checkbox, and submit button",
    "dashboard": "A dashboard with stats cards, a chart area, and a recent activity feed",
    "settings": "A settings page with toggles for notifications, dark mode, and language selector",
    "profile": "A user profile card with avatar, name, bio, and edit button",
    "pricing": "A pricing table with three tiers: Basic, Pro, and Enterprise",
    "faq": "An FAQ section with expandable questions and answers",
    "contact": "A contact form with name, email, subject, and message fields",
    "search": "A search page with search bar, filters, and results list",
}


def get_example_prompt(name: str) -> Optional[str]:
    """Get an example prompt by name."""
    return EXAMPLE_PROMPTS.get(name)


def list_example_prompts() -> List[str]:
    """List all available example prompts."""
    return list(EXAMPLE_PROMPTS.keys())
