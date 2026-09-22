"""Chart builder component for creating interactive charts."""
from typing import Any, Callable, Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum


class ChartType(str, Enum):
    """Chart types."""
    LINE = "line"
    BAR = "bar"
    PIE = "pie"
    DOUGHNUT = "doughnut"
    RADAR = "radar"
    POLAR_AREA = "polarArea"
    BUBBLE = "bubble"
    SCATTER = "scatter"
    AREA = "area"
    COMBO = "combo"


class ChartTheme(str, Enum):
    """Chart themes."""
    DEFAULT = "default"
    DARK = "dark"
    MINIMAL = "minimal"
    COLORFUL = "colorful"
    PASTEL = "pastel"
    NEON = "neon"


class ChartAnimation(str, Enum):
    """Chart animation types."""
    NONE = "none"
    BASIC = "basic"
    BOUNCE = "bounce"
    ELASTIC = "elastic"
    PULSE = "pulse"


@dataclass
class ChartDataset:
    """Chart dataset."""
    label: str
    data: List[Any]
    background_color: str = ""
    border_color: str = ""
    border_width: int = 1
    fill: bool = False
    tension: float = 0
    point_radius: int = 3
    point_hover_radius: int = 5
    hidden: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> dict:
        return {
            "label": self.label,
            "data": self.data,
            "backgroundColor": self.background_color,
            "borderColor": self.border_color,
            "borderWidth": self.border_width,
            "fill": self.fill,
            "tension": self.tension,
            "pointRadius": self.point_radius,
            "pointHoverRadius": self.point_hover_radius,
            "hidden": self.hidden,
        }


@dataclass
class ChartOptions:
    """Chart options."""
    responsive: bool = True
    maintain_aspect_ratio: bool = True
    show_legend: bool = True
    legend_position: str = "top"
    show_title: bool = True
    title_text: str = ""
    show_tooltips: bool = True
    tooltip_mode: str = "index"
    show_grid: bool = True
    show_scale: bool = True
    scale_type: str = "linear"
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    animation: ChartAnimation = ChartAnimation.BASIC
    animation_duration: int = 750
    plugins: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> dict:
        return {
            "responsive": self.responsive,
            "maintainAspectRatio": self.maintain_aspect_ratio,
            "showLegend": self.show_legend,
            "legendPosition": self.legend_position,
            "showTitle": self.show_title,
            "titleText": self.title_text,
            "showTooltips": self.show_tooltips,
            "tooltipMode": self.tooltip_mode,
            "showGrid": self.show_grid,
            "showScale": self.show_scale,
            "scaleType": self.scale_type,
            "minValue": self.min_value,
            "maxValue": self.max_value,
            "animation": self.animation.value,
            "animationDuration": self.animation_duration,
        }


