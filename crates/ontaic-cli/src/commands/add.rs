use anyhow::Result;
use reqwest::Client;
use tokio::fs;

const REGISTRY_BASE: &str = "https://raw.githubusercontent.com/ontaic/ontaic-ui/main/registry";

pub async fn execute(component: &str, theme: Option<&str>) -> Result<()> {
    let client = Client::new();

    let component_url = format!("{}/{}.py", REGISTRY_BASE, component);
    let response = client.get(&component_url).send().await?;

    if !response.status().is_success() {
        anyhow::bail!(
            "Component '{}' not found in registry. Available: button, card, input, datagrid, modal",
            component
        );
    }

    let component_code = response.text().await?;

    let meta_url = format!("{}/{}.json", REGISTRY_BASE, component);
    let meta_response = client.get(&meta_url).send().await?;
    let meta: serde_json::Value = if meta_response.status().is_success() {
        meta_response.json().await?
    } else {
        serde_json::json!({})
    };

    let final_code = if let Some(theme_name) = theme {
        apply_theme(&component_code, theme_name)?
    } else {
        component_code
    };

    fs::create_dir_all("src/components/ui").await?;
    fs::write(
        format!("src/components/ui/{}.py", component),
        &final_code,
    )
    .await?;

    if !meta.as_object().map_or(true, |o| o.is_empty()) {
        fs::write(
            format!("src/components/ui/{}.json", component),
            serde_json::to_string_pretty(&meta)?,
        )
        .await?;
    }

    println!("[ontaic] Added component: {}", component);
    if let Some(theme_name) = theme {
        println!("[ontaic] Theme applied: {}", theme_name);
    }

    Ok(())
}

fn apply_theme(code: &str, theme: &str) -> Result<String> {
    let themed = match theme {
        "glassmorphism" => code.replace(
            "class_name=\"",
            "class_name=\"backdrop-blur-md bg-white/10 border border-white/20 rounded-xl shadow-xl ",
        ),
        "brutalist" => code.replace(
            "class_name=\"",
            "class_name=\"border-4 border-black bg-yellow-300 font-mono uppercase ",
        ),
        "neon" => code.replace(
            "class_name=\"",
            "class_name=\"bg-black border-2 border-cyan-400 text-cyan-400 shadow-[0_0_15px_rgba(0,255,255,0.5)] ",
        ),
        "minimal" => code.replace(
            "class_name=\"",
            "class_name=\"bg-white border border-gray-200 rounded-lg shadow-sm ",
        ),
        _ => code.to_string(),
    };
    Ok(themed)
}
