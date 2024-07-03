import os
import subprocess
import schedule
import time
from datetime import datetime

# Set up your GitHub repository path and commit message
REPO_PATH = '/path/to/your/project/'
SCRIPT_PATH = '/path/to/your/project/auto_commit.py'  # Path to this script
COMMIT_MESSAGE = 'Automated commit message'
BRANCH_NAME = 'main'  # or 'master' based on your branch name
LOG_FILE = '/path/to/your/logs/auto_commit.log'  # Log file path

def add_comment_to_script():
    try:
        with open(SCRIPT_PATH, 'a') as script:
            script.write(f'# Automated comment added on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n')
    except Exception as e:
        with open(LOG_FILE, 'a') as log:
            log.write(f'{datetime.now()} - An error occurred while adding a comment to the script: {e}\n')

def git_commit():
    try:
        # Change to the repository directory
        os.chdir(REPO_PATH)

        # Add a comment to the script to ensure a new commit
        add_comment_to_script()

        # Add changes to staging
        subprocess.run(['git', 'add', SCRIPT_PATH], check=True)

        # Commit changes
        subprocess.run(['git', 'commit', '-m', COMMIT_MESSAGE], check=True)

        # Push changes to the remote repository
        result = subprocess.run(['git', 'push', 'origin', BRANCH_NAME], check=True, capture_output=True, text=True)

        with open(LOG_FILE, 'a') as log:
            log.write(f'{datetime.now()} - Commit successful\n')
    except subprocess.CalledProcessError as e:
        with open(LOG_FILE, 'a') as log:
            log.write(f'{datetime.now()} - An error occurred: {e}\n')
            log.write(f'Output: {e.output}\n')
            log.write(f'Stderr: {e.stderr}\n')

# Schedule the commit job to run every minute
schedule.every(1).minutes.do(git_commit)

if __name__ == "__main__":
    with open(LOG_FILE, 'a') as log:
        log.write(f'{datetime.now()} - Service started\n')
    while True:
        schedule.run_pending()
        time.sleep(1)
