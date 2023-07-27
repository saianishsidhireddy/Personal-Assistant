import os
import sqlite3
from SpeakingModule import speak
from SpeechRecognitionModule import TakeCommand
from HelperFunctions import universal_number_converter as word2num

def get_all_apps():
    installed_apps = {}

    # Start Menu folders for current user and all users
    start_menu_folders = [
        os.path.join(os.environ["APPDATA"], "Microsoft", "Windows", "Start Menu", "Programs"),
        os.path.join(os.environ["ProgramData"], "Microsoft", "Windows", "Start Menu", "Programs")
    ]

    for folder in start_menu_folders:
        for root, _, files in os.walk(folder):
            for file in files:
                if file.endswith(".lnk"):  # Look for shortcuts with .lnk extension
                    app_name = os.path.splitext(file)[0]  # Remove the .lnk extension
                    app_path = os.path.join(root, file)
                    installed_apps[app_name] = app_path

    return installed_apps

def save_apps_to_database(apps_data, database_file):
    try:
        conn = sqlite3.connect(database_file)
        cursor = conn.cursor()

        # Create a table to store the app names and paths if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS installed_apps (
                id INTEGER PRIMARY KEY,
                app_name TEXT,
                app_path TEXT
            )
        ''')

        # Check for existing entries before inserting data into the table
        for app_name, app_path in apps_data.items():
            cursor.execute('SELECT id FROM installed_apps WHERE app_name = ? AND app_path = ?', (app_name, app_path))
            existing_entry = cursor.fetchone()
            if not existing_entry:
                cursor.execute('INSERT INTO installed_apps (app_name, app_path) VALUES (?, ?)', (app_name, app_path))

        conn.commit()
        print("Data saved to the database successfully.")
    except sqlite3.Error as e:
        print(f"Error saving data to the database: {e}")
    finally:
        if conn:
            conn.close()

def open_app(app_path):
    try:
        os.startfile(app_path)
    except Exception as e:
        print(f"Error opening the application: {e}")


def search_apps_in_database(input_string, database_file):
    matching_apps = []
    
    try:
        conn = sqlite3.connect(database_file)
        cursor = conn.cursor()

        # Search for matching app names in the database
        cursor.execute("SELECT app_name, app_path FROM installed_apps WHERE app_name LIKE ?", ('%' + input_string + '%',))
        matching_apps = cursor.fetchall()

    except sqlite3.Error as e:
        print(f"Error searching the database: {e}")

    finally:
        if conn:
            conn.close()

    if len(matching_apps) == 0:
        return speak("No matching apps found.")
    
    elif len(matching_apps) == 1:
        app_name, app_path = matching_apps[0]
        speak(f'opening {app_name}')
        return open_app(app_path)
    
    else:
        speak("Multiple matching apps found please choose the app you want to start using the indexes displayed beside the list of apps:")
        for i, (app_name, _) in enumerate(matching_apps, start=1):
            print(f"{i}. {app_name}")

        while True:
            choice = word2num(TakeCommand())
            try:
                index = int(choice)
                if 1 <= index <= len(matching_apps):
                    app_name, app_path = matching_apps[index - 1]
                    return open_app(app_path)
                else:
                    speak("Invalid choice. Please enter a valid index number.")
            except ValueError:
                speak("Invalid input. Please enter a valid index number.")

if __name__ == "__main__":
    # installed_apps = get_all_apps()
    # save_apps_to_database(installed_apps, 'installed_apps.db')
    speak('what do you want me to open')
    input_string = TakeCommand()
    print(input_string)
    database_file = 'installed_apps.db'
    search_apps_in_database(input_string, database_file)


