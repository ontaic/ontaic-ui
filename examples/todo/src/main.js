import init, { patch } from 'ontaic-runtime';

let schema = null;
let state = {};

async function loadSchema() {
  try {
    const response = await fetch('/schema.json');
    schema = await response.json();
    state = { ...schema.initialState };
    renderApp();
  } catch (error) {
    console.error('Failed to load schema:', error);
    document.getElementById('app').innerHTML = `
      <div class="p-8 text-center">
        <h1 class="text-2xl font-bold mb-4">Schema not found</h1>
        <p class="text-gray-600">Run the compiler to generate schema.json</p>
      </div>
    `;
  }
}

function renderApp() {
  const app = document.getElementById('app');
  app.innerHTML = schema.html;
  
  // Apply bindings
  Object.entries(schema.bindings).forEach(([stateKey, nodeId]) => {
    const element = document.getElementById(nodeId);
    if (element) {
      element.textContent = state[stateKey] || '';
    }
  });
  
  // Setup events
  Object.entries(schema.events).forEach(([nodeId, events]) => {
    const element = document.getElementById(nodeId);
    if (element) {
      Object.entries(events).forEach(([eventType, handler]) => {
        element.addEventListener(eventType, () => {
          evaluateHandler(handler);
        });
      });
    }
  });
}

function evaluateHandler(handler) {
  try {
    const stateKeys = Object.keys(state);
    const stateValues = Object.values(state);
    
    const fn = new Function(...stateKeys, handler);
    const result = fn(...stateValues);
    
    if (typeof result === 'string' && result.startsWith('update_state(')) {
      const match = result.match(/update_state\('(\w+)',\s*(.+)\)/);
      if (match) {
        const [, key, value] = match;
        state[key] = evaluateValue(value);
        renderApp();
      }
    }
  } catch (error) {
    console.error('Handler error:', error);
  }
}

function evaluateValue(value) {
  if (value === 'true') return true;
  if (value === 'false') return false;
  if (!isNaN(value)) return Number(value);
  return value.replace(/['"]/g, '');
}

function get_state(key) {
  return state[key];
}

function update_state(key, value) {
  state[key] = value;
  renderApp();
}

// Make functions available globally
window.get_state = get_state;
window.update_state = update_state;
window.navigate = (path) => {
  window.history.pushState({}, '', path);
  renderApp();
};

// Initialize
loadSchema();

// Handle navigation
window.addEventListener('popstate', () => {
  renderApp();
});
