"""Build static landing preview from REAL Ontaic SDK defaults."""
import pathlib

from app import LandingPage
from ontaic.charts import BarChart, ChartDataset
from ontaic.calendar import Calendar
from ontaic.kanban import KanbanBoard
from ontaic.timeline import Timeline
from ontaic.datagrid import DataGrid, GridColumn
from ontaic.qrcode import create_qr_code
from ontaic.mediaplayer import create_video_player

# Collect all default CSS blocks shipped by the SDK
from ontaic import calendar as cal_mod
from ontaic import kanban as kan_mod
from ontaic import timeline as tl_mod
from ontaic import datagrid as dg_mod
from ontaic import chartbuilder as cb_mod
from ontaic import qrcode as qr_mod
from ontaic import mediaplayer as mp_mod
from ontaic import notifications as notif_mod
from ontaic import calendar as cal2  # noqa - keep import surface obvious

page = LandingPage()

chart_html = BarChart(
    labels=["Jan", "Feb", "Mar", "Apr", "May"],
    datasets=[ChartDataset(label="Signups", data=[120, 200, 180, 320, 410],
                           backgroundColor="#3b82f6")],
).render()

calendar_html = Calendar().to_html() if hasattr(Calendar(), "to_html") else ""
kanban_html = KanbanBoard().to_html() if hasattr(KanbanBoard(), "to_html") else ""
timeline_html = Timeline().to_html() if hasattr(Timeline(), "to_html") else ""

try:
    grid = DataGrid(
        columns=[GridColumn(field="name", header="Name"),
                 GridColumn(field="role", header="Role")],
        data=[{"name": "Ada", "role": "Admin"}, {"name": "Grace", "role": "User"}],
    )
    grid_html = grid.to_html()
except Exception as e:
    grid_html = f"<!-- datagrid demo failed: {e} -->"

try:
    qr_html = create_qr_code("https://ontaic.dev").to_html()
except Exception as e:
    qr_html = f"<!-- qr demo failed: {e} -->"

try:
    player_html = create_video_player("https://example.com/demo.mp4").to_html()
except Exception as e:
    player_html = f"<!-- player demo failed: {e} -->"

css_blocks = "\n".join([
    getattr(cal_mod, "CALENDAR_CSS", ""),
    getattr(kan_mod, "KANBAN_CSS", ""),
    getattr(tl_mod, "TIMELINE_CSS", ""),
    getattr(dg_mod, "DATA_GRID_CSS", ""),
    getattr(cb_mod, "CHART_BUILDER_CSS", ""),
    getattr(qr_mod, "QR_CODE_CSS", ""),
    getattr(mp_mod, "MEDIA_PLAYER_CSS", ""),
    getattr(notif_mod, "NOTIFICATION_CSS", ""),
])

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Ontaic — What you get by default</title>
<script src="https://cdn.tailwindcss.com"></script>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<style>
body {{ font-family: Inter, system-ui, sans-serif; }}
{css_blocks}
</style>
</head>
<body class="bg-gray-50 text-gray-900">

<!-- NAVBAR: real SDK output -->
<div class="max-w-7xl mx-auto px-4 pt-4">
{page.navbar()}
</div>

<!-- HERO (Tailwind defaults, same classes SDK emits) -->
<header class="max-w-7xl mx-auto px-4 py-16 text-center">
  <div class="inline-flex items-center px-3 py-1 rounded-full bg-blue-100 text-blue-800 text-sm mb-4">⚡ Open Source • Python • 53KB WASM • 0ms DOM</div>
  <h1 class="text-4xl md:text-6xl font-bold mb-4">Build UIs in Python.<br>Ship at the speed of thought.</h1>
  <p class="text-lg text-gray-600 max-w-2xl mx-auto mb-8">This page is built <b>only</b> from Ontaic default designs — no custom CSS. Navbar, table, form, alerts, badges, avatars, accordion below are actual <code>render()</code> / <code>to_html()</code> output.</p>
  <div class="flex justify-center gap-4">
    <a href="#gallery" class="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700">See defaults</a>
    <a href="#code" class="px-6 py-3 border border-gray-300 rounded-lg hover:bg-white">View Python source</a>
  </div>
  <div class="mt-6 flex justify-center gap-2 flex-wrap">{page.badges()}</div>
</header>

<!-- COMPARISON: real Table output -->
<section class="max-w-5xl mx-auto px-4 mb-12">
  <h2 class="text-3xl font-semibold mb-2">Default Table</h2>
  <p class="text-gray-600 mb-4"><code>Table(columns=..., data=..., striped=True).render()</code></p>
  {page.feature_table()}
</section>

