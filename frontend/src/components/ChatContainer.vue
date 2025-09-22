<template>
  <div class="chat-container">
    <div class="messages-container" ref="messagesContainer">
      <div v-if="messages.length === 0" class="welcome-message">
        <div class="welcome-card">
          <h2>👋 Hello!</h2>
          <p>I'm your AI assistant. Ask me anything!</p>
          <div class="example-queries">
            <p><strong>Try asking:</strong></p>
            <p>"What is the company policy on vacation?"</p>
            <p>"Tell me about remote work"</p>
          </div>
        </div>
      </div>
      
      <MessageBubble
        v-for="message in messages"
        :key="message.id"
        :message="message"
      />
      
      <LoadingIndicator v-if="isLoading" />
    </div>
    
    <InputArea
      @send-message="handleSendMessage"
      :disabled="isLoading"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, nextTick, onMounted } from 'vue'
import MessageBubble from './MessageBubble.vue'
import InputArea from './InputArea.vue'
import LoadingIndicator from './LoadingIndicator.vue'
import { searchPolicyStream, searchPolicySimple } from '../services/apiService'

interface Message {
  id: number
  text: string
  isUser: boolean
  timestamp: Date
}

const messages = ref<Message[]>([])
const isLoading = ref(false)
const messagesContainer = ref<HTMLElement>()
let messageIdCounter = 0

const scrollToBottom = () => {
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
    }
  })
}

const handleSendMessage = async (messageText: string) => {
  if (!messageText.trim()) return
  
  // Add user message
  const userMessage: Message = {
    id: messageIdCounter++,
    text: messageText,
    isUser: true,
    timestamp: new Date()
  }
  messages.value.push(userMessage)
  scrollToBottom()
  
  // Show loading indicator
  isLoading.value = true
  
  try {
    let hasReceivedData = false
    
    try {
      // Try streaming first
      await searchPolicyStream(messageText, (chunk: string) => {
        console.log('Processing chunk in UI:', chunk)
        
        if (!hasReceivedData) {
          // Create AI response message only when we get the first chunk
          const aiMessage: Message = {
            id: messageIdCounter++,
            text: chunk,
            isUser: false,
            timestamp: new Date()
          }
          messages.value.push(aiMessage)
          hasReceivedData = true
          console.log('Created new AI message with first chunk:', aiMessage.text)
        } else {
          // Find the last AI message and update it
          const lastMessageIndex = messages.value.length - 1
          const lastMessage = messages.value[lastMessageIndex]
          
          if (lastMessage && !lastMessage.isUser) {
            // Create a completely new message object to trigger reactivity
            const updatedMessage: Message = {
              ...lastMessage,
              text: lastMessage.text + chunk
            }
            // Replace the entire message in the array
            messages.value.splice(lastMessageIndex, 1, updatedMessage)
            console.log('Updated AI message, new text length:', updatedMessage.text.length)
          }
        }
        
        // Force scroll and UI update
        nextTick(() => {
          scrollToBottom()
        })
      })
    } catch (streamError) {
      console.log('Streaming failed, trying simple request:', streamError)
      
      try {
        // Fallback to simple request
        const response = await searchPolicySimple(messageText)
        if (response && response.trim()) {
          const fallbackMessage: Message = {
            id: messageIdCounter++,
            text: response,
            isUser: false,
            timestamp: new Date()
          }
          messages.value.push(fallbackMessage)
          hasReceivedData = true
        }
      } catch (fallbackError) {
        console.error('Both streaming and simple request failed:', fallbackError)
      }
    }
    
    // If no data was received, show a helpful message
    if (!hasReceivedData) {
      const helpMessage: Message = {
        id: messageIdCounter++,
        text: "I'm sorry, I couldn't find relevant information about that topic. This might be because:\n\n• No policy documents have been uploaded yet\n• The backend AI model isn't loaded\n• Your query doesn't match the available documents\n\nTry uploading some PDF documents first using the /policy/upload endpoint.",
        isUser: false,
        timestamp: new Date()
      }
      messages.value.push(helpMessage)
    }
    
  } catch (error) {
    console.error('Error getting AI response:', error)
    
    const errorMessage: Message = {
      id: messageIdCounter++,
      text: 'Sorry, I encountered an error while processing your request. Please make sure the backend server is running on http://localhost:8000.',
      isUser: false,
      timestamp: new Date()
    }
    messages.value.push(errorMessage)
  } finally {
    isLoading.value = false
    scrollToBottom()
  }
}

onMounted(() => {
  scrollToBottom()
})
</script>

<style scoped>
.chat-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  max-width: 800px;
  margin: 0 auto;
  height: calc(100vh - 100px);
}

.messages-container {
  flex: 1;
  overflow-y: auto;
  padding: 0.75rem;
  margin-bottom: 0.5rem;
}

.welcome-message {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  min-height: 200px;
}

.welcome-card {
  background: #2d3748;
  border-radius: 12px;
  padding: 1.5rem;
  text-align: center;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  border: 1px solid #4a5568;
  max-width: 400px;
}

.welcome-card h2 {
  color: #e2e8f0;
  margin: 0 0 0.75rem 0;
  font-size: 1.3rem;
}

.welcome-card p {
  color: #a0aec0;
  margin: 0 0 1rem 0;
  font-size: 0.95rem;
}

.example-queries {
  text-align: left;
  background: #1a202c;
  border-radius: 8px;
  padding: 0.75rem;
  margin-top: 0.75rem;
}

.example-queries p {
  margin: 0.3rem 0;
  color: #cbd5e0;
  font-size: 0.85rem;
}

.example-queries p:first-child {
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: #e2e8f0;
}

/* Scrollbar styling */
.messages-container::-webkit-scrollbar {
  width: 6px;
}

.messages-container::-webkit-scrollbar-track {
  background: #2d3748;
  border-radius: 3px;
}

.messages-container::-webkit-scrollbar-thumb {
  background: #4a5568;
  border-radius: 3px;
}

.messages-container::-webkit-scrollbar-thumb:hover {
  background: #718096;
}
</style>