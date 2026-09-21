"""Additional component variants for ontaic."""
from typing import Any, Callable, Dict, List, Optional
from dataclasses import dataclass, field


class Accordion:
    """Accordion/collapsible component."""
    
    def __init__(
        self,
        items: List[Dict[str, str]],
        allowMultiple: bool = False,
        defaultOpen: List[int] = None,
        class_name: str = "",
    ):
        self.items = items
        self.allowMultiple = allowMultiple
        self.defaultOpen = defaultOpen or []
        self.class_name = class_name
    
    def render(self) -> str:
        accordion_id = f"accordion-{id(self)}"
        
        items_html = ""
        for i, item in enumerate(self.items):
            is_open = i in self.defaultOpen
            display = "block" if is_open else "none"
            transform = "rotate(180deg)" if is_open else "rotate(0deg)"
            
            items_html += f"""
            <div class="border-b">
                <button 
                    class="w-full px-4 py-3 text-left font-medium flex justify-between items-center hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-blue-500"
                    onclick="toggleAccordion('{accordion_id}', {i})"
                    aria-expanded="{str(is_open).lower()}"
                    aria-controls="{accordion_id}-panel-{i}"
                >
                    <span>{item.get('header', '')}</span>
                    <svg class="w-5 h-5 transform transition-transform" style="transform: {transform}" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
                    </svg>
                </button>
                <div 
                    id="{accordion_id}-panel-{i}"
                    class="overflow-hidden transition-all duration-300"
                    style="display: {display}; max-height: {'auto' if is_open else '0'}"
                    role="region"
                    aria-labelledby="{accordion_id}-header-{i}"
                >
                    <div class="px-4 pb-3 text-gray-700">
                        {item.get('content', '')}
                    </div>
                </div>
            </div>
            """
        
        return f"""
        <div id="{accordion_id}" class="border rounded-lg {self.class_name}" role="presentation">
            {items_html}
        </div>
        <script>
        function toggleAccordion(id, index) {{
            const accordion = document.getElementById(id);
            const panels = accordion.querySelectorAll('[id^="' + id + '-panel-"]');
            const buttons = accordion.querySelectorAll('button');
            
            panels.forEach((panel, i) => {{
                if (i === index) {{
                    const isOpen = panel.style.display === 'block';
                    panel.style.display = isOpen ? 'none' : 'block';
                    panel.style.maxHeight = isOpen ? '0' : panel.scrollHeight + 'px';
                    buttons[i].setAttribute('aria-expanded', !isOpen);
                    buttons[i].querySelector('svg').style.transform = isOpen ? 'rotate(0deg)' : 'rotate(180deg)';
                }}
            }});
        }}
        </script>
        """


class Breadcrumb:
    """Breadcrumb navigation component."""
    
    def __init__(
        self,
        items: List[Dict[str, str]],
        separator: str = "/",
        class_name: str = "",
    ):
        self.items = items
        self.separator = separator
        self.class_name = class_name
    
    def render(self) -> str:
        items_html = ""
        for i, item in enumerate(self.items):
            is_last = i == len(self.items) - 1
            if is_last:
                items_html += f"""
                <li class="flex items-center">
                    <span class="text-gray-500" aria-current="page">{item.get('label', '')}</span>
                </li>
                """
            else:
                items_html += f"""
                <li class="flex items-center">
                    <a href="{item.get('href', '#')}" class="text-blue-600 hover:text-blue-800">{item.get('label', '')}</a>
                    <span class="mx-2 text-gray-400">{self.separator}</span>
                </li>
                """
        
        return f"""
        <nav aria-label="Breadcrumb" class="{self.class_name}">
            <ol class="flex items-center flex-wrap">
                {items_html}
            </ol>
        </nav>
        """


