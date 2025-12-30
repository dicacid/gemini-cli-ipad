import os
import sys
import argparse
import re
from pathlib import Path
from typing import Optional, List
from google import genai
from google.genai import types
from PIL import Image
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def setup_client() -> genai.Client:
    """Initialize and return Gemini client."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not found in environment variables.", file=sys.stderr)
        print("Please set it in a .env file or export it in your terminal.", file=sys.stderr)
        sys.exit(1)
    return genai.Client(api_key=api_key)

def validate_image(path: str) -> Path:
    """Validate image file exists and is readable."""
    img_path = Path(path)
    if not img_path.exists():
        raise FileNotFoundError(f"Image not found: {path}")
    if img_path.stat().st_size > 20 * 1024 * 1024:  # 20MB limit
        raise ValueError("Image exceeds 20MB size limit")
    return img_path

def generate_content(client: genai.Client, 
                     model: str, 
                     contents: List, 
                     stream: bool = False) -> str:
    """Generate content with proper error handling and streaming support."""
    try:
        response = client.models.generate_content(
            model=model,
            contents=contents,
            config={'stream': stream} if stream else None
        )
        
        if stream:
            full_text = []
            for chunk in response:
                if chunk.text:
                    print(chunk.text, end='', flush=True)
                    full_text.append(chunk.text)
            print() # New line after stream
            return ''.join(full_text)
        
        return response.text or ""
        
    except Exception as e:
        print(f"API Error: {e}", file=sys.stderr)
        sys.exit(1)

def handle_multimodal(client: genai.Client, 
                      prompt: str, 
                      image_path: str, 
                      model: str, 
                      stream: bool = False) -> str:
    """Handle text + image request with resource management."""
    img_path = validate_image(image_path)
    with Image.open(img_path) as img:
        return generate_content(client, model, [prompt, img], stream)

def interactive_chat(client: genai.Client, model_name: str):
    """Run interactive chat with streaming and improved parsing."""
    chat = client.chats.create(model=model_name)
    print(f"\n🚀 Gemini Interactive Chat ({model_name})")
    print("Commands: 'exit', 'quit', or use '--image path' in prompt")
    
    while True:
        try:
            user_input = input("\nYou: ").strip()
            if not user_input or user_input.lower() in ('exit', 'quit'):
                break
            
            # Parse prompt --image path using regex
            if '--image' in user_input:
                match = re.match(r"(.+?)\s*--image\s+(.+)", user_input)
                if match:
                    prompt, img_path = match.groups()
                    img_path = img_path.strip()
                    if os.path.exists(img_path):
                        print("\nGemini: ", end='')
                        handle_multimodal(
                            client, prompt.strip(), img_path, 
                            model_name, stream=True
                        )
                    else:
                        print(f"❌ Image not found: {img_path}")
                    continue
            
            # Text-only chat with streaming
            response = chat.send_message(user_input, stream=True)
            print("\nGemini: ", end='')
            for chunk in response:
                if chunk.text:
                    print(chunk.text, end='', flush=True)
            print()
                
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)

def main():
    parser = argparse.ArgumentParser(
        description="Gemini Multimodal CLI for iPadOS",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Examples:\n"
               "  %(prog)s 'What is in this image?' --image photo.jpg\n"
               "  %(prog)s 'Explain quantum computing'\n"
               "  %(prog)s -i --model gemini-1.5-pro"
    )
    parser.add_argument("prompt", nargs="?", help="Text prompt")
    parser.add_argument("--image", type=str, help="Path to image file")
    parser.add_argument("-i", "--interactive", action="store_true", help="Interactive mode")
    parser.add_argument("--model", default="gemini-1.5-flash", 
                        choices=["gemini-1.5-flash", "gemini-1.5-pro"],
                        help="Model to use (default: gemini-1.5-flash)")
    parser.add_argument("--stream", action="store_true", help="Stream responses")
    
    args = parser.parse_args()
    
    client = setup_client()
    
    if args.interactive:
        interactive_chat(client, args.model)
    elif args.prompt:
        if args.image:
            result = handle_multimodal(client, args.prompt, args.image, args.model, args.stream)
            if not args.stream:
                print(result)
        else:
            result = generate_content(client, args.model, [args.prompt], args.stream)
            if not args.stream:
                print(result)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
