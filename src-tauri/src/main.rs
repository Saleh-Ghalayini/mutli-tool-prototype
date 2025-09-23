// ==============================================================================
// TAURI DESKTOP APPLICATION ENTRY POINT (Rust)
// ==============================================================================
// Tauri allows building desktop apps using web frontends (Vue 3) backed by Rust.
//
// What is this line?
// `#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]`
// On Windows, when you build a release executable (.exe), Windows normally launches
// a black Command Prompt window behind your graphical window.
// This attribute tells the Windows OS compiler: "In release builds, this is a pure GUI
// application, so do NOT open a terminal console window."
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

fn main() {
    // Calls the run() function defined in src/lib.rs, which configures Tauri plugins,
    // registers IPC command handlers, launches the Python backend, and creates the window.
    policy_prototype_lib::run();
}

