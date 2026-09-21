"""Testing utilities for ontaic."""
import json
from typing import Any, Callable, Dict, List, Optional
from dataclasses import dataclass, field
from pathlib import Path
import tempfile
import shutil


@dataclass
class TestResult:
    """Test result."""
    name: str
    passed: bool
    message: str = ""
    duration: float = 0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "passed": self.passed,
            "message": self.message,
            "duration": self.duration,
        }


class TestSuite:
    """Test suite for ontaic components."""
    
    def __init__(self, name: str = "Ontaic Tests"):
        self.name = name
        self.tests: List[Callable] = []
        self.results: List[TestResult] = []
        self.setup_func: Optional[Callable] = None
        self.teardown_func: Optional[Callable] = None
    
    def setup(self, func: Callable):
        """Register a setup function."""
        self.setup_func = func
        return func
    
    def teardown(self, func: Callable):
        """Register a teardown function."""
        self.teardown_func = func
        return func
    
    def test(self, name: str = None):
        """Decorator to register a test function."""
        def decorator(func: Callable) -> Callable:
            test_name = name or func.__name__
            func._test_name = test_name
            self.tests.append(func)
            return func
        return decorator
    
    def run(self) -> List[TestResult]:
        """Run all tests."""
        self.results = []
        
        for test_func in self.tests:
            test_name = getattr(test_func, '_test_name', test_func.__name__)
            
            try:
                # Run setup
                if self.setup_func:
                    self.setup_func()
                
                # Run test
                import time
                start = time.time()
                test_func()
                duration = time.time() - start
                
                self.results.append(TestResult(
                    name=test_name,
                    passed=True,
                    duration=duration,
                ))
            except AssertionError as e:
                self.results.append(TestResult(
                    name=test_name,
                    passed=False,
                    message=str(e),
                ))
            except Exception as e:
                self.results.append(TestResult(
                    name=test_name,
                    passed=False,
                    message=f"Error: {str(e)}",
                ))
            finally:
                # Run teardown
                if self.teardown_func:
                    self.teardown_func()
        
        return self.results
    
    def assert_equal(self, actual: Any, expected: Any, message: str = ""):
        """Assert that two values are equal."""
        if actual != expected:
            msg = message or f"Expected {expected}, got {actual}"
            raise AssertionError(msg)
    
    def assert_not_equal(self, actual: Any, expected: Any, message: str = ""):
        """Assert that two values are not equal."""
        if actual == expected:
            msg = message or f"Expected not equal to {expected}"
            raise AssertionError(msg)
    
    def assert_true(self, value: bool, message: str = ""):
        """Assert that a value is True."""
        if not value:
            raise AssertionError(message or "Expected True")
    
    def assert_false(self, value: bool, message: str = ""):
        """Assert that a value is False."""
        if value:
            raise AssertionError(message or "Expected False")
    
    def assert_in(self, item: Any, container: Any, message: str = ""):
        """Assert that an item is in a container."""
        if item not in container:
            msg = message or f"Expected {item} to be in {container}"
            raise AssertionError(msg)
    
    def assert_not_in(self, item: Any, container: Any, message: str = ""):
        """Assert that an item is not in a container."""
        if item in container:
            msg = message or f"Expected {item} not to be in {container}"
            raise AssertionError(msg)
    
    def assert_raises(self, exception: type, func: Callable, *args, **kwargs):
        """Assert that a function raises an exception."""
        try:
            func(*args, **kwargs)
            raise AssertionError(f"Expected {exception.__name__} to be raised")
        except exception:
            pass
    
    def assert_is_none(self, value: Any, message: str = ""):
        """Assert that a value is None."""
        if value is not None:
            raise AssertionError(message or f"Expected None, got {value}")
    
    def assert_is_not_none(self, value: Any, message: str = ""):
        """Assert that a value is not None."""
        if value is None:
            raise AssertionError(message or "Expected not None")
    
    def assert_length(self, container: Any, length: int, message: str = ""):
        """Assert that a container has a specific length."""
        actual_length = len(container)
        if actual_length != length:
            msg = message or f"Expected length {length}, got {actual_length}"
            raise AssertionError(msg)
    
    def get_summary(self) -> Dict[str, Any]:
        """Get test summary."""
        total = len(self.results)
        passed = sum(1 for r in self.results if r.passed)
        failed = total - passed
        
        return {
            "suite": self.name,
            "total": total,
            "passed": passed,
            "failed": failed,
            "results": [r.to_dict() for r in self.results],
        }
    
    def print_summary(self):
        """Print test summary."""
        summary = self.get_summary()
        print(f"\n{'='*60}")
        print(f"Test Suite: {summary['suite']}")
        print(f"{'='*60}")
        print(f"Total: {summary['total']}")
        print(f"Passed: {summary['passed']}")
        print(f"Failed: {summary['failed']}")
        print(f"{'='*60}\n")
        
        for result in self.results:
            status = "✓" if result.passed else "✗"
            print(f"{status} {result.name}")
            if result.message:
                print(f"  {result.message}")
        
        print(f"\n{'='*60}")


