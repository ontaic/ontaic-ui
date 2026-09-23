"""Registry crawler: fetch public JSON registries and import into Ontaic.

Usage:
  python registry_crawler.py fetch             # download all 4 registries
  python registry_crawler.py shadcn button     # import one component
  python registry_crawler.py all               # import everything

This is the "steal the design system" layer — we grab pre-tested,
pixel-perfect components from Radix + Tailwind registries and emit
them as Ontaic-native component classes so they run in the WASM runtime.
"""
import json
import os
import sys
import hashlib
import pathlib
import urllib.request
from typing import Any, Dict, List, Optional

REGISTRIES = {
    "shadcn": {
        "url": "https://ui.shadcn.com/r/index.json",
        "base": "https://ui.shadcn.com/r",
        "component_dir": "registry/components/shadcn",
    },
    "aceternity": {
        "url": "https://ui.aceternity.com/registry.json",
        "base": "https://ui.aceternity.com",
        "component_dir": "registry/components/aceternity",
    },
    "magicui": {
        "url": "https://magicui.design/r/index.json",
        "base": "https://magicui.design/r",
        "component_dir": "registry/components/magicui",
    },
    "cult": {
        "url": "https://cult-ui.com/r/index.json",
        "base": "https://cult-ui.com/r",
        "component_dir": "registry/components/cult",
    },
}

HERE = pathlib.Path(__file__).parent


