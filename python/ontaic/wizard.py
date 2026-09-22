"""Multi-step form wizard component."""
from typing import Any, Callable, Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum


class WizardStepStatus(str, Enum):
    """Wizard step status."""
    PENDING = "pending"
    ACTIVE = "active"
    COMPLETED = "completed"
    ERROR = "error"


class WizardLayout(str, Enum):
    """Wizard layout."""
    HORIZONTAL = "horizontal"
    VERTICAL = "vertical"


@dataclass
class WizardStep:
    """Wizard step definition."""
    id: str
    title: str
    description: str = ""
    icon: str = ""
    status: WizardStepStatus = WizardStepStatus.PENDING
    optional: bool = False
    disabled: bool = False
    content: str = ""
    fields: List[Dict[str, Any]] = field(default_factory=list)
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "icon": self.icon,
            "status": self.status.value,
            "optional": self.optional,
            "disabled": self.disabled,
            "fields": self.fields,
        }


class FormWizard:
    """Multi-step form wizard."""
    
    def __init__(self, steps: List[WizardStep] = None, layout: WizardLayout = WizardLayout.HORIZONTAL):
        self.steps = steps or []
        self.layout = layout
        self._current_index: int = 0
        self._show_progress: bool = True
        self._show_step_numbers: bool = True
        self._allow_back: bool = True
        self._allow_skip: bool = False
        self._linear: bool = True
        self._on_step_change: Optional[Callable] = None
        self._on_complete: Optional[Callable] = None
        self._on_validate: Optional[Callable] = None
        self._class_name: str = ""
        self._label: str = ""
        self._help_text: str = ""
        self._next_text: str = "Next"
        self._prev_text: str = "Previous"
        self._submit_text: str = "Submit"
        self._finish_text: str = "Finish"
    
    @property
    def current_step(self) -> Optional[WizardStep]:
        """Get current step."""
        if 0 <= self._current_index < len(self.steps):
            return self.steps[self._current_index]
        return None
    
    @property
    def current_index(self) -> int:
        """Get current index."""
        return self._current_index
    
    @property
    def total_steps(self) -> int:
        """Get total steps."""
        return len(self.steps)
    
    @property
    def is_first(self) -> bool:
        """Check if first step."""
        return self._current_index == 0
    
    @property
    def is_last(self) -> bool:
        """Check if last step."""
        return self._current_index == len(self.steps) - 1
    
    @property
    def progress(self) -> float:
        """Get progress percentage."""
        if not self.steps:
            return 0
        return (self._current_index / len(self.steps)) * 100
    
    def add_step(self, step: WizardStep) -> "FormWizard":
        """Add a step."""
        self.steps.append(step)
        return self
    
    def step(self, id: str, title: str, **kwargs) -> "FormWizard":
        """Add a step."""
        step = WizardStep(id=id, title=title, **kwargs)
        self.steps.append(step)
        return self
    
    def show_progress(self, show: bool = True) -> "FormWizard":
        """Show progress bar."""
        self._show_progress = show
        return self
    
    def show_step_numbers(self, show: bool = True) -> "FormWizard":
        """Show step numbers."""
        self._show_step_numbers = show
        return self
    
    def allow_back(self, allow: bool = True) -> "FormWizard":
        """Allow going back."""
        self._allow_back = allow
        return self
    
    def allow_skip(self, allow: bool = True) -> "FormWizard":
        """Allow skipping steps."""
        self._allow_skip = allow
        return self
    
    def linear(self, linear: bool = True) -> "FormWizard":
        """Set linear mode."""
        self._linear = linear
        return self
    
    def on_step_change(self, callback: Callable) -> "FormWizard":
        """Set step change handler."""
        self._on_step_change = callback
        return self
    
    def on_complete(self, callback: Callable) -> "FormWizard":
        """Set complete handler."""
        self._on_complete = callback
        return self
    
    def on_validate(self, callback: Callable) -> "FormWizard":
        """Set validation handler."""
        self._on_validate = callback
        return self
    
    def class_name(self, class_name: str) -> "FormWizard":
        """Set CSS class."""
        self._class_name = class_name
        return self
    
    def label(self, label: str) -> "FormWizard":
        """Set label."""
        self._label = label
        return self
    
    def help_text(self, text: str) -> "FormWizard":
        """Set help text."""
        self._help_text = text
        return self
    
    def button_texts(self, next_text: str = None, prev_text: str = None, submit_text: str = None) -> "FormWizard":
        """Set button texts."""
        if next_text:
            self._next_text = next_text
        if prev_text:
            self._prev_text = prev_text
        if submit_text:
            self._submit_text = submit_text
        return self
    
    def go_to(self, index: int) -> bool:
        """Go to step by index."""
        if 0 <= index < len(self.steps):
            old_index = self._current_index
            self._current_index = index
            
            if self._on_step_change:
                self._on_step_change(self.steps[old_index], self.steps[index])
            
            return True
        return False
    
    def next(self) -> bool:
        """Go to next step."""
        return self.go_to(self._current_index + 1)
    
    def prev(self) -> bool:
        """Go to previous step."""
        if self._allow_back:
            return self.go_to(self._current_index - 1)
        return False
    
    def complete(self):
        """Complete the wizard."""
        for step in self.steps:
            step.status = WizardStepStatus.COMPLETED
        
        if self._on_complete:
            self._on_complete()
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "steps": [s.to_dict() for s in self.steps],
            "layout": self.layout.value,
            "currentIndex": self._current_index,
            "showProgress": self._show_progress,
            "showStepNumbers": self._show_step_numbers,
            "allowBack": self._allow_back,
            "allowSkip": self._allow_skip,
            "linear": self._linear,
            "className": self._class_name,
            "label": self._label,
            "helpText": self._help_text,
            "nextText": self._next_text,
            "prevText": self._prev_text,
            "submitText": self._submit_text,
            "finishText": self._finish_text,
        }
    
    def to_html(self) -> str:
        """Generate HTML."""
        label_html = f'<h3 class="wizard-label">{self._label}</h3>' if self._label else ""
        help_html = f'<p class="wizard-help">{self._help_text}</p>' if self._help_text else ""
        class_attr = f" {self._class_name}" if self._class_name else ""
        layout_class = f" wizard-{self.layout.value}"
        
        # Step indicators
        steps_html = ""
        for i, step in enumerate(self.steps):
            status_class = f" step-{step.status.value}"
            active_class = " active" if i == self._current_index else ""
            completed_class = " completed" if step.status == WizardStepStatus.COMPLETED else ""
            
            number = f'<span class="step-number">{i + 1}</span>' if self._show_step_numbers else ""
            icon = f'<span class="step-icon">{step.icon}</span>' if step.icon else ""
            
            steps_html += f'''<div class="wizard-step{status_class}{active_class}{completed_class}" data-step="{i}">
                {number}{icon}
                <div class="step-content">
                    <span class="step-title">{step.title}</span>
                    <span class="step-description">{step.description}</span>
                </div>
            </div>'''
        
        # Progress bar
        progress_html = ""
        if self._show_progress:
            progress_html = f'''<div class="wizard-progress">
                <div class="wizard-progress-bar" style="width: {self.progress}%"></div>
            </div>'''
        
        # Current step content
        current = self.current_step
        content_html = current.content if current and current.content else ""
        
        # Navigation buttons
        buttons_html = f'''<div class="wizard-buttons">
            <button type="button" class="wizard-btn wizard-prev"{' style="display: none"' if self.is_first else ''}>{self._prev_text}</button>
            <button type="button" class="wizard-btn wizard-next">{self._next_text if not self.is_last else self._finish_text}</button>
        </div>'''
        
        return f'''<div class="wizard{layout_class}{class_attr}">
            {label_html}
            {progress_html}
            <div class="wizard-steps">{steps_html}</div>
            <div class="wizard-body">
                <div class="wizard-content">{content_html}</div>
                {buttons_html}
            </div>
            {help_html}
        </div>'''
    
    def generate_js_code(self) -> str:
        """Generate JavaScript."""
        config = self.to_dict()
        return f"""
        // Form Wizard
        (function() {{
            const config = {str(config).replace("'", '"')};
            
            const wizard = document.querySelector('.wizard');
            if (!wizard) return;
            
            let currentIndex = config.currentIndex;
            
            const steps = wizard.querySelectorAll('.wizard-step');
            const prevBtn = wizard.querySelector('.wizard-prev');
            const nextBtn = wizard.querySelector('.wizard-next');
            const progressBar = wizard.querySelector('.wizard-progress-bar');
            
            function updateUI() {{
                steps.forEach((step, i) => {{
                    step.classList.toggle('active', i === currentIndex);
                    step.classList.toggle('completed', i < currentIndex);
                }});
                
                if (prevBtn) {{
                    prevBtn.style.display = currentIndex === 0 ? 'none' : 'block';
                }}
                
                if (nextBtn) {{
                    nextBtn.textContent = currentIndex === steps.length - 1 ? config.finishText : config.nextText;
                }}
                
                if (progressBar) {{
                    progressBar.style.width = ((currentIndex / steps.length) * 100) + '%';
                }}
                
                console.log('Step changed:', currentIndex);
            }}
            
            if (prevBtn) {{
                prevBtn.addEventListener('click', () => {{
                    if (currentIndex > 0) {{
                        currentIndex--;
                        updateUI();
                    }}
                }});
            }}
            
            if (nextBtn) {{
                nextBtn.addEventListener('click', () => {{
                    if (currentIndex < steps.length - 1) {{
                        currentIndex++;
                        updateUI();
                    }} else {{
                        console.log('Wizard completed');
                    }}
                }});
            }}
            
            steps.forEach((step, i) => {{
                step.addEventListener('click', () => {{
                    if (!step.classList.contains('disabled')) {{
                        currentIndex = i;
                        updateUI();
                    }}
                }});
            }});
            
            updateUI();
        }})();
        """


