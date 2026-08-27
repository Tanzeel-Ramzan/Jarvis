import json
import os
from datetime import datetime

MEMORY_FILE = "memory.json"


# -----------------------------
# Load previous conversations
# -----------------------------
def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r", encoding="utf-8") as file:
            return json.load(file)

    return []


# -----------------------------
# Save conversations
# -----------------------------
def save_memory(memory):
    with open(MEMORY_FILE, "w", encoding="utf-8") as file:
        json.dump(memory, file, indent=4)


# -----------------------------
# Jarvis response
# -----------------------------
def jarvis_response(user_message, memory):
    message = user_message.lower()

    if message in ["hello", "hi", "hey"]:
        return "Hello! How can I help you?"

    elif "your name" in message:
        return "My name is Jarvis."

    elif "how are you" in message:
        return "I'm doing great. Thanks for asking!"

    elif "time" in message:
        return datetime.now().strftime("The current time is %H:%M:%S")

    elif "what do you remember" in message:
        if not memory:
            return "I don't remember anything yet."

        return f"I remember {len(memory)} previous messages."

    elif "clear memory" in message:
        memory.clear()
        save_memory(memory)
        return "I cleared my memory."

    elif "bye" in message or "exit" in message:
        return "Goodbye! See you later."

    else:
        return "I understand. Tell me more."


# -----------------------------
# Main program
# -----------------------------
def main():

    memory = load_memory()

    print("=" * 40)
    print("        JARVIS AI")
    print("=" * 40)
    print("Type 'exit' to stop.")
    print("Type 'what do you remember' to check memory.")
    print("Type 'clear memory' to delete memory.")
    print()

    while True:

        user_message = input("You: ")

        if user_message.lower() in ["exit", "bye"]:
            print("Jarvis: Goodbye!")
            break

        # Get Jarvis response
        response = jarvis_response(user_message, memory)

        print("Jarvis:", response)

        # Save conversation
        memory.append({
            "user": user_message,
            "jarvis": response,
            "time": datetime.now().isoformat()
        })

        save_memory(memory)


if __name__ == "__main__":
    main()