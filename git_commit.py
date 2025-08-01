#!/usr/bin/env python3
"""
Git commit and push script
"""

import os
import subprocess
import sys
import shutil

def run_command(command, description, capture_output=True):
    """Run a command and handle errors."""
    print(f"🔄 {description}...")
    try:
        if capture_output:
            result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        else:
            result = subprocess.run(command, shell=True, check=True)
        print(f"✅ {description} completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        if capture_output and e.stderr:
            print(f"Error output: {e.stderr}")
        return False

def check_first_commit():
    """Check if this is the first commit."""
    try:
        result = subprocess.run("git log --oneline", shell=True, capture_output=True, text=True)
        return result.returncode != 0 or not result.stdout.strip()
    except:
        return True

def check_remote_exists():
    """Check if remote origin exists."""
    try:
        result = subprocess.run("git remote get-url origin", shell=True, capture_output=True, text=True)
        return result.returncode == 0
    except:
        return False

def main():
    """Main function to commit and push."""
    print("🌿 Leaflet - Git Commit and Push")
    print("=" * 40)
    
    # Remove build files
    print("\n🧹 Cleaning build files...")
    
    dirs_to_remove = ["dist", "node_modules"]
    files_to_remove = ["bash.exe.stackdump", "sh.exe.stackdump"]
    
    for dir_name in dirs_to_remove:
        if os.path.exists(dir_name):
            try:
                shutil.rmtree(dir_name)
                print(f"✅ Removed {dir_name}/")
            except Exception as e:
                print(f"⚠️  Could not remove {dir_name}/: {e}")
    
    for file_name in files_to_remove:
        if os.path.exists(file_name):
            try:
                os.remove(file_name)
                print(f"✅ Removed {file_name}")
            except Exception as e:
                print(f"⚠️  Could not remove {file_name}: {e}")
    
    # Add files
    if not run_command("git add .", "Adding files to git"):
        return False
    
    # Check if this is the first commit
    is_first_commit = check_first_commit()
    
    if is_first_commit:
        print("\n📝 This is the first commit...")
        
        # First commit
        if not run_command('git commit -m "first commit"', "Making first commit"):
            return False
        
        # Rename branch to main
        if not run_command("git branch -M main", "Renaming branch to main"):
            return False
        
        # Check if remote exists
        if not check_remote_exists():
            if not run_command("git remote add origin https://github.com/Anthonymm0994/leaflet.git", "Adding remote origin"):
                return False
        else:
            print("✅ Remote origin already exists")
        
        # Push with upstream
        if not run_command("git push -u origin main", "Pushing to remote repository"):
            return False
    else:
        print("\n📝 Committing changes...")
        
        # Regular commit
        if not run_command('git commit -m "Update: Clean build files and improve gitignore"', "Committing changes"):
            return False
        
        # Push
        if not run_command("git push", "Pushing to remote repository"):
            return False
    
    print("\n🎉 Successfully committed and pushed to GitHub!")
    print("📁 Repository: https://github.com/Anthonymm0994/leaflet.git")
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        print("\n❌ Failed to complete git operations")
        sys.exit(1) 