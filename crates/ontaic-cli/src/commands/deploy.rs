use anyhow::Result;
use std::process::Command;

pub async fn execute(target: &str) -> Result<()> {
    match target {
        "cloudflare" => {
            println!("[ontaic] Deploying to Cloudflare Pages...");
            let status = Command::new("npx")
                .args(["wrangler", "pages", "deploy", "dist"])
                .status()?;
            if status.success() {
                println!("[ontaic] Deployed successfully");
            } else {
                anyhow::bail!("Cloudflare deployment failed");
            }
        }
        "vercel" => {
            println!("[ontaic] Deploying to Vercel...");
            let status = Command::new("npx")
                .args(["vercel", "--prod"])
                .status()?;
            if status.success() {
                println!("[ontaic] Deployed successfully");
            } else {
                anyhow::bail!("Vercel deployment failed");
            }
        }
        "s3" => {
            println!("[ontaic] Deploying to S3...");
            let status = Command::new("aws")
                .args(["s3", "sync", "dist/", "s3://my-ontaic-app"])
                .status()?;
            if status.success() {
                println!("[ontaic] Deployed successfully");
            } else {
                anyhow::bail!("S3 deployment failed");
            }
        }
        "local" => {
            println!("[ontaic] Serving locally...");
            Command::new("npx")
                .args(["vite", "preview"])
                .status()?;
        }
        _ => {
            anyhow::bail!(
                "Unknown target '{}'. Use: cloudflare, vercel, s3, local",
                target
            );
        }
    }

    Ok(())
}
