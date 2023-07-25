import os
import winreg
import sqlite3

def get_installed_apps():
    installed_apps = {}
    
    # Open the Windows Registry key where information about installed applications is stored
    key = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"
    with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key) as reg_key:
        try:
            index = 0
            while True:
                # Enumerate subkeys (application entries) under the "Uninstall" key
                sub_key_name = winreg.EnumKey(reg_key, index)
                with winreg.OpenKey(reg_key, sub_key_name) as app_key:
                    try:
                        # Get the application name and its executable file
                        app_name = winreg.QueryValueEx(app_key, "DisplayName")[0].strip()
                        app_exe = winreg.QueryValueEx(app_key, "DisplayIcon")[0].strip()
                        
                        # Clean up the DisplayIcon path to get the actual executable file
                        app_exe = app_exe.strip('"').split(",")[0].strip()
                        
                        # Some entries might have empty names or executable paths, so we skip those
                        if app_name and app_exe:
                            installed_apps[app_name] = app_exe
                    except FileNotFoundError:
                        # Some subkeys may not have the required values, so we skip those
                        pass
                    except Exception as e:
                        print(f"Error processing {sub_key_name}: {e}")
                index += 1
        except OSError:
            # When there are no more subkeys to enumerate, we'll get an OSError, so we stop the loop.
            pass
        
        # Store the data in the database
        with sqlite3.connect("installed_apps.db") as conn:
            cursor = conn.cursor()
            # Create a table if it doesn't exist
            cursor.execute("CREATE TABLE IF NOT EXISTS apps (name TEXT PRIMARY KEY, executable TEXT)")
            # Insert or update the data in the database
            for app_name, app_exe in installed_apps.items():
                cursor.execute("INSERT OR REPLACE INTO apps (name, executable) VALUES (?, ?)", (app_name, app_exe))
            conn.commit()

        print("Data stored in the database.")
        return installed_apps

if __name__ == "__main__":
    installed_apps = get_installed_apps()
    for app_name, app_exe in installed_apps.items():
        print(f"{app_name}:================= {app_exe}\n")
