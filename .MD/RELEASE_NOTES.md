# Vortex AI Android - v1.0.0 Release 🎉

We are incredibly excited to announce the initial release of **Vortex AI Android**! 
This release establishes Vortex AI as a centralized, powerful hub for your mobile device, granting you robust control over the world's leading Text, UI, Image, and Voice AI models.

## 🚀 Key Features

### 🧠 Multi-Platform LLM Hub
*   **Massive Provider Support**: Connect fluidly to OpenRouter, Together AI, Gemini, Grok, and ModelsLab.
*   **Character Card System V2**: Perfect for roleplayers. Import JSON character cards, auto-extract portraits, and chat with customized personas.
*   **Vortex Mode**: A specialized internal autonomous handler for high-context handling logic.

### 🖼️ Advanced Image Generation & Editing
*   **Leading Visual Models**: Native generation integrations with FLUX (Together AI, ModelsLab, ComfyUI) and Stable Diffusion options. 
*   **Qwen Image Editing**: Direct prompt-to-image manipulation via Replicate, automatically routing your character avatars through image-to-image enhancements.
*   **Asynchronous Processing**: Fire off heavy generations, minimize the app, and Vortex handles the rest using Background Services. 

### 🗣️ Text To Speech (TTS)
*   **High-Quality Voice Delivery**: Directly interface with ElevenLabs and Together AI TTS architectures.
*   **Custom Voice Generation**: Dictate speaking rates and trigger automated read-aloud options from your chat interface conditionally.

### ⚙️ The "Custom API" Advantage
*   Bring your own backend! Fully supported database endpoints allowing you to map Swagger files or custom JSON architectures onto the Vortex Hub without tweaking any internal frontend code.

### 🔒 Privacy and Security
*   **Zero Leak Architecture**: Completely stripped of all hardcoded credentials. Keys are supplied *by you* natively via Jetpack Compose's Settings UI and dynamically injected using `SettingsDataStore`.
*   **Local Persistence**: All Chats, Generated Images, and Character states are preserved locally using Room Database caching.

## 🛠️ Changes Since Final Beta/Commits
*   *Security Update*: Purged testing script contexts (`test/`, `Other Files/`) from housing internal logic tokens—meeting GitHub’s stringent Secret Scanning policies. 
*   *Refactored Build Stability*: Included advanced `.gitignore` constraints preventing messy `/build` folder uploads ensuring the repository remains lightweight.
*   *Polished Settings Schema*: All custom API overrides and parameter tweaks successfully read globally across the application.

## 📦 Getting Started
1. Download the `app-release.apk` attached to this release.
2. Install the APK on your Android device. *(You may need to bypass Google Play Protect "Install Anyway" if you do not have Play Protect signed configurations set up locally).*
3. Boot the application, tap your **Settings** tab, and enter your respective provider API keys to begin generating!
