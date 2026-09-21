"""SaaS dashboard example with charts and metrics."""
from ontaic import Component, Box, Text, Button, Input, Container, Flex, Stack, Card, Divider, Badge
from ontaic import Table, DataTable, Modal, Toast, Navbar, Sidebar, SidebarLink
from ontaic import Chart, LineChart, BarChart, PieChart, DoughnutChart
from ontaic import StatCard, ProgressBar, MetricCard, Gauge, Timeline
from ontaic import If, ForEach


class SaaSDashboard(Component):
    """Main SaaS dashboard application."""
    
    show_modal: bool = False
    notification: str = ""
    current_page: str = "dashboard"
    
    def render(self):
        return Box(
            # Navbar
            Navbar(
                NavLink("/", "Dashboard"),
                NavLink("/analytics", "Analytics"),
                NavLink("/users", "Users"),
                NavLink("/settings", "Settings"),
                brand="SaaS Platform",
                class_name="bg-white shadow-sm",
            ),
            
            # Main layout
            Flex(
                # Sidebar
                Sidebar(
                    SidebarLink("/dashboard", "Dashboard", icon=""),
                    SidebarLink("/analytics", "Analytics", icon=""),
                    SidebarLink("/users", "Users", icon=""),
                    SidebarLink("/orders", "Orders", icon=""),
                    SidebarLink("/settings", "Settings", icon=""),
                    class_name="bg-gray-50 border-r w-64",
                ),
                
                # Main content
                Router(
                    {
                        "/": DashboardPage(),
                        "/analytics": AnalyticsPage(),
                        "/users": UsersPage(),
                        "/settings": SettingsPage(),
                    },
                    initial_route="/",
                ),
                
                class_name="flex",
            ),
            
            # Toast notification
            Toast(
                message=self.notification,
                type="success",
                duration=3000,
            ) if self.notification else Text(""),
            
            class_name="min-h-screen bg-gray-100",
        )


class NavLink(Element):
    """Navigation link component."""
    
    def __init__(self, href: str, text: str, class_name: str = ""):
        self.href = href
        self.link_text = text
        super().__init__("a", class_name=class_name)

    def render(self):
        return f'<a href="{self.href}" class="text-gray-600 hover:text-gray-900 px-3 py-2 text-sm font-medium">{self.link_text}</a>'


class Router(Element):
    """Simple router component."""
    
    def __init__(self, routes: dict, initial_route: str = "/", **kwargs):
        self.routes = routes
        self.initial_route = initial_route
        super().__init__("div", **kwargs)

    def render(self):
        routes_html = []
        for path, component in self.routes.items():
            if hasattr(component, "render"):
                content = component.render()
            else:
                content = str(component)
            routes_html.append(f'<div data-route="{path}" class="route-page">{content}</div>')
        
        return f"""<div id="router" class="flex-1 p-8">
            {"".join(routes_html)}
            <script>
            (function() {{
                const router = document.getElementById('router');
                const pages = router.querySelectorAll('.route-page');
                
                function navigate(path) {{
                    pages.forEach(p => p.style.display = 'none');
                    const page = router.querySelector('[data-route="' + path + '"]');
                    if (page) page.style.display = 'block';
                    window.history.pushState({{}}, '', path);
                }}
                
                window.addEventListener('popstate', () => {{
                    navigate(window.location.pathname);
                }});
                
                navigate(window.location.pathname || '{self.initial_route}');
            }})();
            </script>
        </div>"""


