import os
from SpeakingModule import speak
from SpeechRecognitionModule import TakeCommand



if __name__ == '__main__':
    speak('hello i am ronni, How may i assist you')
    print(TakeCommand())

