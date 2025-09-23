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
// ==============================================================================
// INPUT AREA COMPONENT
// ==============================================================================
// Responsible for:
// 1. Providing an auto-expanding multi-line text input field
// 2. Handling Enter / Shift+Enter keyboard events
// 3. Emitting the message text to the parent ChatContainer component
// 4. Disabling input and button while the AI is generating an answer

import { ref, nextTick } from 'vue'

// ------------------------------------------------------------------------------
// Component Events (defineEmits)
// ------------------------------------------------------------------------------
// In Vue 3, child components do not modify parent state directly.
// Instead, they "emit" custom events that parents listen to (e.g. @send-message="...").
const emit = defineEmits<{
  sendMessage: [message: string] // Emits an event named 'sendMessage' carrying the string payload
}>()

// ------------------------------------------------------------------------------
// Component Properties (defineProps)
// ------------------------------------------------------------------------------
// Passed from parent: disabled is true when the AI is actively streaming a response
defineProps<{
  disabled?: boolean
}>()

// Reactive variable bound to the <textarea> via v-model
const message = ref('')
// Template reference allowing direct access to the DOM <textarea> element
const textareaRef = ref<HTMLTextAreaElement>()

// ------------------------------------------------------------------------------
// Dynamic Textarea Auto-Growing
// ------------------------------------------------------------------------------
const adjustHeight = () => {
  nextTick(() => {
    if (textareaRef.value) {
      // Reset height to 'auto' first so shrinking works if text is deleted
      textareaRef.value.style.height = 'auto'
      // Set height equal to scrollHeight (content height), capped at a maximum of 120px
      textareaRef.value.style.height = Math.min(textareaRef.value.scrollHeight, 120) + 'px'
    }
  })
}

// ------------------------------------------------------------------------------
// Send Message Action
// ------------------------------------------------------------------------------
const sendMessage = () => {
  // Only send if the input has non-empty text
  if (message.value.trim()) {
    // Notify parent component with the typed message
    emit('sendMessage', message.value)
    // Clear the input box
    message.value = ''
    // Reset textarea height back to single-row
    adjustHeight()
  }
}

// ------------------------------------------------------------------------------
// Keyboard Event Listener: Enter vs Shift+Enter
// ------------------------------------------------------------------------------
const handleKeyDown = (event: KeyboardEvent) => {
  // If the user hits Enter WITHOUT pressing Shift, submit the message.
  // If Shift+Enter is pressed, default behavior occurs (inserts a regular newline).
  if (event.key === 'Enter' && !event.shiftKey) {
    event.preventDefault() // Prevent insertion of a blank newline character
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