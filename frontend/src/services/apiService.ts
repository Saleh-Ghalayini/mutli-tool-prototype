// ==============================================================================
// FRONTEND API SERVICE (HTTP & STREAMING CLIENT)
// ==============================================================================
// This service module is the communication bridge between the Vue.js user
// interface and the FastAPI Python backend server.
//
// Key Concepts:
// 1. Fetch API vs Axios:
//    While Axios is common for standard JSON requests, modern web browsers provide
//    the native `fetch()` API, which has first-class support for `ReadableStream`.
//    This allows reading incoming bytes continuously before the HTTP request closes.
// 2. Token Streaming:
//    Instead of waiting 5–10 seconds for the entire LLM response, the backend sends
//    tokens as they are generated. This file reads those chunks and immediately
//    hands them over to the UI for instant rendering.

// Base URL where the Python FastAPI backend server is listening
const API_BASE_URL = 'http://localhost:8000'

/**
 * Stream policy search results from the backend in real-time.
 * 
 * How Streaming Works:
 * 1. Sends an HTTP GET request to /policy/search with the query encoded in the URL.
 * 2. Accesses `response.body`, which is a web-standard ReadableStream of Uint8Array bytes.
 * 3. Uses a `TextDecoder` to convert incoming byte arrays into UTF-8 characters.
 * 4. Runs an asynchronous `while(true)` loop, calling `reader.read()` until `done === true`.
 * 5. Calls the `onChunk(chunk)` callback every time new characters arrive,
 *    allowing the Vue component to append tokens immediately.
 * 
 * @param query - The user's question (e.g., "What is the vacation policy?")
 * @param onChunk - Callback function executed whenever a new text chunk is received
 */
export async function searchPolicyStream(
  query: string,
  onChunk: (chunk: string) => void
): Promise<void> {
  try {
    console.log('Sending query to backend:', query)
    
    // encodeURIComponent converts spaces and special characters into URL-safe format
    // (e.g. "leave policy?" becomes "leave%20policy%3F")
    const response = await fetch(
      `${API_BASE_URL}/policy/search?query=${encodeURIComponent(query)}&top_k=3`,
      {
        method: 'GET',
        headers: {
          'Accept': 'text/plain',       // We expect plain text tokens from the stream
          'Cache-Control': 'no-cache',  // Prevent browsers/proxies from caching streaming responses
        },
      }
    )

    console.log('Response status:', response.status)
    console.log('Response headers:', response.headers)

    // Check if the HTTP status code is outside the 200-299 success range
    if (!response.ok) {
      const errorText = await response.text()
      console.error('HTTP error response:', errorText)
      throw new Error(`HTTP error! status: ${response.status}. ${errorText}`)
    }

    // Ensure the response has a readable body stream
    if (!response.body) {
      throw new Error('Response body is null')
    }

    // Acquire a reader lock on the byte stream
    const reader = response.body.getReader()
    // TextDecoder decodes streams of binary Uint8Array chunks into readable text strings
    const decoder = new TextDecoder()
    let buffer = ''

    try {
      while (true) {
        // reader.read() returns a Promise that resolves to:
        // - done (boolean): true when the server finishes sending the response
        // - value (Uint8Array): the binary chunk of bytes received
        const { done, value } = await reader.read()
        
        if (done) {
          // Stream is finished
          // NOTE FOR INTERVIEWS: In the initial prototype, buffer was also flushed here.
          // Since chunks are dispatched as they arrive below, this block simply signals completion.
          if (buffer.trim()) {
            onChunk(buffer)
          }
          break
        }

        // Decode the binary bytes into a string ({ stream: true } handles multi-byte characters split across chunks)
        const chunk = decoder.decode(value, { stream: true })
        console.log('Received chunk:', chunk)
        
        // Add to buffer
        buffer += chunk
        
        // If the chunk contains non-whitespace characters, notify the UI callback immediately
        if (chunk.trim()) {
          console.log('Sending chunk to UI:', chunk)
          onChunk(chunk)
        }
      }
    } finally {
      // Always release the reader lock when reading completes or if an error is thrown
      reader.releaseLock()
    }
  } catch (error) {
    console.error('Error in searchPolicyStream:', error)
    throw error
  }
}

/**
 * Search with a simple non-streaming fallback.
 * 
 * Used when streaming fails (e.g. network proxy disables chunked transfer encoding).
 * Waits for the entire HTTP response to finish before returning the complete text string.
 * 
 * @param query - The user's question
 * @returns Promise<string> - The complete answer string
 */
export async function searchPolicySimple(query: string): Promise<string> {
  try {
    const response = await fetch(
      `${API_BASE_URL}/policy/search?query=${encodeURIComponent(query)}&top_k=3`,
      {
        method: 'GET',
        headers: {
          'Accept': 'text/plain',
        },
      }
    )

    if (!response.ok) {
      const errorText = await response.text()
      throw new Error(`HTTP error! status: ${response.status}. ${errorText}`)
    }

    // response.text() waits for the entire body stream to finish and returns it as a string
    return await response.text()
  } catch (error) {
    console.error('Error in searchPolicySimple:', error)
    throw error
  }
}

/**
 * Check if the backend server is reachable and healthy.
 * 
 * @returns Promise<boolean> - true if server returns HTTP 200, false otherwise
 */
export async function checkHealth(): Promise<boolean> {
  try {
    const response = await fetch(`${API_BASE_URL}/health`)
    return response.ok
  } catch (error) {
    console.error('Health check failed:', error)
    return false
  }
}

/**
 * Upload policy documents (PDFs) to the backend.
 * 
 * Uses multipart/form-data encoding to upload one or more binary files.
 * 
 * @param files - Array of File objects selected by the user
 * @returns Promise<any> - Parsed JSON response from the backend
 */
export async function uploadPolicyFiles(files: File[]): Promise<any> {
  try {
    // FormData is a standard browser object for sending multipart/form-data payloads
    const formData = new FormData()
    files.forEach(file => {
      // 'files' must match the parameter name expected by FastAPI in upload_policy()
      formData.append('files', file)
    })

    const response = await fetch(`${API_BASE_URL}/policy/upload`, {
      method: 'POST',
      body: formData, // Browser automatically sets Content-Type to multipart/form-data with boundary
    })

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    return await response.json()
  } catch (error) {
    console.error('Error uploading files:', error)
    throw error
  }
}