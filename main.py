import speech_recognition as sr
import webbrowser
import pyttsx3
import requests
import os
import musiclibrary
from openai import OpenAI
from gtts import gTTS
import pygame
import sqlite3
from dotenv import load_dotenv  # Secure API key handling
import time  # Import time module to manage timing

# Load environment variables
load_dotenv()

# Initialize Recognizer and Text-to-Speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Securely load API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
NEWS_API_KEY = os.getenv("58a9e5b5a65145868f443ed649c5dffb")

# Check if API keys are set
if not OPENAI_API_KEY:
    print("Error: OpenAI API key is missing. Set it in .env file.")
    exit(1)

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# Function to initialize the database
def init_db():
    conn = sqlite3.connect('user_commands.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS commands (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        command TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )''')
    conn.commit()
    conn.close()

# Function to insert the user command into the database
def insert_command(command):
    conn = sqlite3.connect('user_commands.db')
    c = conn.cursor()
    c.execute('INSERT INTO commands (command) VALUES (?)', (command,))
    conn.commit()
    conn.close()

# Function to retrieve commands from the database
def get_commands():
    conn = sqlite3.connect('user_commands.db')
    c = conn.cursor()
    c.execute('SELECT command, timestamp FROM commands ORDER BY timestamp DESC')
    commands = c.fetchall()
    conn.close()
    return commands

# Function to Speak
def speak(text, use_pyttsx3=False):
    if use_pyttsx3:
        engine.say(text)
        engine.runAndWait()
    else:
        try:
            tts = gTTS(text)
            tts.save("temp.mp3")
            pygame.mixer.init()
            pygame.mixer.music.load("temp.mp3")
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            pygame.mixer.music.unload()
            os.remove("temp.mp3")
        except Exception as e:
            print(f"Speech error: {e}")
            engine.say(text)
            engine.runAndWait()

# Function to Process AI Response
def ai_process(command):
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "system", "content": "You are Jarvis, a helpful AI assistant. Provide short responses."},
                      {"role": "user", "content": command}]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"OpenAI API Error: {e}")
        return "I'm having trouble connecting to OpenAI."

# Function to Process Commands
def process_command(command):
    command = command.lower()

    # Insert the command into the database
    insert_command(command)

    # If the command is "output", speak the previous commands
    if "output" in command:
        commands = get_commands()
        if commands:
            speak("Here are your previous commands:")
            for command, timestamp in commands:
                speak(f"Command: {command} at {timestamp}")
        else:
            speak("No commands found.")
    elif "open google" in command:
        webbrowser.open("https://google.com")
    elif "open facebook" in command:
        webbrowser.open("https://facebook.com")
    elif "open youtube" in command:
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in command:
        webbrowser.open("https://linkedin.com")
        
    elif command.startswith("play"):
        song = command.split(" ", 1)[1]  # Get the song name
        if song in musiclibrary.music:
            link = musiclibrary.music[song]
            webbrowser.open(link)
            speak(f"Playing {song} for you.")
        else:
            speak("Sorry, I couldn't find that song in the library.")      
            
    elif "news" in command:
        if not NEWS_API_KEY:
            speak("News API key is missing. Please check your configuration.")
            return
        try:
            response = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={NEWS_API_KEY}")
            if response.status_code == 200:
                articles = response.json().get('articles', [])
                for article in articles[:5]:  # Limit to 5 headlines
                    speak(article['title'])
            else:
                speak("Unable to fetch news.")
        except Exception as e:
            print(f"News API Error: {e}")
            speak("News service is currently unavailable.")
    else:
        output = ai_process(command)
        speak(output)

# Function to Listen for the Wake Word
def listen_for_wake_word():
    with sr.Microphone() as source:
        print("Listening for 'Wake word'...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=3)
            return recognizer.recognize_google(audio).lower() == "hello"
        except Exception:
            return False

# Function to Listen and Process Commands
def listen_and_process():
    with sr.Microphone() as source:
        print("Virtual Assistant is active... Listening for commands.")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            command = recognizer.recognize_google(audio)
            process_command(command)
        except Exception as e:
            print(f"Error: {e}")
            speak("Sorry, I didn't understand that.")

# Main Execution
if __name__ == "__main__":
    speak("Initializing Virtual Assistant...")
    init_db()  # Initialize the database at startup

    while True:
        if listen_for_wake_word():
            speak("Yes?")
            listen_and_process()
