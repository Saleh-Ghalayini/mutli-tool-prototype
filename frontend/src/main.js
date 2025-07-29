// Multi-Tool AI Platform - Updated Frontend for Python Backend
// Now using HTTP API instead of Tauri invoke commands

// Python backend configuration
const BACKEND_URL = 'http://127.0.0.1:8000';

// Application state
let currentTool = null;

// DOM elements
const toolsGrid = document.getElementById('tools-grid');
const toolInterface = document.getElementById('tool-interface');
const toolTitle = document.getElementById('tool-title');
const toolContent = document.getElementById('tool-content');
const backBtn = document.getElementById('back-btn');

// API Helper functions
async function apiCall(endpoint, method = 'GET', data = null) {
    try {
        const config = {
            method: method,
            headers: {
                'Content-Type': 'application/json',
            }
        };
        
        if (data) {
            config.body = JSON.stringify(data);
        }
        
        const response = await fetch(`${BACKEND_URL}${endpoint}`, config);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error(`API call failed for ${endpoint}:`, error);
        throw error;
    }
}

async function uploadFile(file) {
    try {
        const formData = new FormData();
        formData.append('file', file);
        
        const response = await fetch(`${BACKEND_URL}/upload_file`, {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            throw new Error(`Upload failed! status: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('File upload failed:', error);
        throw error;
    }
}

// Test backend connection
async function testBackendConnection() {
    try {
        console.log('Testing backend connection...');
        console.log('Tauri API available:', !!window.__TAURI__);
        console.log('Tauri invoke available:', !!window.__TAURI__?.invoke);
        
        // First, try to start the Python backend using Tauri command
        if (window.__TAURI__ && window.__TAURI__.invoke) {
            console.log('Starting Python backend via Tauri...');
            try {
                const result = await window.__TAURI__.invoke('start_python_backend');
                console.log('Backend start result:', result);
                
                // Wait a moment for the backend to fully start
                console.log('Waiting for backend to start...');
                await new Promise(resolve => setTimeout(resolve, 3000));
                console.log('Done waiting, testing connection...');
            } catch (error) {
                console.error('Failed to start backend via Tauri:', error);
                
                // Show Tauri error in UI
                const statusDiv = document.createElement('div');
                statusDiv.className = 'connection-status error';
                statusDiv.innerHTML = `🔴 Tauri Backend Start Failed: ${error.message}`;
                document.body.appendChild(statusDiv);
                setTimeout(() => statusDiv.remove(), 5000);
            }
        } else {
            console.warn('Tauri API not available - running in browser mode');
            
            // Show warning in UI
            const statusDiv = document.createElement('div');
            statusDiv.className = 'connection-status warning';
            statusDiv.innerHTML = '⚠️ Tauri API not available - start Python server manually';
            document.body.appendChild(statusDiv);
            setTimeout(() => statusDiv.remove(), 5000);
        }
        
        const response = await apiCall('/health');
        console.log('✅ Backend connection successful:', response);
        
        // Remove any existing error status messages
        document.querySelectorAll('.connection-status.error, .connection-status.warning').forEach(el => el.remove());
        
        // Show connection status in UI
        const statusDiv = document.createElement('div');
        statusDiv.className = 'connection-status success';
        statusDiv.innerHTML = '🟢 Connected to AI Backend';
        document.body.appendChild(statusDiv);
        
        setTimeout(() => statusDiv.remove(), 3000);
        
        return true;
    } catch (error) {
        console.error('❌ Backend connection failed:', error);
        
        // Show error status in UI
        const statusDiv = document.createElement('div');
        statusDiv.className = 'connection-status error';
        statusDiv.innerHTML = '🔴 Backend Not Available - Please start Python server';
        document.body.appendChild(statusDiv);
        
        return false;
    }
}

// Initialize the application
document.addEventListener('DOMContentLoaded', async () => {
    console.log('Multi-Tool AI Platform loaded');
    console.log('Using Python backend at:', BACKEND_URL);
    
    // Add click listeners to tool cards
    document.querySelectorAll('.tool-card:not([disabled])').forEach(card => {
        card.addEventListener('click', () => {
            const toolId = card.dataset.tool;
            selectTool(toolId);
        });
    });
    
    // Back button listener
    backBtn.addEventListener('click', () => {
        showToolsGrid();
    });
    
    // Test backend connection
    await testBackendConnection();
});

// Tool selection handler
function selectTool(toolId) {
    currentTool = toolId;
    
    // Update UI
    document.querySelectorAll('.tool-card').forEach(card => {
        card.classList.remove('selected');
    });
    document.querySelector(`[data-tool="${toolId}"]`).classList.add('selected');
    
    // Show tool interface
    showToolInterface(toolId);
}

// Show tools grid
function showToolsGrid() {
    toolsGrid.style.display = 'grid';
    toolInterface.style.display = 'none';
    currentTool = null;
    
    // Clear selection
    document.querySelectorAll('.tool-card').forEach(card => {
        card.classList.remove('selected');
    });
}

// Show tool interface
function showToolInterface(toolId) {
    toolsGrid.style.display = 'none';
    toolInterface.style.display = 'block';
    
    // Set tool title and load interface
    switch(toolId) {
        case 'pdf-summarizer':
            toolTitle.textContent = 'PDF Summarizer';
            loadPDFSummarizerInterface();
            break;
        case 'keyword-detector':
            toolTitle.textContent = 'Keyword Detector';
            loadKeywordDetectorInterface();
            break;
        case 'text-analyzer':
            toolTitle.textContent = 'Text Analyzer';
            loadTextAnalyzerInterface();
            break;
        case 'ai-chat':
            toolTitle.textContent = 'AI Chat Assistant';
            loadAIChatInterface();
            break;
        default:
            toolTitle.textContent = 'Tool';
            toolContent.innerHTML = '<p>Tool not implemented yet.</p>';
    }
}

// Load PDF Summarizer Interface - Updated for Python Backend
function loadPDFSummarizerInterface() {
    toolContent.innerHTML = `
        <div class="pdf-summarizer-container">
            <!-- Centered Upload Area -->
            <div class="upload-section-centered">
                <div class="upload-area-enhanced" onclick="document.getElementById('pdf-file').click()">
                    <div class="upload-icon-large">📄</div>
                    <h3 class="upload-title">Click to select PDF file</h3>
                    <p class="upload-hint">Maximum size: 50MB</p>
                    <div class="upload-border-decoration"></div>
                </div>
                <input type="file" id="pdf-file" accept=".pdf" style="display: none;">
            </div>
            
            <!-- Settings Row -->
            <div class="settings-row">
                <div class="setting-group-inline">
                    <label for="summary-length">Summary Length:</label>
                    <select id="summary-length">
                        <option value="short">Short (1-2 paragraphs)</option>
                        <option value="medium" selected>Medium (3-4 paragraphs)</option>
                        <option value="long">Long (5+ paragraphs)</option>
                    </select>
                </div>
                
                <div class="setting-group-inline">
                    <label for="summary-strategy">Strategy:</label>
                    <select id="summary-strategy">
                        <option value="balanced_extraction" selected>Balanced</option>
                        <option value="key_points">Key Points</option>
                        <option value="detailed">Detailed</option>
                    </select>
                </div>
            </div>
            
            <!-- Action Button -->
            <div class="action-section">
                <button id="summarize-btn" class="action-btn-primary" disabled>
                    <span class="btn-text">📝 Analyze PDF with AI</span>
                </button>
            </div>
            
            <div id="summary-result" class="result-section" style="display: none;">
                <div class="result-header">
                    <h3>📋 Summary Result</h3>
                    <div class="result-actions">
                        <button id="copy-summary" class="secondary-btn">📋 Copy to Clipboard</button>
                        <button id="save-summary" class="secondary-btn">💾 Save as Text</button>
                    </div>
                </div>
                <div class="result-content">
                    <div id="summary-text" class="summary-output"></div>
                    <div id="summary-stats" class="summary-stats"></div>
                </div>
            </div>
        </div>
    `;
    
    // Set up file input listener
    const fileInput = document.getElementById('pdf-file');
    const summarizeBtn = document.getElementById('summarize-btn');
    const uploadArea = document.querySelector('.upload-area-enhanced');
    
    fileInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
            uploadArea.innerHTML = `
                <div class="upload-icon-large" style="color: #28a745;">✅</div>
                <h3 class="upload-title">File selected: ${file.name}</h3>
                <p class="upload-hint">Size: ${(file.size / 1024 / 1024).toFixed(2)} MB</p>
                <div class="upload-border-decoration"></div>
            `;
            uploadArea.style.borderColor = '#28a745';
            uploadArea.style.background = 'linear-gradient(145deg, #f8fff8 0%, #ffffff 100%)';
            summarizeBtn.disabled = false;
            summarizeBtn.classList.add('success-pulse');
            
            // Remove pulse animation after 2 seconds
            setTimeout(() => {
                summarizeBtn.classList.remove('success-pulse');
            }, 2000);
        }
    });
    
    // Set up summarize button listener - Updated for Python Backend
    summarizeBtn.addEventListener('click', async () => {
        const btnText = summarizeBtn.querySelector('.btn-text');
        const originalText = btnText.textContent;
        
        btnText.innerHTML = '<div class="loading-spinner"></div>Processing PDF...';
        summarizeBtn.disabled = true;
        
        try {
            const file = fileInput.files[0];
            const fileName = file.name;
            const summaryLength = document.getElementById('summary-length').value;
            const summaryStrategy = document.getElementById('summary-strategy').value;
            
            console.log('Processing PDF file:', fileName);
            console.log('Settings:', { summaryLength, summaryStrategy });
            
            // Step 1: Upload file to Python backend
            btnText.innerHTML = '<div class="loading-spinner"></div>Uploading file...';
            console.log('Uploading file to Python backend:', fileName, file.size, 'bytes');
            
            const uploadResult = await uploadFile(file);
            console.log('File uploaded successfully:', uploadResult);
            
            // Step 2: Summarize the PDF using Python backend
            btnText.innerHTML = '<div class="loading-spinner"></div>Analyzing with AI...';
            console.log('Calling Python backend to summarize PDF...');
            
            const result = await apiCall('/summarize_pdf', 'POST', {
                file_path: uploadResult.file_path
            });
            
            console.log('Python backend response:', result);
            showSummaryResult(result);
            
        } catch (error) {
            console.error('Error:', error);
            showSummaryResult({ 
                success: false,
                error: 'Failed to process PDF: ' + error.toString(),
                summary: '' 
            });
        } finally {
            // Restore button state
            btnText.textContent = originalText;
            summarizeBtn.disabled = false;
        }
    });
    
    // Add copy and save functionality
    setupResultActions();
}

// Load AI Chat Interface - New Feature using Python Backend
function loadAIChatInterface() {
    toolContent.innerHTML = `
        <div class="tool-panel">
            <div class="chat-container">
                <div id="chat-messages" class="chat-messages">
                    <div class="chat-message assistant">
                        <div class="message-content">
                            <strong>🤖 AI Assistant:</strong> Hello! I'm powered by your local Phi-3 model. Ask me anything!
                        </div>
                    </div>
                </div>
                
                <div class="chat-input-section">
                    <div class="input-group">
                        <textarea id="chat-input" placeholder="Type your message here..." rows="3"></textarea>
                        <button id="send-btn" class="action-btn">
                            <span class="btn-text">🚀 Send</span>
                        </button>
                    </div>
                    
                    <div class="chat-settings">
                        <label>
                            Max Response Length:
                            <select id="max-tokens">
                                <option value="128">Short (128 tokens)</option>
                                <option value="256" selected>Medium (256 tokens)</option>
                                <option value="512">Long (512 tokens)</option>
                            </select>
                        </label>
                        <label>
                            Creativity:
                            <select id="temperature">
                                <option value="0.3">Focused</option>
                                <option value="0.7" selected>Balanced</option>
                                <option value="1.0">Creative</option>
                            </select>
                        </label>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    const chatInput = document.getElementById('chat-input');
    const sendBtn = document.getElementById('send-btn');
    const chatMessages = document.getElementById('chat-messages');
    
    // Send message function
    async function sendMessage() {
        const message = chatInput.value.trim();
        if (!message) return;
        
        // Add user message to chat
        addMessageToChat('user', message);
        chatInput.value = '';
        sendBtn.disabled = true;
        
        const btnText = sendBtn.querySelector('.btn-text');
        const originalText = btnText.textContent;
        btnText.innerHTML = '<div class="loading-spinner"></div>Thinking...';
        
        try {
            const maxTokens = parseInt(document.getElementById('max-tokens').value);
            const temperature = parseFloat(document.getElementById('temperature').value);
            
            console.log('Sending message to AI:', { message, maxTokens, temperature });
            
            const result = await apiCall('/generate', 'POST', {
                prompt: message,
                max_tokens: maxTokens,
                temperature: temperature
            });
            
            if (result.success) {
                addMessageToChat('assistant', result.response);
            } else {
                addMessageToChat('assistant', `Sorry, I encountered an error: ${result.error}`);
            }
            
        } catch (error) {
            console.error('Chat error:', error);
            addMessageToChat('assistant', 'Sorry, I\'m having trouble connecting to the AI backend. Please make sure the Python server is running.');
        } finally {
            btnText.textContent = originalText;
            sendBtn.disabled = false;
            chatInput.focus();
        }
    }
    
    // Add message to chat display
    function addMessageToChat(role, content) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `chat-message ${role}`;
        
        const icon = role === 'user' ? '👤' : '🤖';
        const sender = role === 'user' ? 'You' : 'AI Assistant';
        
        messageDiv.innerHTML = `
            <div class="message-content">
                <strong>${icon} ${sender}:</strong> ${content}
            </div>
        `;
        
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    // Event listeners
    sendBtn.addEventListener('click', sendMessage);
    chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
}

// Show summary result - Updated for Python Backend response format
function showSummaryResult(result) {
    const resultSection = document.getElementById('summary-result');
    const summaryText = document.getElementById('summary-text');
    const summaryStats = document.getElementById('summary-stats');
    
    if (result.success && result.summary) {
        // Clean and format the summary text
        let cleanSummary = result.summary.trim();
        
        // Remove any duplicate paragraphs or repeated content
        const paragraphs = cleanSummary.split('\n\n').filter(p => p.trim().length > 0);
        const uniqueParagraphs = [];
        const seenContent = new Set();
        
        paragraphs.forEach(paragraph => {
            const cleanPara = paragraph.trim().toLowerCase();
            if (!seenContent.has(cleanPara) && cleanPara.length > 20) {
                seenContent.add(cleanPara);
                uniqueParagraphs.push(paragraph.trim());
            }
        });
        
        summaryText.textContent = uniqueParagraphs.join('\n\n');
        
        // Build stats display
        let statsHTML = '<div class="stats-grid">';
        if (result.original_length) {
            statsHTML += `<div class="stat-item"><strong>Original:</strong> ${result.original_length.toLocaleString()} chars</div>`;
        }
        if (result.summary_length) {
            statsHTML += `<div class="stat-item"><strong>Summary:</strong> ${result.summary_length.toLocaleString()} chars</div>`;
        }
        if (result.compression_ratio) {
            statsHTML += `<div class="stat-item"><strong>Compression:</strong> ${(result.compression_ratio * 100).toFixed(1)}%</div>`;
        }
        if (result.strategy_used) {
            statsHTML += `<div class="stat-item"><strong>Strategy:</strong> ${result.strategy_used}</div>`;
        }
        statsHTML += '</div>';
        
        summaryStats.innerHTML = statsHTML;
        resultSection.style.display = 'block';
        
        // Scroll to result
        resultSection.scrollIntoView({ behavior: 'smooth' });
    } else {
        // Show error
        summaryText.innerHTML = `<div class="error-message">❌ ${result.error || 'Unknown error occurred'}</div>`;
        summaryStats.innerHTML = '';
        resultSection.style.display = 'block';
    }
}

// Set up result actions (copy, save)
function setupResultActions() {
    // This will be called after the interface is loaded
    setTimeout(() => {
        const copyBtn = document.getElementById('copy-summary');
        const saveBtn = document.getElementById('save-summary');
        
        if (copyBtn) {
            copyBtn.addEventListener('click', async () => {
                const summaryText = document.getElementById('summary-text').textContent;
                try {
                    await navigator.clipboard.writeText(summaryText);
                    copyBtn.textContent = '✅ Copied!';
                    setTimeout(() => {
                        copyBtn.textContent = '📋 Copy to Clipboard';
                    }, 2000);
                } catch (err) {
                    console.error('Failed to copy:', err);
                    copyBtn.textContent = '❌ Copy Failed';
                    setTimeout(() => {
                        copyBtn.textContent = '📋 Copy to Clipboard';
                    }, 2000);
                }
            });
        }
        
        if (saveBtn) {
            saveBtn.addEventListener('click', () => {
                const summaryText = document.getElementById('summary-text').textContent;
                const blob = new Blob([summaryText], { type: 'text/plain' });
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = 'summary.txt';
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                URL.revokeObjectURL(url);
                
                saveBtn.textContent = '✅ Saved!';
                setTimeout(() => {
                    saveBtn.textContent = '💾 Save as Text';
                }, 2000);
            });
        }
    }, 100);
}

// Placeholder functions for other tools
function loadKeywordDetectorInterface() {
    toolContent.innerHTML = `
        <div class="tool-panel">
            <div class="coming-soon">
                <h2>🔍 Keyword Detector</h2>
                <p>This tool will help you detect and analyze keywords in your documents.</p>
                <p><strong>Coming Soon!</strong> Currently building this feature...</p>
            </div>
        </div>
    `;
}

function loadTextAnalyzerInterface() {
    toolContent.innerHTML = `
        <div class="tool-panel">
            <div class="coming-soon">
                <h2>📊 Text Analyzer</h2>
                <p>This tool will provide detailed text analysis including sentiment, readability, and statistics.</p>
                <p><strong>Coming Soon!</strong> Currently building this feature...</p>
            </div>
        </div>
    `;
}

// Add some CSS for the new features
const additionalStyles = `
<style>
.connection-status {
    position: fixed;
    top: 20px;
    right: 20px;
    padding: 10px 20px;
    border-radius: 5px;
    font-weight: bold;
    z-index: 1000;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.connection-status.success {
    background: #4CAF50;
    color: white;
}

.connection-status.error {
    background: #f44336;
    color: white;
}

.chat-container {
    display: flex;
    flex-direction: column;
    height: 600px;
    border: 1px solid #ddd;
    border-radius: 8px;
    overflow: hidden;
}

.chat-messages {
    flex: 1;
    padding: 20px;
    overflow-y: auto;
    background: #f9f9f9;
}

.chat-message {
    margin-bottom: 15px;
    padding: 10px;
    border-radius: 8px;
}

.chat-message.user {
    background: #e3f2fd;
    margin-left: 50px;
}

.chat-message.assistant {
    background: #f1f8e9;
    margin-right: 50px;
}

.chat-input-section {
    border-top: 1px solid #ddd;
    padding: 20px;
    background: white;
}

.input-group {
    display: flex;
    gap: 10px;
    margin-bottom: 15px;
}

.input-group textarea {
    flex: 1;
    resize: vertical;
    min-height: 60px;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 4px;
}

.chat-settings {
    display: flex;
    gap: 20px;
    font-size: 14px;
}

.chat-settings label {
    display: flex;
    align-items: center;
    gap: 5px;
}

.coming-soon {
    text-align: center;
    padding: 60px 20px;
    color: #666;
}

.stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 10px;
    margin-top: 15px;
}

.stat-item {
    padding: 8px;
    background: #f5f5f5;
    border-radius: 4px;
    text-align: center;
    font-size: 14px;
}
</style>
`;

// Add the additional styles to the document
document.head.insertAdjacentHTML('beforeend', additionalStyles);
