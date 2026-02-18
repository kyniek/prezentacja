import requests
import json
import time
import sys

# OpenAI API configuration
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
def load_api_key():
    """Load API key from key.txt file"""
    try:
        with open("key.txt", "r") as f:
            api_key = f.read().strip()
        if not api_key:
            print("Error: API key file is empty")
            sys.exit(1)
        return api_key
    except FileNotFoundError:
        print("Error: key.txt file not found. Please create a file named 'key.txt' with your OpenAI API key.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading API key file: {e}")
        sys.exit(1)

API_KEY = load_api_key()

if not API_KEY:
    print("Error: OPENAI_API_KEY environment variable is not set")
    sys.exit(1)

HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}"
}


def main():
    print("Connecting to OpenAI API...")

    # Test connection with a simple request
    try:
        payload = {
            "model": "gpt-4-turbo",
            "messages": [
                {"role": "user", "content": "Hello"}
            ],
            "stream": False
        }

        response = requests.post(
            OPENAI_API_URL,
            headers=HEADERS,
            json=payload
        )

        if response.status_code != 200:
            print(f"Error: Could not connect to OpenAI API. Status code: {response.status_code}")
            print(f"Response: {response.text}")
            return
    except Exception as e:
        print(f"Error connecting to OpenAI API: {e}")
        return

    print("Connected to OpenAI successfully!")
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
                "model": "gpt-4-turbo",
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
                    OPENAI_API_URL,
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
