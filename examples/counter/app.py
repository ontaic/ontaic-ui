from ontaic.component import Component, State, Box, Text, Button


class Counter(Component):
    count: int = 0

    def render(self):
        return Box(
            Box(
                Text(f"Clicks: {self.count}", tag="h1", class_name="text-4xl font-bold text-gray-900"),
                class_name="text-center mb-6"
            ),
            Box(
                Button(
                    "Increment",
                    on_click=lambda: self.count + 1,
                    class_name="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg font-medium"
                ),
                Button(
                    "Decrement",
                    on_click=lambda: self.count - 1,
                    class_name="bg-gray-200 hover:bg-gray-300 text-gray-800 px-6 py-3 rounded-lg font-medium ml-2"
                ),
                Button(
                    "Reset",
                    on_click=lambda: 0,
                    class_name="bg-red-100 hover:bg-red-200 text-red-700 px-6 py-3 rounded-lg font-medium ml-2"
                ),
                class_name="flex justify-center gap-2"
            ),
            class_name="min-h-screen flex flex-col items-center justify-center bg-gray-50 p-8"
        )