class Pagination:
    """Pagination component."""
    
    def __init__(
        self,
        currentPage: int,
        totalPages: int,
        onPageChange: str = "",
        class_name: str = "",
    ):
        self.currentPage = currentPage
        self.totalPages = totalPages
        self.onPageChange = onPageChange
        self.class_name = class_name
    
    def render(self) -> str:
        pagination_id = f"pagination-{id(self)}"
        
        items_html = ""
        
        # Previous button
        prev_disabled = "disabled" if self.currentPage <= 1 else ""
        items_html += f"""
        <li>
            <button 
                class="px-3 py-2 border rounded-l-lg hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500 {prev_disabled}"
                onclick="{self.onPageChange}({self.currentPage - 1})"
                {prev_disabled}
                aria-label="Previous page"
            >
                ←
            </button>
        </li>
        """
        
        # Page numbers
        for page in range(1, self.totalPages + 1):
            if page == self.currentPage:
                items_html += f"""
                <li>
                    <button 
                        class="px-3 py-2 border bg-blue-500 text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                        aria-current="page"
                    >
                        {page}
                    </button>
                </li>
                """
            elif abs(page - self.currentPage) <= 2 or page == 1 or page == self.totalPages:
                items_html += f"""
                <li>
                    <button 
                        class="px-3 py-2 border hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500"
                        onclick="{self.onPageChange}({page})"
                    >
                        {page}
                    </button>
                </li>
                """
            elif abs(page - self.currentPage) == 3:
                items_html += """
                <li>
                    <span class="px-3 py-2 border">...</span>
                </li>
                """
        
        # Next button
        next_disabled = "disabled" if self.currentPage >= self.totalPages else ""
        items_html += f"""
        <li>
            <button 
                class="px-3 py-2 border rounded-r-lg hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500 {next_disabled}"
                onclick="{self.onPageChange}({self.currentPage + 1})"
                {next_disabled}
                aria-label="Next page"
            >
                →
            </button>
        </li>
        """
        
        return f"""
        <nav aria-label="Pagination" class="{self.class_name}">
            <ul class="flex items-center">
                {items_html}
            </ul>
        </nav>
        """


class Tooltip:
    """Tooltip component."""
    
    def __init__(
        self,
        text: str,
        position: str = "top",  # top, bottom, left, right
        delay: int = 200,
    ):
        self.text = text
        self.position = position
        self.delay = delay
    
    def render(self, content: str) -> str:
        position_classes = {
            "top": "bottom-full left-1/2 -translate-x-1/2 mb-2",
            "bottom": "top-full left-1/2 -translate-x-1/2 mt-2",
            "left": "right-full top-1/2 -translate-y-1/2 mr-2",
            "right": "left-full top-1/2 -translate-y-1/2 ml-2",
        }
        
        position_class = position_classes.get(self.position, position_classes["top"])
        
        return f"""
        <div class="relative inline-block group">
            {content}
            <div class="absolute {position_class} px-2 py-1 text-sm text-white bg-gray-900 rounded opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200 pointer-events-none whitespace-nowrap z-50">
                {self.text}
                <div class="absolute w-2 h-2 bg-gray-900 transform rotate-45"></div>
            </div>
        </div>
        """


class Popover:
    """Popover component."""
    
    def __init__(
        self,
        title: str,
        content: str,
        position: str = "bottom",
        trigger: str = "click",
    ):
        self.title = title
        self.content = content
        self.position = position
        self.trigger = trigger
    
    def render(self, trigger_content: str) -> str:
        popover_id = f"popover-{id(self)}"
        
        position_classes = {
            "top": "bottom-full left-1/2 -translate-x-1/2 mb-2",
            "bottom": "top-full left-1/2 -translate-x-1/2 mt-2",
            "left": "right-full top-1/2 -translate-y-1/2 mr-2",
            "right": "left-full top-1/2 -translate-y-1/2 ml-2",
        }
        
        position_class = position_classes.get(self.position, position_classes["bottom"])
        
        trigger_event = f"onclick=\"togglePopover('{popover_id}')\"" if self.trigger == "click" else f"onmouseenter=\"showPopover('{popover_id}')\" onmouseleave=\"hidePopover('{popover_id}')\""
        
        return f"""
        <div class="relative inline-block">
            <div {trigger_event}>{trigger_content}</div>
            <div 
                id="{popover_id}"
                class="absolute {position_class} w-64 bg-white border rounded-lg shadow-lg opacity-0 invisible transition-all duration-200 z-50"
            >
                <div class="px-4 py-2 border-b font-medium">{self.title}</div>
                <div class="px-4 py-3 text-sm text-gray-700">{self.content}</div>
            </div>
        </div>
        <script>
        function togglePopover(id) {{
            const popover = document.getElementById(id);
            popover.classList.toggle('opacity-0');
            popover.classList.toggle('invisible');
        }}
        
        function showPopover(id) {{
            const popover = document.getElementById(id);
            popover.classList.remove('opacity-0', 'invisible');
        }}
        
        function hidePopover(id) {{
            const popover = document.getElementById(id);
            popover.classList.add('opacity-0', 'invisible');
        }}
        </script>
        """


