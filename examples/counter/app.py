from ontaic.component import Component, State, Box, Text, Button


class Counter(Component):
    count: int = 0

    def render(self):
        return Box(
            Box(
                Text(f"Count: {self.count}", tag="h1", class_name="text-4xl font-bold text-gray-900 mb-4"),
                Text("Click the buttons to update the counter", tag="p", class_name="text-gray-500 mb-6"),
                class_name="text-center"
            ),
            Box(
                Button(
                    "-10",
                    on_click=lambda: self.count - 10,
                    class_name="px-4 py-2 bg-gray-200 hover:bg-gray-300 rounded-lg font-medium"
                ),
                Button(
                    "-1",
                    on_click=lambda: self.count - 1,
                    class_name="px-4 py-2 bg-gray-200 hover:bg-gray-300 rounded-lg font-medium"
                ),
                Button(
                    "Reset",
                    on_click=lambda: 0,
                    class_name="px-4 py-2 bg-red-100 hover:bg-red-200 text-red-700 rounded-lg font-medium"
                ),
                Button(
                    "+1",
                    on_click=lambda: self.count + 1,
                    class_name="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium"
                ),
                Button(
                    "+10",
                    on_click=lambda: self.count + 10,
                    class_name="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium"
                ),
                class_name="flex justify-center gap-2"
            ),
            class_name="min-h-screen flex flex-col items-center justify-center bg-gray-50 p-8"
        )
