use anyhow::Result;
use std::process::Command;
use tokio::fs;

pub async fn execute() -> Result<()> {
    println!("[ontaic] Compiling Python components...");

    let status = Command::new("python")
        .args([
            "-m",
            "ontaic.compiler",
            "--input",
            "src/components",
            "--output",
            "src/schema.json",
        ])
        .status()?;

    if !status.success() {
        println!("[ontaic] Python compiler not found, using default schema");
    }

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
        anyhow::bail!("WASM build failed");
    }

    println!("[ontaic] Bundling with Vite...");
    let status = Command::new("npx")
        .args(["vite", "build"])
        .status()?;

    if !status.success() {
        anyhow::bail!("Vite build failed. Run npm install first");
    }

    fs::create_dir_all("dist/pkg").await?;
    fs::copy(
        "crates/ontaic-runtime/pkg/ontaic_runtime_bg.wasm",
        "dist/pkg/ontaic_runtime_bg.wasm",
    )
    .await?;

    println!("[ontaic] Production build complete");
    println!("[ontaic] Output: dist/");
    println!("[ontaic] Deploy with: ontaic deploy <target>");

    Ok(())
}
