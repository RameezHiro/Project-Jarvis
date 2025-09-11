import speech_recognition as sr
import webbrowser
import pyttsx3
import time
import musicLibrary
import winsound  # Windows built-in module for beep
import requests

recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = "c471a6c10be84886b5f83d8a83ac0766"


# Configure voice & speed (optional)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # change to voices[1] for female voice
engine.setProperty('rate', 180)

def speak(text):
    engine.say(text)
    engine.runAndWait()
    time.sleep(0.3)

def play_beep():
    # frequency (Hz), duration (ms)
    winsound.Beep(1000, 200)  # Short 200ms beep at 1kHz

def processCommand(command):
    command = command.lower()
    print(f"Command: {command}")
    if "open google" in command:
        speak("Opening Google")
        webbrowser.open("https://www.google.com")
    elif "open youtube" in command:
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")
    elif "open " in command:
        speak("Opening Github")
        webbrowser.open("https://www.github.com")
    elif command.lower().startswith("play"):
        song = command.lower().split(" ")[1]
        link = musicLibrary.music[song]
        webbrowser.open(link)

    elif "news" in command.lower():
        r = requests.get("https://newsapi.org/v2/top-headlines?sources=bbc-news&apiKey=c471a6c10be84886b5f83d8a83ac0766")
        if r.status_code == 200:
          data = r.json()  # Convert response to dictionary
          articles = data.get("articles", [])  # Get list of articles
        
        print("Top BBC News Headlines:\n")
        for i, article in enumerate(articles, start=1):
            title = article.get('title', 'No title')
            print(f"{i}. {title}")
            def speak(text):
                engine = pyttsx3.init()
                voices = engine.getProperty('voices')
                engine.setProperty('voice', voices[0].id)
                engine.setProperty('rate', 180)
                engine.say(text)
                engine.runAndWait()
                time.sleep(0.3)
            speak(title)
             
        else:
         speak("Sorry, I couldn't fetch the news.")
            
            




if __name__ == "__main__":
    speak("Initializing Jarvis.....")
    while True:
        print("Recognizing...")
        try:
            with sr.Microphone() as source:
                print("Listening for wake word...")
                audio = recognizer.listen(source, timeout=3, phrase_time_limit=2)

            try:
                word = recognizer.recognize_google(audio)
                print(f"Heard: {word}")
            except sr.UnknownValueError:
                continue

            if word.lower() == "jarvis":
                print("Wake word detected.")
                time.sleep(0.2)  # allow mic to release
                play_beep()  # Play the activation beep
                time.sleep(0.3)  # short pause before next listen

                with sr.Microphone() as source:
                    print("Jarvis Active... Listening for command")
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)

                try:
                    command = recognizer.recognize_google(audio)
                    processCommand(command)
                except sr.UnknownValueError:
                    speak("Sorry, I didn't catch that.")
        except sr.WaitTimeoutError:
            continue
        except Exception as e:
            print(f"Error: {e}")

