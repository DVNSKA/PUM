# GitHub Permission Manager

Manage GitHub repo collaborators via the GitHub REST API.

---

## Project Structure

```
github_permission_manager/
├── mAin.py              → entry point, runs everything
├── src/
│   ├── github_client.py → core API wrapper
│   └── settings.py      → app settings
├── logs/                → log files saved here
├── .env                 → your secrets (never commit this)
└── requirements.txt
```

---

## .env File

Create a file called `.env` in the project root with these two lines:

```
GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxx
GITHUB_OWNER=your-github-username
```

### How to get your GitHub Token

1. Go to github.com → click your profile pic → Settings
2. Scroll down → Developer Settings
3. Personal access tokens → Tokens (classic)
4. Click "Generate new token"
5. Give it a name, set expiry, check the `repo` scope
6. Click Generate and copy it immediately (shown only once)

### Rules
- Never commit .env to git (it's already in .gitignore)
- If your token leaks, revoke it immediately from GitHub settings

---

## How mAin.py Works

It runs through every GitHubClient method one by one:

1. validate_token        → checks your token is valid
2. is_collaborator       → checks if user is already on the repo
3. add_collaborator      → invites the user with a permission level
4. is_collaborator       → confirms the add worked
5. list_collaborators    → prints everyone on the repo
6. add_collaborator      → tests an invalid permission (shows error handling)
7. remove_collaborator   → removes the user
8. is_collaborator       → confirms removal worked

### Before running, edit these 3 lines at the top of mAin.py:

```
REPO         = "my-test-repo"        # a repo you own
COLLABORATOR = "some-github-user"    # github username to test with
PERMISSION   = "push"                # pull / triage / push / maintain / admin
```

### Permission levels

- pull     → read only
- triage   → read + manage issues, no code write
- push     → read + write (good for contributors)
- maintain → push + repo settings, no admin
- admin    → full control

---

## Logging

Logs go to both terminal and file at the same time.
File location: logs/app.log

To watch logs live in a second terminal:
```
tail -f logs/app.log
```

---

## Quickstart

```bash
# 1. create and activate venv
python3 -m venv venv
source venv/bin/activate

# 2. install dependencies
pip install -r requirements.txt

# 3. create .env file with your token and owner

# 4. edit REPO and COLLABORATOR in mAin.py

# 5. run
python mAin.py
```