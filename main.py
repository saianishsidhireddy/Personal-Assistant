from SpeakingModule import speak
from SpeechRecognitionModule import TakeCommand



if __name__ == '__main__':
    speak('hello i am Grim, How may i assist you')
    while True:
        print(TakeCommand())