class Alert:
    """Alert/banner component."""
    
    def __init__(
        self,
        title: str = "",
        message: str = "",
        type: str = "info",
        dismissible: bool = False,
        icon: str = "",
        class_name: str = "",
    ):
        self.title = title
        self.message = message
        self.alert_type = type
        self.dismissible = dismissible
        self.icon = icon
        self.class_name = class_name
    
    def render(self) -> str:
        type_classes = {
            "info": "bg-blue-50 text-blue-800 border-blue-200",
            "success": "bg-green-50 text-green-800 border-green-200",
            "warning": "bg-yellow-50 text-yellow-800 border-yellow-200",
            "error": "bg-red-50 text-red-800 border-red-200",
        }
        
        icon_colors = {
            "info": "text-blue-500",
            "success": "text-green-500",
            "warning": "text-yellow-500",
            "error": "text-red-500",
        }
        
        title_html = f'<h4 class="font-medium">{self.title}</h4>' if self.title else ""
        
        dismiss_button = ""
        if self.dismissible:
            dismiss_button = """
            <button class="ml-auto -mx-1.5 -my-1.5 rounded-lg focus:ring-2 focus:ring-offset-2 p-1.5 hover:bg-gray-100" onclick="this.parentElement.remove()">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                </svg>
            </button>
            """
        
        return f"""
        <div class="flex items-start p-4 rounded-lg border {type_classes.get(self.alert_type, type_classes['info'])} {self.class_name}" role="alert">
            {f'<span class="{icon_colors.get(self.alert_type, "text-blue-500")}">{self.icon}</span>' if self.icon else ''}
            <div class="flex-1">
                {title_html}
                {f'<p class="text-sm">{self.message}</p>' if self.message else ''}
            </div>
            {dismiss_button}
        </div>
        """


class Avatar:
    """Avatar component."""
    
    def __init__(
        self,
        src: str = "",
        alt: str = "",
        name: str = "",
        size: str = "md",
        class_name: str = "",
    ):
        self.src = src
        self.alt = alt
        self.name = name
        self.size = size
        self.class_name = class_name
    
    def render(self) -> str:
        size_classes = {
            "xs": "w-6 h-6 text-xs",
            "sm": "w-8 h-8 text-sm",
            "md": "w-10 h-10 text-base",
            "lg": "w-12 h-12 text-lg",
            "xl": "w-16 h-16 text-xl",
        }
        
        size_class = size_classes.get(self.size, size_classes["md"])
        
        if self.src:
            return f"""
            <img 
                src="{self.src}" 
                alt="{self.alt or self.name}"
                class="{size_class} rounded-full object-cover {self.class_name}"
            />
            """
        else:
            initials = "".join(word[0].upper() for word in self.name.split()[:2]) if self.name else "?"
            return f"""
            <div class="{size_class} rounded-full bg-blue-500 text-white flex items-center justify-center font-medium {self.class_name}">
                {initials}
            </div>
            """


class Badge:
    """Badge/tag component."""
    
    def __init__(
        self,
        text: str,
        variant: str = "default",
        size: str = "md",
        class_name: str = "",
    ):
        self.text = text
        self.variant = variant
        self.size = size
        self.class_name = class_name
    
    def render(self) -> str:
        variant_classes = {
            "default": "bg-gray-100 text-gray-800",
            "primary": "bg-blue-100 text-blue-800",
            "success": "bg-green-100 text-green-800",
            "warning": "bg-yellow-100 text-yellow-800",
            "danger": "bg-red-100 text-red-800",
        }
        
        size_classes = {
            "sm": "px-2 py-0.5 text-xs",
            "md": "px-2.5 py-0.5 text-sm",
            "lg": "px-3 py-1 text-base",
        }
        
        variant_class = variant_classes.get(self.variant, variant_classes["default"])
        size_class = size_classes.get(self.size, size_classes["md"])
        
        return f"""
        <span class="inline-flex items-center font-medium rounded-full {variant_class} {size_class} {self.class_name}">
            {self.text}
        </span>
        """


