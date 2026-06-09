GitHub Permission Manager
Python CLI tool to manage GitHub repository collaborators via the GitHub REST API.

Project Structure
github_permission_manager/
├── mAin.py              # Entry point — runs all GitHubClient features
├── src/
│   ├── __init__.py
│   ├── github_client.py # Core API wrapper (add/remove/list collaborators)
│   └── settings.py      # App settings
├── config/              # Config files
├── logs/                # Log output (auto-created)
├── .env                 # Secret credentials (never commit this)
├── .gitignore
└── requirements.txt


.env File — Setup & Reference
The .env file stores sensitive credentials locally so they are never hardcoded in source code or committed to Git.

Location
Place .env in the project root (same folder as mAin.py):
github_permission_manager/.env

Contents
GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxx
GITHUB_OWNER=your-github-username-or-org

Variable Reference


How to Get a GitHub Token
Go to github.com → Profile → Settings
Scroll to Developer Settings → Personal access tokens → Tokens (classic)
Click Generate new token
Note: give it a name like github-permission-manager
Scopes: check repo and (if org repos) admin:org
Click Generate token and copy it immediately — it is shown only once

Security Rules
Never commit .env — it is already in .gitignore
Set a token expiration date (e.g. 90 days) for safety
If leaked, revoke it immediately in GitHub Developer Settings

How mAin.py Works
mAin.py is the entry point that exercises every method in GitHubClient in sequence. It is designed to demo and test the full API surface.

Execution Flow


Configuration Constants
Edit these three constants at the top of mAin.py before running:
REPO         = 'my-test-repo'       # A repo you own or admin
COLLABORATOR = 'some-github-user'   # GitHub username to invite
PERMISSION   = 'push'               # pull | triage | push | maintain | admin

Permission Levels



Logging
Logs are written to both the terminal and a file simultaneously.



Watch Logs Live
tail -f logs/app.log


Quickstart
Clone the repo and cd into it
git clone https://github.com/your-org/github_permission_manager.git
cd github_permission_manager

Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

Install dependencies
pip install -r requirements.txt

Create your .env file
GITHUB_TOKEN=ghp_your_token_here
GITHUB_OWNER=your-github-username

Edit REPO and COLLABORATOR constants in mAin.py

Run
python mAin.py