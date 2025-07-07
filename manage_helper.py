import subprocess
import sys

def run_command(cmd):
    print(f"\n[RUNNING] {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)
    if result.returncode != 0:
        print(f"[ERROR] Command failed: {' '.join(cmd)}", file=sys.stderr)
        sys.exit(result.returncode)

def main():
    print("Django Management Helper Script\n")
    run_command([sys.executable, 'manage.py', 'migrate'])
    run_command([sys.executable, 'manage.py', 'collectstatic', '--noinput'])
    run_command([sys.executable, 'manage.py', 'create_admin'])
    print("\n[INFO] All commands completed.")

if __name__ == "__main__":
    main() 