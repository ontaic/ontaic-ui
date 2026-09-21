"""Admin dashboard example with tables and modals."""
from ontaic import Component, Box, Text, Button, Input, Container, Flex, Stack, Card, Divider, Badge
from ontaic import Table, DataTable, Modal, Toast, ConfirmDialog
from ontaic import Navbar, Sidebar, SidebarLink


class AdminDashboard(Component):
    """Admin dashboard with sidebar and main content."""
    
    show_modal: bool = False
    show_confirm: bool = False
    selected_user: str = ""
    notification: str = ""
    
    def render(self):
        return Box(
            # Navbar
            Navbar(
                NavLink("/", "Home"),
                NavLink("/users", "Users"),
                NavLink("/settings", "Settings"),
                brand="Admin Dashboard",
                class_name="bg-white shadow-sm",
            ),
            
            # Main layout
            Flex(
                # Sidebar
                Sidebar(
                    SidebarLink("/dashboard", "Dashboard", icon=""),
                    SidebarLink("/users", "Users", icon=""),
                    SidebarLink("/orders", "Orders", icon=""),
                    SidebarLink("/settings", "Settings", icon=""),
                    class_name="bg-gray-50 border-r",
                ),
                
                # Main content
                Box(
                    # Stats cards
                    Flex(
                        StatsCard("Total Users", "1,234", "+12%"),
                        StatsCard("Revenue", "$45,678", "+8%"),
                        StatsCard("Orders", "567", "+5%"),
                        StatsCard("Conversion", "3.2%", "+0.5%"),
                        class_name="grid grid-cols-4 gap-4 mb-8",
                    ),
                    
                    # Users table
                    Card(
                        Text("Recent Users", tag="h2", class_name="text-lg font-semibold mb-4"),
                        DataTable(
                            columns=[
                                {"key": "name", "header": "Name"},
                                {"key": "email", "header": "Email"},
                                {"key": "role", "header": "Role"},
                                {"key": "status", "header": "Status"},
                            ],
                            data=[
                                {"name": "John Doe", "email": "john@example.com", "role": "Admin", "status": "Active"},
                                {"name": "Jane Smith", "email": "jane@example.com", "role": "User", "status": "Active"},
                                {"name": "Bob Johnson", "email": "bob@example.com", "role": "User", "status": "Inactive"},
                                {"name": "Alice Brown", "email": "alice@example.com", "role": "Editor", "status": "Active"},
                                {"name": "Charlie Wilson", "email": "charlie@example.com", "role": "User", "status": "Pending"},
                            ],
                            page_size=5,
                        ),
                        class_name="p-6",
                    ),
                    
                    class_name="flex-1 p-8",
                ),
                
                class_name="flex",
            ),
            
            # Modal
            Modal(
                Text("Add New User", tag="h3", class_name="text-lg font-semibold mb-4"),
                Input(placeholder="Name", class_name="w-full px-3 py-2 border rounded-lg mb-3"),
                Input(placeholder="Email", class_name="w-full px-3 py-2 border rounded-lg mb-3"),
                Button("Save", class_name="bg-blue-500 text-white px-4 py-2 rounded-lg"),
                title="Add User",
                is_open=self.show_modal,
                size="md",
            ),
            
            # Confirm dialog
            ConfirmDialog(
                message="Are you sure you want to delete this user?",
                title="Delete User",
                is_open=self.show_confirm,
            ),
            
            # Toast notification
            Toast(
                message=self.notification,
                type="success",
                duration=3000,
            ) if self.notification else Text(""),
            
            class_name="min-h-screen bg-gray-100",
        )


class StatsCard(Element):
    """Statistics card component."""
    
    def __init__(self, title: str, value: str, change: str = "", class_name: str = ""):
        self.card_title = title
        self.value = value
        self.change = change
        
        change_color = "text-green-500" if change.startswith("+") else "text-red-500"
        change_html = f'<span class="{change_color} text-sm">{change}</span>' if change else ""
        
        super().__init__("div", class_name=class_name)

    def render(self):
        return f"""<div class="bg-white rounded-lg shadow p-6">
            <div class="text-sm font-medium text-gray-500">{self.card_title}</div>
            <div class="mt-2 text-3xl font-bold text-gray-900">{self.value}</div>
            {f'<div class="mt-1">{self.change}</div>' if self.change else ''}
        </div>"""


class NavLink(Element):
    """Navigation link component."""
    
    def __init__(self, href: str, text: str, class_name: str = ""):
        self.href = href
        self.link_text = text
        super().__init__("a", class_name=class_name)

    def render(self):
        return f'<a href="{self.href}" class="text-gray-600 hover:text-gray-900 px-3 py-2 text-sm font-medium">{self.link_text}</a>'


if __name__ == "__main__":
    app = AdminDashboard()
    print("Admin dashboard created!")
    print("Run 'ontaic dev' to start the development server.")
