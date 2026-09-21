"""Modal, dialog, and overlay components."""
from typing import Any, Callable, Optional
from ontaic.component import Element


class Modal(Element):
    """Modal dialog component."""
    
    def __init__(
        self,
        *children,
        title: str = "",
        is_open: bool = False,
        close_on_overlay: bool = True,
        close_on_escape: bool = True,
        size: str = "md",  # sm, md, lg, xl, full
        class_name: str = "",
        **kwargs,
    ):
        self.title = title
        self.is_open = is_open
        self.close_on_overlay = close_on_overlay
        self.close_on_escape = close_on_escape
        self.size = size

        super().__init__("div", class_name=class_name, **kwargs)
        self.children = list(children)

    def render(self):
        size_classes = {
            "sm": "max-w-sm",
            "md": "max-w-md",
            "lg": "max-w-lg",
            "xl": "max-w-xl",
            "full": "max-w-4xl",
        }
        size_class = size_classes.get(self.size, "max-w-md")
        
        display = "flex" if self.is_open else "none"
        
        title_html = ""
        if self.title:
            title_html = f"""<div class="flex items-center justify-between p-4 border-b">
                <h3 class="text-lg font-semibold text-gray-900">{self.title}</h3>
                <button onclick="this.closest('.modal').style.display='none'" class="text-gray-400 hover:text-gray-600">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                    </svg>
                </button>
            </div>"""
        
        inner = "".join(
            child.render() if hasattr(child, "render") else str(child)
            for child in self.children
        )
        
        overlay_click = "this.closest('.modal').style.display='none'" if self.close_on_overlay else ""
        
        return f"""<div class="modal fixed inset-0 z-50 overflow-y-auto" style="display:{display}" aria-modal="true">
            <div class="flex items-center justify-center min-h-screen px-4 pt-4 pb-20 text-center sm:block sm:p-0">
                <div class="fixed inset-0 transition-opacity bg-gray-500 bg-opacity-75" onclick="{overlay_click}"></div>
                <span class="hidden sm:inline-block sm:align-middle sm:h-screen">&#8203;</span>
                <div class="inline-block {size_class} w-full p-6 my-8 overflow-hidden text-left align-bottom transition-all transform bg-white shadow-xl rounded-2xl sm:align-middle">
                    {title_html}
                    <div class="p-4">
                        {inner}
                    </div>
                </div>
            </div>
        </div>"""


class ConfirmDialog(Element):
    """Confirmation dialog with OK/Cancel buttons."""
    
    def __init__(
        self,
        message: str = "Are you sure?",
        title: str = "Confirm",
        confirm_text: str = "Confirm",
        cancel_text: str = "Cancel",
        on_confirm: Optional[Callable] = None,
        on_cancel: Optional[Callable] = None,
        is_open: bool = False,
        class_name: str = "",
        **kwargs,
    ):
        self.message = message
        self.confirm_text = confirm_text
        self.cancel_text = cancel_text
        self.on_confirm = on_confirm
        self.on_cancel = on_cancel

        super().__init__("div", class_name=class_name, **kwargs)

    def render(self):
        return Modal(
            title="",
            is_open=self.is_open,
            size="sm",
            class_name="confirm-dialog",
            children=[
                f'<div class="text-center"><p class="text-gray-700">{self.message}</p></div>',
                f"""<div class="flex justify-center gap-3 mt-6">
                    <button class="px-4 py-2 text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200" 
                        onclick="this.closest('.modal').style.display='none'">{self.cancel_text}</button>
                    <button class="px-4 py-2 text-white bg-red-500 rounded-lg hover:bg-red-600"
                        onclick="this.closest('.modal').style.display='none'">{self.confirm_text}</button>
                </div>""",
            ],
        ).render()


class AlertDialog(Element):
    """Alert dialog with a single OK button."""
    
    def __init__(
        self,
        message: str = "",
        title: str = "Alert",
        button_text: str = "OK",
        is_open: bool = False,
        class_name: str = "",
        **kwargs,
    ):
        self.message = message
        self.button_text = button_text

        super().__init__("div", class_name=class_name, **kwargs)

    def render(self):
        return Modal(
            title="",
            is_open=self.is_open,
            size="sm",
            class_name="alert-dialog",
            children=[
                f'<div class="text-center"><p class="text-gray-700">{self.message}</p></div>',
                f"""<div class="flex justify-center mt-6">
                    <button class="px-4 py-2 text-white bg-blue-500 rounded-lg hover:bg-blue-600"
                        onclick="this.closest('.modal').style.display='none'">{self.button_text}</button>
                </div>""",
            ],
        ).render()


