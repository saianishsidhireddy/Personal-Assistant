from SpeakingModule import speak
from SpeechRecognitionModule import TakeCommand
import os


# if __name__ == '__main__':
#     speak('hello i am Grim, How may i assist you')
#     # while True:
#     #     print(TakeCommand())

#     import os

def open_app(app_path):
    try:
        os.startfile(app_path)
    except Exception as e:
        print(f"Error opening the application: {e}")

if __name__ == "__main__":
    # Replace the app_link variable with the path to the .lnk file you want to open
    app_link = r"C:\Users\anees\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Discord Inc\Discord.lnk"
    open_app(app_link)
