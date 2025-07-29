# Multi-Tool AI Platform 🚀

A sophisticated desktop application providing **offline AI-powered productivity tools** built with Tauri, Python FastAPI, and modern web technologies.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![Rust](https://img.shields.io/badge/rust-1.70+-orange.svg)
![Tauri](https://img.shields.io/badge/tauri-2.x-blue.svg)

## 🌟 Overview

This platform delivers **enterprise-grade AI capabilities** without requiring internet connectivity, ensuring complete privacy and data security. All AI processing happens locally on your machine using Microsoft's Phi-3 Mini model.

### ✨ Key Features

- 🔒 **100% Offline AI Processing**: Complete functionality without internet
- 📄 **Professional PDF Summarization**: Advanced prompt engineering with hallucination detection  
- 🖥️ **Native Desktop Experience**: Built with Tauri for optimal performance
- 🛡️ **Privacy-First Design**: No data collection or external dependencies
- 🌐 **Cross-Platform Support**: Windows, macOS, and Linux
- 🎨 **Modern UI**: Glassmorphism design with smooth animations

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-------------|
| **Frontend** | HTML5/CSS3/JavaScript + Vite |
| **Backend** | Python FastAPI + Service Architecture |
| **AI Model** | Microsoft Phi-3 Mini (2.3GB GGUF) |
| **Desktop** | Tauri 2.x + Rust |
| **Documents** | PyMuPDF for PDF processing |

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+ and npm
- Rust 1.70+ and Cargo (for desktop builds)

### 📦 Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/Saleh-Ghalayini/mutli-tool-prototype.git
   cd mutli-tool-prototype
   ```

2. **Install Python dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. **Install frontend dependencies**
   ```bash
   cd frontend
   npm install
   ```

4. **📥 Download AI Model** (Required - 2.3GB)
   - Download Microsoft Phi-3 Mini GGUF model
   - Create folder: `backend/models/`
   - Place model as: `backend/models/phi3-mini.gguf`
   - **Note**: Model not included in repo due to size

### 🏃‍♂️ Running the Application

#### Option 1: Quick Launch (Windows)
```bash
# Double-click this file in project root
run_app.bat
```

#### Option 2: Manual Development
```bash
# Terminal 1: Start backend
cd backend && python main.py

# Terminal 2: Start frontend  
cd frontend && npm run dev

# Open browser to http://localhost:8000
```

#### Option 3: Desktop App (Development)
```bash
cargo tauri dev
```

### 🏗️ Building for Production

```bash
# Build optimized frontend
cd frontend && npm run build

# Build standalone desktop executable  
cargo tauri build
```

## 📁 Project Structure

```
mutli-tool-prototype/
├── 🐍 backend/                 # Python FastAPI backend
│   ├── main.py                # API routes & application entry
│   ├── services/              # Business logic services  
│   │   ├── ai_service.py      # AI model management
│   │   ├── pdf_service.py     # PDF processing
│   │   └── ...                # Other services
│   ├── requirements.txt       # Python dependencies
│   └── models/               # AI model storage (gitignored)
├── 🌐 frontend/               # Web frontend
│   ├── src/
│   │   ├── index.html        # Main interface
│   │   ├── main.js          # Application logic
│   │   └── styles.css       # Modern styling
│   ├── package.json         # Node dependencies
│   └── dist/               # Built assets (gitignored)
├── 🦀 src-tauri/             # Desktop app wrapper
│   ├── src/lib.rs           # Rust backend integration
│   ├── tauri.conf.json      # App configuration
│   └── Cargo.toml          # Rust dependencies
├── 📖 PROJECT_DOCUMENTATION.md # Complete technical docs
├── 🚀 run_app.bat            # Quick launcher script
└── 📋 README.md             # This file
```

## 📖 Documentation

📚 **[Complete Technical Documentation](PROJECT_DOCUMENTATION.md)** includes:
- 🏗️ Architecture overview and design patterns
- 🤖 AI model integration and prompt engineering
- ⚡ Performance characteristics and benchmarks  
- 🔐 Security features and privacy guarantees
- 🛠️ Development workflow and deployment guide

## 🔒 Privacy & Security

- ✅ **Zero data collection** - No telemetry or analytics
- ✅ **Offline processing** - Documents never leave your machine
- ✅ **Memory safety** - Rust ensures secure operations
- ✅ **Local storage** - Temporary files auto-deleted

## 📊 Download & System Requirements

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| **RAM** | 8GB | 16GB+ |
| **Storage** | 4GB free | 8GB+ free |
| **CPU** | Dual-core | Quad-core+ |
| **OS** | Win 10+, macOS 10.15+, Ubuntu 18.04+ | Latest versions |

**Download Size**: ~2.8GB (includes AI model)

## 🤝 Contributing

1. 🍴 Fork the repository
2. 🌟 Create a feature branch (`git checkout -b feature/amazing-feature`)
3. 💻 Make your changes
4. ✅ Test thoroughly
5. 📝 Commit changes (`git commit -m 'Add amazing feature'`)
6. 🚀 Push to branch (`git push origin feature/amazing-feature`)
7. 🔃 Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Microsoft for the Phi-3 Mini model
- Tauri team for the excellent desktop framework
- FastAPI for the high-performance web framework
- Contributors and the open-source community

---

<div align="center">

**🚀 Built with ❤️ for Privacy-First AI Processing**

[⭐ Star this repo](https://github.com/Saleh-Ghalayini/mutli-tool-prototype) • [🐛 Report Bug](https://github.com/Saleh-Ghalayini/mutli-tool-prototype/issues) • [💡 Request Feature](https://github.com/Saleh-Ghalayini/mutli-tool-prototype/issues)

</div>