# Gemini CLI for iPadOS Design

## Overview
A multimodal CLI for interacting with Google's Gemini API, optimized for iPadOS terminal environments like a-Shell, iSH, or Pythonista.

## Key Features
- **Multimodal Support**: Send text prompts along with images.
- **Interactive Chat**: Maintain conversation history.
- **File Integration**: Easily attach local images from the iPad filesystem.
- **Environment Compatibility**: Designed to run with standard Python libraries available in mobile terminal environments.

## Technical Stack
- **Language**: Python 3.x
- **API**: Google Generative AI SDK (`google-generativeai`)
- **Dependencies**: `python-dotenv` (for API key management), `Pillow` (for image processing).

## CLI Structure
- `gemini-cli.py`: Main entry point.
- `config.py`: Configuration and API key handling.
- `utils.py`: Helper functions for image loading and text formatting.

## Usage Examples
- `python gemini-cli.py "What is in this image?" --image photo.jpg`
- `python gemini-cli.py --interactive`
