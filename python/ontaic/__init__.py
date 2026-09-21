"""Ontaic: Bi-Directional Compiler & State Runtime for Python UI."""
from ontaic.component import Component, State, Element, Box, Text, Button, Input, Image
from ontaic.layouts import (
    Container, Flex, Grid, Stack, Center, Spacer,
    Card, Divider, Badge, Heading, Paragraph
)
from ontaic.forms import FormField, Form, Select, Checkbox, Radio
from ontaic.conditional import If, Show, ForEach, Switch, Unless, Fragment
from ontaic.navigation import Router, NavLink, Navbar, Sidebar, SidebarLink
from ontaic.overlay import Modal, ConfirmDialog, AlertDialog, Drawer, Toast
from ontaic.table import Table, DataTable, DataGrid, CardList
from ontaic.validation import (
    FormValidator, Required, MinLength, MaxLength, Pattern,
    Email, URL, Phone, Numeric, Integer, Min, Max, Custom, MatchField,
)
from ontaic.state import PersistentState, ComputedState, StateManager
from ontaic.watcher import FileWatcher
from ontaic.compiler import OntaicCompiler
from ontaic.ai import (
    generate_component_prompt,
    generate_schema_prompt,
    validate_generated_code,
    EXAMPLE_PROMPTS,
)

__version__ = "0.1.0"
__all__ = [
    # Core
    "Component", "State", "Element", "Box", "Text", "Button", "Input", "Image",
    # Layouts
    "Container", "Flex", "Grid", "Stack", "Center", "Spacer",
    "Card", "Divider", "Badge", "Heading", "Paragraph",
    # Forms
    "FormField", "Form", "Select", "Checkbox", "Radio",
    # Conditionals
    "If", "Show", "ForEach", "Switch", "Unless", "Fragment",
    # Navigation
    "Router", "NavLink", "Navbar", "Sidebar", "SidebarLink",
    # Overlays
    "Modal", "ConfirmDialog", "AlertDialog", "Drawer", "Toast",
    # Tables
    "Table", "DataTable", "DataGrid", "CardList",
    # Validation
    "FormValidator", "Required", "MinLength", "MaxLength", "Pattern",
    "Email", "URL", "Phone", "Numeric", "Integer", "Min", "Max", "Custom", "MatchField",
    # State
    "PersistentState", "ComputedState", "StateManager",
    # Utilities
    "FileWatcher", "OntaicCompiler",
    # AI
    "generate_component_prompt", "generate_schema_prompt",
    "validate_generated_code", "EXAMPLE_PROMPTS",
]
