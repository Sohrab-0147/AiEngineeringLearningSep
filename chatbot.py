
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(override=True)

client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.environ["GROQ_API_KEY"]
)

MODEL = "openai/gpt-oss-120b"
MAX_HISTORY = 20   # keep system + last N messages

messages = [
    {
        "role": "system",
        "content": "You are a friendly, concise AI instructor. Keep answers short and clear."
    }
]


def trim_history(msgs, keep_last=MAX_HISTORY):
    """Keep the system message + the most recent exchanges."""
    return [msgs[0]] + msgs[-keep_last:]


def chat(user_input):
    """Send one turn, stream the reply, return (reply_text, usage)."""
    global messages

    messages.append({"role": "user", "content": user_input})
    messages = trim_history(messages)

    stream = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0.3,
        stream=True,
        stream_options={"include_usage": True}
    )

    print("AI: ", end="", flush=True)
    reply = ""
    usage = None

    for chunk in stream:
        # usage arrives on the final chunk
        if chunk.usage:
            usage = chunk.usage
        delta = chunk.choices[0].delta.content if chunk.choices else None
        if delta:
            print(delta, end="", flush=True)
            reply += delta

    print()
    messages.append({"role": "assistant", "content": reply})
    return reply, usage


def main():
    print("Chatbot ready. Type 'exit' to quit, 'reset' to clear memory.\n")

    turn = 0
    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye.")
            break

        if user_input.lower() in ("exit", "quit"):
            print("Bye.")
            break
        if not user_input:
            continue
        if user_input.lower() == "reset":
            del messages[1:]
            turn = 0
            print("[memory cleared]\n")
            continue

        turn += 1
        _, usage = chat(user_input)

        if usage:
            print(
                f"  [turn {turn} · "
                f"in {usage.prompt_tokens} · "
                f"out {usage.completion_tokens} · "
                f"total {usage.total_tokens} tokens]\n"
            )
        else:
            print()


if __name__ == "__main__":
    main()



# Watch two things:

# It remembers — until you type reset.

# in tokens climb every turn — because each turn resends the whole history. Turn 1 might be ~50 input tokens. Turn 5 might be ~200. That's the context window filling in real time. This is the single most important thing to feel about AI apps.

# 4. What each piece does
# messages list — this is the memory. The model has no memory of its own; you resend the whole conversation every call.

# trim_history — keeps the system prompt + last 20 messages. Without this, long chats eventually exceed the model's context window (Groq's gpt-oss-120b is 131,072 tokens — big, but not infinite, and costs scale linearly).

# stream=True — tokens arrive as they're generated. That's why you see the reply appear word by word.

# stream_options={"include_usage": True} — Groq sends a final chunk with token counts. Without this, chunk.usage is None during streaming.

# reset — clears everything except the system prompt, so you can see the difference between remembered and forgotten.