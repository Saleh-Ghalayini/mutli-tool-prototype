<template>
  <div class="input-area">
    <div class="input-container">
      <textarea
        v-model="message"
        @keydown="handleKeyDown"
        @input="adjustHeight"
        ref="textareaRef"
        placeholder="Type your message..."
        :disabled="disabled"
        class="message-input"
        rows="1"
      ></textarea>
      
      <button
        @click="sendMessage"
        :disabled="disabled || !message.trim()"
        class="send-button"
      >
        <span v-if="!disabled">Send</span>
        <span v-else>...</span>
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, nextTick } from 'vue'

const emit = defineEmits<{
  sendMessage: [message: string]
}>()

defineProps<{
  disabled?: boolean
}>()

const message = ref('')
const textareaRef = ref<HTMLTextAreaElement>()

const adjustHeight = () => {
  nextTick(() => {
    if (textareaRef.value) {
      textareaRef.value.style.height = 'auto'
      textareaRef.value.style.height = Math.min(textareaRef.value.scrollHeight, 120) + 'px'
    }
  })
}

const sendMessage = () => {
  if (message.value.trim()) {
    emit('sendMessage', message.value)
    message.value = ''
    adjustHeight()
  }
}

const handleKeyDown = (event: KeyboardEvent) => {
  if (event.key === 'Enter' && !event.shiftKey) {
    event.preventDefault()
    sendMessage()
  }
}
</script>

<style scoped>
.input-area {
  padding: 0.75rem;
  background: #2d3748;
  border-top: 1px solid #4a5568;
}

.input-container {
  max-width: 800px;
  margin: 0 auto;
  display: flex;
  align-items: flex-end;
  gap: 0.6rem;
  background: #1a202c;
  border-radius: 8px;
  padding: 0.4rem;
  border: 1px solid #4a5568;
}

.message-input {
  flex: 1;
  border: none;
  outline: none;
  background: transparent;
  font-size: 0.9rem;
  line-height: 1.4;
  padding: 0.4rem 0.6rem;
  resize: none;
  max-height: 120px;
  min-height: 20px;
  font-family: inherit;
  color: #e2e8f0;
}

.message-input::placeholder {
  color: #718096;
}

.message-input:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.send-button {
  padding: 0.4rem 0.8rem;
  border: none;
  border-radius: 6px;
  background: #4299e1;
  color: white;
  font-size: 0.85rem;
  cursor: pointer;
  transition: background-color 0.2s ease;
  flex-shrink: 0;
  font-weight: 500;
}

.send-button:hover:not(:disabled) {
  background: #3182ce;
}

.send-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  background: #718096;
}

/* Mobile responsiveness */
@media (max-width: 768px) {
  .input-area {
    padding: 0.6rem;
  }
  
  .input-container {
    padding: 0.3rem;
  }
  
  .message-input {
    padding: 0.3rem 0.5rem;
    font-size: 0.85rem;
  }
  
  .send-button {
    padding: 0.3rem 0.6rem;
    font-size: 0.8rem;
  }
}
</style>