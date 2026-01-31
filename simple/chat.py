import requests
import json
import time
import sys
from datetime import datetime

# 192.168.32.15
# LMStudio API configuration
LMSTUDIO_URL = "http://192.168.32.18:1234/v1/chat/completions"
HEADERS = {
    "Content-Type": "application/json"
}


def main():
    print("Connecting to LMStudio...")

    # Test connection
    try:
        health_url = f"{LMSTUDIO_URL.replace('/v1/chat/completions', '/health')}"
        response = requests.get(health_url)
        if response.status_code != 200:
            print("Error: Could not connect to LMStudio. Make sure it's running on port 1234")
            return
    except Exception as e:
        print(f"Error connecting to LMStudio: {e}")
        print("Make sure LMStudio is running with API enabled")
        return

    print("Connected to LMStudio successfully!")
    print("Type 'quit' to exit")
    print("-" * 50)

    # Chat loop
    while True:
        try:
            user_input = input("\nYou: ").strip()

            if user_input.lower() in ['quit', 'exit']:
                print("Goodbye!")
                break

            if not user_input:
                continue

            # Prepare chat request
            payload = {
                "model": "",  # LMStudio will use default model
                "messages": [
                    {"role": "user", "content": user_input}
                ],
                "stream": True,
                "temperature": 0.7
            }

            # Start timing
            start_time = time.time()
            tokens_processed = 0

            print("Assistant: ", end="", flush=True)

            # Stream response
            try:
                response = requests.post(
                    LMSTUDIO_URL,
                    headers=HEADERS,
                    json=payload,
                    stream=True
                )

                if response.status_code != 200:
                    print(f"Error: {response.status_code} - {response.text}")
                    continue

                # Process streaming response
                for line in response.iter_lines():
                    if line:
                        line = line.decode('utf-8')
                        if line.startswith("data: "):
                            data = line[6:]  # Remove 'data: ' prefix

                            if data.strip() == "[DONE]":
                                break

                            try:
                                json_data = json.loads(data)
                                content = json_data.get("choices", [{}])[0].get("delta", {}).get("content", "")

                                if content:
                                    print(content, end="", flush=True)
                                    tokens_processed += 1
                            except json.JSONDecodeError:
                                continue

                # End timing
                end_time = time.time()
                processing_time = end_time - start_time

                # Calculate metrics
                tokens_per_second = tokens_processed / processing_time if processing_time > 0 else 0

                # Display metadata
                print(f"\n\n--- Metadata ---")
                print(f"Tokens processed: {tokens_processed}")
                print(f"Processing time: {processing_time:.2f} seconds")
                print(f"Tokens per second: {tokens_per_second:.2f}")

            except Exception as e:
                print(f"\nError during streaming: {e}")

        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"\nError: {e}")




if __name__ == "__main__":
    main()
