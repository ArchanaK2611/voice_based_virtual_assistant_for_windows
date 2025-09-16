import time
import speech_recognition as sr
import pyttsx3
import webbrowser
import datetime
import requests
import os
import subprocess
from plyer import notification
from bs4 import BeautifulSoup
import vlc
from pytube import Search

# Initialize the recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Flags to control the assistant's behavior
is_speaking = True
is_paused = False

def speak(text):
    """Converts text to speech if the assistant is allowed to speak."""
    global is_speaking
    if is_speaking:
        engine.say(text)
        engine.runAndWait()

def listen():
    """Listens to the user's voice command and returns it as text."""
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio).lower()
            print(f"You said: {command}")
            return command
        except sr.UnknownValueError:
            speak("Sorry, I didn't understand that.")
            return ""
        except sr.RequestError:
            speak("Sorry, my speech service is down.")
            return ""

def activate_assistant():
    """Activates the assistant when 'hey boom' is said."""
    global is_speaking
    speak("Say 'Hey Boom' to activate me.")
    while True:
        command = listen().strip().lower()
        if "hey boom" in command:
            speak("Hello! I am Boom. How can I assist you today?")
            while True:
                small_talk = listen().strip().lower()
                print(f"Small talk heard: {small_talk}")
                if "how are you" in small_talk:
                    speak("I'm doing great, thank you! How about you?")
                elif "what can you do" in small_talk:
                    speak("I can help you with weather updates, play music, search Google, tell the time, open apps like Notepad and Calculator, and more.")
                elif "nothing" in small_talk or "let's go" in small_talk or "ready" in small_talk:
                    speak("Great! I'm ready to help.")
                    is_speaking = True
                    print(">>> ENTERING MAIN ASSISTANT MODE <<<")       # ✅ Now the assistant is fully active
                    main()                  # ✅ Begin main loop
                    return
                else:
                    speak("You can ask me something or say 'ready' to begin.")
def main():
    """Main loop to continuously listen and respond to commands."""
    global is_paused
    speak("I am ready to take commands. How can I assist you?")
    while True:
        command = listen()
        if "stop" in command:
            speak("Pausing the current task.")
            is_paused = True
            while is_paused:
                speak("Task paused. Say 'resume' to continue or 'back' to go back to listening mode.")
                command = listen()
                if "resume" in command:
                    speak("Resuming the task.")
                    is_paused = False
                elif "back" in command:
                    speak("Stopping the current task and going back.")
                    is_speaking = True
                    return  # Exit the loop to go back to listening mode

        if command:
            respond_to_command(command)
def main():
    global is_paused
    speak("I am ready to take commands. How can I assist you?")
    
    while True:
        if is_paused:
            speak("Task is currently paused. Say 'resume' to continue or 'back' to go to listening mode.")
            while is_paused:
                command = listen().strip().lower()
                if "resume" in command:
                    speak("Resuming the task.")
                    is_paused = False
                elif "back" in command:
                    speak("Stopping the current task and going back.")
                    is_paused = False
                    return
                else:
                    speak("Still paused. Say 'resume' or 'back'.")
        else:
            command = listen().strip().lower()
            if "stop" in command:
                speak("Pausing the current task.")
                is_paused = True
            elif command:
                respond_to_command(command)


def respond_to_command(command):
    global is_speaking, is_paused
    if "weather" in command:
        speak("Which location's weather do you want?")
        location = listen() or "Bangalore"  # Use default if no input
        weather_condition, temperature = get_weather(location)
        print(f"The current weather in {location} is {weather_condition}.")
        speak(f"The current weather in {location} is {weather_condition}.")
        print(f"The temperature is {temperature} degrees Celsius.")
        speak(f"The temperature is {temperature} degrees Celsius.")
    
    elif "open notepad" in command:
        speak("Opening Notepad")
        subprocess.Popen("notepad.exe")
        is_paused = True
    
    elif "open calculator" in command:
        speak("Opening calculator")
        subprocess.Popen("calc.exe")
        is_paused = True
    
    elif "open browser" in command or "open google" in command:
        speak("Opening the web browser")
        webbrowser.open("http://www.google.com")
        is_paused = True

    elif "time" in command:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        print(f"The current time is {current_time}")
        speak(f"The current time is {current_time}")

    elif "date" in command:
        current_date = datetime.datetime.now().strftime("%B %d, %Y")
        print(f"Today is {current_date}")
        speak(f"Today is {current_date}")

    elif "search" in command:
        search_query = command.replace("search", "").strip()
        if search_query:
            speak(f"Searching for {search_query}")
            webbrowser.open(f"https://www.google.com/search?q={search_query}")
        else:
            speak("What would you like me to search for?")
    
    elif "play music" in command:
        speak("Do you want to play music locally, on YouTube, or Spotify?")
        source = listen()
        if "local" in source:
            play_local_music()
        elif "youtube" in source:
            speak("What should I search on YouTube?")
            search_query = listen()
            play_youtube_music(search_query)
        elif "spotify" in source:
            speak("What should I search on Spotify?")
            search_query = listen()
            play_spotify(search_query)
        else:
            speak("I didn't understand the source for playing music.")

    elif "exit" in command or "quit" in command:
        speak("Goodbye!")
        time.sleep(3000)
        exit(0)

    else:
        speak("I didn't recognize that command.")

def get_weather(location="Bangalore"):
    try:
        # Use wttr.in to fetch weather information
        API_KEY = "877719ebb92fb5fdbc237f821ded8722"  # Replace with your OpenWeatherMap API key
        url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={API_KEY}&units=metric"
        url = f"https://wttr.in/{location}?format=j1"  # JSON format for structured data
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            weather_condition = data['current_condition'][0]['weatherDesc'][0]['value']
            temperature = data['current_condition'][0]['temp_C']  # Temperature in Celsius
            return weather_condition, temperature
        else:
            return "Unable to fetch data", "N/A"
    except Exception as e:
        return "Error occurred", "N/A"

def play_local_music():
    """Plays music from a local directory."""
    try:
        music_dir = "path_to_your_music_folder"
        songs = [os.path.join(music_dir, song) for song in os.listdir(music_dir) if song.endswith(".mp3")]
        if songs:
            speak("Playing music.")
            # Initialize VLC media player
            player = vlc.MediaPlayer(songs[0])
            player.play()
            while player.is_playing():  # Wait until the song finishes playing
                time.sleep(1)
        else:
            speak("No music files found in the directory.")
    except Exception as e:
        speak("An error occurred while trying to play music.")

def play_youtube_music(search_query):
    """Plays music from YouTube."""
    try:
        speak(f"Searching YouTube for {search_query}")
        results = Search(search_query).results
        if results:
            url = results[0].watch_url
            speak(f"Playing {results[0].title} from YouTube.")
            webbrowser.open(url)
            is_paused = True
        else:
            speak("No results found on YouTube.")
    except Exception as e:
        speak("An error occurred while searching on YouTube.")

def play_spotify(search_query):
    """Opens Spotify and searches for music."""
    try:
        speak(f"Searching Spotify for {search_query}")
        query_url = f"https://open.spotify.com/search/{search_query}"
        webbrowser.open(query_url)
        speak("Here is what I found on Spotify.")
    except Exception as e:
        speak("An error occurred while opening Spotify.")

if __name__ == "__main__":
    activate_assistant()