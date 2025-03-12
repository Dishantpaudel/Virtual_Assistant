import speech_recognition as sr
import webbrowser
import pyttsx3

engine = pyttsx3.init()
recognizer = sr.Recognizer()

def Speak(text):
    engine.say(text)
    engine.runAndWait()


if __name__ == '__main__':
    Speak("How can I help you dear?")

