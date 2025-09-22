// API configuration
const API_BASE_URL = 'http://localhost:8000'

/**
 * Stream policy search results from the backend
 * @param query - The search query
 * @param onChunk - Callback function to handle each chunk of data
 */
export async function searchPolicyStream(
  query: string,
  onChunk: (chunk: string) => void
): Promise<void> {
  try {
    console.log('Sending query to backend:', query)
    
    const response = await fetch(
      `${API_BASE_URL}/policy/search?query=${encodeURIComponent(query)}&top_k=3`,
      {
        method: 'GET',
        headers: {
          'Accept': 'text/plain',
          'Cache-Control': 'no-cache',
        },
      }
    )

    console.log('Response status:', response.status)
    console.log('Response headers:', response.headers)

    if (!response.ok) {
      const errorText = await response.text()
      console.error('HTTP error response:', errorText)
      throw new Error(`HTTP error! status: ${response.status}. ${errorText}`)
    }

    if (!response.body) {
      throw new Error('Response body is null')
    }

    const reader = response.body.getReader()
    const decoder = new TextDecoder()
    let buffer = ''

    try {
      while (true) {
        const { done, value } = await reader.read()
        
        if (done) {
          // Process any remaining buffer content
          if (buffer.trim()) {
            onChunk(buffer)
          }
          break
        }

        const chunk = decoder.decode(value, { stream: true })
        console.log('Received chunk:', chunk)
        
        // Add to buffer and process complete chunks
        buffer += chunk
        
        // For streaming text, we can send each chunk immediately
        if (chunk.trim()) {
          console.log('Sending chunk to UI:', chunk)
          onChunk(chunk)
        }
      }
    } finally {
      reader.releaseLock()
    }
  } catch (error) {
    console.error('Error in searchPolicyStream:', error)
    throw error
  }
}

/**
 * Search with a simple non-streaming fallback
 * @param query - The search query
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

    return await response.text()
  } catch (error) {
    console.error('Error in searchPolicySimple:', error)
    throw error
  }
}

/**
 * Check if the backend is healthy
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
 * Upload policy documents (for future use)
 * @param files - Array of files to upload
 */
export async function uploadPolicyFiles(files: File[]): Promise<any> {
  try {
    const formData = new FormData()
    files.forEach(file => {
      formData.append('files', file)
    })

    const response = await fetch(`${API_BASE_URL}/policy/upload`, {
      method: 'POST',
      body: formData,
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