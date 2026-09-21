"""Performance monitoring utilities for ontaic."""
import time
from typing import Any, Callable, Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
from functools import wraps


@dataclass
class PerformanceMetric:
    """Performance metric."""
    name: str
    value: float
    unit: str = "ms"
    timestamp: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "value": self.value,
            "unit": self.unit,
            "timestamp": self.timestamp,
            "metadata": self.metadata,
        }


@dataclass
class WebVital:
    """Web Vital metric."""
    name: str  # FCP, LCP, FID, CLS, TTFB
    value: float
    rating: str = ""  # good, needs-improvement, poor
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "value": self.value,
            "rating": self.rating,
        }


class PerformanceMonitor:
    """Performance monitoring system."""
    
    def __init__(self):
        self.metrics: List[PerformanceMetric] = []
        self.marks: Dict[str, float] = {}
        self.measures: List[Dict[str, Any]] = []
        self.web_vitals: List[WebVital] = []
        self.max_metrics: int = 1000
    
    def mark(self, name: str):
        """Mark a point in time."""
        self.marks[name] = time.perf_counter()
    
    def measure(self, name: str, start_mark: str, end_mark: str = None):
        """Measure time between marks."""
        if start_mark not in self.marks:
            raise ValueError(f"Start mark '{start_mark}' not found")
        
        start_time = self.marks[start_mark]
        end_time = self.marks.get(end_mark, time.perf_counter())
        
        duration = (end_time - start_time) * 1000  # Convert to ms
        
        self.measures.append({
            "name": name,
            "startMark": start_mark,
            "endMark": end_mark,
            "duration": duration,
            "timestamp": datetime.now().isoformat(),
        })
        
        return duration
    
    def record_metric(self, name: str, value: float, unit: str = "ms", metadata: Dict[str, Any] = None):
        """Record a performance metric."""
        metric = PerformanceMetric(
            name=name,
            value=value,
            unit=unit,
            metadata=metadata or {},
        )
        
        self.metrics.append(metric)
        
        # Keep only max_metrics
        if len(self.metrics) > self.max_metrics:
            self.metrics = self.metrics[-self.max_metrics:]
        
        return metric
    
    def record_web_vital(self, name: str, value: float):
        """Record a Web Vital metric."""
        # Rate the metric
        rating = self._rate_web_vital(name, value)
        
        vital = WebVital(name=name, value=value, rating=rating)
        self.web_vitals.append(vital)
        
        return vital
    
    def _rate_web_vital(self, name: str, value: float) -> str:
        """Rate a Web Vital metric."""
        thresholds = {
            "FCP": (1800, 3000),
            "LCP": (2500, 4000),
            "FID": (100, 300),
            "CLS": (0.1, 0.25),
            "TTFB": (800, 1800),
            "INP": (200, 500),
        }
        
        if name in thresholds:
            good, poor = thresholds[name]
            if value <= good:
                return "good"
            elif value <= poor:
                return "needs-improvement"
            else:
                return "poor"
        
        return "unknown"
    
    def get_metrics(self, name: str = None, limit: int = 100) -> List[PerformanceMetric]:
        """Get recorded metrics."""
        metrics = self.metrics
        if name:
            metrics = [m for m in metrics if m.name == name]
        return metrics[-limit:]
    
    def get_web_vitals(self) -> List[WebVital]:
        """Get recorded Web Vitals."""
        return self.web_vitals
    
    def get_average(self, name: str) -> float:
        """Get average value for a metric."""
        metrics = [m for m in self.metrics if m.name == name]
        if not metrics:
            return 0
        return sum(m.value for m in metrics) / len(metrics)
    
    def get_summary(self) -> Dict[str, Any]:
        """Get performance summary."""
        metric_summary = {}
        for metric in self.metrics:
            if metric.name not in metric_summary:
                metric_summary[metric.name] = {
                    "count": 0,
                    "total": 0,
                    "min": float('inf'),
                    "max": float('-inf'),
                }
            
            stats = metric_summary[metric.name]
            stats["count"] += 1
            stats["total"] += metric.value
            stats["min"] = min(stats["min"], metric.value)
            stats["max"] = max(stats["max"], metric.value)
        
        # Calculate averages
        for name, stats in metric_summary.items():
            stats["average"] = stats["total"] / stats["count"]
        
        return {
            "totalMetrics": len(self.metrics),
            "totalMeasures": len(self.measures),
            "webVitals": [v.to_dict() for v in self.web_vitals],
            "metrics": metric_summary,
        }
    
    def clear(self):
        """Clear all recorded data."""
        self.metrics.clear()
        self.marks.clear()
        self.measures.clear()
        self.web_vitals.clear()
    
    def generate_js_code(self) -> str:
        """Generate JavaScript performance monitoring code."""
        return """
        // Performance Monitor
        const perfMonitor = {
            metrics: [],
            marks: {},
            measures: [],
            
            mark(name) {
                this.marks[name] = performance.now();
            },
            
            measure(name, startMark, endMark) {
                const start = this.marks[startMark];
                const end = this.marks[endMark] || performance.now();
                const duration = end - start;
                
                this.measures.push({
                    name,
                    startMark,
                    endMark,
                    duration,
                    timestamp: new Date().toISOString()
                });
                
                return duration;
            },
            
            recordMetric(name, value, unit = 'ms', metadata = {}) {
                const metric = {
                    name,
                    value,
                    unit,
                    timestamp: new Date().toISOString(),
                    metadata
                };
                
                this.metrics.push(metric);
                return metric;
            },
            
            async observeWebVitals() {
                // First Contentful Paint
                const fcpEntry = performance.getEntriesByName('first-contentful-paint')[0];
                if (fcpEntry) {
                    this.recordMetric('FCP', fcpEntry.startTime);
                }
                
                // Largest Contentful Paint
                if ('PerformanceObserver' in window) {
                    try {
                        const lcpObserver = new PerformanceObserver((list) => {
                            const entries = list.getEntries();
                            const lastEntry = entries[entries.length - 1];
                            this.recordMetric('LCP', lastEntry.startTime);
                        });
                        lcpObserver.observe({ type: 'largest-contentful-paint', buffered: true });
                    } catch (e) {}
                    
                    // First Input Delay
                    try {
                        const fidObserver = new PerformanceObserver((list) => {
                            const entries = list.getEntries();
                            entries.forEach(entry => {
                                this.recordMetric('FID', entry.processingStart - entry.startTime);
                            });
                        });
                        fidObserver.observe({ type: 'first-input', buffered: true });
                    } catch (e) {}
                    
                    // Cumulative Layout Shift
                    try {
                        let clsValue = 0;
                        const clsObserver = new PerformanceObserver((list) => {
                            list.getEntries().forEach(entry => {
                                if (!entry.hadRecentInput) {
                                    clsValue += entry.value;
                                    this.recordMetric('CLS', clsValue);
                                }
                            });
                        });
                        clsObserver.observe({ type: 'layout-shift', buffered: true });
                    } catch (e) {}
                    
                    // Time to First Byte
                    const navEntry = performance.getEntriesByType('navigation')[0];
                    if (navEntry) {
                        this.recordMetric('TTFB', navEntry.responseStart);
                    }
                }
            },
            
            getMetrics(name = null, limit = 100) {
                let metrics = this.metrics;
                if (name) {
                    metrics = metrics.filter(m => m.name === name);
                }
                return metrics.slice(-limit);
            },
            
            getAverage(name) {
                const metrics = this.metrics.filter(m => m.name === name);
                if (metrics.length === 0) return 0;
                return metrics.reduce((sum, m) => sum + m.value, 0) / metrics.length;
            },
            
            getSummary() {
                const summary = {};
                this.metrics.forEach(metric => {
                    if (!summary[metric.name]) {
                        summary[metric.name] = { count: 0, total: 0, min: Infinity, max: -Infinity };
                    }
                    const stats = summary[metric.name];
                    stats.count++;
                    stats.total += metric.value;
                    stats.min = Math.min(stats.min, metric.value);
                    stats.max = Math.max(stats.max, metric.value);
                });
                
                Object.keys(summary).forEach(name => {
                    summary[name].average = summary[name].total / summary[name].count;
                });
                
                return {
                    totalMetrics: this.metrics.length,
                    totalMeasures: this.measures.length,
                    metrics: summary
                };
            },
            
            clear() {
                this.metrics = [];
                this.marks = {};
                this.measures = [];
            }
        };
        
        // Initialize Web Vitals observation
        perfMonitor.observeWebVitals();
        """


