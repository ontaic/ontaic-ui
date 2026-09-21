use std::collections::HashMap;

#[derive(Debug, Clone)]
pub struct NodeKey {
    pub id: String,
    pub tag: String,
    pub attributes: HashMap<String, String>,
    pub children: Vec<String>,
    pub text_content: Option<String>,
    pub parent: Option<String>,
}

pub struct VirtualTree {
    nodes: HashMap<String, NodeKey>,
    root_id: Option<String>,
}

impl VirtualTree {
    pub fn new() -> Self {
        Self {
            nodes: HashMap::new(),
            root_id: None,
        }
    }

    pub fn insert_node(
        &mut self,
        id: String,
        tag: String,
        parent: Option<String>,
    ) {
        let node = NodeKey {
            id: id.clone(),
            tag,
            attributes: HashMap::new(),
            children: Vec::new(),
            text_content: None,
            parent: parent.clone(),
        };

        if let Some(ref parent_id) = parent {
            if let Some(parent_node) = self.nodes.get_mut(parent_id) {
                parent_node.children.push(id.clone());
            }
        } else {
            self.root_id = Some(id.clone());
        }

        self.nodes.insert(id, node);
    }

    pub fn set_text(&mut self, id: &str, text: &str) {
        if let Some(node) = self.nodes.get_mut(id) {
            node.text_content = Some(text.to_string());
        }
    }

    pub fn set_attribute(&mut self, id: &str, key: &str, value: &str) {
        if let Some(node) = self.nodes.get_mut(id) {
            node.attributes.insert(key.to_string(), value.to_string());
        }
    }

    pub fn remove_attribute(&mut self, id: &str, key: &str) {
        if let Some(node) = self.nodes.get_mut(id) {
            node.attributes.remove(key);
        }
    }

    pub fn get_node(&self, id: &str) -> Option<&NodeKey> {
        self.nodes.get(id)
    }

    pub fn get_text(&self, id: &str) -> Option<&str> {
        self.nodes.get(id).and_then(|n| n.text_content.as_deref())
    }

    pub fn get_attribute(&self, id: &str, key: &str) -> Option<&str> {
        self.nodes
            .get(id)
            .and_then(|n| n.attributes.get(key))
            .map(|s| s.as_str())
    }

    pub fn remove_node(&mut self, id: &str) -> Option<NodeKey> {
        if let Some(node) = self.nodes.remove(id) {
            if let Some(ref parent_id) = node.parent {
                if let Some(parent) = self.nodes.get_mut(parent_id) {
                    parent.children.retain(|c| c != id);
                }
            }
            Some(node)
        } else {
            None
        }
    }

    pub fn root_id(&self) -> Option<&str> {
        self.root_id.as_deref()
    }

    pub fn node_count(&self) -> usize {
        self.nodes.len()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_insert_and_get() {
        let mut tree = VirtualTree::new();
        tree.insert_node("root".into(), "div".into(), None);
        tree.insert_node("child".into(), "span".into(), Some("root".into()));

        assert_eq!(tree.node_count(), 2);
        assert_eq!(tree.root_id(), Some("root"));
    }

    #[test]
    fn test_set_text() {
        let mut tree = VirtualTree::new();
        tree.insert_node("n1".into(), "p".into(), None);
        tree.set_text("n1", "hello");
        assert_eq!(tree.get_text("n1"), Some("hello"));
    }
}
