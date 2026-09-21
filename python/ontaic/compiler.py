import ast
import json
from typing import Dict, Any, Optional
from pathlib import Path
import sys


class OntaicCompiler:
    """Compiles Python component ASTs to static JSON schemas."""

    def __init__(self):
        self.node_counter = 0

    def compile_file(self, file_path: str) -> Dict[str, Any]:
        source = Path(file_path).read_text()
        tree = ast.parse(source)

        schema = {
            "version": "1.0",
            "html": "",
            "bindings": {},
            "events": {},
            "initialState": {},
            "components": [],
        }

        for node in ast.iter_child_nodes(tree):
            if isinstance(node, ast.ClassDef):
                self._compile_class(node, schema)

        return schema

    def compile_directory(self, dir_path: str) -> Dict[str, Any]:
        combined = {
            "version": "1.0",
            "html": "",
            "bindings": {},
            "events": {},
            "initialState": {},
            "components": [],
        }

        py_files = sorted(Path(dir_path).glob("**/*.py"))
        for py_file in py_files:
            if py_file.name.startswith("_"):
                continue
            try:
                schema = self.compile_file(str(py_file))
                combined["html"] += schema["html"]
                combined["bindings"].update(schema["bindings"])
                combined["events"].update(schema["events"])
                combined["initialState"].update(schema["initialState"])
                combined["components"].extend(schema["components"])
            except Exception as e:
                print(f"[ontaic] Warning: Failed to compile {py_file}: {e}", file=sys.stderr)

        return combined

    def _compile_class(self, node: ast.ClassDef, schema: Dict) -> None:
        class_name = node.name
        state_fields = {}
        render_method = None

        for item in node.body:
            if isinstance(item, ast.Assign):
                for target in item.targets:
                    if isinstance(target, ast.Name):
                        state_name = target.id
                        default_value = self._extract_value(item.value)
                        state_fields[state_name] = default_value
                        schema["initialState"][state_name] = str(default_value)

            elif isinstance(item, ast.FunctionDef) and item.name == "render":
                render_method = item

        if render_method:
            html = self._compile_render_method(render_method, schema)
            schema["html"] = html
            schema["components"].append({
                "name": class_name,
                "states": list(state_fields.keys()),
            })

    def _compile_render_method(self, method: ast.FunctionDef, schema: Dict) -> str:
        for node in ast.walk(method):
            if isinstance(node, ast.Return):
                return self._compile_element(node.value, schema)
        return "<div></div>"

    def _compile_element(self, node: ast.expr, schema: Dict) -> str:
        if isinstance(node, ast.Call):
            return self._compile_call(node, schema)
        elif isinstance(node, ast.JoinedStr):
            return self._compile_fstring(node, schema)
        elif isinstance(node, ast.Constant):
            return str(node.value)
        elif isinstance(node, ast.Name):
            return ""
        return ""

    def _compile_call(self, node: ast.Call, schema: Dict) -> str:
        if isinstance(node.func, ast.Name):
            tag = self._map_tag(node.func.id)
        elif isinstance(node.func, ast.Attribute):
            tag = self._map_tag(node.func.attr)
        else:
            tag = "div"

        class_name = ""
        node_id = f"v-{self.node_counter}"
        self.node_counter += 1
        props = {}
        children = []
        event_bindings = {}

        for kw in node.keywords:
            if kw.arg == "class_name":
                class_name = self._extract_value(kw.value)
            elif kw.arg and kw.arg.startswith("on_"):
                event_name = kw.arg[3:]
                event_bindings[event_name] = self._compile_event_handler(kw.value, schema)
            elif kw.arg == "id":
                node_id = self._extract_value(kw.value)
            elif kw.arg == "src":
                props["src"] = self._extract_value(kw.value)
            elif kw.arg == "alt":
                props["alt"] = self._extract_value(kw.value)
            elif kw.arg == "placeholder":
                props["placeholder"] = self._extract_value(kw.value)
            elif kw.arg == "value":
                props["value"] = self._extract_value(kw.value)
            elif kw.arg == "input_type":
                props["type"] = self._extract_value(kw.value)

        for arg in node.args:
            content = self._compile_element(arg, schema)
            if content:
                children.append(content)

        attrs = f' id="{node_id}"'
        if class_name:
            attrs += f' class="{class_name}"'

        for k, v in props.items():
            if v:
                attrs += f' {k}="{v}"'

        if tag == "img":
            return f"<{tag}{attrs} />"

        inner = "".join(children)

        if event_bindings:
            for event, handler in event_bindings.items():
                schema["events"][node_id] = schema["events"].get(node_id, {})
                schema["events"][node_id][event] = handler

        if inner:
            return f"<{tag}{attrs}>{inner}</{tag}>"
        else:
            return f"<{tag}{attrs}></{tag}>"

    def _compile_fstring(self, node: ast.JoinedStr, schema: Dict) -> str:
        parts = []
        for value in node.values:
            if isinstance(value, ast.Constant):
                parts.append(str(value.value))
            elif isinstance(value, ast.FormattedValue):
                state_ref = self._extract_state_ref(value.value)
                if state_ref:
                    node_id = f"v-{self.node_counter}"
                    self.node_counter += 1
                    schema["bindings"][state_ref] = node_id
                    parts.append(f'<span id="{node_id}">{{{{{state_ref}}}}}</span>')
        return "".join(parts)

    def _extract_state_ref(self, node: ast.expr) -> Optional[str]:
        if isinstance(node, ast.Attribute):
            if isinstance(node.value, ast.Name) and node.value.id == "self":
                return node.attr
        return None

    def _extract_value(self, node: ast.expr) -> Any:
        if isinstance(node, ast.Constant):
            return node.value
        elif isinstance(node, ast.List):
            return [self._extract_value(elt) for elt in node.elts]
        elif isinstance(node, ast.Dict):
            return {
                self._extract_value(k): self._extract_value(v)
                for k, v in zip(node.keys, node.values)
            }
        elif isinstance(node, ast.Name):
            return node.id
        return ""

    def _compile_event_handler(self, node: ast.expr, schema: Dict) -> str:
        if isinstance(node, ast.Lambda):
            return self._compile_expr_to_js(node.body)
        elif isinstance(node, ast.Call):
            return self._compile_call_to_js(node)
        return ""

    def _compile_call_to_js(self, node: ast.Call) -> str:
        if isinstance(node.func, ast.Attribute):
            obj = self._compile_expr_to_js(node.func.value)
            method = node.func.attr
            args = [self._compile_expr_to_js(arg) for arg in node.args]
            return f"update_state('{method}', {', '.join(args)})"
        return ""

    def _compile_expr_to_js(self, node: ast.expr) -> str:
        if isinstance(node, ast.BinOp):
            left = self._compile_expr_to_js(node.left)
            right = self._compile_expr_to_js(node.right)
            op = self._get_js_binop(node.op)
            return f"({left} {op} {right})"
        elif isinstance(node, ast.UnaryOp):
            operand = self._compile_expr_to_js(node.operand)
            op = self._get_js_unaryop(node.op)
            return f"({op}{operand})"
        elif isinstance(node, ast.Constant):
            return json.dumps(node.value)
        elif isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            obj = self._compile_expr_to_js(node.value)
            return f"{obj}.{node.attr}"
        return ""

    def _map_tag(self, name: str) -> str:
        tag_map = {
            "box": "div",
            "text": "span",
            "button": "button",
            "input": "input",
            "image": "img",
            "link": "a",
            "heading": "h1",
            "paragraph": "p",
            "list": "ul",
            "listitem": "li",
        }
        return tag_map.get(name.lower(), name.lower())

    def _get_js_binop(self, op: ast.operator) -> str:
        ops = {
            ast.Add: "+",
            ast.Sub: "-",
            ast.Mult: "*",
            ast.Div: "/",
            ast.Mod: "%",
        }
        return ops.get(type(op), "+")

    def _get_js_unaryop(self, op: ast.unaryop) -> str:
        ops = {
            ast.USub: "-",
            ast.UAdd: "+",
            ast.Not: "!",
        }
        return ops.get(type(op), "")

    def save_schema(self, schema: Dict, output_path: str) -> None:
        Path(output_path).write_text(json.dumps(schema, indent=2))


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Ontaic Python to Schema Compiler")
    parser.add_argument("--input", required=True, help="Input Python file or directory")
    parser.add_argument("--output", required=True, help="Output JSON schema path")
    args = parser.parse_args()

    compiler = OntaicCompiler()
    input_path = Path(args.input)

    if input_path.is_file():
        schema = compiler.compile_file(str(input_path))
    elif input_path.is_dir():
        schema = compiler.compile_directory(str(input_path))
    else:
        print(f"Error: {args.input} is not a valid file or directory", file=sys.stderr)
        sys.exit(1)

    compiler.save_schema(schema, args.output)
    print(f"[ontaic] Compiled schema saved to {args.output}")


if __name__ == "__main__":
    main()
