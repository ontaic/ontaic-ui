use wasm_bindgen::prelude::*;
use std::sync::Mutex;
use lazy_static::lazy_static;

mod ops;
mod state;
mod dom;
mod tree;

use state::StateStore;
use dom::DomDriver;
use ops::PatchBatch;

lazy_static! {
    static ref GLOBAL_STATE: Mutex<StateStore> = Mutex::new(StateStore::new());
}

#[wasm_bindgen(start)]
pub fn init_engine() -> Result<(), JsValue> {
    #[cfg(feature = "console_error_panic_hook")]
    console_error_panic_hook::set_once();
    Ok(())
}

#[wasm_bindgen]
pub fn bind_state_to_node(state_key: &str, node_id: &str) {
    if let Ok(mut store) = GLOBAL_STATE.lock() {
        store.bind_node(state_key, node_id);
    }
}

#[wasm_bindgen]
pub fn update_state(key: &str, value: &str) -> Result<(), JsValue> {
    let mut store = GLOBAL_STATE.lock().unwrap();
    let patches = store.set_state(key, value);

    if !patches.is_empty() {
        let driver = DomDriver::new()?;
        let batch = PatchBatch {
            ops: patches,
            timestamp: js_sys::Date::now() as u64,
        };
        driver.apply_batch(&batch)?;
    }

    Ok(())
}

#[wasm_bindgen]
pub fn update_state_attr(key: &str, attr: &str, value: &str) -> Result<(), JsValue> {
    let mut store = GLOBAL_STATE.lock().unwrap();
    let patches = store.set_state_attribute(key, attr, value);

    if !patches.is_empty() {
        let driver = DomDriver::new()?;
        let batch = PatchBatch {
            ops: patches,
            timestamp: js_sys::Date::now() as u64,
        };
        driver.apply_batch(&batch)?;
    }

    Ok(())
}

#[wasm_bindgen]
pub fn get_state(key: &str) -> Option<String> {
    GLOBAL_STATE
        .lock()
        .unwrap()
        .get_state(key)
        .map(|s| s.to_string())
}

#[wasm_bindgen]
pub fn init_state(key: &str, value: &str) {
    let mut store = GLOBAL_STATE.lock().unwrap();
    store.set_state(key, value);
}

#[wasm_bindgen]
pub fn has_changed(key: &str) -> bool {
    GLOBAL_STATE.lock().unwrap().has_changed(key)
}
