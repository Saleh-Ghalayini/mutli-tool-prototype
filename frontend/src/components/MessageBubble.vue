<template>
  <!-- 
    Dynamic Class Binding:
    - If message.isUser is true, adds 'user-message' class (aligns right, blue background).
    - If message.isUser is false, adds 'ai-message' class (aligns left, dark-grey background).
  -->
  <div class="message-bubble" :class="{ 'user-message': message.isUser, 'ai-message': !message.isUser }">
    <div class="message-content">
      <div class="message-text">
        <!-- Render the message text. white-space: pre-wrap preserves newlines and formatting -->
        <p>{{ message.text }}</p>
        <!-- Formatted timestamp display (e.g. 10:24 AM) -->
        <div class="message-time">
          {{ formatTime(message.timestamp) }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// ==============================================================================
// MESSAGE BUBBLE COMPONENT
// ==============================================================================
// A presentational component responsible for displaying an individual chat entry.
// Automatically distinguishes between user queries and AI responses.

interface Message {
  id: number
  text: string
  isUser: boolean
  timestamp: Date
}

// Receive the message object from parent ChatContainer
defineProps<{
  message: Message
}>()

/**
 * Format a Date object into a readable 12-hour or 24-hour time string (e.g. "02:30 PM")
 */
const formatTime = (date: Date) => {
  return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}
</script>

<style scoped>
.message-bubble {
  margin: 0.5rem 0;
  display: flex;
  animation: fadeInUp 0.3s ease-out;
}

.user-message {
  justify-content: flex-end;
}

.ai-message {
  justify-content: flex-start;
}

.message-content {
  max-width: 75%;
}

.message-text {
  padding: 0.6rem 0.9rem;
  border-radius: 12px;
  word-wrap: break-word;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
}

.user-message .message-text {
  background: #4299e1;
  color: white;
}

.ai-message .message-text {
  background: #2d3748;
  color: #e2e8f0;
  border: 1px solid #4a5568;
}

.message-text p {
  margin: 0;
  line-height: 1.4;
  font-size: 0.9rem;
  white-space: pre-wrap;
}

.message-time {
  font-size: 0.7rem;
  opacity: 0.7;
  margin-top: 0.2rem;
  text-align: right;
}

.user-message .message-time {
  color: rgba(255, 255, 255, 0.8);
}

.ai-message .message-time {
  color: #a0aec0;
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

/* Mobile responsiveness */
@media (max-width: 768px) {
  .message-content {
    max-width: 90%;
  }
  
  .message-text {
    padding: 0.5rem 0.7rem;
  }
}
</style>