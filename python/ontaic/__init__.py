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
from ontaic.animation import (
    AnimationManager, AnimatedElement, FadeIn, SlideIn, ScaleIn,
    Spinner, Skeleton, Collapse, Tabs, Carousel,
    FADE_IN, SLIDE_IN_UP, SCALE_IN, BOUNCE, SPIN, PULSE, SHAKE,
)
from ontaic.accessibility import (
    AriaAttributes, AccessibleComponent, AccessibleButton, AccessibleInput,
    AccessibleSelect, AccessibleCheckbox, AccessibleRadio, AccessibleModal,
    AccessibleAlert, SkipLink, LiveRegion, generate_keyboard_nav_js, sr_only,
)
from ontaic.extra_components import (
    Accordion, Breadcrumb, Pagination, Tooltip, Popover,
    Alert, Avatar, Tag, StatusDot, EmptyState,
)
from ontaic.errors import (
    ErrorHandler, ErrorBoundary, ErrorInfo,
    ValidationError, NotFoundError, AuthenticationError, AuthorizationError,
    retry, CircuitBreaker, Cache, RateLimiter,
)
from ontaic.performance import (
    PerformanceMonitor, Timer, timed, cache,
    MemoryMonitor, CpuMonitor, get_performance_monitor,
)
from ontaic.testing import (
    TestSuite, ComponentTestSuite, CompilerTestSuite, IntegrationTestSuite,
    TestResult, create_example_tests,
)
from ontaic.watcher import FileWatcher
from ontaic.compiler import OntaicCompiler
from ontaic.ai import (
    generate_component_prompt,
    generate_schema_prompt,
    validate_generated_code,
    EXAMPLE_PROMPTS,
)
from ontaic.ssr import (
    SSRContext, SSRMeta, SSRRenderer, SSRCache, SSRMiddleware,
    ssr_route, ssr_layout, get_ssr_renderer, render_ssr, render_ssr_page,
)
from ontaic.graphql import (
    GraphQLClient, GraphQLField, GraphQLOperation, GraphQLResponse,
    GraphQLQueryBuilder, GraphQLSchemaBuilder,
    gql_query, gql_mutation, gql_subscription,
    create_gql_client, build_schema, build_query, build_mutation,
)
from ontaic.storage import (
    Storage, LocalStorage, SessionStorage, MemoryStorage, IndexedDBStorage,
    StorageType, StorageItem,
    create_storage, localStorage, sessionStorage, memoryStorage,
)
from ontaic.datetime_utils import (
    DateTime, DateFormat, DateInfo, now, today,
    from_timestamp, from_string, format_date, format_relative,
    time_ago, generate_calendar,
)
from ontaic.rest import (
    RestClient, CRUDBase, ApiResponse, RequestConfig, HttpMethod,
    UsersCRUD, PostsCRUD, CommentsCRUD, ApiFactory,
    create_api, create_client, create_crud,
)
from ontaic.dragdrop import (
    Draggable, Droppable, Sortable, DragDropManager, DragOptions, DropZone, DragData,
    create_drag_drop, make_draggable, make_droppable, make_sortable,
)
from ontaic.virtualscroll import (
    VirtualList, VirtualGrid, VirtualScrollOptions,
    create_virtual_list, create_virtual_grid,
)
from ontaic.formbuilder import (
    FormBuilder, FormField as FormFieldDef, FieldOption, FieldValidation, FieldType,
    create_form, form_field, field_option, field_validation,
)
from ontaic.richtext import (
    RichTextEditor, EditorToolbar, EditorFormat, ToolbarButton,
    create_editor, create_markdown_editor,
)
from ontaic.datepicker import (
    DatePicker, PickerMode, PickerSize, PickerPreset, PRESETS,
    create_date_picker, create_date_range_picker,
)
from ontaic.fileupload import (
    FileUpload, UploadedFile, UploadConfig, UploadStatus, FileType,
    create_file_upload, create_image_upload,
)
from ontaic.colorpicker import (
    ColorPicker, ColorFormat, ColorPreset, DEFAULT_PRESETS,
    create_color_picker, color_preset,
)
from ontaic.wizard import (
    FormWizard, WizardStep, WizardStepStatus, WizardLayout,
    create_wizard, wizard_step,
)
from ontaic.markdown import (
    MarkdownEditor, MarkdownViewMode, MarkdownToolbarItem, DEFAULT_TOOLBAR,
    create_markdown_editor,
)
from ontaic.notifications import (
    NotificationManager, Notification, NotificationType, NotificationPosition,
    NotificationSize, NotificationAction,
    create_notification_manager, notify_success, notify_error, notify_warning, notify_info,
)
from ontaic.codeeditor import (
    CodeEditor, CodeLanguage, EditorTheme, EditorFontSize, EditorKeyBinding, EditorSnippet,
    create_code_editor, code_snippet, key_binding,
)
from ontaic.calendar import (
    Calendar, CalendarEvent, CalendarView, EventColor, CalendarSlot,
    create_calendar, calendar_event,
)
from ontaic.treeview import (
    TreeView, TreeNode, TreeSelectionMode,
    create_tree_view, tree_node,
)
from ontaic.timeline import (
    Timeline, TimelineItem, TimelineOrientation, TimelineAlign, TimelineSize, TimelineDot,
    create_timeline, timeline_item, timeline_dot,
)
from ontaic.kanban import (
    KanbanBoard, KanbanColumn, KanbanCard, KanbanCardSize, KanbanPriority,
    create_kanban, kanban_column, kanban_card,
)
from ontaic.datagrid import (
    DataGrid, GridColumn, GridSort, GridFilter, GridPagination,
    create_datagrid, grid_column,
)
from ontaic.imagecropper import (
    ImageCropper, CropArea, CropAspect, CropShape,
    create_image_cropper,
)
from ontaic.spreadsheet import (
    Spreadsheet, Cell, SpreadsheetRange, CellStyle,
    create_spreadsheet, cell_style,
)
from ontaic.mediaplayer import (
    MediaPlayer, MediaType, PlayerSize, MediaSource, Caption,
    create_video_player, create_audio_player,
)
from ontaic.chartbuilder import (
    ChartBuilder, ChartType, ChartTheme, ChartDataset, ChartOptions,
    ChartAnimation, create_chart_builder, chart_dataset, chart_options,
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
    # Animation
    "AnimationManager", "AnimatedElement", "FadeIn", "SlideIn", "ScaleIn",
    "Spinner", "Skeleton", "Collapse", "Tabs", "Carousel",
    "FADE_IN", "SLIDE_IN_UP", "SCALE_IN", "BOUNCE", "SPIN", "PULSE", "SHAKE",
    # Accessibility
    "AriaAttributes", "AccessibleComponent", "AccessibleButton", "AccessibleInput",
    "AccessibleSelect", "AccessibleCheckbox", "AccessibleRadio", "AccessibleModal",
    "AccessibleAlert", "SkipLink", "LiveRegion", "generate_keyboard_nav_js", "sr_only",
    # Components
    "Accordion", "Breadcrumb", "Pagination", "Tooltip", "Popover",
    "Alert", "Avatar", "Tag", "StatusDot", "EmptyState",
    # Errors
    "ErrorHandler", "ErrorBoundary", "ErrorInfo",
    "ValidationError", "NotFoundError", "AuthenticationError", "AuthorizationError",
    "retry", "CircuitBreaker", "Cache", "RateLimiter",
    # Performance
    "PerformanceMonitor", "Timer", "timed", "cache",
    "MemoryMonitor", "CpuMonitor", "get_performance_monitor",
    # Testing
    "TestSuite", "ComponentTestSuite", "CompilerTestSuite", "IntegrationTestSuite",
    "TestResult", "create_example_tests",
    # Utilities
    "FileWatcher", "OntaicCompiler",
    # AI
    "generate_component_prompt", "generate_schema_prompt",
    "validate_generated_code", "EXAMPLE_PROMPTS",
    # SSR
    "SSRContext", "SSRMeta", "SSRRenderer", "SSRCache", "SSRMiddleware",
    "ssr_route", "ssr_layout", "get_ssr_renderer", "render_ssr", "render_ssr_page",
    # GraphQL
    "GraphQLClient", "GraphQLField", "GraphQLOperation", "GraphQLResponse",
    "GraphQLQueryBuilder", "GraphQLSchemaBuilder",
    "gql_query", "gql_mutation", "gql_subscription",
    "create_gql_client", "build_schema", "build_query", "build_mutation",
    # Storage
    "Storage", "LocalStorage", "SessionStorage", "MemoryStorage", "IndexedDBStorage",
    "StorageType", "StorageItem",
    "create_storage", "localStorage", "sessionStorage", "memoryStorage",
    # DateTime
    "DateTime", "DateFormat", "DateInfo", "now", "today",
    "from_timestamp", "from_string", "format_date", "format_relative",
    "time_ago", "generate_calendar",
    # REST
    "RestClient", "CRUDBase", "ApiResponse", "RequestConfig", "HttpMethod",
    "UsersCRUD", "PostsCRUD", "CommentsCRUD", "ApiFactory",
    "create_api", "create_client", "create_crud",
    # Drag & Drop
    "Draggable", "Droppable", "Sortable", "DragDropManager", "DragOptions", "DropZone", "DragData",
    "create_drag_drop", "make_draggable", "make_droppable", "make_sortable",
    # Virtual Scroll
    "VirtualList", "VirtualGrid", "VirtualScrollOptions",
    "create_virtual_list", "create_virtual_grid",
    # Form Builder
    "FormBuilder", "FormFieldDef", "FieldOption", "FieldValidation", "FieldType",
    "create_form", "form_field", "field_option", "field_validation",
    # Rich Text
    "RichTextEditor", "EditorToolbar", "EditorFormat", "ToolbarButton",
    "create_editor", "create_markdown_editor",
    # Date Picker
    "DatePicker", "PickerMode", "PickerSize", "PickerPreset", "PRESETS",
    "create_date_picker", "create_date_range_picker",
    # File Upload
    "FileUpload", "UploadedFile", "UploadConfig", "UploadStatus", "FileType",
    "create_file_upload", "create_image_upload",
    # Color Picker
    "ColorPicker", "ColorFormat", "ColorPreset", "DEFAULT_PRESETS",
    "create_color_picker", "color_preset",
    # Wizard
    "FormWizard", "WizardStep", "WizardStepStatus", "WizardLayout",
    "create_wizard", "wizard_step",
    # Markdown
    "MarkdownEditor", "MarkdownViewMode", "MarkdownToolbarItem", "DEFAULT_TOOLBAR",
    "create_markdown_editor",
    # Notifications
    "NotificationManager", "Notification", "NotificationType", "NotificationPosition",
    "NotificationSize", "NotificationAction",
    "create_notification_manager", "notify_success", "notify_error", "notify_warning", "notify_info",
    # Code Editor
    "CodeEditor", "CodeLanguage", "EditorTheme", "EditorFontSize", "EditorKeyBinding", "EditorSnippet",
    "create_code_editor", "code_snippet", "key_binding",
    # Calendar
    "Calendar", "CalendarEvent", "CalendarView", "EventColor", "CalendarSlot",
    "create_calendar", "calendar_event",
    # Tree View
    "TreeView", "TreeNode", "TreeSelectionMode",
    "create_tree_view", "tree_node",
    # Timeline
    "Timeline", "TimelineItem", "TimelineOrientation", "TimelineAlign", "TimelineSize", "TimelineDot",
    "create_timeline", "timeline_item", "timeline_dot",
    # Kanban
    "KanbanBoard", "KanbanColumn", "KanbanCard", "KanbanCardSize", "KanbanPriority",
    "create_kanban", "kanban_column", "kanban_card",
    # Data Grid
    "DataGrid", "GridColumn", "GridSort", "GridFilter", "GridPagination",
    "create_datagrid", "grid_column",
    # Image Cropper
    "ImageCropper", "CropArea", "CropAspect", "CropShape",
    "create_image_cropper",
    # Spreadsheet
    "Spreadsheet", "Cell", "SpreadsheetRange", "CellStyle",
    "create_spreadsheet", "cell_style",
    # Media Player
    "MediaPlayer", "MediaType", "PlayerSize", "MediaSource", "Caption",
    "create_video_player", "create_audio_player",
    # Chart Builder
    "ChartBuilder", "ChartType", "ChartTheme", "ChartDataset", "ChartOptions",
    "ChartAnimation", "create_chart_builder", "chart_dataset", "chart_options",
]
