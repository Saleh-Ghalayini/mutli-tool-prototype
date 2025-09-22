<template>
  <div id="app">
    <div class="app-container">
      <header class="app-header">
        <h1>🤖 AI Assistant</h1>
        <p>Ask me anything about your documents</p>
      </header>
      
      <ChatContainer />
    </div>
  </div>
</template>

<script setup lang="ts">
import ChatContainer from './components/ChatContainer.vue'
</script>

<style scoped>
.app-container {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: #1a202c;
}

.app-header {
  text-align: center;
  padding: 1rem;
  background: #2d3748;
  border-bottom: 1px solid #4a5568;
  box-shadow: 0 2px 4px rgba(0,0,0,0.3);
}

.app-header h1 {
  margin: 0 0 0.3rem 0;
  font-size: 1.6rem;
  font-weight: 600;
  color: #e2e8f0;
}

.app-header p {
  margin: 0;
  color: #a0aec0;
  font-size: 0.9rem;
}
</style>