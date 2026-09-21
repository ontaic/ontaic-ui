use anyhow::Result;
use std::process::Command;

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
    println!("[ontaic] Edit app.py and save to see changes");

    Command::new("npx")
        .args(["vite", "--port", &port.to_string()])
        .status()?;

    Ok(())
}