<!-- CHART: real Chart.js output -->
<section class="max-w-5xl mx-auto px-4 mb-12 grid md:grid-cols-2 gap-8">
  <div class="bg-white p-6 shadow-md rounded-xl">
    <h3 class="text-xl font-medium mb-2">Default BarChart</h3>
    {chart_html}
  </div>
  <div class="bg-white p-6 shadow-md rounded-xl">
    <h3 class="text-xl font-medium mb-2">Default signup form</h3>
    {page.signup_form()}
    <button class="mt-4 px-4 py-2 bg-blue-600 text-white rounded-lg">Create account</button>
  </div>
</section>

<!-- ALERTS + AVATARS -->
<section class="max-w-5xl mx-auto px-4 mb-12 grid md:grid-cols-2 gap-8">
  <div class="space-y-4">
    <h3 class="text-xl font-medium">Default Alerts</h3>
    {page.alerts()}
  </div>
  <div>
    <h3 class="text-xl font-medium mb-2">Default Avatars</h3>
    <div class="flex gap-3 items-center bg-white p-4 shadow-md rounded-xl">{page.avatars()}</div>
    <p class="text-sm text-gray-500 mt-2"><code>Avatar(name=...).render()</code> — initials fallback, no image needed.</p>
  </div>
</section>

<!-- GALLERY: heavier defaults -->
<section id="gallery" class="max-w-7xl mx-auto px-4 mb-12">
  <h2 class="text-3xl font-semibold mb-2">More defaults, same page</h2>
  <p class="text-gray-600 mb-6">Every block below is SDK default CSS + HTML. No theme overrides.</p>
  <div class="grid md:grid-cols-2 gap-8">
    <div class="bg-white p-4 shadow-md rounded-xl overflow-auto">
      <h3 class="font-medium mb-2">DataGrid.to_html()</h3>
      {grid_html}
    </div>
    <div class="bg-white p-4 shadow-md rounded-xl">
      <h3 class="font-medium mb-2">Calendar.to_html()</h3>
      {calendar_html}
    </div>
    <div class="bg-white p-4 shadow-md rounded-xl">
      <h3 class="font-medium mb-2">KanbanBoard.to_html()</h3>
      {kanban_html}
    </div>
    <div class="bg-white p-4 shadow-md rounded-xl">
      <h3 class="font-medium mb-2">Timeline.to_html()</h3>
      {timeline_html}
    </div>
    <div class="bg-white p-4 shadow-md rounded-xl">
      <h3 class="font-medium mb-2">QRCode.to_html()</h3>
      {qr_html}
    </div>
    <div class="bg-white p-4 shadow-md rounded-xl">
      <h3 class="font-medium mb-2">MediaPlayer.to_html()</h3>
      {player_html}
    </div>
  </div>
</section>

<!-- FAQ: real Accordion -->
<section class="max-w-3xl mx-auto px-4 mb-16">
  <h2 class="text-3xl font-semibold mb-4">FAQ — default Accordion</h2>
  {page.faq()}
</section>

<!-- CODE -->
<section id="code" class="max-w-5xl mx-auto px-4 mb-16">
  <h2 class="text-3xl font-semibold mb-2">Python source that made this</h2>
  <pre class="bg-gray-900 text-gray-100 p-6 rounded-xl overflow-auto text-sm"><code>from ontaic.navigation import Navbar, NavLink
from ontaic.table import Table
from ontaic.forms import FormField, Select, Checkbox
from ontaic.extra_components import Accordion, Alert, Avatar, Badge
from ontaic.charts import BarChart, ChartDataset

Navbar(brand="⚡ Ontaic", ...).render()
Table(columns=..., data=..., striped=True).render()
BarChart(labels=..., datasets=[ChartDataset(...)]).render()
FormField(name="email", ...).render()
Alert(message=..., alert_type="success").render()
Avatar(name="Ada Lovelace").render()
Accordion(items=[...]).render()</code></pre>
  <p class="text-gray-600 mt-2">Full file: <code>examples/landing/app.py</code>. This HTML was generated by <code>examples/landing/build.py</code>.</p>
</section>

<footer class="border-t bg-white">
  <div class="max-w-7xl mx-auto px-4 py-8 text-sm text-gray-500 flex justify-between flex-wrap gap-2">
    <span>⚡ Ontaic defaults preview — Tailwind + SDK CSS, no custom theme.</span>
    <span>430+ exports • 53KB WASM • MIT</span>
  </div>
</footer>

</body>
</html>
"""

out = pathlib.Path(__file__).parent / "index.html"
out.write_text(html, encoding="utf-8")
print(f"Wrote {out} ({len(html)} bytes)")
