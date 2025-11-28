import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser as wb
import os
import random
import pyjokes
from PIL import ImageGrab  # Only works on Windows, so we fallback on server

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 150)
engine.setProperty('volume', 1)


def speak(audio) -> None:
    engine.say(audio)
    engine.runAndWait()


def time() -> None:
    current_time = datetime.datetime.now().strftime("%I:%M:%S %p")
    speak("The current time is")
    speak(current_time)
    print("The current time is", current_time)


def date() -> None:
    now = datetime.datetime.now()
    speak("The current date is")
    speak(f"{now.day} {now.strftime('%B')} {now.year}")
    print(f"The current date is {now.day}/{now.month}/{now.year}")


def wishme() -> None:
    speak("Welcome back!")
    print("Welcome back!")

    hour = datetime.datetime.now().hour
    if 4 <= hour < 12:
        speak("Good morning!")
    elif 12 <= hour < 16:
        speak("Good afternoon!")
    elif 16 <= hour < 24:
        speak("Good evening!")
    else:
        speak("Good night, see you tomorrow.")

    assistant_name = load_name()
    speak(f"{assistant_name} at your service. Please tell me how may I help you.")
    print(f"{assistant_name} at your service. Please tell me how may I help you.")


def screenshot() -> None:
    """Headless-safe screenshot function"""
    try:
        img = ImageGrab.grab()   # Works on Windows only
        img_path = os.path.expanduser("~/screenshot.png")
        img.save(img_path)
        speak(f"Screenshot saved at {img_path}")
        print(f"Screenshot saved at {img_path}")
    except Exception:
        speak("Screenshot feature is unavailable on this device.")
        print("Screenshot not supported on server.")


def takecommand() -> str:
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1

        try:
            audio = r.listen(source, timeout=5)
        except sr.WaitTimeoutError:
            speak("Timeout occurred. Please try again.")
            return None

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language="en-in")
        print(query)
        return query.lower()

    except sr.UnknownValueError:
        speak("Sorry, I did not understand that.")
        return None

    except sr.RequestError:
        speak("Speech service unavailable.")
        return None

    except Exception as e:
        speak(f"An error occurred: {e}")
        print(e)
        return None


def play_music(song_name=None) -> None:
    music_dir = os.path.expanduser("~/Music")

    if not os.path.exists(music_dir):
        speak("Music folder not found.")
        return

    songs = os.listdir(music_dir)

    if song_name:
        songs = [s for s in songs if song_name.lower() in s.lower()]

    if songs:
        song = random.choice(songs)
        song_path = os.path.join(music_dir, song)

        # Linux-compatible open
        os.system(f"xdg-open '{song_path}'")

        speak(f"Playing {song}")
        print(f"Playing {song}")

    else:
        speak("No songs found.")
        print("No songs found.")


def set_name() -> None:
    speak("What would you like to name me?")
    name = takecommand()
    if name:
        with open("assistant_name.txt", "w") as f:
            f.write(name)
        speak(f"Alright, I will be called {name} from now on.")
    else:
        speak("Sorry, I couldn't catch that.")


def load_name() -> str:
    try:
        with open("assistant_name.txt", "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return "Jarvis"


def search_wikipedia(query):
    try:
        speak("Searching Wikipedia...")
        result = wikipedia.summary(query, sentences=2)
        speak(result)
        print(result)
    except:
        speak("I couldn't find anything on Wikipedia.")


if __name__ == "__main__":
    wishme()

    while True:
        query = takecommand()
        if not query:
            continue

        if "time" in query:
            time()

        elif "date" in query:
            date()

        elif "wikipedia" in query:
            query = query.replace("wikipedia", "").strip()
            search_wikipedia(query)

        elif "play music" in query:
            song_name = query.replace("play music", "").strip()
            play_music(song_name)

        elif "open youtube" in query:
            wb.open("youtube.com")

        elif "open google" in query:
            wb.open("google.com")

        elif "change your name" in query:
            set_name()

        elif "screenshot" in query:
            screenshot()

        elif "tell me a joke" in query:
            joke = pyjokes.get_joke()
            speak(joke)
            print(joke)

        elif "shutdown" in query:
            speak("Shutting down the system.")
            os.system("shutdown now")
            break

        elif "restart" in query:
            speak("Restarting system.")
            os.system("reboot")
            break

        elif "exit" in query or "offline" in query:
            speak("Going offline, goodbye!")
            break
