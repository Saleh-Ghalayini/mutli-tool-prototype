<template>
  <div class="loading-indicator">
    <div class="loading-content">
      <div class="typing-dots">
        <span></span>
        <span></span>
        <span></span>
      </div>
      <div class="loading-text">AI is thinking...</div>
    </div>
  </div>
</template>

<script setup lang="ts">
// No props needed for this component
</script>

<style scoped>
.loading-indicator {
  margin: 0.5rem 0;
  display: flex;
  justify-content: flex-start;
  animation: fadeInUp 0.3s ease-out;
}

.loading-content {
  background: #2d3748;
  border: 1px solid #4a5568;
  border-radius: 12px;
  padding: 0.6rem 0.8rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
  display: flex;
  align-items: center;
  gap: 0.6rem;
}

.typing-dots {
  display: flex;
  gap: 3px;
}

.typing-dots span {
  width: 5px;
  height: 5px;
  border-radius: 50%;
  background: #4299e1;
  animation: typing 1.4s infinite ease-in-out;
}

.typing-dots span:nth-child(1) {
  animation-delay: 0s;
}

.typing-dots span:nth-child(2) {
  animation-delay: 0.2s;
}

.typing-dots span:nth-child(3) {
  animation-delay: 0.4s;
}

.loading-text {
  font-size: 0.8rem;
  color: #a0aec0;
  font-style: italic;
}

@keyframes typing {
  0%, 60%, 100% {
    transform: translateY(0);
    opacity: 0.4;
  }
  30% {
    transform: translateY(-6px);
    opacity: 1;
  }
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(8px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>