class DashboardPage(Element):
    """Dashboard page with metrics and charts."""
    
    def render(self):
        return f"""<div>
            <h1 class="text-2xl font-bold text-gray-900 mb-6">Dashboard</h1>
            
            <!-- Stats Cards -->
            <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
                {StatCard("Total Revenue", "$45,231", "+20.1% from last month", "positive", "💰").render()}
                {StatCard("Subscriptions", "+2,350", "+180.1% from last month", "positive", "👥").render()}
                {StatCard("Sales", "+12,234", "+19% from last month", "positive", "📈").render()}
                {StatCard("Active Now", "+573", "+201 since last hour", "positive", "⚡").render()}
            </div>
            
            <!-- Charts Row -->
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
                <Card class_name="p-6">
                    <h3 class="text-lg font-semibold mb-4">Revenue Overview</h3>
                    {LineChart(
                        labels=["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul"],
                        datasets=[
                            ChartDataset("Revenue", [4000, 3000, 5000, 4000, 6000, 5000, 7000], borderColor="#3B82F6", fill=True),
                            ChartDataset("Expenses", [2000, 2500, 3000, 2500, 3500, 3000, 4000], borderColor="#EF4444", fill=True),
                        ],
                        height="300px",
                    ).render()}
                </Card>
                
                <Card class_name="p-6">
                    <h3 class="text-lg font-semibold mb-4">Sales by Category</h3>
                    {PieChart(
                        labels=["Electronics", "Clothing", "Home & Garden", "Sports", "Books"],
                        data=[300, 250, 200, 150, 100],
                        height="300px",
                    ).render()}
                </Card>
            </div>
            
            <!-- Recent Orders -->
            <Card class_name="p-6">
                <h3 class="text-lg font-semibold mb-4">Recent Orders</h3>
                {DataTable(
                    columns=[
                        {"key": "id", "header": "Order ID"},
                        {"key": "customer", "header": "Customer"},
                        {"key": "product", "header": "Product"},
                        {"key": "amount", "header": "Amount"},
                        {"key": "status", "header": "Status"},
                    ],
                    data=[
                        {"id": "ORD-001", "customer": "John Doe", "product": "MacBook Pro", "amount": "$2,499", "status": "Completed"},
                        {"id": "ORD-002", "customer": "Jane Smith", "product": "iPhone 14", "amount": "$999", "status": "Processing"},
                        {"id": "ORD-003", "customer": "Bob Johnson", "product": "AirPods Pro", "amount": "$249", "status": "Completed"},
                        {"id": "ORD-004", "customer": "Alice Brown", "product": "iPad Air", "amount": "$599", "status": "Pending"},
                        {"id": "ORD-005", "customer": "Charlie Wilson", "product": "Apple Watch", "amount": "$399", "status": "Completed"},
                    ],
                ).render()}
            </Card>
        </div>"""


class AnalyticsPage(Element):
    """Analytics page with detailed charts."""
    
    def render(self):
        return f"""<div>
            <h1 class="text-2xl font-bold text-gray-900 mb-6">Analytics</h1>
            
            <!-- Metrics -->
            <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
                {MetricCard("Page Views", "12,345", [10, 15, 12, 18, 14, 20, 16, 22, 18, 25], "blue").render()}
                {MetricCard("Unique Visitors", "8,901", [8, 12, 10, 15, 12, 18, 14, 20, 16, 22], "green").render()}
                {MetricCard("Bounce Rate", "45.2%", [50, 48, 45, 42, 40, 38, 35, 33, 30, 28], "red").render()}
                {MetricCard("Avg. Session", "3:45", [3.2, 3.5, 3.8, 4.0, 3.7, 4.2, 3.9, 4.5, 4.1, 4.8], "purple").render()}
            </div>
            
            <!-- Charts -->
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
                <Card class_name="p-6">
                    <h3 class="text-lg font-semibold mb-4">Traffic Sources</h3>
                    {BarChart(
                        labels=["Direct", "Social", "Organic", "Referral", "Email"],
                        datasets=[
                            ChartDataset("Visitors", [4000, 3000, 5000, 2000, 1500], backgroundColor="#3B82F6"),
                        ],
                        height="300px",
                    ).render()}
                </Card>
                
                <Card class_name="p-6">
                    <h3 class="text-lg font-semibold mb-4">Conversion Funnel</h3>
                    {DoughnutChart(
                        labels=["Visitors", "Leads", "Customers", "Repeat"],
                        data=[10000, 2500, 800, 300],
                        height="300px",
                    ).render()}
                </Card>
            </div>
            
            <!-- Progress -->
            <Card class_name="p-6 mb-8">
                <h3 class="text-lg font-semibold mb-4">Monthly Goals</h3>
                <div class="space-y-4">
                    <div>
                        <div class="flex justify-between mb-1">
                            <span class="text-sm font-medium">Revenue Goal</span>
                            <span class="text-sm text-gray-500">$45,231 / $50,000</span>
                        </div>
                        {ProgressBar(45231, 50000, "blue").render()}
                    </div>
                    <div>
                        <div class="flex justify-between mb-1">
                            <span class="text-sm font-medium">New Customers</span>
                            <span class="text-sm text-gray-500">2,350 / 2,500</span>
                        </div>
                        {ProgressBar(2350, 2500, "green").render()}
                    </div>
                    <div>
                        <div class="flex justify-between mb-1">
                            <span class="text-sm font-medium">Support Tickets</span>
                            <span class="text-sm text-gray-500">89 / 100</span>
                        </div>
                        {ProgressBar(89, 100, "yellow").render()}
                    </div>
                </div>
            </Card>
            
            <!-- Gauges -->
            <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
                {Gauge(72, 0, 100, "CPU Usage", "blue", "md").render()}
                {Gauge(45, 0, 100, "Memory", "green", "md").render()}
                {Gauge(89, 0, 100, "Disk", "yellow", "md").render()}
                {Gauge(23, 0, 100, "Network", "red", "md").render()}
            </div>
        </div>"""


