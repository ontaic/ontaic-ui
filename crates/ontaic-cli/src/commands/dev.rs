use anyhow::Result;
use std::path::Path;
use std::process::Command;
use std::time::Duration;
use notify::{Config, RecommendedWatcher, RecursiveMode, Watcher};

pub async fn execute(port: u16) -> Result<()> {
    println!("[ontaic] Building WASM runtime...");

    let status = Command::new("wasm-pack")
        .args([
            "build",
            "--target",
            "web",
            "--release",
            "crates/ontaic-runtime",
        ])
        .status()?;

    if !status.success() {
        anyhow::bail!("WASM build failed. Is wasm-pack installed? cargo install wasm-pack");
    }

    std::fs::create_dir_all("src/pkg")?;
    std::fs::create_dir_all("public/pkg")?;

    std::fs::copy(
        "crates/ontaic-runtime/pkg/ontaic_runtime_bg.wasm",
        "public/pkg/ontaic_runtime_bg.wasm",
    )?;
    std::fs::copy(
        "crates/ontaic-runtime/pkg/ontaic_runtime.js",
        "src/pkg/ontaic_runtime.js",
    )?;

    println!("[ontaic] WASM build complete");
    println!("[ontaic] Starting dev server on port {}...", port);
    println!("[ontaic] Watching for Python file changes...");

    // Spawn Vite dev server
    let mut vite_child = Command::new("npx")
        .args(["vite", "--port", &port.to_string()])
        .spawn()?;

    // Watch for Python file changes
    let (tx, rx) = std::sync::mpsc::channel();
    let mut watcher = RecommendedWatcher::new(tx, Config::default())?;

    // Watch current directory for .py files
    let watch_path = Path::new(".");
    watcher.watch(watch_path, RecursiveMode::Recursive)?;

    println!("[ontaic] Hot-reload enabled. Edit .py files to see changes.");

    // Event loop
    loop {
        // Check for file changes
        if let Ok(event) = rx.recv_timeout(Duration::from_millis(100)) {
            if let Ok(event) = event {
                if event.kind.is_modify() || event.kind.is_create() {
                    // Check if any changed file is a .py file
                    let has_python_change = event.paths.iter().any(|p| {
                        p.extension().map_or(false, |e| e == "py")
                    });

                    if has_python_change {
                        println!("[ontaic] Python file changed, recompiling schema...");

                        // Find app.py in current directory
                        let app_py = Path::new("app.py");
                        if app_py.exists() {
                            // Run Python compiler
                            let compile_status = Command::new("python")
                                .args(["-c", "from ontaic.compiler import OntaicCompiler; OntaicCompiler().compile_directory('.', 'public/schema.json')"])
                                .status();

                            match compile_status {
                                Ok(status) if status.success() => {
                                    println!("[ontaic] Schema recompiled successfully");
                                    // Touch index.html to trigger Vite HMR
                                    let _ = std::fs::write("index.html", std::fs::read_to_string("index.html")?);
                                }
                                Ok(_) => {
                                    eprintln!("[ontaic] Compilation failed");
                                }
                                Err(e) => {
                                    eprintln!("[ontaic] Failed to run compiler: {}", e);
                                }
                            }
                        }
                    }
                }
            }
        }

        // Check if Vite is still running
        if let Ok(Some(_)) = vite_child.try_wait() {
            println!("[ontaic] Dev server stopped");
            break;
        }
    }

    Ok(())
}
