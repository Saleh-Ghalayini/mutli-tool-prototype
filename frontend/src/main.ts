// ==============================================================================
// FRONTEND ENTRY POINT (main.ts)
// ==============================================================================
// This is the very first TypeScript file executed by the browser when index.html loads.
//
// What it does:
// 1. Imports Vue's createApp function to bootstrap a new Vue 3 application.
// 2. Imports global stylesheet (style.css) containing CSS resets and fonts.
// 3. Imports the root component (App.vue).
// 4. Mounts the Vue application onto the <div id="app"> element in index.html.

import { createApp } from 'vue'
import './style.css'
import App from './App.vue'

// Create the Vue app instance and mount it to the DOM
createApp(App).mount('#app')