class UsersPage(Element):
    """Users management page."""
    
    def render(self):
        return f"""<div>
            <h1 class="text-2xl font-bold text-gray-900 mb-6">Users</h1>
            
            <Card class_name="p-6">
                <div class="flex justify-between items-center mb-4">
                    <h3 class="text-lg font-semibold">All Users</h3>
                    <button class="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600">Add User</button>
                </div>
                {DataTable(
                    columns=[
                        {"key": "name", "header": "Name"},
                        {"key": "email", "header": "Email"},
                        {"key": "role", "header": "Role"},
                        {"key": "status", "header": "Status"},
                        {"key": "joined", "header": "Joined"},
                    ],
                    data=[
                        {"name": "John Doe", "email": "john@example.com", "role": "Admin", "status": "Active", "joined": "Jan 1, 2024"},
                        {"name": "Jane Smith", "email": "jane@example.com", "role": "User", "status": "Active", "joined": "Jan 5, 2024"},
                        {"name": "Bob Johnson", "email": "bob@example.com", "role": "User", "status": "Inactive", "joined": "Jan 10, 2024"},
                        {"name": "Alice Brown", "email": "alice@example.com", "role": "Editor", "status": "Active", "joined": "Jan 15, 2024"},
                        {"name": "Charlie Wilson", "email": "charlie@example.com", "role": "User", "status": "Pending", "joined": "Jan 20, 2024"},
                    ],
                ).render()}
            </Card>
        </div>"""


class SettingsPage(Element):
    """Settings page."""
    
    def render(self):
        return f"""<div>
            <h1 class="text-2xl font-bold text-gray-900 mb-6">Settings</h1>
            
            <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
                <Card class_name="p-6">
                    <h3 class="text-lg font-semibold mb-4">Profile</h3>
                    <div class="space-y-4">
                        <input type="text" placeholder="Full Name" value="John Doe" class="w-full px-3 py-2 border border-gray-300 rounded-lg">
                        <input type="email" placeholder="Email" value="john@example.com" class="w-full px-3 py-2 border border-gray-300 rounded-lg">
                        <button class="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600">Save Changes</button>
                    </div>
                </Card>
                
                <Card class_name="p-6">
                    <h3 class="text-lg font-semibold mb-4">Notifications</h3>
                    <div class="space-y-4">
                        <label class="flex items-center">
                            <input type="checkbox" checked class="mr-2">
                            <span>Email notifications</span>
                        </label>
                        <label class="flex items-center">
                            <input type="checkbox" checked class="mr-2">
                            <span>Push notifications</span>
                        </label>
                        <label class="flex items-center">
                            <input type="checkbox" class="mr-2">
                            <span>SMS notifications</span>
                        </label>
                    </div>
                </Card>
                
                <Card class_name="p-6">
                    <h3 class="text-lg font-semibold mb-4">Recent Activity</h3>
                    {Timeline(
                        items=[
                            {"title": "Profile updated", "date": "2 hours ago", "description": "You updated your profile information"},
                            {"title": "Password changed", "date": "1 day ago", "description": "You changed your password"},
                            {"title": "Account created", "date": "1 week ago", "description": "You created your account"},
                        ],
                    ).render()}
                </Card>
            </div>
        </div>"""


if __name__ == "__main__":
    app = SaaSDashboard()
    print("SaaS dashboard created!")
    print("Run 'ontaic dev' to start the development server.")
