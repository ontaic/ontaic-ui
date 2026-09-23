"""Landing page example — what users get with Ontaic defaults.

Run:
  python build.py        # generates index.html from real SDK output
  python -m http.server 8000
  # open http://localhost:8000/examples/landing/
"""
from ontaic.navigation import Navbar, NavLink
from ontaic.table import Table
from ontaic.forms import FormField, Select, Checkbox
from ontaic.extra_components import Accordion, Alert, Avatar, Badge


class LandingPage:
    """Composes the landing page from default SDK components."""

    def navbar(self):
        return Navbar(
            NavLink("/", "Features"),
            NavLink("/docs", "Docs"),
            NavLink("/examples", "Examples"),
            NavLink("/pricing", "Pricing"),
            brand="⚡ Ontaic",
            class_name="bg-white shadow-sm px-6 py-4",
        ).render()

    def feature_table(self):
        return Table(
            columns=[
                {"key": "feature", "header": "Feature"},
                {"key": "ontaic", "header": "Ontaic"},
                {"key": "other", "header": "Others"},
            ],
            data=[
                {"feature": "DOM update", "ontaic": "0ms (WASM)", "other": "200-500ms"},
                {"feature": "Language", "ontaic": "Pure Python", "other": "JS / DSL"},
                {"feature": "Deploy", "ontaic": "Static CDN", "other": "Server needed"},
                {"feature": "Bundle", "ontaic": "53KB WASM", "other": "MBs of JS"},
            ],
            striped=True,
        ).render()

    def signup_form(self):
        return (
            FormField(name="email", label="Email", input_type="email",
                      placeholder="you@company.com", required=True).render()
            + Select(name="role",
                     options=[{"value": "dev", "label": "Developer"},
                              {"value": "team", "label": "Team"},
                              {"value": "enterprise", "label": "Enterprise"}]).render()
            + Checkbox(name="news", label="Send me updates", checked=True).render()
        )

    def alerts(self):
        return (
            Alert(message="0ms DOM updates via Rust WASM.", type="success",
                  title="Fast by default").render()
            + Alert(message="430+ exports and counting.", type="info",
                    title="Batteries included").render()
        )

    def badges(self):
        return " ".join([
            Badge(text="0ms", variant="success").render(),
            Badge(text="Python", variant="primary").render(),
            Badge(text="53KB WASM", variant="default").render(),
            Badge(text="430+ components", variant="warning").render(),
        ])

    def avatars(self):
        return " ".join([
            Avatar(name="Ada Lovelace", size="lg").render(),
            Avatar(name="Grace Hopper", size="lg").render(),
            Avatar(name="Linus Torvalds", size="lg").render(),
        ])

    def faq(self):
        return Accordion(
            items=[
                {"header": "Do I need JavaScript?",
                 "content": "No. Write Python, Ontaic compiles to schema + WASM."},
                {"header": "How fast is it?",
                 "content": "State patches apply directly to the DOM — 0ms, no round-trip."},
                {"header": "How do I deploy?",
                 "content": "Static output. Any CDN, S3, or GitHub Pages works."},
            ],
            defaultOpen=[0],
        ).render()


if __name__ == "__main__":
    page = LandingPage()
    print("Navbar bytes:", len(page.navbar()))
    print("Table bytes:", len(page.feature_table()))
    print("Run python build.py to generate index.html")
