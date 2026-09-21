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
from ontaic.database import Database, Repository, UserManager, PostManager, init_database
from ontaic.auth import AuthManager, User, Session, CookieAuth, JWTAuth
from ontaic.api import ApiClient, UsersApi, PostsApi, AuthApi, create_api_client
from ontaic.upload import FileUploader, ImageUploader, DocumentUploader, UploadComponent
from ontaic.theme import ThemeManager, ThemeToggle, ThemeSelector, LIGHT_THEME, DARK_THEME
from ontaic.websocket_server import WebSocketServer, WebSocketClient
from ontaic.i18n import I18n, LocaleSelector, T, LOCALES
from ontaic.charts import (
    Chart, LineChart, BarChart, PieChart, DoughnutChart, RadarChart,
    PolarAreaChart, BubbleChart, ScatterChart, ChartDataset, ChartOptions,
    StatCard, ProgressBar, MetricCard, Gauge, Timeline,
)
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
    # Database
    "Database", "Repository", "UserManager", "PostManager", "init_database",
    # Auth
    "AuthManager", "User", "Session", "CookieAuth", "JWTAuth",
    # API
    "ApiClient", "UsersApi", "PostsApi", "AuthApi", "create_api_client",
    # Upload
    "FileUploader", "ImageUploader", "DocumentUploader", "UploadComponent",
    # Theme
    "ThemeManager", "ThemeToggle", "ThemeSelector", "LIGHT_THEME", "DARK_THEME",
    # WebSocket
    "WebSocketServer", "WebSocketClient",
    # i18n
    "I18n", "LocaleSelector", "T", "LOCALES",
    # Charts
    "Chart", "LineChart", "BarChart", "PieChart", "DoughnutChart", "RadarChart",
    "PolarAreaChart", "BubbleChart", "ScatterChart", "ChartDataset", "ChartOptions",
    "StatCard", "ProgressBar", "MetricCard", "Gauge", "Timeline",
    # Utilities
    "FileWatcher", "OntaicCompiler",
    # AI
    "generate_component_prompt", "generate_schema_prompt",
    "validate_generated_code", "EXAMPLE_PROMPTS",
]
