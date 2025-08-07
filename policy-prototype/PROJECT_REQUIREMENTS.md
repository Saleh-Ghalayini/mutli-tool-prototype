# Project Requirements: Multi-Tool AI Desktop Platform (Final Proposal)

## 1. Project Vision & Objective

**Vision:** To create a commercial, offline-first desktop application that empowers users to run a variety of local, privacy-preserving AI models for different tasks.

**Objective:** Develop a secure, user-friendly platform for Windows that manages the download, configuration, and execution of pre-trained AI models. The platform will be monetized through a one-time license key, giving users access to a suite of powerful AI tools that run entirely on their own hardware.

---

## 2. Core Architectural Principles

- **Offline-First:** The primary functionality of running AI models and tasks must be available without an internet connection.
- **User Consent for Connectivity:** The application must explicitly ask for the user's permission before connecting to the internet.
- **Local Processing:** All AI inference and user data processing must happen on the user's local machine.
- **Resource-Aware:** The application must inspect the host machine's hardware to provide intelligent feedback.

---

## 3. Functional Requirements

### 3.1. Installation & Onboarding

- [ ] **MSI Installer:** The application must be packaged and delivered as a standard MSI installer for Windows.
- [ ] **Correct File Paths:** The installer will place the application executables in `C:\Program Files`. All user-generated data, downloaded models, settings, and logs **must** be stored in the user's `AppData` directory to ensure proper permissions and system compliance.
- [ ] **Web Portal for Purchase & Tutorial:** Users will purchase a license key and view tutorials/documentation through an external web portal.
- [ ] **Mandatory Activation:** Upon first launch, the application must prompt for a license key. Core features are inaccessible until activation is complete. No demo mode is required.
- [ ] **Online Validation:** The license key must be validated against a central server, requiring a one-time, user-approved internet connection.
- [ ] **Machine ID Binding:** The application must generate a unique, anonymous identifier for the user's machine to associate with the license key.
- [ ] **Silent 3-Machine Limit:** A single license key can be activated on a maximum of three (3) machines. An attempt on a fourth machine will fail, requiring the user to purchase a new license.

### 3.2. Model & Task Management

- [ ] **Model Marketplace:** The UI shall present a list of available models, displaying their name, version, intended task, resource requirements (RAM, CPU, Disk), and release date.
- [ ] **Hardware Compatibility Check:** Before download, the app must warn the user if their machine does not meet a model's requirements.
- [ ] **Secure, Resumable Downloads:** Models must be downloaded from a secure server. The download process should be resumable if interrupted.
- [ ] **Model Library:** A dedicated screen must allow users to view installed models, their disk space usage, and delete them.
- [ ] **Model File Security:** Downloaded model files must be encrypted on disk to deter unauthorized copying (can be discussed).
- [ ] **Dynamic Task UI:** The application's UI must adapt to the selected model/task, presenting the appropriate layout and controls (e.g., a chat view for Q&A, a text editor for summarization).

### 3.3. Project & Data Management

- [ ] **Project/Workspace System:** The app must allow users to create "Projects" that save a configuration of a selected model, its parameter settings, and associated local data (e.g., a knowledge base index) (should be discussed).
- [ ] **Project Switching:** Users must be able to easily switch between saved projects/models (should be discussed).
- [ ] **Persistent Settings:** User-configured model parameters for a project must be saved automatically and persist between sessions (should be discussed).
- [ ] **Secure Local Data:** For tasks requiring a knowledge base, the generated index files must be stored locally. The user must have an option to delete this data securely (should be discussed).

### 3.4. Application Stability & Maintenance

- [ ] **Resource Monitoring:** The application must monitor its own resource usage during AI processing.
- [ ] **Process Termination:** The app must include a mechanism to gracefully stop/kill a runaway AI process that is consuming excessive resources or has become unresponsive.
- [ ] **User-Approved Updates:** The application may check for updates when online. But before that, the user must approve the scanning, downloading and installation.
- [ ] **Error Logging:** In case of an error, the app must save a detailed, non-personal error log. The UI should provide an easy way for the user to export this log for customer support through a specified method to be decided later on.

---

## 4. B2B (Business-to-Business) Requirements

- [ ] **Custom-Trained Models:** The system must support the concept of models trained on a specific client's private data (e.g., company's policy or a manual).
- [ ] **Secure B2B Model Delivery:** A secure mechanism for delivering custom models to B2B clients must be designed (e.g., via private authenticated download or a special license key).

---

## 5. Key Discussion Points for Client / Future Enhancements

- **Subscription Model:** Evaluate a yearly subscription vs. a one-time payment.
- **White-Labeling:** For B2B clients, offer the ability to brand the application.
- **Knowledge Base Updates:** Define a clear UI workflow for updating the documents in an existing RAG project, unless a pretrained model is wanted for such things as "company policy" so a new model should be trained based on the new data and downloaded on the users' machine.
- **License Revocation:** Formulate a policy and technical mechanism for revoking fraudulent or refunded license keys.
- **Platform Expansion:** Plan for future support for macOS and Linux.
- **User-Managed Deactivation:** Consider a future web portal for users to manage their own machine activations.