class Timer:
    """Simple timer for measuring code execution."""
    
    def __init__(self, name: str = "timer"):
        self.name = name
        self.start_time = 0
        self.end_time = 0
        self.elapsed = 0
    
    def start(self):
        """Start the timer."""
        self.start_time = time.perf_counter()
        return self
    
    def stop(self):
        """Stop the timer."""
        self.end_time = time.perf_counter()
        self.elapsed = (self.end_time - self.start_time) * 1000  # ms
        return self.elapsed
    
    def __enter__(self):
        self.start()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()
        return False
    
    def __repr__(self):
        return f"Timer({self.name}: {self.elapsed:.2f}ms)"


def timed(func: Callable) -> Callable:
    """Decorator to measure function execution time."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        with Timer(func.__name__) as timer:
            result = func(*args, **kwargs)
        
        # Record metric
        monitor = get_performance_monitor()
        monitor.record_metric(f"function.{func.__name__}", timer.elapsed)
        
        return result
    return wrapper


def cache(ttl: float = 300, max_size: int = 100):
    """Decorator for caching function results."""
    def decorator(func: Callable) -> Callable:
        _cache = {}
        _timestamps = {}
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            import time
            
            # Create cache key
            key = str(args) + str(sorted(kwargs.items()))
            
            # Check if cached and valid
            if key in _cache:
                if time.time() - _timestamps[key] < ttl:
                    return _cache[key]
            
            # Call function
            result = func(*args, **kwargs)
            
            # Cache result
            _cache[key] = result
            _timestamps[key] = time.time()
            
            # Evict old entries if needed
            if len(_cache) > max_size:
                oldest_key = min(_timestamps.keys(), key=lambda k: _timestamps[k])
                del _cache[oldest_key]
                del _timestamps[oldest_key]
            
            return result
        
        wrapper.cache_clear = lambda: (_cache.clear(), _timestamps.clear())
        wrapper.cache_info = lambda: {"size": len(_cache), "max_size": max_size, "ttl": ttl}
        
        return wrapper
    return decorator


# Global performance monitor instance
_performance_monitor = None


def get_performance_monitor() -> PerformanceMonitor:
    """Get the global performance monitor instance."""
    global _performance_monitor
    if _performance_monitor is None:
        _performance_monitor = PerformanceMonitor()
    return _performance_monitor


# Memory monitoring
class MemoryMonitor:
    """Memory usage monitoring."""
    
    @staticmethod
    def get_usage() -> Dict[str, Any]:
        """Get current memory usage."""
        try:
            import psutil
            process = psutil.Process()
            memory_info = process.memory_info()
            
            return {
                "rss": memory_info.rss / 1024 / 1024,  # MB
                "vms": memory_info.vms / 1024 / 1024,  # MB
                "percent": process.memory_percent(),
            }
        except ImportError:
            return {"error": "psutil not installed"}
    
    @staticmethod
    def get_system_usage() -> Dict[str, Any]:
        """Get system memory usage."""
        try:
            import psutil
            memory = psutil.virtual_memory()
            
            return {
                "total": memory.total / 1024 / 1024 / 1024,  # GB
                "available": memory.available / 1024 / 1024 / 1024,  # GB
                "percent": memory.percent,
                "used": memory.used / 1024 / 1024 / 1024,  # GB
            }
        except ImportError:
            return {"error": "psutil not installed"}


# CPU monitoring
class CpuMonitor:
    """CPU usage monitoring."""
    
    @staticmethod
    def get_usage() -> float:
        """Get current CPU usage."""
        try:
            import psutil
            return psutil.cpu_percent(interval=0.1)
        except ImportError:
            return 0
    
    @staticmethod
    def get_count() -> int:
        """Get CPU count."""
        try:
            import psutil
            return psutil.cpu_count()
        except ImportError:
            return 1


# Performance CSS
PERFORMANCE_CSS = """
/* Performance styles */
.perf-metric {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.5rem 1rem;
    background: #f9fafb;
    border-radius: 0.375rem;
    margin-bottom: 0.5rem;
}

.perf-metric-name {
    font-weight: 500;
    color: #374151;
}

.perf-metric-value {
    font-family: monospace;
    color: #059669;
}

.perf-metric-value.poor {
    color: #dc2626;
}

.perf-metric-value.needs-improvement {
    color: #d97706;
}

.perf-web-vital {
    padding: 1rem;
    border-radius: 0.5rem;
    margin-bottom: 1rem;
}

.perf-web-vital.good {
    background: #d1fae5;
    border: 1px solid #6ee7b7;
}

.perf-web-vital.needs-improvement {
    background: #fef3c7;
    border: 1px solid #fcd34d;
}

.perf-web-vital.poor {
    background: #fee2e2;
    border: 1px solid #fca5a5;
}
"""
