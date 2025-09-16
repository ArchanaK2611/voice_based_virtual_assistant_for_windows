# Voice-Based Virtual Assistant for Windows

This project is a Python-based **voice-controlled virtual assistant named Boom**, designed for Windows. It listens to user commands via voice input, processes them, and performs tasks such as fetching weather updates, telling the time/date, searching Google, opening applications, or playing music from local storage, YouTube, or Spotify.

***

### Features

- Wake-up phrase: "Hey Boom" to activate assistant.
- Small talk responses (e.g., greetings, "how are you", "what can you do").
- Voice commands for:
    - **Weather updates** (using wttr.in API)
    - **Time and date announcements**
    - **Search** queries on Google
    - **Open applications**: Notepad, Calculator, Web Browser
    - **Play music** from:
        - Local directory (MP3 files)
        - YouTube (via Pytube \& web browser)
        - Spotify (search link in browser)
- Task control: **pause**, **resume**, or **go back** to listening mode.
- Exit command: Say "exit" or "quit".

***

### Requirements

Install dependencies using `pip install -r requirements.txt` with the following contents:

```
speechrecognition
pyttsx3
requests
plyer
beautifulsoup4
python-vlc
pytube
```

Additional requirements:

- **Python 3.8+** (recommended)
- **Microphone** (for speech recognition input)
- **VLC Media Player** (for local music playback with `python-vlc`)
- **Internet connection** (for APIs, YouTube, Spotify, and web search)

***

### Setup and Usage

1. Clone or download this repository.
2. Install the dependencies:

```bash
pip install -r requirements.txt
```

3. Set up your local environment:
    - Replace the default weather location in `get_weather()` if desired.
    - Update `music_dir` in `play_local_music()` with the path to your local music folder.
4. Make sure VLC is installed and available in PATH.
5. Run the assistant:

```bash
python boom_assistant.py
```

6. Say **"Hey Boom"** to activate.
7. Start interacting with commands like:
    - “What's the weather in London?”
    - “Open Notepad”
    - “Search Python voice assistant”
    - “Play music on YouTube”
    - “What's the time?”
    - “Exit”

***

### Notes

- By default, weather data uses **wttr.in** (no API key needed). The OpenWeatherMap API key placeholder is included but not used directly.
- Music playback with YouTube and Spotify opens the web browser instead of embedding streaming.
- **Google’s Speech Recognition service** requires internet access and is subject to availability.
- Since voice recognition may occasionally misinterpret commands, speaking clearly is recommended.

***

### Future Enhancements

- Add support for reminders and notifications.
- Integrate email and messaging commands.
- Improve conversation flow with NLP libraries.
- Support for multiple wake words or hotkeys.

***

