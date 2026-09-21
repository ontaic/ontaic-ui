use std::collections::HashMap;
use crate::ops::PatchOp;

#[derive(Debug, Clone)]
pub struct StateValue {
    pub raw: String,
    pub value_type: ValueType,
}

#[derive(Debug, Clone, PartialEq)]
pub enum ValueType {
    String,
    Number,
    Boolean,
    Json,
}

pub struct StateStore {
    values: HashMap<String, StateValue>,
    node_bindings: HashMap<String, Vec<String>>,
    prev_values: HashMap<String, StateValue>,
}

impl StateStore {
    pub fn new() -> Self {
        Self {
            values: HashMap::new(),
            node_bindings: HashMap::new(),
            prev_values: HashMap::new(),
        }
    }

    pub fn set_state(&mut self, key: &str, value: &str) -> Vec<PatchOp> {
        let mut patches = Vec::new();
        let key_str = key.to_string();

        if let Some(old) = self.values.get(&key_str) {
            self.prev_values.insert(key_str.clone(), old.clone());
        }

        if let Some(current) = self.values.get(&key_str) {
            if current.raw == value {
                return patches;
            }
        }

        let value_type = Self::detect_type(value);
        self.values.insert(
            key_str.clone(),
            StateValue {
                raw: value.to_string(),
                value_type: value_type.clone(),
            },
        );

        if let Some(node_ids) = self.node_bindings.get(&key_str) {
            for node_id in node_ids {
                match value_type {
                    ValueType::String | ValueType::Number | ValueType::Boolean => {
                        patches.push(PatchOp::UpdateText {
                            node_id: node_id.clone(),
                            text: value.to_string(),
                        });
                    }
                    ValueType::Json => {}
                }
            }
        }

        patches
    }

    pub fn set_state_attribute(&mut self, key: &str, attr: &str, value: &str) -> Vec<PatchOp> {
        let mut patches = Vec::new();
        let binding_key = format!("{}.{}", key, attr);

        if let Some(node_ids) = self.node_bindings.get(&binding_key) {
            for node_id in node_ids {
                patches.push(PatchOp::SetAttribute {
                    node_id: node_id.clone(),
                    key: attr.to_string(),
                    value: value.to_string(),
                });
            }
        }

        patches
    }

    pub fn bind_node(&mut self, state_key: &str, node_id: &str) {
        self.node_bindings
            .entry(state_key.to_string())
            .or_insert_with(Vec::new)
            .push(node_id.to_string());
    }

    pub fn unbind_node(&mut self, state_key: &str, node_id: &str) {
        if let Some(nodes) = self.node_bindings.get_mut(state_key) {
            nodes.retain(|n| n != node_id);
        }
    }

    pub fn get_state(&self, key: &str) -> Option<&str> {
        self.values.get(key).map(|v| v.raw.as_str())
    }

    pub fn get_all_bindings(&self) -> &HashMap<String, Vec<String>> {
        &self.node_bindings
    }

    pub fn has_changed(&self, key: &str) -> bool {
        match (self.prev_values.get(key), self.values.get(key)) {
            (Some(prev), Some(curr)) => prev.raw != curr.raw,
            _ => false,
        }
    }

    fn detect_type(value: &str) -> ValueType {
        if value.parse::<f64>().is_ok() {
            ValueType::Number
        } else if value == "true" || value == "false" {
            ValueType::Boolean
        } else if value.starts_with('{') || value.starts_with('[') {
            ValueType::Json
        } else {
            ValueType::String
        }
    }
}