class ChartBuilder:
    """Interactive chart builder component."""
    
    def __init__(self, chart_type: ChartType = ChartType.BAR):
        self._chart_type = chart_type
        self._labels: List[str] = []
        self._datasets: List[ChartDataset] = []
        self._options: ChartOptions = ChartOptions()
        self._theme: ChartTheme = ChartTheme.DEFAULT
        self._width: int = 600
        self._height: int = 400
        self._show_builder: bool = True
        self._editable: bool = True
        self._exportable: bool = True
        self._export_formats: List[str] = field(default_factory=lambda: ["png", "jpg", "svg", "pdf"])
        self._on_change: Optional[Callable] = None
        self._on_export: Optional[Callable] = None
        self._on_click: Optional[Callable] = None
        self._class_name: str = ""
        self._label: str = ""
        self._help_text: str = ""
    
    def labels(self, labels: List[str]) -> "ChartBuilder":
        """Set labels."""
        self._labels = labels
        return self
    
    def add_dataset(self, dataset: ChartDataset) -> "ChartBuilder":
        """Add a dataset."""
        self._datasets.append(dataset)
        return self
    
    def dataset(self, label: str, data: List[Any], **kwargs) -> "ChartBuilder":
        """Add a dataset."""
        ds = ChartDataset(label=label, data=data, **kwargs)
        self._datasets.append(ds)
        return self
    
    def options(self, options: ChartOptions) -> "ChartBuilder":
        """Set options."""
        self._options = options
        return self
    
    def theme(self, theme: ChartTheme) -> "ChartBuilder":
        """Set theme."""
        self._theme = theme
        return self
    
    def size(self, width: int, height: int) -> "ChartBuilder":
        """Set size."""
        self._width = width
        self._height = height
        return self
    
    def show_builder(self, show: bool = True) -> "ChartBuilder":
        """Show chart builder UI."""
        self._show_builder = show
        return self
    
    def on_change(self, callback: Callable) -> "ChartBuilder":
        """Set change handler."""
        self._on_change = callback
        return self
    
    def on_export(self, callback: Callable) -> "ChartBuilder":
        """Set export handler."""
        self._on_export = callback
        return self
    
    def on_click(self, callback: Callable) -> "ChartBuilder":
        """Set click handler."""
        self._on_click = callback
        return self
    
    def class_name(self, class_name: str) -> "ChartBuilder":
        """Set CSS class."""
        self._class_name = class_name
        return self
    
    def label(self, label: str) -> "ChartBuilder":
        """Set label."""
        self._label = label
        return self
    
    def help_text(self, text: str) -> "ChartBuilder":
        """Set help text."""
        self._help_text = text
        return self
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "chartType": self._chart_type.value,
            "labels": self._labels,
            "datasets": [d.to_dict() for d in self._datasets],
            "options": self._options.to_dict(),
            "theme": self._theme.value,
            "width": self._width,
            "height": self._height,
            "showBuilder": self._show_builder,
            "editable": self._editable,
            "exportable": self._exportable,
            "exportFormats": self._export_formats,
            "className": self._class_name,
            "label": self._label,
        }
    
    def to_html(self) -> str:
        """Generate HTML."""
        label_html = f'<h3 class="chart-builder-label">{self._label}</h3>' if self._label else ""
        help_html = f'<p class="chart-builder-help">{self._help_text}</p>' if self._help_text else ""
        class_attr = f" {self._class_name}" if self._class_name else ""
        theme_class = f" theme-{self._theme.value}"
        
        # Builder panel
        builder_html = ""
        if self._show_builder:
            chart_types = "".join(
                f'<button type="button" class="chart-type-btn{" active" if t.value == self._chart_type.value else ""}" data-type="{t.value}">{t.value.title()}</button>'
                for t in ChartType
            )
            
            export_btns = ""
            if self._exportable:
                export_btns = "".join(
                    f'<button type="button" class="chart-export-btn" data-format="{fmt}">{fmt.upper()}</button>'
                    for fmt in self._export_formats
                )
            
            builder_html = f'''<div class="chart-builder-panel">
                <div class="chart-type-selector">
                    <label>Chart Type</label>
                    <div class="chart-type-buttons">{chart_types}</div>
                </div>
                <div class="chart-datasets">
                    <label>Datasets</label>
                    <button type="button" class="chart-add-dataset">+ Add Dataset</button>
                </div>
                <div class="chart-export">
                    <label>Export</label>
                    <div class="chart-export-buttons">{export_btns}</div>
                </div>
            </div>'''
        
        return f'''<div class="chart-builder{theme_class}{class_attr}">
            {label_html}
            {builder_html}
            <div class="chart-canvas-container">
                <canvas id="chart-canvas" width="{self._width}" height="{self._height}"></canvas>
            </div>
            {help_html}
        </div>'''
    
    def generate_js_code(self) -> str:
        """Generate JavaScript."""
        config = self.to_dict()
        return f"""
        // Chart Builder
        (function() {{
            const config = {str(config).replace("'", '"')};
            
            const builder = document.querySelector('.chart-builder');
            if (!builder) return;
            
            const canvas = builder.querySelector('#chart-canvas');
            if (!canvas) return;
            
            let chartType = config.chartType;
            let chartInstance = null;
            
            // Chart data
            const chartData = {{
                labels: config.labels,
                datasets: config.datasets
            }};
            
            // Chart options
            const chartOptions = {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    legend: {{ display: config.options.showLegend }},
                    title: {{ display: config.options.showTitle, text: config.options.titleText }}
                }},
                scales: {{
                    y: {{ display: config.options.showScale, beginAtZero: true }}
                }}
            }};
            
            // Initialize chart (placeholder - in real app use Chart.js)
            function initChart() {{
                console.log('Initializing chart:', chartType, chartData);
                
                // Simple placeholder rendering
                const ctx = canvas.getContext('2d');
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                
                ctx.fillStyle = '#f3f4f6';
                ctx.fillRect(0, 0, canvas.width, canvas.height);
                
                ctx.fillStyle = '#374151';
                ctx.font = '14px system-ui';
                ctx.textAlign = 'center';
                ctx.fillText(chartType.toUpperCase() + ' CHART', canvas.width / 2, canvas.height / 2);
            }}
            
            // Chart type selection
            builder.querySelectorAll('.chart-type-btn').forEach(btn => {{
                btn.addEventListener('click', () => {{
                    builder.querySelectorAll('.chart-type-btn').forEach(b => b.classList.remove('active'));
                    btn.classList.add('active');
                    chartType = btn.dataset.type;
                    initChart();
                }});
            }});
            
            // Add dataset
            builder.querySelector('.chart-add-dataset')?.addEventListener('click', () => {{
                const label = 'Dataset ' + (chartData.datasets.length + 1);
                const data = Array.from({{ length: chartData.labels.length }}, () => Math.floor(Math.random() * 100));
                chartData.datasets.push({{ label, data }});
                initChart();
            }});
            
            // Export
            builder.querySelectorAll('.chart-export-btn').forEach(btn => {{
                btn.addEventListener('click', () => {{
                    const format = btn.dataset.format;
                    console.log('Export as:', format);
                    
                    if (format === 'png' || format === 'jpg') {{
                        const link = document.createElement('a');
                        link.download = 'chart.' + format;
                        link.href = canvas.toDataURL('image/' + format);
                        link.click();
                    }}
                }});
            }});
            
            // Canvas click
            canvas.addEventListener('click', (e) => {{
                console.log('Chart clicked');
            }});
            
            initChart();
        }})();
        """


