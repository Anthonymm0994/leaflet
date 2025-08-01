import subprocess
import sys

def run_git_commands():
    commands = [
        "git add .",
        'git commit -m "Update: Clean build files and improve gitignore"',
        "git push"
    ]
    
    for cmd in commands:
        print(f"Running: {cmd}")
        try:
            result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
            print(f"✅ Success: {cmd}")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed: {cmd}")
            print(f"Error: {e.stderr}")
            return False
    return True

if __name__ == "__main__":
    success = run_git_commands()
    if success:
        print("🎉 All git commands completed successfully!")
    else:
        print("❌ Some git commands failed")
        sys.exit(1) 