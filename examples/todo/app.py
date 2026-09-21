from ontaic.component import Component, State, Box, Text, Button, Input


class TodoApp(Component):
    todos: str = "[]"
    new_todo: str = ""

    def render(self):
        return Box(
            Box(
                Text("Ontaic Todo", tag="h1", class_name="text-3xl font-bold text-gray-900 mb-8"),
                Box(
                    Input(
                        placeholder="Add a new todo...",
                        value=self.new_todo,
                        class_name="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    ),
                    Button(
                        "Add",
                        on_click=lambda: self.todos,
                        class_name="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg ml-2"
                    ),
                    class_name="flex items-center gap-2 mb-6"
                ),
                Box(
                    Text("No todos yet. Add one above!", class_name="text-gray-500 text-center py-8"),
                    class_name="bg-white rounded-xl shadow-sm border border-gray-200"
                ),
                class_name="max-w-md mx-auto p-8"
            ),
            class_name="min-h-screen bg-gray-50"
        )
