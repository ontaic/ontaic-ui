import pytest
import json
import tempfile
import os
from pathlib import Path
from ontaic.compiler import OntaicCompiler


class TestOntaicCompiler:
    """Tests for the Ontaic Python AST compiler."""

    def setup_method(self):
        self.compiler = OntaicCompiler()

    def _create_temp_file(self, content: str, suffix: str = '.py') -> str:
        """Create a temporary file and return its path."""
        fd, path = tempfile.mkstemp(suffix=suffix)
        with os.fdopen(fd, 'w') as f:
            f.write(content)
        return path

    def test_compile_empty_file(self):
        """Test compiling an empty Python file."""
        path = self._create_temp_file("")
        schema = self.compiler.compile_file(path)
        os.unlink(path)

        assert schema["version"] == "1.0"
        assert schema["html"] == ""
        assert schema["bindings"] == {}
        assert schema["events"] == {}
        assert schema["initialState"] == {}

    def test_compile_simple_component(self):
        """Test compiling a simple component with no state."""
        content = """
from ontaic.component import Component, Box, Text

class Simple(Component):
    def render(self):
        return Box(
            Text("Hello World", tag="h1", class_name="text-xl"),
            class_name="p-4"
        )
"""
        path = self._create_temp_file(content)
        schema = self.compiler.compile_file(path)
        os.unlink(path)

        assert "Hello World" in schema["html"]
        assert 'class="text-xl"' in schema["html"]
        assert 'class="p-4"' in schema["html"]
        assert len(schema["components"]) == 1
        assert schema["components"][0]["name"] == "Simple"

    def test_compile_state_fields(self):
        """Test compiling component with annotated state fields."""
        content = """
from ontaic.component import Component, Box, Text

class Counter(Component):
    count: int = 0
    name: str = "test"

    def render(self):
        return Box(Text("Hello"))
"""
        path = self._create_temp_file(content)
        schema = self.compiler.compile_file(path)
        os.unlink(path)

        assert "count" in schema["initialState"]
        assert schema["initialState"]["count"] == "0"
        assert "name" in schema["initialState"]
        assert schema["initialState"]["name"] == "test"

    def test_compile_boolean_state(self):
        """Test compiling component with boolean state."""
        content = """
from ontaic.component import Component, Box

class Toggle(Component):
    active: bool = True

    def render(self):
        return Box("Content")
"""
        path = self._create_temp_file(content)
        schema = self.compiler.compile_file(path)
        os.unlink(path)

        assert schema["initialState"]["active"] == "true"

    def test_compile_fstring_bindings(self):
        """Test that f-string state references create proper bindings."""
        content = """
from ontaic.component import Component, Box, Text

class Counter(Component):
    count: int = 0

    def render(self):
        return Box(
            Text(f"Count: {self.count}", tag="h1"),
            class_name="p-4"
        )
"""
        path = self._create_temp_file(content)
        schema = self.compiler.compile_file(path)
        os.unlink(path)

        assert "count" in schema["bindings"]
        assert len(schema["bindings"]["count"]) > 0
        assert schema["bindings"]["count"].startswith("v-")

    def test_compile_event_increment(self):
        """Test that increment event handlers compile correctly."""
        content = """
from ontaic.component import Component, Box, Button

class Counter(Component):
    count: int = 0

    def render(self):
        return Box(
            Button("Add", on_click=lambda: self.count + 1),
            class_name="p-4"
        )
"""
        path = self._create_temp_file(content)
        schema = self.compiler.compile_file(path)
        os.unlink(path)

        assert len(schema["events"]) > 0
        first_event = list(schema["events"].values())[0]
        assert "click" in first_event
        assert "update_state('count'" in first_event["click"]
        assert "+ 1" in first_event["click"]

    def test_compile_event_decrement(self):
        """Test that decrement event handlers compile correctly."""
        content = """
from ontaic.component import Component, Box, Button

class Counter(Component):
    count: int = 0

    def render(self):
        return Box(
            Button("Subtract", on_click=lambda: self.count - 1),
            class_name="p-4"
        )
"""
        path = self._create_temp_file(content)
        schema = self.compiler.compile_file(path)
        os.unlink(path)

        first_event = list(schema["events"].values())[0]
        assert "update_state('count'" in first_event["click"]
        assert "- 1" in first_event["click"]

    def test_compile_event_reset(self):
        """Test that reset event handlers compile correctly."""
        content = """
from ontaic.component import Component, Box, Button

class Counter(Component):
    count: int = 0

    def render(self):
        return Box(
            Button("Reset", on_click=lambda: 0),
            class_name="p-4"
        )
"""
        path = self._create_temp_file(content)
        schema = self.compiler.compile_file(path)
        os.unlink(path)

        first_event = list(schema["events"].values())[0]
        assert "update_state('count', '0')" in first_event["click"]

    def test_compile_button_element(self):
        """Test that Button elements compile to correct HTML."""
        content = """
from ontaic.component import Component, Box, Button

class App(Component):
    def render(self):
        return Box(
            Button("Click Me", class_name="bg-blue-500 text-white"),
            class_name="p-4"
        )
"""
        path = self._create_temp_file(content)
        schema = self.compiler.compile_file(path)
        os.unlink(path)

        assert "<button" in schema["html"]
        assert "Click Me" in schema["html"]
        assert 'class="bg-blue-500 text-white"' in schema["html"]

    def test_compile_nested_components(self):
        """Test that nested components compile correctly."""
        content = """
from ontaic.component import Component, Box, Text, Button

class App(Component):
    title: str = "Hello"

    def render(self):
        return Box(
            Box(
                Text(f"Title: {self.title}", tag="h1"),
                class_name="header"
            ),
            Box(
                Button("Click", class_name="btn"),
                class_name="content"
            ),
            class_name="container"
        )
"""
        path = self._create_temp_file(content)
        schema = self.compiler.compile_file(path)
        os.unlink(path)

        assert 'class="container"' in schema["html"]
        assert 'class="header"' in schema["html"]
        assert 'class="content"' in schema["html"]
        assert "title" in schema["bindings"]

    def test_compile_input_element(self):
        """Test that Input elements compile correctly."""
        content = """
from ontaic.component import Component, Box, Input

class Form(Component):
    def render(self):
        return Box(
            Input(placeholder="Enter text", class_name="input-field"),
            class_name="p-4"
        )
"""
        path = self._create_temp_file(content)
        schema = self.compiler.compile_file(path)
        os.unlink(path)

        assert "<input" in schema["html"]
        assert 'placeholder="Enter text"' in schema["html"]
        assert 'class="input-field"' in schema["html"]

    def test_compile_multiple_components(self):
        """Test compiling multiple components in one file."""
        content = """
from ontaic.component import Component, Box

class Header(Component):
    def render(self):
        return Box("Header", class_name="header")

class Footer(Component):
    def render(self):
        return Box("Footer", class_name="footer")
"""
        path = self._create_temp_file(content)
        schema = self.compiler.compile_file(path)
        os.unlink(path)

        assert len(schema["components"]) == 2
        names = [c["name"] for c in schema["components"]]
        assert "Header" in names
        assert "Footer" in names

    def test_compile_image_element(self):
        """Test that Image elements compile correctly."""
        content = """
from ontaic.component import Component, Box, Image

class App(Component):
    def render(self):
        return Box(
            Image(src="/logo.png", alt="Logo", class_name="h-10"),
            class_name="p-4"
        )
"""
        path = self._create_temp_file(content)
        schema = self.compiler.compile_file(path)
        os.unlink(path)

        assert "<img" in schema["html"]
        assert 'src="/logo.png"' in schema["html"]
        assert 'alt="Logo"' in schema["html"]

    def test_save_schema(self):
        """Test saving schema to file."""
        schema = {
            "version": "1.0",
            "html": "<div>test</div>",
            "bindings": {},
            "events": {},
            "initialState": {},
            "components": []
        }

        fd, path = tempfile.mkstemp(suffix='.json')
        os.close(fd)

        self.compiler.save_schema(schema, path)
        with open(path) as result:
            loaded = json.load(result)
        os.unlink(path)

        assert loaded["html"] == "<div>test</div>"
        assert loaded["version"] == "1.0"

    def test_compile_directory(self):
        """Test compiling a directory of Python files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with open(os.path.join(tmpdir, "header.py"), 'w') as f:
                f.write("""
from ontaic.component import Component, Box

class Header(Component):
    def render(self):
        return Box("Header")
""")

            with open(os.path.join(tmpdir, "footer.py"), 'w') as f:
                f.write("""
from ontaic.component import Component, Box

class Footer(Component):
    def render(self):
        return Box("Footer")
""")

            with open(os.path.join(tmpdir, "__init__.py"), 'w') as f:
                f.write("")

            schema = self.compiler.compile_directory(tmpdir)

            assert len(schema["components"]) == 2
            names = [c["name"] for c in schema["components"]]
            assert "Header" in names
            assert "Footer" in names


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
