#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "google-genai>=1.0.0",
#     "pillow>=10.0.0",
# ]
# ///
"""
Interactive chat mode for Nano Banana 2 image generation.
Enables multi-turn refinement of images with Flash speed.

Usage:
    uv run chat_image.py

Commands:
    /save <filename>     - Save the last generated image
    /config              - Show current configuration
    /aspect <ratio>      - Set aspect ratio (1:1, 16:9, 1:4, 8:1, etc.)
    /resolution <size>   - Set resolution (0.5K, 1K, 2K, 4K)
    /thinking <level>    - Set thinking level (high, minimal)
    /search              - Toggle Google Web Search grounding
    /imgsearch           - Toggle Google Image Search grounding
    /clear               - Clear conversation history
    /help                - Show this help
    exit, quit           - Exit the chat

Example session:
    > Create a logo for "Acme Corp"
    [Image generated]
    > Make the text bolder and add a blue gradient
    [Refined image]
    > /save acme_logo.png
    Saved: /path/to/acme_logo.png
"""

import os
import sys
from pathlib import Path
from datetime import datetime


SUPPORTED_ASPECT_RATIOS = [
    "1:1", "1:4", "1:8", "2:3", "3:2", "3:4", "4:1", "4:3", "4:5", "5:4", "8:1", "9:16", "16:9", "21:9"
]


def get_api_key():
    """Get API key from environment."""
    return os.environ.get("GEMINI_API_KEY")


