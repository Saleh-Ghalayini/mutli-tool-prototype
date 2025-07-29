use serde::{Deserialize, Serialize};
use std::process::{Command, Child, Stdio};
use std::sync::Arc;
use tokio::sync::Mutex as TokioMutex;
use anyhow::Result;
use tauri::Manager;

// Global Python backend process
static PYTHON_BACKEND: std::sync::OnceLock<Arc<TokioMutex<Option<Child>>>> = std::sync::OnceLock::new();

// Data structures for our API
#[derive(Serialize, Deserialize, Debug)]
pub struct AppInfo {
    name: String,
    version: String,
    description: String,
}

// Tauri command functions
#[tauri::command]
async fn get_app_info() -> Result<AppInfo, String> {
    Ok(AppInfo {
        name: "Multi-Tool AI".to_string(),
        version: "1.0.0".to_string(),
        description: "A multi-tool platform made up of small, single-use AI utilities".to_string(),
    })
}

#[tauri::command]
async fn start_python_backend(app_handle: tauri::AppHandle) -> Result<String, String> {
    log::info!("Starting Python backend subprocess...");
    
    // Get or initialize the Python backend container
    let backend_container = PYTHON_BACKEND.get_or_init(|| {
        Arc::new(TokioMutex::new(None))
    });
    
    let mut backend = backend_container.lock().await;
    
    // If already running, return success
    if let Some(ref mut child) = *backend {
        match child.try_wait() {
            Ok(Some(_)) => {
                log::info!("Previous Python backend process has exited, starting new one");
                *backend = None;
            },
            Ok(None) => {
                log::info!("Python backend is already running");
                return Ok("Python backend already running".to_string());
            },
            Err(e) => {
                log::error!("Error checking Python backend status: {}", e);
                *backend = None;
            }
        }
    }
    
    // Start new Python backend process
    // In bundled mode, resources are in the app's resource directory
    let app_dir = app_handle
        .path()
        .resource_dir()
        .map_err(|e| format!("Failed to get resource directory: {}", e))?;
    
    let python_backend_dir = app_dir.join("backend");
    
    log::info!("Starting Python backend in directory: {:?}", python_backend_dir);
    
    // Try different Python executables in order of preference
    let python_executables = vec!["python", "python3", "py"];
    let mut child = None;
    
    for python_exe in python_executables {
        match Command::new(python_exe)
            .arg("main.py")
            .current_dir(&python_backend_dir)
            .stdout(Stdio::piped())
            .stderr(Stdio::piped())
            .spawn()
        {
            Ok(c) => {
                child = Some(c);
                log::info!("Python backend started with: {}", python_exe);
                break;
            }
            Err(e) => {
                log::warn!("Failed to start with {}: {}", python_exe, e);
                continue;
            }
        }
    }
    
    let child = child.ok_or("Failed to start Python backend with any Python executable")?;
    
    *backend = Some(child);
    log::info!("Python backend started successfully");
    
    Ok("Python backend started successfully".to_string())
}

#[tauri::command]
async fn stop_python_backend() -> Result<String, String> {
    log::info!("Stopping Python backend subprocess...");
    
    if let Some(backend_container) = PYTHON_BACKEND.get() {
        let mut backend = backend_container.lock().await;
        
        if let Some(mut child) = backend.take() {
            match child.kill() {
                Ok(_) => {
                    log::info!("Python backend stopped successfully");
                    Ok("Python backend stopped successfully".to_string())
                },
                Err(e) => {
                    log::error!("Failed to stop Python backend: {}", e);
                    Err(format!("Failed to stop Python backend: {}", e))
                }
            }
        } else {
            Ok("Python backend was not running".to_string())
        }
    } else {
        Ok("Python backend was not initialized".to_string())
    }
}

#[tauri::command]
async fn get_python_backend_status() -> Result<String, String> {
    if let Some(backend_container) = PYTHON_BACKEND.get() {
        let mut backend = backend_container.lock().await;
        
        if let Some(ref mut child) = *backend {
            match child.try_wait() {
                Ok(Some(status)) => Ok(format!("Exited with status: {:?}", status)),
                Ok(None) => Ok("Running".to_string()),
                Err(e) => Ok(format!("Error checking status: {}", e)),
            }
        } else {
            Ok("Not started".to_string())
        }
    } else {
        Ok("Not initialized".to_string())
    }
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![
            get_app_info,
            start_python_backend,
            stop_python_backend,
            get_python_backend_status
        ])
        .setup(|app| {
            if cfg!(debug_assertions) {
                app.handle().plugin(
                    tauri_plugin_log::Builder::default()
                        .level(log::LevelFilter::Info)
                        .build(),
                )?;
            }
            log::info!("Tauri app started - Auto-starting Python backend...");
            
            // Auto-start the Python backend on app startup
            let app_handle = app.handle().clone();
            tauri::async_runtime::spawn(async move {
                // Wait a moment for the app to fully initialize
                tokio::time::sleep(tokio::time::Duration::from_millis(1000)).await;
                
                // In dev mode, start from the actual backend directory
                let python_backend_dir = if cfg!(debug_assertions) {
                    // Development mode - use the actual backend directory
                    std::env::current_dir()
                        .unwrap()
                        .parent()
                        .unwrap()
                        .join("backend")
                } else {
                    // Production mode - use bundled resources
                    let app_dir = app_handle
                        .path()
                        .resource_dir()
                        .expect("Failed to get resource directory");
                    app_dir.join("backend")
                };
                
                log::info!("Auto-starting Python backend in directory: {:?}", python_backend_dir);
                
                // Try different Python executables in order of preference
                let python_executables = vec!["python", "python3", "py"];
                let mut child = None;
                
                for python_exe in python_executables {
                    match Command::new(python_exe)
                        .arg("main.py")
                        .current_dir(&python_backend_dir)
                        .stdout(Stdio::piped())
                        .stderr(Stdio::piped())
                        .spawn()
                    {
                        Ok(c) => {
                            child = Some(c);
                            log::info!("Python backend auto-started with: {}", python_exe);
                            break;
                        }
                        Err(e) => {
                            log::warn!("Failed to auto-start with {}: {}", python_exe, e);
                            continue;
                        }
                    }
                }
                
                if let Some(child) = child {
                    let backend_container = PYTHON_BACKEND.get_or_init(|| {
                        Arc::new(TokioMutex::new(None))
                    });
                    let mut backend = backend_container.lock().await;
                    *backend = Some(child);
                    log::info!("Python backend auto-started successfully");
                } else {
                    log::error!("Failed to auto-start Python backend with any Python executable");
                }
            });
            
            // Cleanup Python backend on app shutdown
            let _app_handle = app.handle().clone();
            tauri::async_runtime::spawn(async move {
                // Wait for app to be ready, then set up cleanup
                tokio::signal::ctrl_c().await.ok();
                log::info!("Shutting down Python backend...");
                if let Some(backend_container) = PYTHON_BACKEND.get() {
                    let mut backend = backend_container.lock().await;
                    if let Some(mut child) = backend.take() {
                        let _ = child.kill();
                    }
                }
            });
            
            Ok(())
        })
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
