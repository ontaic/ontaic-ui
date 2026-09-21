use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize, Debug, Clone, PartialEq)]
pub enum PatchOp {
    UpdateText {
        node_id: String,
        text: String,
    },
    SetAttribute {
        node_id: String,
        key: String,
        value: String,
    },
    RemoveAttribute {
        node_id: String,
        key: String,
    },
    ReplaceNode {
        node_id: String,
        new_html: String,
    },
    InsertNode {
        parent_id: String,
        node_id: String,
        html: String,
    },
    RemoveNode {
        parent_id: String,
        node_id: String,
    },
}

#[derive(Serialize, Deserialize, Debug, Clone)]
pub struct PatchBatch {
    pub ops: Vec<PatchOp>,
    pub timestamp: u64,
}
