# Gemini CLI for iPadOS

A lightweight, multimodal CLI for interacting with Google's Gemini API. Optimized for iPadOS terminal environments like **a-Shell**, **iSH**, or **Pythonista**.

## Features
- **Multimodal Support**: Send text and images together.
- **Interactive Mode**: Chat with Gemini and maintain context.
- **Easy Setup**: Simple configuration via `.env` file.

## Installation

1. **Clone the repository** (or copy the script):
   ```bash
   git clone https://github.com/yourusername/gemini-cli-ipad.git
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

### Single Prompt
```bash
python gemini-cli.py "Explain this code snippet" --model gemini-2.0-flash
```

### Multimodal (Text + Image)
```bash
python gemini-cli.py "What is in this image?" --image photo.jpg
```

### Interactive Chat
```bash
python gemini-cli.py --interactive
```
In interactive mode, you can also attach images using:
`Your prompt --image path/to/image.jpg`

## Compatibility
- **a-Shell**: Works natively with the included Python environment.
- **iSH**: Requires installing Python and dependencies via `apk`.
- **Pythonista**: Can be run by importing the script or using the stash terminal.