def create_chart_builder(chart_type: ChartType = ChartType.BAR) -> ChartBuilder:
    """Create a chart builder."""
    return ChartBuilder(chart_type)


def chart_dataset(label: str, data: List[Any], **kwargs) -> ChartDataset:
    """Create a chart dataset."""
    return ChartDataset(label=label, data=data, **kwargs)


def chart_options(**kwargs) -> ChartOptions:
    """Create chart options."""
    return ChartOptions(**kwargs)


CHART_BUILDER_CSS = """
.chart-builder {
    border: 1px solid #e5e7eb;
    border-radius: 0.5rem;
    overflow: hidden;
    background: white;
}

.chart-builder-label {
    padding: 1rem;
    margin: 0;
    font-size: 1.25rem;
    font-weight: 600;
    color: #111827;
    border-bottom: 1px solid #e5e7eb;
}

.chart-builder-panel {
    padding: 1rem;
    background: #f9fafb;
    border-bottom: 1px solid #e5e7eb;
}

.chart-type-selector,
.chart-datasets,
.chart-export {
    margin-bottom: 1rem;
}

.chart-type-selector label,
.chart-datasets label,
.chart-export label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: 500;
    color: #374151;
    font-size: 0.875rem;
}

.chart-type-buttons {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
}

.chart-type-btn {
    padding: 0.375rem 0.75rem;
    border: 1px solid #d1d5db;
    background: white;
    border-radius: 0.375rem;
    cursor: pointer;
    font-size: 0.875rem;
}

.chart-type-btn.active {
    background: #3b82f6;
    color: white;
    border-color: #3b82f6;
}

.chart-type-btn:hover:not(.active) {
    background: #f3f4f6;
}

.chart-add-dataset {
    padding: 0.375rem 0.75rem;
    border: 1px dashed #d1d5db;
    background: white;
    border-radius: 0.375rem;
    cursor: pointer;
    color: #6b7280;
}

.chart-add-dataset:hover {
    border-color: #3b82f6;
    color: #3b82f6;
}

.chart-export-buttons {
    display: flex;
    gap: 0.5rem;
}

.chart-export-btn {
    padding: 0.375rem 0.75rem;
    border: 1px solid #d1d5db;
    background: white;
    border-radius: 0.375rem;
    cursor: pointer;
    font-size: 0.75rem;
    font-weight: 500;
}

.chart-export-btn:hover {
    background: #f3f4f6;
}

.chart-canvas-container {
    padding: 1rem;
    display: flex;
    justify-content: center;
}

.chart-canvas-container canvas {
    max-width: 100%;
}

.chart-builder-help {
    padding: 0.75rem 1rem;
    margin: 0;
    font-size: 0.875rem;
    color: #6b7280;
    border-top: 1px solid #e5e7eb;
}

/* Themes */
.theme-dark .chart-builder {
    background: #1f2937;
    border-color: #374151;
}

.theme-dark .chart-builder-label {
    color: #f9fafb;
    border-color: #374151;
}

.theme-dark .chart-builder-panel {
    background: #111827;
    border-color: #374151;
}

.theme-dark .chart-type-btn,
.theme-dark .chart-export-btn {
    background: #374151;
    border-color: #4b5563;
    color: #f9fafb;
}

.theme-minimal .chart-builder {
    border: none;
}

.theme-minimal .chart-builder-panel {
    background: transparent;
    border-bottom: none;
}
"""
