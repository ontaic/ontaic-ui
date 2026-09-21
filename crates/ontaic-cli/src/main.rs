use clap::{Parser, Subcommand};

mod commands;

#[derive(Parser)]
#[command(name = "ontaic")]
#[command(about = "Ontaic: Bi-Directional Compiler & State Runtime")]
struct Cli {
    #[command(subcommand)]
    command: Commands,
}

#[derive(Subcommand)]
enum Commands {
    /// Initialize a new Ontaic project
    Init {
        #[arg(default_value = ".")]
        path: String,
    },
    /// Add a component from the registry
    Add {
        /// Component name (e.g., button, datagrid)
        component: String,
        #[arg(short, long)]
        theme: Option<String>,
    },
    /// Start development server
    Dev {
        #[arg(short, long, default_value = "5173")]
        port: u16,
    },
    /// Build for production
    Build,
    /// Deploy to edge hosting
    Deploy {
        #[arg(value_parser = ["cloudflare", "vercel", "s3", "local"])]
        target: String,
    },
}

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    let cli = Cli::parse();

    match cli.command {
        Commands::Init { path } => commands::init::execute(&path).await,
        Commands::Add { component, theme } => {
            commands::add::execute(&component, theme.as_deref()).await
        }
        Commands::Dev { port } => commands::dev::execute(port).await,
        Commands::Build => commands::build::execute().await,
        Commands::Deploy { target } => commands::deploy::execute(&target).await,
    }
}
