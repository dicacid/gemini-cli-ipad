# Gemini CLI for iPadOS (Improved)

A lightweight, multimodal CLI for interacting with Google's Gemini API. Optimized for iPadOS terminal environments like **a-Shell**, **iSH**, or **Pythonista**.

## Features
- **Multimodal Support**: Send text and images together.
- **Streaming Responses**: Real-time output for long generations.
- **Interactive Mode**: Chat with Gemini and maintain context.
- **Robust Parsing**: Improved regex-based parsing for image attachments in chat.
- **Resource Management**: Proper handling of image files to prevent memory leaks.

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/dicacid/gemini-cli-ipad.git
   cd gemini-cli-ipad
   ```

2. **Install dependencies**:
   ```bash
   pip install google-genai python-dotenv pillow
   ```

3. **Configure API Key**:
   Create a `.env` file in the project directory:
   ```env
   GEMINI_API_KEY=your_google_ai_studio_api_key
   ```

## Usage

### Single Prompt (with Streaming)
```bash
python gemini-cli.py "Explain quantum computing" --stream
```

### Multimodal (Text + Image)
```bash
python gemini-cli.py "What is in this image?" --image photo.jpg
```

### Interactive Chat
```bash
python gemini-cli.py --interactive
```
In interactive mode, you can attach images using:
`Your prompt --image path/to/image.jpg`

## Compatibility
- **a-Shell**: Works natively with the included Python environment.
- **iSH**: Requires installing Python and dependencies via `apk`.
- **Pythonista**: Can be run by importing the script or using the stash terminal.
