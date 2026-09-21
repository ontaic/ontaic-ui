"""Simple todo app without routing for testing."""
from ontaic import Component, Box, Text, Button, Input, Container, Flex, Stack, Divider


class SimpleTodo(Component):
    """Simple todo list component."""
    
    todos: str = "Learn Ontaic,Build an app,Deploy to production"
    new_todo: str = ""
    
    def render(self):
        return Container(
            Box(
                Text("Simple Todo", tag="h1", class_name="text-2xl font-bold mb-4"),
                
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
                
                Divider(class_name="my-4"),
                
                # Todo list
                Stack(
                    Text("Todo items will appear here", tag="p", class_name="text-gray-500"),
                    class_name="space-y-2",
                ),
                
                class_name="bg-white p-6 rounded-lg shadow",
            ),
            class_name="max-w-2xl mx-auto py-8",
        )
    
    def add_todo(self):
        """Add a new todo."""
        print(f"Adding todo: {self.new_todo}")
        self.new_todo = ""


if __name__ == "__main__":
    app = SimpleTodo()
    print("Simple todo app created!")
