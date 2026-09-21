// Ontaic Runtime - Browser-side state management
// Works with WASM or pure JS fallback

(function() {
  'use strict';

  // State store
  const state = {};
  const bindings = {};
  const events = {};
  let wasmReady = false;

  // Initialize WASM if available
  async function initWasm() {
    try {
      const wasmUrl = '/pkg/ontaic_runtime_bg.wasm';
      const jsUrl = '/pkg/ontaic_runtime.js';

      // Check if WASM files exist
      const response = await fetch(wasmUrl, { method: 'HEAD' });
      if (!response.ok) {
        console.log('[ontaic] WASM not found, using JS fallback');
        return false;
      }

      // Dynamic import of WASM JS wrapper
      const wasmJs = await import(jsUrl);
      await wasmJs.default(wasmUrl);

      // Expose WASM functions globally
      window.ontaic = {
        bind_state_to_node: wasmJs.bind_state_to_node,
        update_state: wasmJs.update_state,
        init_state: wasmJs.init_state,
        get_state: wasmJs.get_state,
      };

      wasmReady = true;
      console.log('[ontaic] WASM loaded');
      return true;
    } catch (e) {
      console.log('[ontaic] WASM load failed, using JS fallback:', e.message);
      return false;
    }
  }

  // JS fallback implementation
  function initJsFallback() {
    window.ontaic = {
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
    console.log('[ontaic] JS fallback initialized');
  }

  // Update DOM elements for a state key
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

  // Execute event handler
  function executeHandler(handler, event) {
    try {
      // Create function with access to state API
      const fn = new Function(
        'update_state',
        'get_state',
        'event',
        `return ${handler}`
      );
      const result = fn(
        window.ontaic.update_state,
        window.ontaic.get_state,
        event
      );

      // If handler returns undefined, try to update the first state
      if (result === undefined) {
        // Handler already called update_state
      }
    } catch (e) {
      console.error('[ontaic] Handler error:', e);
    }
  }

  // Hydrate schema into DOM
  function hydrateSchema(schema) {
    const app = document.getElementById('app');
    if (!app) {
      console.error('[ontaic] #app element not found');
      return;
    }

    // Set HTML
    app.innerHTML = schema.html;

    // Initialize state
    for (const [key, value] of Object.entries(schema.initialState || {})) {
      window.ontaic.init_state(key, value);
    }

    // Bind state to nodes
    for (const [stateKey, nodeId] of Object.entries(schema.bindings || {})) {
      window.ontaic.bind_state_to_node(stateKey, nodeId);
      // Initial render
      updateDomForState(stateKey);
    }

    // Attach event listeners
    for (const [nodeId, nodeEvents] of Object.entries(schema.events || {})) {
      const el = document.getElementById(nodeId);
      if (!el) continue;

      for (const [event, handler] of Object.entries(nodeEvents)) {
        el.addEventListener(event, (e) => executeHandler(handler, e));
      }
    }

    console.log('[ontaic] Schema hydrated');
  }

  // Load schema from file or inline
  async function loadSchema() {
    // Check for inline schema first
    const inlineSchema = document.getElementById('ontaic-schema');
    if (inlineSchema) {
      return JSON.parse(inlineSchema.textContent);
    }

    // Try to load from file
    try {
      const response = await fetch('/src/schema.json');
      if (response.ok) {
        return await response.json();
      }
    } catch (e) {
      // Ignore
    }

    return null;
  }

  // Boot sequence
  async function boot() {
    // Initialize WASM or JS fallback
    const wasmLoaded = await initWasm();
    if (!wasmLoaded) {
      initJsFallback();
    }

    // Load and hydrate schema
    const schema = await loadSchema();
    if (schema) {
      hydrateSchema(schema);
    } else {
      console.error('[ontaic] No schema found');
      document.getElementById('app').innerHTML = `
        <div style="min-height:100vh;display:flex;align-items:center;justify-content:center;background:#f9fafb;">
          <div style="text-align:center;">
            <h1 style="font-size:1.5rem;font-weight:600;color:#111827;margin-bottom:0.5rem;">Schema not found</h1>
            <p style="color:#6b7280;">Run: python -m ontaic.compiler --input app.py --output src/schema.json</p>
          </div>
        </div>
      `;
    }
  }

  // Expose API globally
  window.ontaic = window.ontaic || {};
  window.ontaic.hydrate = hydrateSchema;
  window.ontaic.boot = boot;

  // Auto-boot when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