class ComponentTestSuite(TestSuite):
    """Test suite for component rendering."""
    
    def assert_html_contains(self, html: str, expected: str, message: str = ""):
        """Assert that HTML contains expected content."""
        if expected not in html:
            msg = message or f"HTML does not contain: {expected}"
            raise AssertionError(msg)
    
    def assert_html_not_contains(self, html: str, not_expected: str, message: str = ""):
        """Assert that HTML does not contain content."""
        if not_expected in html:
            msg = message or f"HTML contains unexpected: {not_expected}"
            raise AssertionError(msg)
    
    def assert_has_attribute(self, html: str, tag: str, attribute: str, message: str = ""):
        """Assert that HTML has a specific attribute on a tag."""
        import re
        pattern = f'<{tag}[^>]*{attribute}[^>]*>'
        if not re.search(pattern, html):
            msg = message or f"HTML does not have {attribute} on <{tag}>"
            raise AssertionError(msg)
    
    def assert_valid_html(self, html: str, message: str = ""):
        """Assert that HTML is valid (basic check)."""
        if not html.strip():
            raise AssertionError(message or "HTML is empty")
        
        # Basic checks
        open_tags = html.count('<')
        close_tags = html.count('>')
        if open_tags != close_tags:
            raise AssertionError(message or "Mismatched tags")


class CompilerTestSuite(TestSuite):
    """Test suite for the compiler."""
    
    def assert_schema_valid(self, schema: Dict[str, Any], message: str = ""):
        """Assert that a schema is valid."""
        required_keys = ["version", "html", "bindings", "events", "initialState"]
        for key in required_keys:
            if key not in schema:
                raise AssertionError(message or f"Schema missing key: {key}")
    
    def assert_has_state(self, schema: Dict[str, Any], state_name: str, message: str = ""):
        """Assert that schema has a specific state."""
        if state_name not in schema.get("initialState", {}):
            raise AssertionError(message or f"Schema missing state: {state_name}")
    
    def assert_has_event(self, schema: Dict[str, Any], node_id: str, event: str, message: str = ""):
        """Assert that schema has a specific event."""
        events = schema.get("events", {})
        if node_id not in events or event not in events[node_id]:
            raise AssertionError(message or f"Schema missing event: {node_id}.{event}")
    
    def assert_html_not_empty(self, schema: Dict[str, Any], message: str = ""):
        """Assert that schema has non-empty HTML."""
        if not schema.get("html", "").strip():
            raise AssertionError(message or "Schema has empty HTML")


class IntegrationTestSuite(TestSuite):
    """Integration test suite."""
    
    def __init__(self, name: str = "Integration Tests"):
        super().__init__(name)
        self.temp_dir = None
    
    def setup(self):
        """Create a temporary directory for tests."""
        self.temp_dir = tempfile.mkdtemp()
    
    def teardown(self):
        """Clean up temporary directory."""
        if self.temp_dir and Path(self.temp_dir).exists():
            shutil.rmtree(self.temp_dir)
    
    def create_test_file(self, filename: str, content: str) -> str:
        """Create a test file."""
        file_path = Path(self.temp_dir) / filename
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content)
        return str(file_path)
    
    def assert_file_exists(self, filename: str, message: str = ""):
        """Assert that a file exists."""
        file_path = Path(self.temp_dir) / filename
        if not file_path.exists():
            raise AssertionError(message or f"File not found: {filename}")
    
    def assert_file_content(self, filename: str, expected: str, message: str = ""):
        """Assert file content matches expected."""
        file_path = Path(self.temp_dir) / filename
        if not file_path.exists():
            raise AssertionError(message or f"File not found: {filename}")
        
        actual = file_path.read_text()
        if actual != expected:
            raise AssertionError(message or f"File content mismatch")


# Example test suite
def create_example_tests() -> ComponentTestSuite:
    """Create an example test suite."""
    suite = ComponentTestSuite("Example Tests")
    
    @suite.test("Box renders correctly")
    def test_box_render():
        from ontaic.component import Box
        box = Box("Hello", class_name="test")
        html = box.render()
        suite.assert_html_contains(html, "Hello")
        suite.assert_html_contains(html, 'class="test"')
    
    @suite.test("Text renders correctly")
    def test_text_render():
        from ontaic.component import Text
        text = Text("Hello", tag="p", class_name="text-lg")
        html = text.render()
        suite.assert_html_contains(html, "Hello")
        suite.assert_html_contains(html, "<p")
    
    @suite.test("Button renders correctly")
    def test_button_render():
        from ontaic.component import Button
        button = Button("Click me", class_name="bg-blue-500")
        html = button.render()
        suite.assert_html_contains(html, "Click me")
        suite.assert_html_contains(html, "button")
    
    return suite


if __name__ == "__main__":
    # Run example tests
    suite = create_example_tests()
    suite.run()
    suite.print_summary()
