from ontaic.component import Component, State, Box, Text, Button, Input


class Dashboard(Component):
    user_name: str = "Admin"
    notifications: int = 3
    dark_mode: bool = False
    search_query: str = ""
    counter: int = 0

    def render(self):
        return Box(
            # Header
            Box(
                Box(
                    Text("Ontaic Dashboard", tag="h1", class_name="text-2xl font-bold text-white"),
                    Box(
                        Text(f"Notifications: {self.notifications}", class_name="text-sm text-gray-300 mr-4"),
                        Button(
                            "Toggle Theme",
                            on_click=lambda: self.dark_mode,
                            class_name="text-sm px-3 py-1 bg-gray-700 hover:bg-gray-600 text-white rounded"
                        ),
                        class_name="flex items-center"
                    ),
                    class_name="flex items-center justify-between"
                ),
                class_name="bg-gray-900 p-4"
            ),
            # Main content
            Box(
                # Stats cards
                Box(
                    Box(
                        Box(
                            Text("Users", class_name="text-sm text-gray-500 mb-1"),
                            Text("1,234", class_name="text-2xl font-bold text-gray-900"),
                            Text("+12%", class_name="text-sm text-green-600"),
                            class_name="p-4"
                        ),
                        class_name="bg-white rounded-lg shadow"
                    ),
                    Box(
                        Box(
                            Text("Revenue", class_name="text-sm text-gray-500 mb-1"),
                            Text("$45,678", class_name="text-2xl font-bold text-gray-900"),
                            Text("+8%", class_name="text-sm text-green-600"),
                            class_name="p-4"
                        ),
                        class_name="bg-white rounded-lg shadow"
                    ),
                    Box(
                        Box(
                            Text("Orders", class_name="text-sm text-gray-500 mb-1"),
                            Text("567", class_name="text-2xl font-bold text-gray-900"),
                            Text("+23%", class_name="text-sm text-green-600"),
                            class_name="p-4"
                        ),
                        class_name="bg-white rounded-lg shadow"
                    ),
                    Box(
                        Box(
                            Text("Conversion", class_name="text-sm text-gray-500 mb-1"),
                            Text("3.2%", class_name="text-2xl font-bold text-gray-900"),
                            Text("+1.5%", class_name="text-sm text-green-600"),
                            class_name="p-4"
                        ),
                        class_name="bg-white rounded-lg shadow"
                    ),
                    class_name="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6"
                ),
                # Counter section
                Box(
                    Box(
                        Text("Interactive Counter", tag="h2", class_name="text-lg font-semibold mb-4"),
                        Text(f"Count: {self.counter}", tag="p", class_name="text-3xl font-bold text-blue-600 mb-4"),
                        Box(
                            Button("-5", on_click=lambda: self.counter - 5, class_name="px-4 py-2 bg-gray-200 hover:bg-gray-300 rounded font-medium"),
                            Button("-1", on_click=lambda: self.counter - 1, class_name="px-4 py-2 bg-gray-200 hover:bg-gray-300 rounded font-medium"),
                            Button("Reset", on_click=lambda: self.counter - self.counter, class_name="px-4 py-2 bg-red-100 hover:bg-red-200 text-red-700 rounded font-medium"),
                            Button("+1", on_click=lambda: self.counter + 1, class_name="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded font-medium"),
                            Button("+5", on_click=lambda: self.counter + 5, class_name="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded font-medium"),
                            class_name="flex gap-2"
                        ),
                        class_name="bg-white rounded-lg shadow p-6"
                    ),
                    # Search section
                    Box(
                        Text("Search", tag="h2", class_name="text-lg font-semibold mb-4"),
                        Box(
                            Input(
                                placeholder="Search components...",
                                class_name="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                            ),
                            Button("Search", class_name="ml-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg"),
                            class_name="flex"
                        ),
                        class_name="bg-white rounded-lg shadow p-6"
                    ),
                    class_name="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6"
                ),
                # Recent activity
                Box(
                    Text("Recent Activity", tag="h2", class_name="text-lg font-semibold mb-4"),
                    Box(
                        Text("New user registered", class_name="text-sm text-gray-900"),
                        Text("2 minutes ago", class_name="text-xs text-gray-500"),
                        class_name="py-3 border-b border-gray-100"
                    ),
                    Box(
                        Text("Order #1234 placed", class_name="text-sm text-gray-900"),
                        Text("5 minutes ago", class_name="text-xs text-gray-500"),
                        class_name="py-3 border-b border-gray-100"
                    ),
                    Box(
                        Text("Payment received", class_name="text-sm text-gray-900"),
                        Text("10 minutes ago", class_name="text-xs text-gray-500"),
                        class_name="py-3 border-b border-gray-100"
                    ),
                    Box(
                        Text("Product updated", class_name="text-sm text-gray-900"),
                        Text("15 minutes ago", class_name="text-xs text-gray-500"),
                        class_name="py-3"
                    ),
                    class_name="bg-white rounded-lg shadow p-6"
                ),
                class_name="p-6"
            ),
            # Footer
            Box(
                Text("Built with Ontaic Engine", class_name="text-sm text-gray-400"),
                class_name="bg-gray-900 p-4 text-center"
            ),
            class_name="min-h-screen bg-gray-100"
        )
