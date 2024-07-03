# Automating GitHub Commits with a Python Script and Systemd

## Overview
This repo outlines the steps to create a Python script that automatically commits changes to a GitHub repository every minute. The script is set up to run as a systemd service on Debian 12, ensuring it starts every time the PC is on.

## Prerequisites
- Python 3.11
- Git
- GitHub account with SSH key configured, or you could use ghcli tool, you will thank me later for this tool.
- Any Linux Distro

## Steps

### 1. Create the Python Script

Create a Python script that automates the commit process. Save the script to `/path/to/your/project/auto_commit.py`.

```python
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
```

### 2. Create a Virtual Environment

Create and activate a virtual environment to manage the script's dependencies.

```bash
cd /path/to/your/project
python3 -m venv venv
source venv/bin/activate  # Use activate.fish if you are using the Fish shell
pip install schedule
```

### 3. Create the Systemd Service File

Create a systemd service file to manage the script as a service. Save the file as `/etc/systemd/system/auto_commit.service`.

```ini
[Unit]
Description=Auto Commit Script
After=network.target

[Service]
ExecStart=/path/to/your/project/venv/bin/python /path/to/your/project/auto_commit.py
WorkingDirectory=/path/to/your/project
StandardOutput=inherit
StandardError=inherit
Restart=always
User=yourusername
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
```

### 4. Reload Systemd and Start the Service

Reload systemd to apply the new service configuration and start the service.

```bash
sudo systemctl daemon-reload
sudo systemctl enable auto_commit.service
sudo systemctl start auto_commit.service
sudo systemctl status auto_commit.service
```

### 5. Check the Log File

Monitor the log file to ensure the script is running correctly and commits are being made.

```bash
cat /path/to/your/logs/auto_commit.log
```

### Troubleshooting

- **SSH Authentication**: Ensure your SSH key is added to the ssh-agent and that it’s correctly configured in GitHub.

  ```bash
  eval "$(ssh-agent -s)"
  ssh-add ~/.ssh/id_rsa  # Or the path to your SSH private key
  ssh -T git@github.com
  ```

- **Repository State**: Ensure your local repository is on the correct branch and not in a detached HEAD state.

  ```bash
  cd /path/to/your/project/
  git status
  ```

- **Manual Push**: Test pushing manually to ensure there are no issues with the repository or authentication.

  ```bash
  cd /path/to/your/project/
  git add auto_commit.py
  git commit -m "Test commit"
  git push origin main
  ```

### Conclusion

By following these steps, you can automate the process of committing changes to a GitHub repository every minute using a Python script and systemd. This ensures your GitHub activity graph remains active and updated.
```

Replace `/path/to/your/project`, `/path/to/your/logs`, and `yourusername` with your actual paths and username as appropriate. This document provides all the necessary commands and code to set up and run the automated commit script.
