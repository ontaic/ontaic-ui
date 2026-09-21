use anyhow::Result;
use tokio::fs;

pub async fn execute(path: &str) -> Result<()> {
    let root = std::path::Path::new(path);

    fs::create_dir_all(root.join("src/components/ui")).await?;
    fs::create_dir_all(root.join("src/styles")).await?;
    fs::create_dir_all(root.join("public")).await?;

    let package_json = serde_json::json!({
        "name": "ontaic-app",
        "private": true,
        "scripts": {
            "dev": "vite",
            "build": "vite build",
            "preview": "vite preview"
        },
        "devDependencies": {
            "vite": "^5.0.0",
            "tailwindcss": "^3.4.0",
            "autoprefixer": "^10.0.0",
            "postcss": "^8.0.0"
        }
    });
    fs::write(
        root.join("package.json"),
        serde_json::to_string_pretty(&package_json)?,
    )
    .await?;

    let vite_config = r#"import { defineConfig } from 'vite';
import wasm from "vite-plugin-wasm";

export default defineConfig({
  plugins: [wasm()],
  optimizeDeps: {
    exclude: ["ontaic-runtime"]
  }
});
"#;
    fs::write(root.join("vite.config.js"), vite_config).await?;

    let tailwind_config = r#"/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
    "./src/components/**/*.py"
  ],
  theme: {
    extend: {},
  },
  plugins: [],
};
"#;
    fs::write(root.join("tailwind.config.js"), tailwind_config).await?;

    let postcss_config = r#"export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
};
"#;
    fs::write(root.join("postcss.config.js"), postcss_config).await?;

    let main_css = r#"@tailwind base;
@tailwind components;
@tailwind utilities;
"#;
    fs::write(root.join("src/styles/main.css"), main_css).await?;

    let index_html = r#"<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Ontaic App</title>
  <link href="/src/styles/main.css" rel="stylesheet" />
</head>
<body>
  <div id="app"></div>
  <script type="module" src="/src/main.js"></script>
</body>
</html>
"#;
    fs::write(root.join("index.html"), index_html).await?;

    let main_js = r#"import init, {
  bind_state_to_node,
  update_state,
  init_state,
  get_state
} from './pkg/ontaic_runtime.js';

async function boot() {
  await init();

  const schema = await fetch('/src/schema.json').then(r => r.json()).catch(() => ({
    html: '<div id="app"><p>Loading...</p></div>',
    bindings: {},
    events: {},
    initialState: {}
  }));

  hydrateSchema(schema);
  console.log('[ontaic] Engine ready');
}

function hydrateSchema(schema) {
  const app = document.getElementById('app');
  app.innerHTML = schema.html;

  for (const [stateKey, nodeId] of Object.entries(schema.bindings)) {
    bind_state_to_node(stateKey, nodeId);
    init_state(stateKey, schema.initialState[stateKey] || '');
  }

  for (const [nodeId, events] of Object.entries(schema.events)) {
    const el = document.getElementById(nodeId);
    if (!el) continue;
    for (const [event, handler] of Object.entries(events)) {
      el.addEventListener(event.toLowerCase(), () => {
        const fn = new Function('update_state', 'get_state', handler);
        fn(update_state, get_state);
      });
    }
  }
}

boot();
"#;
    fs::write(root.join("src/main.js"), main_js).await?;

    let schema = serde_json::json!({
        "version": "1.0",
        "html": "<div id=\"app\" class=\"min-h-screen bg-gray-50 flex items-center justify-center\"><p class=\"text-gray-500\">Edit app.py to get started</p></div>",
        "bindings": {},
        "events": {},
        "initialState": {}
    });
    fs::write(
        root.join("src/schema.json"),
        serde_json::to_string_pretty(&schema)?,
    )
    .await?;

    println!("[ontaic] Project initialized at {}", root.display());
    println!("[ontaic] Next steps:");
    println!("  1. cd {}", root.display());
    println!("  2. npm install");
    println!("  3. ontaic dev");

    Ok(())
}
