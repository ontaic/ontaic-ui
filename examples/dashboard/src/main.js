// Ontaic Runtime - Dashboard version
(function() {
  'use strict';

  const state = {};
  const bindings = {};

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

  function updateDomForState(key) {
    const nodeIds = bindings[key] || [];
    const value = state[key] || '';
    for (const nodeId of nodeIds) {
      const el = document.getElementById(nodeId);
      if (el) el.textContent = value;
    }
  }

  function executeHandler(handler) {
    try {
      const fn = new Function('update_state', 'get_state', `return ${handler}`);
      fn(window.ontaic.update_state, window.ontaic.get_state);
    } catch (e) {
      console.error('[ontaic] Handler error:', e);
    }
  }

  function hydrateSchema(schema) {
    const app = document.getElementById('app');
    app.innerHTML = schema.html;

    for (const [key, value] of Object.entries(schema.initialState || {})) {
      window.ontaic.init_state(key, value);
    }

    for (const [stateKey, nodeId] of Object.entries(schema.bindings || {})) {
      window.ontaic.bind_state_to_node(stateKey, nodeId);
      updateDomForState(stateKey);
    }

    for (const [nodeId, nodeEvents] of Object.entries(schema.events || {})) {
      const el = document.getElementById(nodeId);
      if (!el) continue;
      for (const [event, handler] of Object.entries(nodeEvents)) {
        el.addEventListener(event, () => executeHandler(handler));
      }
    }
  }

  async function boot() {
    try {
      const response = await fetch('/src/schema.json');
      const schema = await response.json();
      hydrateSchema(schema);
      console.log('[ontaic] Dashboard ready');
    } catch (e) {
      console.error('[ontaic] Failed to load schema:', e);
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
