import os
import sys
import argparse
from google import genai
from google.genai import types
from PIL import Image
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def setup_client():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not found in environment variables.")
        print("Please set it in a .env file or export it in your terminal.")
        sys.exit(1)
    return genai.Client(api_key=api_key)

def handle_multimodal_request(client, prompt, image_path, model_name):
    try:
        img = Image.open(image_path)
        response = client.models.generate_content(
            model=model_name,
            contents=[prompt, img]
        )
        return response.text
    except Exception as e:
        return f"Error processing multimodal request: {str(e)}"

def handle_text_request(client, prompt, model_name):
    try:
        response = client.models.generate_content(
            model=model_name,
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"Error processing text request: {str(e)}"

def interactive_chat(client, model_name):
    chat = client.chats.create(model=model_name)
    print(f"--- Gemini Interactive Chat ({model_name}) ---")
    print("Type 'exit' or 'quit' to end the session.")
    
    while True:
        try:
            user_input = input("\nYou: ")
            if user_input.lower() in ['exit', 'quit']:
                break
            
            # Check for image attachment command in interactive mode
            # Simple syntax: "prompt --image path/to/image.jpg"
            if "--image" in user_input:
                parts = user_input.split("--image")
                prompt = parts[0].strip()
                img_path = parts[1].strip()
                if os.path.exists(img_path):
                    img = Image.open(img_path)
                    response = client.models.generate_content(
                        model=model_name,
                        contents=[prompt, img]
                    )
                    print(f"\nGemini: {response.text}")
                else:
                    print(f"Error: Image file '{img_path}' not found.")
            else:
                response = chat.send_message(user_input)
                print(f"\nGemini: {response.text}")
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description="Gemini Multimodal CLI for iPadOS")
    parser.add_argument("prompt", nargs="?", help="The text prompt to send to Gemini")
    parser.add_argument("--image", help="Path to an image file for multimodal input")
    parser.add_argument("--interactive", "-i", action="store_true", help="Start an interactive chat session")
    parser.add_argument("--model", default="gemini-2.0-flash", help="Gemini model to use (default: gemini-2.0-flash)")
    
    args = parser.parse_args()
    
    client = setup_client()
    
    if args.interactive:
        interactive_chat(client, args.model)
    elif args.prompt:
        if args.image:
            result = handle_multimodal_request(client, args.prompt, args.image, args.model)
        else:
            result = handle_text_request(client, args.prompt, args.model)
        print(result)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
