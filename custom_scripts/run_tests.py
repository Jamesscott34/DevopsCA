import sys
import os
import subprocess
from datetime import datetime

print("Starting test run...")  # Debug print

# Get the project root directory
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(project_root)  # Change to project root

print(f"Running tests from: {project_root}")

with open('pytest.txt', 'a') as f:
    f.write(f"Test run at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
    try:
        # Run Django tests using manage.py
        result = subprocess.run([
            sys.executable, 'manage.py', 'test', 'books.tests', '--verbosity=2'
        ], capture_output=True, text=True, cwd=project_root)
        
        # Write output to file
        f.write("STDOUT:\n")
        f.write(result.stdout)
        f.write("\nSTDERR:\n")
        f.write(result.stderr)
        
        if result.returncode == 0:
            success_msg = "\n✅ All tests completed successfully!\n"
            f.write(success_msg)
            print(success_msg)
            print("Build Status: PASSING ✅")
        else:
            error_msg = f"\n❌ Tests failed with return code: {result.returncode}\n"
            f.write(error_msg)
            print(error_msg)
            print("Build Status: FAILING ❌")
            sys.exit(1)
            
    except Exception as e:
        error_msg = f"\n❌ Exception occurred: {e}\n"
        f.write(error_msg)
        print(error_msg)
        print("Build Status: FAILING ❌")
        sys.exit(1)

print("Tests complete. See pytest.txt for full results.")  # Debug print 