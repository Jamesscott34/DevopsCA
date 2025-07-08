"""
db_host_helper.py

This helper lets you update your settings.py database host value interactively.

- Use 'localhost' if you are running Django locally with `python manage.py runserver` and your Postgres is running on your local machine.
- Use 'db' if you are running Django in Docker, Docker Compose, or Kubernetes, where the Postgres service is named 'db'.

This script will only update the 'HOST' value in settings.py directly.
"""
import os

SETTINGS_PATH = "sba24070_book_catalogue/settings.py"

def update_settings_db_host(new_host):
    with open(SETTINGS_PATH, "r") as f:
        lines = f.readlines()
    with open(SETTINGS_PATH, "w") as f:
        for line in lines:
            if "'HOST':" in line:
                f.write(f"        'HOST': os.environ.get('POSTGRES_HOST', '{new_host}'), #change to localhost to run django locally\n")
            else:
                f.write(line)
    print(f"Updated settings.py to use '{new_host}' as the default for the database host.")

if __name__ == "__main__":
    print("\nUpdate settings.py database host default value:")
    print("1. Set to localhost")
    print("2. Set to db")
    sub_choice = input("Enter 1 or 2: ").strip()
    if sub_choice == '1':
        update_settings_db_host('localhost')
    elif sub_choice == '2':
        update_settings_db_host('db')
    else:
        print("Invalid choice. Please run the script again and enter 1 or 2.") 