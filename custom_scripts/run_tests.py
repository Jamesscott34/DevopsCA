import sys
import os
import django
from django.conf import settings
from django.core.management import call_command
from contextlib import redirect_stdout, redirect_stderr
from datetime import datetime

print("Starting test run...")  # Debug print

# Set up Django environment if not already set
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sba24070_book_catalogue.settings')
django.setup()

with open('pytest.txt', 'a') as f:
    f.write(f"Test run at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
    try:
        with redirect_stdout(f), redirect_stderr(f):
            call_command('test', 'books.tests', verbosity=3)
    except Exception as e:
        f.write(f"\nException occurred: {e}\n")
        print(f"Exception occurred: {e}")

print("Tests complete. See pytest.txt for full results.")  # Debug print 