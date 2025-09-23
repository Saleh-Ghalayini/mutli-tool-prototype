// ==============================================================================
// TAURI APPLICATION CORE LIBRARY (src/lib.rs)
// ==============================================================================
// This file coordinates the desktop window lifecycle and acts as the bridge
// between the frontend JavaScript UI and the operating system.
//
// Key Responsibilities:
// 1. Spawns the Python FastAPI backend server as a background sidecar subprocess.
// 2. Exposes Tauri IPC (Inter-Process Communication) commands that the frontend can call.
// 3. Initializes and runs the native desktop window.

use serde::{Deserialize, Serialize};
use std::process::{Command, Child, Stdio};
use std::sync::Arc;
use tokio::sync::Mutex as TokioMutex;
use anyhow::Result;
use tauri::Manager;

// ------------------------------------------------------------------------------
// Global Thread-Safe Python Process Handle (Sidecar Management)
// ------------------------------------------------------------------------------
// OnceLock: Ensures this variable is initialized safely only once across threads.
// Arc: Atomic Reference Counting pointer (allows sharing ownership safely across async tasks).
// TokioMutex: Async mutex protecting the Child process handle from concurrent mutations.
// Option<Child>: Holds 'Some(process)' when running, or 'None' when stopped.
static PYTHON_BACKEND: std::sync::OnceLock<Arc<TokioMutex<Option<Child>>>> = std::sync::OnceLock::new();

// ------------------------------------------------------------------------------
// Data Transfer Object (DTO): AppInfo
// ------------------------------------------------------------------------------
// Serialize / Deserialize (from serde):
// Automatically converts this Rust struct into JSON when sending data to JavaScript.
#[derive(Serialize, Deserialize, Debug)]
pub struct AppInfo {
    name: String,
    version: String,
    description: String,
}

// ------------------------------------------------------------------------------
// Tauri Command: get_app_info
// ------------------------------------------------------------------------------
// Functions annotated with `#[tauri::command]` can be directly invoked from
// JavaScript in the Vue frontend via: `await invoke('get_app_info')`.
#[tauri::command]
async fn get_app_info() -> Result<AppInfo, String> {
    Ok(AppInfo {
        name: "Policy Prototype".to_string(),
        version: "0.1.0".to_string(),
        description: "A client-specific, offline policy assistant".to_string(),
    })
}

// ------------------------------------------------------------------------------
// Tauri Command: start_python_backend
// ------------------------------------------------------------------------------
// Spawns the Python FastAPI server as an independent child process.
// This allows the desktop app to start its own backend automatically without
// requiring the user to open a terminal or run `uvicorn main:app`.
#[tauri::command]
async fn start_python_backend(app_handle: tauri::AppHandle) -> Result<String, String> {
    log::info!("Starting Python backend subprocess...");
    
    // Retrieve or initialize the thread-safe container
    let backend_container = PYTHON_BACKEND.get_or_init(|| {
        Arc::new(TokioMutex::new(None))
    });
    
    // Acquire the lock to safely inspect or start the process
    let mut backend = backend_container.lock().await;
    if backend.is_some() {
        return Ok("Python backend already running".to_string());
    }
    
    // Spawn `python -m backend.main` as a child process
    let child = Command::new("python")
        .arg("-m")
        .arg("backend.main")
        .stdout(Stdio::piped())  // Capture standard output
        .stderr(Stdio::piped())  // Capture error logs
        .spawn()
        .map_err(|e| format!("Failed to start Python backend: {}", e))?;
        
    // Store the child process handle in our global state
    *backend = Some(child);
    Ok("Python backend started successfully".to_string())
}

// ------------------------------------------------------------------------------
// Main Application Runner
// ------------------------------------------------------------------------------
pub fn run() {
    tauri::Builder::default()
        // Register the IPC commands so the frontend can call them by name
        .invoke_handler(tauri::generate_handler![get_app_info, start_python_backend])
        // Build and launch the Tauri runtime and open the desktop window
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}

