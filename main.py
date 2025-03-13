import speech_recognition as sr
import webbrowser
import pyttsx3
from musiclibrary import music
import os

#pip1 install pocketsphinx
#pip install pyttsx3
#pip install SpeechRecognition
recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()
    
def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("www.google.com")
    elif "open youtube" in c.lower():    
        webbrowser.open("www.youtube.com")
    elif "open facebook" in c.lower():
        webbrowser.open("www.facebook.com")
    elif "open whatsapp" in c.lower():
        webbrowser.open("https://web.whatsapp.com/")          
    elif c.lower().startswith("play"):
        song = c.lower().split("play")[-1]
        link = music.play[song]
        webbrowser.open(link)

if __name__ == "__main__":
    
    speak("Initializing Jarvis....")
    while True:
        # Listen for the wake word "Jarvis"
        # obtain audio from the microphone
        r = sr.Recognizer()
         
        print("recognizing...")
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source, timeout=2, phrase_time_limit=1)
            word = r.recognize_google(audio)
            if word.lower() == "hey":
                speak("Ya")
                # Listen for command
                with sr.Microphone() as source:
                    print("Jarvis Active...")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)

                    processCommand(command)

        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
        except Exception as e:
            print("Error; {0}".format(e))
            try:
                with sr.Microphone() as source:
                    audio = r.listen(source, timeout=3, phrase_time_limit=5)
                command = r.recognize_google(audio)
                processCommand(command)
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))
            except Exception as e:
                print("Error: {0} ".format(e))