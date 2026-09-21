"""Chart and visualization components for ontaic."""
import json
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field


@dataclass
class ChartDataset:
    """Chart dataset."""
    label: str
    data: List[float]
    backgroundColor: Optional[str] = None
    borderColor: Optional[str] = None
    borderWidth: int = 1
    fill: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        d = {
            "label": self.label,
            "data": self.data,
            "borderWidth": self.borderWidth,
            "fill": self.fill,
        }
        if self.backgroundColor:
            d["backgroundColor"] = self.backgroundColor
        if self.borderColor:
            d["borderColor"] = self.borderColor
        return d


@dataclass
class ChartOptions:
    """Chart options."""
    responsive: bool = True
    maintainAspectRatio: bool = False
    plugins: Optional[Dict[str, Any]] = None
    scales: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        d = {
            "responsive": self.responsive,
            "maintainAspectRatio": self.maintainAspectRatio,
        }
        if self.plugins:
            d["plugins"] = self.plugins
        if self.scales:
            d["scales"] = self.scales
        return d


class Chart:
    """Base chart component using Chart.js."""
    
    def __init__(
        self,
        chart_type: str,
        labels: List[str],
        datasets: List[ChartDataset],
        options: Optional[ChartOptions] = None,
        width: str = "100%",
        height: str = "400px",
        class_name: str = "",
    ):
        self.chart_type = chart_type
        self.labels = labels
        self.datasets = datasets
        self.options = options or ChartOptions()
        self.width = width
        self.height = height
        self.class_name = class_name
    
    def render(self) -> str:
        chart_id = f"chart-{id(self)}"
        datasets_json = json.dumps([d.to_dict() for d in self.datasets])
        options_json = json.dumps(self.options.to_dict())
        
        return f"""
        <div class="{self.class_name}" style="width: {self.width}; height: {self.height};">
            <canvas id="{chart_id}"></canvas>
        </div>
        <script>
        (function() {{
            const ctx = document.getElementById('{chart_id}').getContext('2d');
            new Chart(ctx, {{
                type: '{self.chart_type}',
                data: {{
                    labels: {json.dumps(self.labels)},
                    datasets: {datasets_json}
                }},
                options: {options_json}
            }});
        }})();
        </script>
        """


class LineChart(Chart):
    """Line chart component."""
    
    def __init__(
        self,
        labels: List[str],
        datasets: List[ChartDataset],
        options: Optional[ChartOptions] = None,
        **kwargs,
    ):
        super().__init__("line", labels, datasets, options, **kwargs)


class BarChart(Chart):
    """Bar chart component."""
    
    def __init__(
        self,
        labels: List[str],
        datasets: List[ChartDataset],
        options: Optional[ChartOptions] = None,
        **kwargs,
    ):
        super().__init__("bar", labels, datasets, options, **kwargs)


class PieChart(Chart):
    """Pie chart component."""
    
    def __init__(
        self,
        labels: List[str],
        data: List[float],
        backgroundColors: List[str] = None,
        options: Optional[ChartOptions] = None,
        **kwargs,
    ):
        dataset = ChartDataset(
            label="",
            data=data,
            backgroundColor=backgroundColors or [
                "#FF6384", "#36A2EB", "#FFCE56", "#4BC0C0",
                "#9966FF", "#FF9F40", "#FF6384", "#C9CBCF"
            ],
        )
        super().__init__("pie", labels, [dataset], options, **kwargs)


class DoughnutChart(Chart):
    """Doughnut chart component."""
    
    def __init__(
        self,
        labels: List[str],
        data: List[float],
        backgroundColors: List[str] = None,
        options: Optional[ChartOptions] = None,
        **kwargs,
    ):
        dataset = ChartDataset(
            label="",
            data=data,
            backgroundColor=backgroundColors or [
                "#FF6384", "#36A2EB", "#FFCE56", "#4BC0C0",
                "#9966FF", "#FF9F40", "#FF6384", "#C9CBCF"
            ],
        )
        super().__init__("doughnut", labels, [dataset], options, **kwargs)


class RadarChart(Chart):
    """Radar chart component."""
    
    def __init__(
        self,
        labels: List[str],
        datasets: List[ChartDataset],
        options: Optional[ChartOptions] = None,
        **kwargs,
    ):
        super().__init__("radar", labels, datasets, options, **kwargs)


