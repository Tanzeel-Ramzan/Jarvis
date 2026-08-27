import speech_recognition as sr
import pyttsx3
import json
import os
from datetime import datetime


MEMORY_FILE = "memory.json"


# ==========================================
# TEXT TO SPEECH
# ==========================================

engine = pyttsx3.init()

engine.setProperty("rate", 170)
engine.setProperty("volume", 1.0)


def speak(text):
    print("Jarvis:", text)

    engine.say(text)
    engine.runAndWait()


# ==========================================
# SPEECH RECOGNITION
# ==========================================

recognizer = sr.Recognizer()


def listen():

    with sr.Microphone() as source:

        print("\nListening...")

        # Adjust microphone for background noise
        recognizer.adjust_for_ambient_noise(source, duration=0.5)

        try:

            audio = recognizer.listen(
                source,
                timeout=5,
                phrase_time_limit=10
            )

            print("Recognizing...")

            text = recognizer.recognize_google(audio)

            print("You:", text)

            return text

        except sr.WaitTimeoutError:
            print("No speech detected.")
            return ""

        except sr.UnknownValueError:
            print("I couldn't understand you.")
            return ""

        except sr.RequestError:
            speak("Speech recognition service is unavailable.")
            return ""


# ==========================================
# MEMORY
# ==========================================

def load_memory():

    if os.path.exists(MEMORY_FILE):

        with open(MEMORY_FILE, "r", encoding="utf-8") as file:
            return json.load(file)

    return []


def save_memory(memory):

    with open(MEMORY_FILE, "w", encoding="utf-8") as file:
        json.dump(
            memory,
            file,
            indent=4,
            ensure_ascii=False
        )


# ==========================================
# JARVIS BRAIN
# ==========================================

def jarvis_response(message, memory):

    message = message.lower().strip()

    if message in ["hello", "hi", "hey"]:

        return "Hello! How can I help you?"

    elif "your name" in message:

        return "My name is Jarvis."

    elif "how are you" in message:

        return "I'm doing great. Thanks for asking."

    elif "time" in message:

        current_time = datetime.now().strftime("%I:%M %p")

        return f"The current time is {current_time}"

    elif "date" in message:

        current_date = datetime.now().strftime("%d %B %Y")

        return f"Today's date is {current_date}"

    elif "what do you remember" in message:

        if len(memory) == 0:
            return "I don't remember anything yet."

        return f"I remember {len(memory)} previous conversations."

    elif "clear memory" in message:

        memory.clear()

        save_memory(memory)

        return "I have cleared my memory."

    elif "thank you" in message or "thanks" in message:

        return "You're welcome."

    else:

        return "I understand. Tell me more."


# ==========================================
# MAIN
# ==========================================

def main():

    memory = load_memory()

    speak("Hello. I am Jarvis. How can I help you?")

    while True:

        user_message = listen()

        # Nothing recognized
        if user_message == "":
            continue

        # Exit commands
        if user_message.lower() in [
            "exit",
            "quit",
            "goodbye",
            "bye",
            "stop"
        ]:

            speak("Goodbye. See you later.")

            break

        # Get response
        response = jarvis_response(
            user_message,
            memory
        )

        # Speak response
        speak(response)

        # Save conversation
        memory.append({

            "user": user_message,

            "jarvis": response,

            "time": datetime.now().isoformat()

        })

        save_memory(memory)


# ==========================================
# START JARVIS
# ==========================================

if __name__ == "__main__":
    main()