def fetch_json(url: str, timeout: int = 60) -> Any:
    req = urllib.request.Request(url, headers={"User-Agent": "ontaic-registry-crawler/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read())


def fetch_text(url: str, timeout: int = 60) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "ontaic-registry-crawler/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8")


def save_registry_raw(name: str, data: Any, registry_dir: pathlib.Path):
    registry_dir.mkdir(parents=True, exist_ok=True)
    out = registry_dir / f"{name}.json"
    out.write_text(json.dumps(data, indent=2), encoding="utf-8")
    print(f"  {name}: raw registry -> {out} ({len(json.dumps(data))} bytes)")


def parse_shadcn_index(data: Any) -> List[Dict[str, str]]:
    """shadcn index.json: list of {name, files:[...], ...}."""
    comps = []
    if isinstance(data, list):
        for item in data:
            comps.append(item)
    elif isinstance(data, dict):
        comps = data.get("components", data.get("items", []))
    return comps


def parse_generic_registry(data: Any, registry_key: str) -> List[Dict[str, Any]]:
    """Generic parser for any registry with a 'components' or 'items' list."""
    if isinstance(data, dict):
        comps = data.get("components") or data.get("items") or []
    elif isinstance(data, list):
        comps = data
    else:
        comps = []
    return comps


def download_component(registry: dict, comp: Dict[str, Any], registry_name: str) -> Optional[Dict[str, Any]]:
    """Download a single component's source files from its registry."""
    name = comp.get("name") or comp.get("title", "")
    files = comp.get("files") or comp.get("components", [])
    
    if isinstance(files, str):
        files = [{"name": files, "path": files}]
    
    downloaded = {"name": name, "registry": registry_name, "files": []}
    
    for f in files:
        if isinstance(f, str):
            f = {"path": f}
        fname = f.get("name") or pathlib.Path(f.get("path", "")).name
        fpath = f.get("path", f.get("name", ""))
        url = f"{registry['base']}/{fpath.lstrip('/')}"
        
        try:
            content = fetch_text(url)
            downloaded["files"].append({
                "name": fname,
                "path": fpath,
                "url": url,
                "content": content,
                "size": len(content),
            })
            print(f"    [{registry_name}] {name}/{fname} ({len(content)} bytes)")
        except Exception as e:
            print(f"    [{registry_name}] {name}/{fname}: FAILED ({e})")
    
    return downloaded if downloaded["files"] else None


def emit_ontaic_component(comp_data: Dict[str, Any], out_dir: pathlib.Path) -> str:
    """Convert a downloaded TS/Tailwind component into an Ontaic component file."""
    name = comp_data["name"]
    registry = comp_data["registry"]
    reg_conf = REGISTRIES[registry]
    out_dir.mkdir(parents=True, exist_ok=True)
    
    files = comp_data["files"]
    ts_code = ""
    tailwind_classes = ""
    css_content = ""
    
    for f in files:
        if f["name"].endswith((".ts", ".tsx")):
            ts_code += f["content"] + "\n\n"
        elif f["name"].endswith(".css"):
            css_content += f["content"] + "\n\n"
    
    for line in ts_code.split("\n"):
        if "className=" in line:
            start = line.find('"')
            if start >= 0:
                end = line.find('"', start + 1)
                if end > start:
                    tailwind_classes += line[start+1:end] + "\n"
    
    class_name = name.replace("-", " ").title().replace(" ", "")
    
    python_code = f'''"""
Ontaic adapter for {registry} {name}
Source: {reg_conf["base"]} (stolen, not written).
Emits the same HTML + Tailwind classes so the WASM runtime patches it directly.
"""
from ontaic.component import Element


class {class_name}Component(Element):
    """{registry}/{name} — imported from registry."""

    def __init__(self, **kwargs):
        super().__init__("div", class_name=kwargs.get("class_name", ""), **kwargs)
        self.source_registry = "{registry}"
        self.source_name = "{name}"
        self.tailwind_classes = """{tailwind_classes.strip()}"""
        self.original_ts = ''' + repr(ts_code[:2000]) + f'''

    def render(self) -> str:
        # We re-emit the tailwind-markup from the original component.
        # The Ontaic WASM runtime patches the DOM directly — no server round-trip.
        cls = self.tailwind_classes.strip()
        return f'<div class="{{cls}}">{{self._children_html}}</div>'

    _children_html = ""


def create_{name.replace("-", "_")}() -> {class_name}Component:
    return {class_name}Component()
'''
    
    safe_name = name.replace("/", "_").replace("-", "_")
    out = out_dir / f"{safe_name}.py"
    out.write_text(python_code, encoding="utf-8")
    print(f"  -> emitted {out.name}")
    return str(out)


def cmd_fetch():
    """Fetch all registries raw JSON to registry/ dir."""
    registry_dir = HERE / "registry"
    
    for name, conf in REGISTRIES.items():
        print(f"Fetching {name} registry...")
        try:
            data = fetch_json(conf["url"])
            save_registry_raw(name, data, registry_dir)
        except Exception as e:
            print(f"  FAILED: {e}")


def cmd_import(registry_name: str = "all"):
    """Import all components from all (or one) registry."""
    imported = 0
    
    for name, conf in REGISTRIES.items():
        if registry_name != "all" and registry_name != name:
            continue
            
        raw_path = HERE / "registry" / f"{name}.json"
        if not raw_path.exists():
            print(f"{name}: run 'fetch' first")
            continue
        
        print(f"Importing {name} components...")
        data = json.loads(raw_path.read_text(encoding="utf-8"))
        
    if name == "shadcn":
        comps = parse_shadcn_index(data)
    else:
        comps = parse_generic_registry(data, name)
    
    out_dir = HERE / conf["component_dir"]
    out_dir.mkdir(parents=True, exist_ok=True)
    
    for comp in comps[:50]:  # limit per registry
        try:
            downloaded = download_component(conf, comp, name)
            if downloaded:
                emit_ontaic_component(downloaded, out_dir)
                imported += 1
        except Exception as e:
            print(f"  {comp.get('name', '?')}: {e}")
    
    print(f"Imported {imported} components")


def cmd_shadcn(name: str):
    """Import one shadcn component by name."""
    print(f"Importing shadcn/{name}...")
    conf = REGISTRIES["shadcn"]
    
    raw_path = HERE / "registry" / "shadcn.json"
    data = json.loads(raw_path.read_text(encoding="utf-8"))
    
    comp = None
    for c in data:
        if c.get("name") == name:
            comp = c
            break
    
    if not comp:
        print(f"Component '{name}' not found in shadcn registry.")
        return
    
    downloaded = download_component(conf, comp, "shadcn")
    if downloaded:
        out_dir = HERE / conf["component_dir"]
        emit_ontaic_component(downloaded, out_dir)
        print("Done.")
    else:
        print("No files downloaded.")


def cmd_get(registry_name: str, comp_name: str):
    """Get a single component from any registry by name."""
    conf = REGISTRIES[registry_name]
    
    raw_path = HERE / "registry" / f"{registry_name}.json"
    if not raw_path.exists():
        print(f"{registry_name} registry not fetched. Run 'fetch' first.")
        return
    
    data = json.loads(raw_path.read_text(encoding="utf-8"))
    
    if registry_name == "shadcn":
        comps = parse_shadcn_index(data)
    else:
        comps = parse_generic_registry(data, registry_name)
    
    comp = None
    for c in comps:
        if c.get("name") == comp_name:
            comp = c
            break
    
    if not comp:
        print(f"'{comp_name}' not found in {registry_name} registry.")
        available = [c.get('name', '?') for c in comps[:10]]
        print(f"Available: {available}")
        return
    
    downloaded = download_component(conf, comp, registry_name)
    if downloaded:
        out_dir = HERE / conf["component_dir"]
        emit_ontaic_component(downloaded, out_dir)
        print("Done.")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return
    
    cmd = sys.argv[1]
    
    if cmd == "fetch":
        cmd_fetch()
    elif cmd == "all":
        cmd_import("all")
    elif cmd == "import":
        reg = sys.argv[2] if len(sys.argv) > 2 else "all"
        cmd_import(reg)
    elif cmd == "get" and len(sys.argv) > 3:
        # Usage: python registry_crawler.py get shadcn button
        cmd_get(sys.argv[2], sys.argv[3])
    elif cmd in REGISTRIES:
        cmd_shadcn(cmd)
    else:
        print(f"Unknown command: {cmd}")
        print(__doc__)


if __name__ == "__main__":
    main()