class PolarAreaChart(Chart):
    """Polar area chart component."""
    
    def __init__(
        self,
        labels: List[str],
        data: List[float],
        backgroundColors: List[str] = None,
        options: Optional[ChartOptions] = None,
        **kwargs,
    ):
        dataset = ChartDataset(
            label="",
            data=data,
            backgroundColor=backgroundColors or [
                "#FF6384", "#36A2EB", "#FFCE56", "#4BC0C0",
                "#9966FF", "#FF9F40", "#FF6384", "#C9CBCF"
            ],
        )
        super().__init__("polarArea", labels, [dataset], options, **kwargs)


class BubbleChart(Chart):
    """Bubble chart component."""
    
    def __init__(
        self,
        datasets: List[ChartDataset],
        options: Optional[ChartOptions] = None,
        **kwargs,
    ):
        super().__init__("bubble", [], datasets, options, **kwargs)


class ScatterChart(Chart):
    """Scatter chart component."""
    
    def __init__(
        self,
        datasets: List[ChartDataset],
        options: Optional[ChartOptions] = None,
        **kwargs,
    ):
        super().__init__("scatter", [], datasets, options, **kwargs)


# Stat card component
class StatCard:
    """Statistics card with trend."""
    
    def __init__(
        self,
        title: str,
        value: str,
        change: str = "",
        change_type: str = "positive",  # positive, negative, neutral
        icon: str = "",
        class_name: str = "",
    ):
        self.title = title
        self.value = value
        self.change = change
        self.change_type = change_type
        self.icon = icon
        self.class_name = class_name
    
    def render(self) -> str:
        change_colors = {
            "positive": "text-green-500",
            "negative": "text-red-500",
            "neutral": "text-gray-500",
        }
        change_color = change_colors.get(self.change_type, "text-gray-500")
        
        icon_html = f'<div class="text-2xl">{self.icon}</div>' if self.icon else ""
        change_html = f'<span class="{change_color} text-sm">{self.change}</span>' if self.change else ""
        
        return f"""
        <div class="bg-white rounded-lg shadow p-6 {self.class_name}">
            <div class="flex items-center justify-between">
                <div>
                    <p class="text-sm font-medium text-gray-500">{self.title}</p>
                    <p class="text-3xl font-bold text-gray-900 mt-2">{self.value}</p>
                    {change_html}
                </div>
                {icon_html}
            </div>
        </div>
        """


# Progress bar component
class ProgressBar:
    """Progress bar component."""
    
    def __init__(
        self,
        value: float,
        max_value: float = 100,
        color: str = "blue",
        show_label: bool = True,
        height: str = "h-2",
        class_name: str = "",
    ):
        self.value = value
        self.max_value = max_value
        self.color = color
        self.show_label = show_label
        self.height = height
        self.class_name = class_name
    
    def render(self) -> str:
        percentage = min(100, (self.value / self.max_value) * 100)
        
        color_classes = {
            "blue": "bg-blue-500",
            "green": "bg-green-500",
            "red": "bg-red-500",
            "yellow": "bg-yellow-500",
            "purple": "bg-purple-500",
            "gray": "bg-gray-500",
        }
        color_class = color_classes.get(self.color, "bg-blue-500")
        
        label_html = f'<span class="text-sm text-gray-600">{percentage:.1f}%</span>' if self.show_label else ""
        
        return f"""
        <div class="{self.class_name}">
            {label_html}
            <div class="w-full bg-gray-200 rounded-full {self.height}">
                <div class="{color_class} {self.height} rounded-full" style="width: {percentage}%"></div>
            </div>
        </div>
        """


