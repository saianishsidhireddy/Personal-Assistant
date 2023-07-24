import speech_recognition as sr

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
            return "Sorry, I couldn't understand what you said. Please try again."
        except sr.RequestError as e:
            return f"Error occurred during speech recognition: {e}"



