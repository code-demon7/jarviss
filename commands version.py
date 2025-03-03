import speech_recognition as sr
import pyttsx3
import webbrowser

# Initialize the text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Speaking speed
engine.setProperty('volume', 1)  # Volume level

def speak(text):
    """ Convert text to speech """
    engine.say(text)
    engine.runAndWait()

def listen():
    """ Listen to user and convert speech to text """
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening...")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for background noise
        try:
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio, language="en-US")  # Recognize English speech
            print(f"🔹 You said: {text}")
            return text.lower()
        except sr.UnknownValueError:
            print("❌ Sorry, I didn't understand.")
            return ""
        except sr.RequestError:
            print("⚠️ There was an issue connecting to the internet.")
            return ""

# Main loop
if __name__ == "__main__":
    speak("Hello, how can I help you?")
    while True:
        command = listen()
        
        if "hello" in command:
            speak("Hello! How are you?")
        
        elif "how are you" in command:
            speak("I'm fine, thanks for asking!")
        
        elif "search for" in command:
            query = command.replace("search for", "").strip()
            speak(f"Searching for {query} on Google.")
            webbrowser.open(f"https://www.google.com/search?q={query}")
        
        elif "open youtube" in command:
            speak("Opening YouTube.")
            webbrowser.open("https://www.youtube.com")
        
        elif "goodbye" in command or "stop" in command:
            speak("Goodbye! Have a great day.")
            break
        
        elif command:
            speak("Sorry, I didn't understand that.")
