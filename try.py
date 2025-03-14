import speech_recognition as sr

# Initialize recognizer
recognizer = sr.Recognizer()

def listen_and_print():
    with sr.Microphone() as source:
        print("Adjusting for background noise... Please wait.")
        recognizer.adjust_for_ambient_noise(source, duration=1)  # Adjust for ambient noise
        print("Listening... Speak now!")
        
        while True:
            try:
                audio = recognizer.listen(source, timeout=5)  # Listen for 5 seconds
                text = recognizer.recognize_google(audio)  # Convert speech to text
                print(f"You said: {text}")
            except sr.UnknownValueError:
                print("Sorry, I couldn't understand the audio.")
            except sr.RequestError as e:
                print(f"Could not request results; {e}")
                break
            except Exception as e:
                print(f"Error: {e}")
                break

if __name__ == "__main__":
    listen_and_print()
