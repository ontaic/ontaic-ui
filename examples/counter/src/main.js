// WASM module imports
let wasmModule = null;

// State store (mirrors Rust StateStore)
const state = {};
const bindings = {};
const events = {};

// Initialize WASM module
async function initWasm() {
  try {
    // Try to load from local pkg directory
    const wasmUrl = '/pkg/ontaic_runtime_bg.wasm';
    const jsUrl = '/pkg/ontaic_runtime.js';

    // Dynamic import of WASM JS wrapper
    const wasmJs = await import(jsUrl);
    await wasmJs.default(wasmUrl);

    // Get exported functions
    wasmModule = {
      bind_state_to_node: wasmJs.bind_state_to_node,
      update_state: wasmJs.update_state,
      init_state: wasmJs.init_state,
      get_state: wasmJs.get_state,
    };

    console.log('[ontaic] WASM module loaded');
    return true;
  } catch (e) {
    console.warn('[ontaic] WASM not available, using JS fallback', e);
    return false;
  }
}

// Fallback WASM functions (pure JS implementation)
const fallback = {
  bind_state_to_node: (key, nodeId) => {
    if (!bindings[key]) bindings[key] = [];
    bindings[key].push(nodeId);
  },
  update_state: (key, value) => {
    state[key] = value;
    updateDomForState(key);
  },
  init_state: (key, value) => {
    state[key] = value;
  },
  get_state: (key) => {
    return state[key] || '';
  },
};

// Get the appropriate function (WASM or fallback)
function getFn(name) {
  return wasmModule ? wasmModule[name] : fallback[name];
}

// Update DOM elements bound to a state key
function updateDomForState(key) {
  const nodeIds = bindings[key] || [];
  const value = state[key] || '';

  for (const nodeId of nodeIds) {
    const el = document.getElementById(nodeId);
    if (el) {
      el.textContent = value;
    }
  }
}

// Load and hydrate schema
async function hydrateSchema() {
  try {
    const response = await fetch('/src/schema.json');
    const schema = await response.json();

    // Set inner HTML
    const app = document.getElementById('app');
    app.innerHTML = schema.html;

    // Initialize state
    for (const [key, value] of Object.entries(schema.initialState)) {
      getFn('init_state')(key, value);
    }

    // Bind state to nodes
    for (const [stateKey, nodeId] of Object.entries(schema.bindings)) {
      getFn('bind_state_to_node')(stateKey, nodeId);
      // Initial render
      updateDomForState(stateKey);
    }

    // Attach event listeners
    for (const [nodeId, nodeEvents] of Object.entries(schema.events)) {
      const el = document.getElementById(nodeId);
      if (!el) continue;

      for (const [event, handler] of Object.entries(nodeEvents)) {
        el.addEventListener(event, () => {
          // Create a function with access to state functions
          const fn = new Function(
            'update_state',
            'get_state',
            `return ${handler}`
          );
          const result = fn(getFn('update_state'), getFn('get_state'));

          // If handler returns a value, we need to figure out which state to update
          // This is a fallback for simple handlers
          if (result !== undefined && typeof result === 'string') {
            // Try to find which state key this updates
            for (const key of Object.keys(schema.initialState)) {
              if (handler.includes(key)) {
                getFn('update_state')(key, result);
                break;
              }
            }
          }
        });
      }
    }

    console.log('[ontaic] Schema hydrated');
  } catch (e) {
    console.error('[ontaic] Failed to load schema:', e);
    document.getElementById('app').innerHTML = `
      <div class="min-h-screen flex items-center justify-center bg-gray-50">
        <div class="text-center">
          <h1 class="text-2xl font-bold text-gray-900 mb-2">Schema not found</h1>
          <p class="text-gray-500">Run: python -m ontaic.compiler --input app.py --output src/schema.json</p>
        </div>
      </div>
    `;
  }
}

// Boot
async function boot() {
  await initWasm();
  await hydrateSchema();
  console.log('[ontaic] Ready');
}

boot();