def main():
    api_key = get_api_key()
    if not api_key:
        print("Error: GEMINI_API_KEY environment variable not set.", file=sys.stderr)
        sys.exit(1)

    from google import genai
    from google.genai import types
    from PIL import Image as PILImage
    from io import BytesIO
    import base64

    client = genai.Client(api_key=api_key)

    config = {
        "aspect_ratio": "1:1",
        "resolution": "1K",
        "thinking": "high",
        "search": False,
        "image_search": False,
    }

    def make_chat_config():
        return types.GenerateContentConfig(
            response_modalities=["TEXT", "IMAGE"],
            image_config=types.ImageConfig(
                aspect_ratio=config["aspect_ratio"],
                image_size=config["resolution"]
            ),
            thinking_config=types.ThinkingConfig(
                thinking_level=config["thinking"]
            )
        )

    chat = client.chats.create(
        model="gemini-3.1-flash-image-preview",
        config=make_chat_config()
    )

    print("Nano Banana 2 - Interactive Chat Mode (Flash Speed)")
    print("=" * 55)
    print(f"Configuration: aspect={config['aspect_ratio']}, resolution={config['resolution']}, thinking={config['thinking']}")
    print("Type '/help' for commands or start describing your image.\n")

    last_image = None
    conversation_turns = 0

    while True:
        try:
            user_input = input("> ").strip()

            if not user_input:
                continue

            if user_input.lower() in ["exit", "quit"]:
                print("Goodbye!")
                break

            if user_input.startswith("/"):
                parts = user_input.split(maxsplit=1)
                command = parts[0].lower()
                arg = parts[1] if len(parts) > 1 else ""

                if command == "/help":
                    print(__doc__)

                elif command == "/config":
                    print(f"Current configuration:")
                    print(f"  Model: gemini-3.1-flash-image-preview")
                    print(f"  Aspect ratio: {config['aspect_ratio']}")
                    print(f"  Resolution: {config['resolution']}")
                    print(f"  Thinking: {config['thinking']}")
                    print(f"  Web Search: {config['search']}")
                    print(f"  Image Search: {config['image_search']}")
                    print(f"  Turns: {conversation_turns}")

                elif command == "/aspect":
                    if arg in SUPPORTED_ASPECT_RATIOS:
                        config["aspect_ratio"] = arg
                        chat = client.chats.create(
                            model="gemini-3.1-flash-image-preview",
                            config=make_chat_config()
                        )
                        print(f"Aspect ratio set to: {arg}")
                        print("Note: Chat history cleared due to config change")
                        conversation_turns = 0
                    else:
                        print(f"Invalid aspect ratio. Valid options: {', '.join(SUPPORTED_ASPECT_RATIOS)}")

                elif command == "/resolution":
                    if arg.upper() in ["0.5K", "1K", "2K", "4K"]:
                        config["resolution"] = arg.upper()
                        print(f"Resolution set to: {config['resolution']}")
                    else:
                        print("Invalid resolution. Options: 0.5K, 1K, 2K, 4K")

                elif command == "/thinking":
                    if arg in ["high", "minimal"]:
                        config["thinking"] = arg
                        print(f"Thinking level set to: {arg}")
                    else:
                        print("Invalid thinking level. Options: high, minimal")

                elif command == "/search":
                    config["search"] = not config["search"]
                    print(f"Google Web Search grounding: {'enabled' if config['search'] else 'disabled'}")

                elif command == "/imgsearch":
                    config["image_search"] = not config["image_search"]
                    print(f"Google Image Search grounding: {'enabled' if config['image_search'] else 'disabled'}")

                elif command == "/clear":
                    chat = client.chats.create(
                        model="gemini-3.1-flash-image-preview",
                        config=make_chat_config()
                    )
                    last_image = None
                    conversation_turns = 0
                    print("Conversation history cleared.")

                elif command == "/save":
                    if not last_image:
                        print("No image to save. Generate an image first.")
                        continue

                    if not arg:
                        timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
                        arg = f"{timestamp}-image.png"

                    save_path = Path(arg)
                    save_path.parent.mkdir(parents=True, exist_ok=True)
                    last_image.save(str(save_path), "PNG")
                    full_path = save_path.resolve()
                    print(f"Saved: {full_path}")
                    print(f"MEDIA: {full_path}")

                else:
                    print(f"Unknown command: {command}. Type /help for available commands.")

                continue

            # Generate image
            print(f"Generating image (aspect: {config['aspect_ratio']}, resolution: {config['resolution']}, thinking: {config['thinking']})...")

            message_config = types.GenerateContentConfig(
                image_config=types.ImageConfig(
                    aspect_ratio=config["aspect_ratio"],
                    image_size=config["resolution"]
                ),
                thinking_config=types.ThinkingConfig(
                    thinking_level=config["thinking"]
                )
            )

            # Add grounding tools
            tools = []
            if config["search"]:
                tools.append({"google_search": {}})
            if config["image_search"]:
                tools.append({"google_image_search": {}})
            if tools:
                message_config.tools = tools

            response = chat.send_message(
                user_input,
                config=message_config
            )

            conversation_turns += 1

            image_saved = False
            for part in response.parts:
                if part.text:
                    print(f"\n{part.text}\n")
                elif part.inline_data:
                    image_data = part.inline_data.data
                    if isinstance(image_data, str):
                        image_data = base64.b64decode(image_data)

                    image = PILImage.open(BytesIO(image_data))
                    last_image = image

                    temp_path = Path(f"/tmp/nano-banana-2-chat-{conversation_turns}.png")
                    if image.mode == 'RGBA':
                        rgb_image = PILImage.new('RGB', image.size, (255, 255, 255))
                        rgb_image.paste(image, mask=image.split()[3])
                        rgb_image.save(str(temp_path), 'PNG')
                    elif image.mode == 'RGB':
                        image.save(str(temp_path), 'PNG')
                    else:
                        image.convert('RGB').save(str(temp_path), 'PNG')

                    print(f"Image generated (Turn {conversation_turns})")
                    print(f"  Size: {image.size[0]}x{image.size[1]}")
                    print(f"  Use '/save <filename>' to save this image")
                    image_saved = True

            if not image_saved:
                print("No image was generated in the response.")

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)


if __name__ == "__main__":
    main()
