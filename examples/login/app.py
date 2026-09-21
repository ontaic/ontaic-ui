from ontaic.component import Component, State, Box, Text, Button, Input, Image


class Login(Component):
    email: str = ""
    password: str = ""
    error: str = ""

    def render(self):
        return Box(
            Box(
                Box(
                    Image(
                        src="/logo.svg",
                        alt="Ontaic",
                        class_name="h-12 w-auto mb-6"
                    ),
                    Text("Welcome back", tag="h1", class_name="text-2xl font-bold text-gray-900 mb-2"),
                    Text("Sign in to your account", class_name="text-gray-500 mb-8"),
                    Box(
                        Box(
                            Text("Email", tag="label", class_name="block text-sm font-medium text-gray-700 mb-1"),
                            Input(
                                input_type="email",
                                placeholder="you@example.com",
                                value=self.email,
                                class_name="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                            ),
                            class_name="mb-4"
                        ),
                        Box(
                            Text("Password", tag="label", class_name="block text-sm font-medium text-gray-700 mb-1"),
                            Input(
                                input_type="password",
                                placeholder="Enter your password",
                                value=self.password,
                                class_name="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                            ),
                            class_name="mb-6"
                        ),
                        Button(
                            "Sign In",
                            class_name="w-full bg-blue-600 hover:bg-blue-700 text-white py-2 rounded-lg font-medium"
                        ),
                        class_name="space-y-4"
                    ),
                    class_name="w-full max-w-sm"
                ),
                class_name="flex items-center justify-center min-h-screen bg-gray-50 p-4"
            ),
            class_name="min-h-screen"
        )