class Drawer(Element):
    """Drawer/slide-out panel."""
    
    def __init__(
        self,
        *children,
        side: str = "right",  # left, right, top, bottom
        is_open: bool = False,
        size: str = "md",  # sm, md, lg, full
        title: str = "",
        class_name: str = "",
        **kwargs,
    ):
        self.side = side
        self.is_open = is_open
        self.size = size
        self.title = title

        super().__init__("div", class_name=class_name, **kwargs)
        self.children = list(children)

    def render(self):
        size_classes = {
            "sm": "w-64",
            "md": "w-80",
            "lg": "w-96",
            "full": "w-full",
        }
        
        side_classes = {
            "left": "left-0",
            "right": "right-0",
            "top": "top-0",
            "bottom": "bottom-0",
        }
        
        transform_classes = {
            "left": "-translate-x-full",
            "right": "translate-x-full",
            "top": "-translate-y-full",
            "bottom": "translate-y-full",
        }
        
        size_class = size_classes.get(self.size, "w-80")
        side_class = side_classes.get(self.side, "right-0")
        transform_class = transform_classes.get(self.side, "translate-x-full")
        
        if self.is_open:
            transform_class = "translate-x-0"
        
        title_html = ""
        if self.title:
            title_html = f"""<div class="flex items-center justify-between p-4 border-b">
                <h3 class="text-lg font-semibold text-gray-900">{self.title}</h3>
                <button onclick="this.closest('.drawer').classList.add('{transform_class}')" class="text-gray-400 hover:text-gray-600">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                    </svg>
                </button>
            </div>"""
        
        inner = "".join(
            child.render() if hasattr(child, "render") else str(child)
            for child in self.children
        )
        
        return f"""<div class="drawer fixed inset-0 z-50 overflow-hidden" style="{'display:block' if self.is_open else 'display:none'}">
            <div class="absolute inset-0 bg-gray-500 bg-opacity-75"></div>
            <div class="absolute inset-0 overflow-hidden">
                <div class="absolute inset-0 bg-gray-500 bg-opacity-75"></div>
                <div class="fixed {side_class} {size_class} h-full bg-white shadow-xl transform transition-transform {transform_class}">
                    {title_html}
                    <div class="p-4 overflow-y-auto h-full">
                        {inner}
                    </div>
                </div>
            </div>
        </div>"""


class Toast(Element):
    """Toast notification."""
    
    def __init__(
        self,
        message: str = "",
        type: str = "info",  # info, success, warning, error
        duration: int = 3000,
        position: str = "top-right",  # top-left, top-right, bottom-left, bottom-right
        class_name: str = "",
        **kwargs,
    ):
        self.message = message
        self.toast_type = type
        self.duration = duration
        self.position = position

        super().__init__("div", class_name=class_name, **kwargs)

    def render(self):
        type_classes = {
            "info": "bg-blue-500",
            "success": "bg-green-500",
            "warning": "bg-yellow-500",
            "error": "bg-red-500",
        }
        
        position_classes = {
            "top-left": "top-4 left-4",
            "top-right": "top-4 right-4",
            "bottom-left": "bottom-4 left-4",
            "bottom-right": "bottom-4 right-4",
        }
        
        bg_class = type_classes.get(self.toast_type, "bg-blue-500")
        pos_class = position_classes.get(self.position, "top-4 right-4")
        
        return f"""<div class="toast fixed {pos_class} z-50 {bg_class} text-white px-4 py-3 rounded-lg shadow-lg transform transition-all duration-300 opacity-0 translate-y-2"
            style="animation: fadeIn 0.3s forwards;">
            <div class="flex items-center">
                <span class="flex-1">{self.message}</span>
                <button onclick="this.parentElement.parentElement.remove()" class="ml-4 text-white hover:text-gray-200">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                    </svg>
                </button>
            </div>
            <script>
            setTimeout(() => {{
                this.closest('.toast').style.opacity = '0';
                setTimeout(() => this.closest('.toast')?.remove(), 300);
            }}, {self.duration});
            </script>
        </div>"""
