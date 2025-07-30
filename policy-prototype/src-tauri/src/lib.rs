use serde::{Deserialize, Serialize};
use std::process::{Command, Child, Stdio};
use std::sync::Arc;
use tokio::sync::Mutex as TokioMutex;
use anyhow::Result;
use tauri::Manager;

// Global Python backend process
static PYTHON_BACKEND: std::sync::OnceLock<Arc<TokioMutex<Option<Child>>>> = std::sync::OnceLock::new();

#[derive(Serialize, Deserialize, Debug)]
pub struct AppInfo {
    name: String,
    version: String,
    description: String,
}

#[tauri::command]
async fn get_app_info() -> Result<AppInfo, String> {
    Ok(AppInfo {
        name: "Policy Prototype".to_string(),
        version: "0.1.0".to_string(),
        description: "A client-specific, offline policy assistant".to_string(),
    })
}

#[tauri::command]
async fn start_python_backend(app_handle: tauri::AppHandle) -> Result<String, String> {
    log::info!("Starting Python backend subprocess...");
    let backend_container = PYTHON_BACKEND.get_or_init(|| {
        Arc::new(TokioMutex::new(None))
    });
    let mut backend = backend_container.lock().await;
    if backend.is_some() {
        return Ok("Python backend already running".to_string());
    }
    let child = Command::new("python")
        .arg("-m")
        .arg("backend.main")
        .stdout(Stdio::piped())
        .stderr(Stdio::piped())
        .spawn()
        .map_err(|e| format!("Failed to start Python backend: {}", e))?;
    *backend = Some(child);
    Ok("Python backend started".to_string())
}

pub fn run() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![get_app_info, start_python_backend])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
