import os
from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic()

MODEL = "claude-haiku-5-5" 
SYSTEM_PROMPT = "You are a concise, helpful assistant. Keep answers short unless asked for detail."

messages: list[dict] = []

def chat(user_input: str) -> None:
    messages.append({"role": "user","content":user_input})
    print("Claude: ", end="",flush=True)

    with client.messages.stream(
        model=MODEL,
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=messages,
    ) as stream:
        for text in stream.text_stream:
            print(text,end="",flush=True)
        final = stream.get_final_message()
    messages.append({"role": "assistant", "content": final.content})

    usage = final.usage
    print(f"\n  [tokens: {usage.input_tokens} in, {usage.output_tokens} out | turns in history: {len(messages)}]\n")

def main() -> None:
            print("Chat started. Commands: /reset to clear memory, /exit to quit.\n")
            while True:
                 user_input = input("You : ").strip()
                 if not user_input:
                    continue
                 if user_input == "/exit":
                      break
                 if user_input == "/reset":
                      messages.clear()
                      print("  [memory cleared]\n")
                      continue
                 try:
                      chat(user_input)
                 except anthropic.APIError as e:
                      messages.pop()
                      print(f"\n [API error: {e}]\n")

if __name__ == "__main__":
     main()
            

