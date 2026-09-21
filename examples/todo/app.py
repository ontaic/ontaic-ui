"""Todo app example with forms and routing."""
from ontaic import Component, Box, Text, Button, Input, Card, Container, Flex, Stack, Badge, Divider
from ontaic import FormField, Form, Checkbox
from ontaic import Router, NavLink, Navbar
from ontaic import If, ForEach


class TodoApp(Component):
    """Main todo application with routing."""
    
    def render(self):
        return Box(
            Navbar(
                NavLink("/", "Home"),
                NavLink("/todos", "Todos"),
                NavLink("/about", "About"),
                brand="Ontaic Todo",
                class_name="bg-white shadow-sm",
            ),
            Router(
                {
                    "/": HomePage(),
                    "/todos": TodoPage(),
                    "/about": AboutPage(),
                },
                initial_route="/",
            ),
            class_name="min-h-screen bg-gray-100",
        )


class HomePage(Component):
    """Home page component."""
    
    def render(self):
        return Container(
            Box(
                Text("Welcome to Ontaic Todo", tag="h1", class_name="text-3xl font-bold mb-4"),
                Text("A simple todo app built with Ontaic", tag="p", class_name="text-gray-600 mb-6"),
                Button(
                    "Get Started",
                    on_click=lambda: self.navigate("/todos"),
                    class_name="bg-blue-500 text-white px-6 py-3 rounded-lg hover:bg-blue-600",
                ),
                class_name="text-center py-12",
            ),
            class_name="max-w-4xl mx-auto py-8",
        )


class TodoPage(Component):
    """Todo page with list and form."""
    
    todos: str = '[{"id": 1, "text": "Learn Ontaic", "done": false}, {"id": 2, "text": "Build an app", "done": true}]'
    new_todo: str = ""
    show_completed: bool = True
    
    def render(self):
        return Container(
            Box(
                Text("My Todos", tag="h1", class_name="text-2xl font-bold mb-6"),
                
                # Add todo form
                Flex(
                    Input(
                        placeholder="Add a new todo...",
                        value=self.new_todo,
                        class_name="flex-1 px-4 py-2 border border-gray-300 rounded-lg",
                    ),
                    Button(
                        "Add",
                        on_click=lambda: self.add_todo(),
                        class_name="bg-green-500 text-white px-4 py-2 rounded-lg hover:bg-green-600",
                    ),
                    class_name="gap-2 mb-6",
                ),
                
                # Filter toggle
                Checkbox(
                    name="show_completed",
                    label="Show completed",
                    checked=self.show_completed,
                    class_name="mb-4",
                ),
                
                Divider(class_name="my-4"),
                
                # Todo list
                Text("Todos will appear here", tag="p", class_name="text-gray-500"),
                
                class_name="bg-white p-6 rounded-lg shadow",
            ),
            class_name="max-w-2xl mx-auto py-8",
        )
    
    def add_todo(self):
        """Add a new todo."""
        print(f"Adding todo: {self.new_todo}")
        self.new_todo = ""


class AboutPage(Component):
    """About page component."""
    
    def render(self):
        return Container(
            Box(
                Text("About", tag="h1", class_name="text-2xl font-bold mb-4"),
                Text("This todo app was built with Ontaic, a Python UI framework.", tag="p", class_name="text-gray-600"),
                Text("Features:", tag="h2", class_name="text-xl font-semibold mt-6 mb-2"),
                Text("- Client-side routing", tag="li", class_name="text-gray-600"),
                Text("- Form handling", tag="li", class_name="text-gray-600"),
                Text("- State management", tag="li", class_name="text-gray-600"),
                Text("- Hot reload", tag="li", class_name="text-gray-600"),
                class_name="bg-white p-6 rounded-lg shadow",
            ),
            class_name="max-w-2xl mx-auto py-8",
        )


if __name__ == "__main__":
    app = TodoApp()
    print("Todo app created!")
    print("Run 'ontaic dev' to start the development server.")