class Tag:
    """Tag with remove button component."""
    
    def __init__(
        self,
        text: str,
        onRemove: str = "",
        variant: str = "default",
        class_name: str = "",
    ):
        self.text = text
        self.onRemove = onRemove
        self.variant = variant
        self.class_name = class_name
    
    def render(self) -> str:
        variant_classes = {
            "default": "bg-gray-100 text-gray-800",
            "primary": "bg-blue-100 text-blue-800",
            "success": "bg-green-100 text-green-800",
            "warning": "bg-yellow-100 text-yellow-800",
            "danger": "bg-red-100 text-red-800",
        }
        
        variant_class = variant_classes.get(self.variant, variant_classes["default"])
        
        remove_button = ""
        if self.onRemove:
            remove_button = f"""
            <button 
                onclick="{self.onRemove}"
                class="ml-1 -mr-1 p-0.5 rounded-full hover:bg-gray-200"
                aria-label="Remove"
            >
                <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                </svg>
            </button>
            """
        
        return f"""
        <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-sm font-medium {variant_class} {self.class_name}">
            {self.text}
            {remove_button}
        </span>
        """


class StatusDot:
    """Status indicator dot component."""
    
    def __init__(
        self,
        status: str = "success",
        label: str = "",
        size: str = "md",
    ):
        self.status = status
        self.label = label
        self.size = size
    
    def render(self) -> str:
        status_colors = {
            "success": "bg-green-500",
            "warning": "bg-yellow-500",
            "danger": "bg-red-500",
            "info": "bg-blue-500",
            "offline": "bg-gray-400",
        }
        
        size_classes = {
            "sm": "w-2 h-2",
            "md": "w-3 h-3",
            "lg": "w-4 h-4",
        }
        
        color = status_colors.get(self.status, status_colors["offline"])
        size_class = size_classes.get(self.size, size_classes["md"])
        
        label_html = f'<span class="ml-2 text-sm text-gray-700">{self.label}</span>' if self.label else ""
        
        return f"""
        <div class="flex items-center">
            <span class="{size_class} rounded-full {color}"></span>
            {label_html}
        </div>
        """


class Divider:
    """Divider/separator component."""
    
    def __init__(
        self,
        text: str = "",
        orientation: str = "horizontal",
        class_name: str = "",
    ):
        self.text = text
        self.orientation = orientation
        self.class_name = class_name
    
    def render(self) -> str:
        if self.orientation == "vertical":
            return f"""
            <div class="w-px h-full bg-gray-200 {self.class_name}" role="separator" aria-orientation="vertical"></div>
            """
        
        if self.text:
            return f"""
            <div class="relative {self.class_name}">
                <div class="absolute inset-0 flex items-center">
                    <div class="w-full border-t border-gray-200"></div>
                </div>
                <div class="relative flex justify-center text-sm">
                    <span class="px-2 bg-white text-gray-500">{self.text}</span>
                </div>
            </div>
            """
        
        return f"""
        <hr class="border-gray-200 {self.class_name}" role="separator" aria-orientation="horizontal" />
        """


class EmptyState:
    """Empty state component."""
    
    def __init__(
        self,
        title: str,
        description: str = "",
        icon: str = "",
        actionText: str = "",
        onAction: str = "",
        class_name: str = "",
    ):
        self.title = title
        self.description = description
        self.icon = icon
        self.actionText = actionText
        self.onAction = onAction
        self.class_name = class_name
    
    def render(self) -> str:
        icon_html = f'<div class="text-6xl text-gray-400 mb-4">{self.icon}</div>' if self.icon else ""
        
        action_html = ""
        if self.actionText:
            action_html = f"""
            <button 
                onclick="{self.onAction}"
                class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
            >
                {self.actionText}
            </button>
            """
        
        return f"""
        <div class="text-center py-12 {self.class_name}">
            {icon_html}
            <h3 class="text-lg font-medium text-gray-900 mb-2">{self.title}</h3>
            {f'<p class="text-gray-500 mb-4">{self.description}</p>' if self.description else ''}
            {action_html}
        </div>
        """
