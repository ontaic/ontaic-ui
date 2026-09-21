from typing import Any, Callable, Optional, Dict, List
from dataclasses import dataclass
import uuid


class State:
    """Reactive state field descriptor."""

    def __init__(self, default: Any = None, state_type: str = "string"):
        self.default = default
        self.state_type = state_type
        self.name = None

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, f"_state_{self.name}", self.default)

    def __set__(self, obj, value):
        setattr(obj, f"_state_{self.name}", value)


class Component:
    """Base class for all Ontaic components."""

    def __init__(self, **kwargs):
        self._id = str(uuid.uuid4())[:8]
        for key, value in kwargs.items():
            setattr(self, key, value)

    def render(self) -> "Element":
        raise NotImplementedError

    def get_state_fields(self) -> Dict[str, Any]:
        states = {}
        for name in dir(self.__class__):
            attr = getattr(self.__class__, name)
            if isinstance(attr, State):
                states[name] = getattr(self, name)
        return states


class Element:
    """Base class for UI elements."""

    def __init__(
        self,
        tag: str,
        children: Any = None,
        class_name: str = "",
        id: Optional[str] = None,
        **props,
    ):
        self.tag = tag
        self.children = children or []
        self.class_name = class_name
        self.id = id or str(uuid.uuid4())[:8]
        self.props = props
        self.events: Dict[str, Any] = {}

    def on(self, event: str, handler: Callable) -> "Element":
        self.events[event] = handler
        return self

    def to_dict(self) -> Dict:
        return {
            "tag": self.tag,
            "id": self.id,
            "class_name": self.class_name,
            "props": self.props,
            "events": list(self.events.keys()),
        }


class Box(Element):
    """Generic container element."""

    def __init__(self, *children, class_name: str = "", id: Optional[str] = None, **props):
        super().__init__("div", class_name=class_name, id=id, **props)
        self.children = list(children)


class Text(Element):
    """Text element."""

    def __init__(
        self,
        content: str = "",
        tag: str = "span",
        class_name: str = "",
        id: Optional[str] = None,
        **props,
    ):
        super().__init__(tag, class_name=class_name, id=id, **props)
        self.content = content


class Button(Element):
    """Button element."""

    def __init__(
        self,
        text: str = "",
        class_name: str = "",
        on_click: Optional[Callable] = None,
        id: Optional[str] = None,
        **props,
    ):
        super().__init__("button", class_name=class_name, id=id, **props)
        self.content = text
        if on_click:
            self.events["click"] = on_click


class Input(Element):
    """Input element."""

    def __init__(
        self,
        input_type: str = "text",
        placeholder: str = "",
        class_name: str = "",
        value: str = "",
        on_change: Optional[Callable] = None,
        id: Optional[str] = None,
        **props,
    ):
        super().__init__("input", class_name=class_name, id=id, **props)
        self.props["type"] = input_type
        self.props["placeholder"] = placeholder
        self.props["value"] = value
        if on_change:
            self.events["change"] = on_change


class Image(Element):
    """Image element."""

    def __init__(
        self,
        src: str = "",
        alt: str = "",
        class_name: str = "",
        id: Optional[str] = None,
        **props,
    ):
        super().__init__("img", class_name=class_name, id=id, **props)
        self.props["src"] = src
        self.props["alt"] = alt