def create_wizard(layout: WizardLayout = WizardLayout.HORIZONTAL) -> FormWizard:
    """Create a form wizard."""
    return FormWizard(layout=layout)


def wizard_step(id: str, title: str, **kwargs) -> WizardStep:
    """Create a wizard step."""
    return WizardStep(id=id, title=title, **kwargs)


WIZARD_CSS = """
.wizard {
    width: 100%;
}

.wizard-label {
    font-size: 1.25rem;
    font-weight: 600;
    color: #111827;
    margin-bottom: 1rem;
}

.wizard-progress {
    height: 4px;
    background: #e5e7eb;
    border-radius: 2px;
    margin-bottom: 2rem;
    overflow: hidden;
}

.wizard-progress-bar {
    height: 100%;
    background: #3b82f6;
    border-radius: 2px;
    transition: width 0.3s ease;
}

.wizard-steps {
    display: flex;
    margin-bottom: 2rem;
}

.wizard-vertical .wizard-steps {
    flex-direction: column;
}

.wizard-step {
    display: flex;
    align-items: center;
    flex: 1;
    padding: 1rem;
    position: relative;
    cursor: pointer;
}

.wizard-vertical .wizard-step {
    padding: 1rem 1rem 1rem 3rem;
}

.wizard-step:not(:last-child)::after {
    content: '';
    position: absolute;
    right: 0;
    top: 50%;
    width: 100%;
    height: 2px;
    background: #e5e7eb;
    z-index: 1;
}

.wizard-step.completed:not(:last-child)::after {
    background: #10b981;
}

.step-number {
    width: 32px;
    height: 32px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #e5e7eb;
    border-radius: 50%;
    font-weight: 600;
    font-size: 0.875rem;
    color: #6b7280;
    z-index: 2;
    flex-shrink: 0;
}

.wizard-step.active .step-number {
    background: #3b82f6;
    color: white;
}

.wizard-step.completed .step-number {
    background: #10b981;
    color: white;
}

.step-content {
    margin-left: 1rem;
    z-index: 2;
}

.wizard-vertical .step-content {
    margin-left: 0;
}

.step-title {
    display: block;
    font-weight: 500;
    color: #374151;
}

.step-description {
    display: block;
    font-size: 0.875rem;
    color: #6b7280;
}

.wizard-body {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 0.5rem;
    padding: 1.5rem;
}

.wizard-content {
    min-height: 200px;
    margin-bottom: 1.5rem;
}

.wizard-buttons {
    display: flex;
    justify-content: space-between;
}

.wizard-btn {
    padding: 0.5rem 1rem;
    border: 1px solid #d1d5db;
    background: white;
    border-radius: 0.375rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.15s ease;
}

.wizard-btn:hover {
    background: #f9fafb;
    border-color: #9ca3af;
}

.wizard-next {
    background: #3b82f6;
    color: white;
    border-color: #3b82f6;
}

.wizard-next:hover {
    background: #2563eb;
}

.wizard-help {
    margin-top: 1rem;
    font-size: 0.875rem;
    color: #6b7280;
}
"""
