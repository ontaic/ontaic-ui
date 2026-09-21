use wasm_bindgen::prelude::*;
use web_sys::{window, Document, Element};
use crate::ops::{PatchOp, PatchBatch};

pub struct DomDriver {
    document: Document,
}

impl DomDriver {
    pub fn new() -> Result<Self, JsValue> {
        let window = window().ok_or_else(|| JsValue::from_str("No window"))?;
        let document = window
            .document()
            .ok_or_else(|| JsValue::from_str("No document"))?;
        Ok(Self { document })
    }

    pub fn apply_batch(&self, batch: &PatchBatch) -> Result<(), JsValue> {
        for op in &batch.ops {
            self.apply_patch(op)?;
        }
        Ok(())
    }

    fn apply_patch(&self, op: &PatchOp) -> Result<(), JsValue> {
        match op {
            PatchOp::UpdateText { node_id, text } => {
                if let Some(element) = self.document.get_element_by_id(node_id) {
                    element.set_text_content(Some(text));
                }
            }
            PatchOp::SetAttribute { node_id, key, value } => {
                if let Some(element) = self.document.get_element_by_id(node_id) {
                    element.set_attribute(key, value)?;
                }
            }
            PatchOp::RemoveAttribute { node_id, key } => {
                if let Some(element) = self.document.get_element_by_id(node_id) {
                    element.remove_attribute(key)?;
                }
            }
            PatchOp::ReplaceNode { node_id, new_html } => {
                if let Some(element) = self.document.get_element_by_id(node_id) {
                    element.set_outer_html(new_html);
                }
            }
            PatchOp::InsertNode {
                parent_id,
                node_id,
                html,
            } => {
                if let Some(parent) = self.document.get_element_by_id(parent_id) {
                    let container = self.document.create_element("div")?;
                    container.set_inner_html(html);
                    if let Some(new_node) = container.first_child() {
                        let wrapper = self.document.create_element("div")?;
                        wrapper.set_id(node_id);
                        wrapper.append_child(&new_node)?;
                        parent.append_child(&wrapper)?;
                    }
                }
            }
            PatchOp::RemoveNode { parent_id, node_id } => {
                if let Some(parent) = self.document.get_element_by_id(parent_id) {
                    if let Some(child) = self.document.get_element_by_id(node_id) {
                        parent.remove_child(&child)?;
                    }
                }
            }
        }
        Ok(())
    }

    pub fn get_element_by_id(&self, id: &str) -> Option<Element> {
        self.document.get_element_by_id(id)
    }
}
