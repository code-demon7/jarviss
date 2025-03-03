import os
import openai
import speech_recognition as sr
import pyttsx3

# Fetch OpenAI API key from environment variable
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
if OPENAI_API_KEY is None:
    raise ValueError("API key not found. Please set the OPENAI_API_KEY environment variable.")

# Configuration for speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Speech rate
engine.setProperty('volume', 1)  # Volume level

def speak(text):
    """ Convert text to speech """
    engine.say(text)
    engine.runAndWait()

def listen():
    """ Listen to the user and convert speech to text """
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening...")
        recognizer.adjust_for_ambient_noise(source)  # Improve capture quality
        attempts = 0
        while attempts < 3:  # Limit retries to 3 attempts
            try:
                audio = recognizer.listen(source, timeout=5)  # Reduced timeout to 5 seconds
                text = recognizer.recognize_google(audio, language="en-US")  # Recognize speech in English
                print(f"🔹 You said: {text}")
                return text
            except sr.UnknownValueError:
                attempts += 1
                print("❌ Sorry, I couldn't understand. Please try again.")
            except sr.RequestError:
                print("⚠️ Internet connection issue. Please check your connection and try again.")
                return ""
        return ""  # Return empty string after max attempts

def chat_with_gpt(prompt):
    """ Send text to ChatGPT and get a response """
    openai.api_key = OPENAI_API_KEY
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response["choices"][0]["message"]["content"]
    except openai.error.OpenAIError as e:
        print(f"⚠️ OpenAI API error: {e}")
        return "Sorry, I couldn't get a response from the AI."
    except Exception as e:
        print(f"⚠️ Error communicating with OpenAI: {e}")
        return "Sorry, I couldn't get a response from the AI."

# Main loop for the voice assistant
if __name__ == "__main__":
    speak("Hello, I am your AI assistant. How can I help you today?")
    while True:
        command = listen()
        if command.lower() in ["goodbye", "exit", "stop", "quit", "see you later"]:
            speak("Goodbye! Have a great day.")
            break
        elif command:
            response = chat_with_gpt(command)
            print(f"🤖 AI: {response}")
            speak(response)
