import speech_recognition as sr
from SpeakingModule import speak

def TakeCommand():
    print('I am Listening.......')
    r = sr.Recognizer()  # Create an instance of the Recognizer class
    with sr.Microphone() as Source:  # Create an instance of the Microphone class
        r.pause_threshold = 1
        audio = r.listen(Source)
        try:
            query = r.recognize_google(audio, language='en-in')
            return f'User said: {query}'
        except sr.UnknownValueError:
            return speak("Sorry, I couldn't understand what you said. Please try again.")
        except sr.RequestError as e:
            return speak(f"Error occurred during speech recognition: {e}")
 