# Metric card component
class MetricCard:
    """Metric card with sparkline."""
    
    def __init__(
        self,
        title: str,
        value: str,
        data: List[float],
        color: str = "blue",
        class_name: str = "",
    ):
        self.title = title
        self.value = value
        self.data = data
        self.color = color
        self.class_name = class_name
    
    def render(self) -> str:
        chart_id = f"metric-{id(self)}"
        
        color_map = {
            "blue": "#3B82F6",
            "green": "#10B981",
            "red": "#EF4444",
            "yellow": "#F59E0B",
            "purple": "#8B5CF6",
        }
        color = color_map.get(self.color, "#3B82F6")
        
        return f"""
        <div class="bg-white rounded-lg shadow p-6 {self.class_name}">
            <p class="text-sm font-medium text-gray-500">{self.title}</p>
            <p class="text-2xl font-bold text-gray-900 mt-2">{self.value}</p>
            <div class="mt-4" style="height: 60px;">
                <canvas id="{chart_id}"></canvas>
            </div>
            <script>
            (function() {{
                const ctx = document.getElementById('{chart_id}').getContext('2d');
                new Chart(ctx, {{
                    type: 'line',
                    data: {{
                        labels: {json.dumps(list(range(len(self.data))))},
                        datasets: [{{
                            data: {json.dumps(self.data)},
                            borderColor: '{color}',
                            borderWidth: 2,
                            fill: true,
                            backgroundColor: '{color}20',
                            tension: 0.4,
                            pointRadius: 0,
                        }}]
                    }},
                    options: {{
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {{ legend: {{ display: false }} }},
                        scales: {{
                            x: {{ display: false }},
                            y: {{ display: false }}
                        }}
                    }}
                }});
            }})();
            </script>
        </div>
        """


# Gauge component
class Gauge:
    """Gauge/meter component."""
    
    def __init__(
        self,
        value: float,
        min_value: float = 0,
        max_value: float = 100,
        label: str = "",
        color: str = "blue",
        size: str = "md",  # sm, md, lg
        class_name: str = "",
    ):
        self.value = value
        self.min_value = min_value
        self.max_value = max_value
        self.label = label
        self.color = color
        self.size = size
        self.class_name = class_name
    
    def render(self) -> str:
        percentage = min(100, max(0, ((self.value - self.min_value) / (self.max_value - self.min_value)) * 100))
        
        size_classes = {
            "sm": "w-24 h-24",
            "md": "w-32 h-32",
            "lg": "w-40 h-40",
        }
        size_class = size_classes.get(self.size, "w-32 h-32")
        
        color_map = {
            "blue": "#3B82F6",
            "green": "#10B981",
            "red": "#EF4444",
            "yellow": "#F59E0B",
        }
        color = color_map.get(self.color, "#3B82F6")
        
        label_html = f'<p class="text-sm text-gray-600 mt-2">{self.label}</p>' if self.label else ""
        
        return f"""
        <div class="flex flex-col items-center {self.class_name}">
            <div class="{size_class} relative">
                <svg viewBox="0 0 100 100" class="w-full h-full transform -rotate-90">
                    <circle cx="50" cy="50" r="40" fill="none" stroke="#E5E7EB" stroke-width="10"/>
                    <circle cx="50" cy="50" r="40" fill="none" stroke="{color}" stroke-width="10"
                        stroke-dasharray="{percentage * 2.51327} 251.327"
                        stroke-linecap="round"/>
                </svg>
                <div class="absolute inset-0 flex items-center justify-center">
                    <span class="text-xl font-bold text-gray-900">{self.value:.0f}%</span>
                </div>
            </div>
            {label_html}
        </div>
        """


# Timeline component
class Timeline:
    """Timeline component."""
    
    def __init__(
        self,
        items: List[Dict[str, Any]],
        class_name: str = "",
    ):
        self.items = items
        self.class_name = class_name
    
    def render(self) -> str:
        items_html = ""
        for i, item in enumerate(self.items):
            dot_color = "bg-blue-500" if i == 0 else "bg-gray-300"
            line_class = "border-l-2 border-gray-200" if i < len(self.items) - 1 else ""
            
            items_html += f"""
            <div class="flex gap-4 pb-8">
                <div class="flex flex-col items-center">
                    <div class="w-3 h-3 rounded-full {dot_color}"></div>
                    {f'<div class="flex-1 {line_class}"></div>' if i < len(self.items) - 1 else ''}
                </div>
                <div class="flex-1">
                    <h4 class="font-medium text-gray-900">{item.get('title', '')}</h4>
                    <p class="text-sm text-gray-500">{item.get('date', '')}</p>
                    <p class="text-gray-700 mt-1">{item.get('description', '')}</p>
                </div>
            </div>
            """
        
        return f'<div class="{self.class_name}">{items_html}</div>'
