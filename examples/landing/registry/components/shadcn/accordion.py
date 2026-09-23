"""
Ontaic adapter for shadcn accordion
Source: https://ui.shadcn.com/r (stolen, not written).
Emits the same HTML + Tailwind classes so the WASM runtime patches it directly.
"""
from ontaic.component import Element


class AccordionComponent(Element):
    """shadcn/accordion — imported from registry."""

    def __init__(self, **kwargs):
        super().__init__("div", class_name=kwargs.get("class_name", ""), **kwargs)
        self.source_registry = "shadcn"
        self.source_name = "accordion"
        self.tailwind_classes = """border-b last:border-b-0
flex
pointer-events-none size-4 shrink-0 translate-y-0.5 text-muted-foreground transition-transform duration-200
overflow-hidden text-sm data-[state=closed]:animate-accordion-up data-[state=open]:animate-accordion-down
pt-0 pb-4"""
        self.original_ts = '"use client"\n\nimport * as React from "react"\nimport { cn } from "cn"\nimport { ChevronDownIcon } from "lucide-react"\nimport { Accordion as AccordionPrimitive } from "radix-ui"\n\nfunction Accordion({\n  ...props\n}: React.ComponentProps<typeof AccordionPrimitive.Root>) {\n  return <AccordionPrimitive.Root data-slot="accordion" {...props} />\n}\n\nfunction AccordionItem({\n  className,\n  ...props\n}: React.ComponentProps<typeof AccordionPrimitive.Item>) {\n  return (\n    <AccordionPrimitive.Item\n      data-slot="accordion-item"\n      className={cn("border-b last:border-b-0", className)}\n      {...props}\n    />\n  )\n}\n\nfunction AccordionTrigger({\n  className,\n  children,\n  ...props\n}: React.ComponentProps<typeof AccordionPrimitive.Trigger>) {\n  return (\n    <AccordionPrimitive.Header className="flex">\n      <AccordionPrimitive.Trigger\n        data-slot="accordion-trigger"\n        className={cn(\n          "flex flex-1 items-start justify-between gap-4 rounded-md py-4 text-left text-sm font-medium transition-all outline-none hover:underline focus-visible:border-ring focus-visible:ring-[3px] focus-visible:ring-ring/50 disabled:pointer-events-none disabled:opacity-50 [&[data-state=open]>svg]:rotate-180",\n          className\n        )}\n        {...props}\n      >\n        {children}\n        <ChevronDownIcon className="pointer-events-none size-4 shrink-0 translate-y-0.5 text-muted-foreground transition-transform duration-200" />\n      </AccordionPrimitive.Trigger>\n    </AccordionPrimitive.Header>\n  )\n}\n\nfunction AccordionContent({\n  className,\n  children,\n  ...props\n}: React.ComponentProps<typeof AccordionPrimitive.Content>) {\n  return (\n    <AccordionPrimitive.Content\n      data-slot="accordion-content"\n      className="overflow-hidden text-sm data-[state=closed]:animate-accordion-up data-[state=open]:animate-accordion-down"\n      {...props}\n    >\n      <div className={cn("pt-0 pb-4", className)}>{children}</div>\n    </AccordionPrimitive.Content>\n  )\n}\n\nexport { Accordion, AccordionItem,'

    def render(self) -> str:
        # We re-emit the tailwind-markup from the original component.
        # The Ontaic WASM runtime patches the DOM directly — no server round-trip.
        cls = self.tailwind_classes.strip()
        return f'<div class="{cls}">{self._children_html}</div>'

    _children_html = ""


def create_accordion() -> AccordionComponent:
    return AccordionComponent()
