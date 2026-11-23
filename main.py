import os

from dotenv import load_dotenv
from openai import OpenAI

from chatbot.prompts import SYSTEM_PROMPT

# Read the settings from the .env file
load_dotenv()

API_KEY = os.getenv("LLM_API_KEY")
BASE_URL = os.getenv("LLM_BASE_URL")
MODEL = os.getenv("LLM_MODEL")


def main():
    # Stop early with a clear message if the .env file is missing something
    if not API_KEY or not MODEL:
        print("Missing LLM_API_KEY or LLM_MODEL in your .env file.")
        return

    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

    # The conversation so far. The bot "remembers" by re-reading this list.
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    print("💗 HeartSpace is here to listen.")
    print("   Type 'quit' to leave.\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nTake care of yourself. 💗")
            break

        if not user_input:
            continue

        if user_input.lower() in ("quit", "exit", "bye"):
            print("HeartSpace: Take care of yourself. I'm here whenever you need to talk. 💗")
            break

        messages.append({"role": "user", "content": user_input})

        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=messages,
            )
        except Exception as error:
            print(f"\n[Something went wrong talking to the AI: {error}]\n")
            messages.pop()  # forget the message that failed, so you can retry
            continue

        reply = response.choices[0].message.content
        messages.append({"role": "assistant", "content": reply})

        print(f"\nHeartSpace: {reply}\n")


if __name__ == "__main__":
    main()