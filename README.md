# GitHub Permission Manager

A professional CLI tool to **grant and revoke GitHub repository access** for users identified by their email address.

---

## Project Structure

```
github_permission_manager/
├── config/
│   ├── .env.example        ← copy to .env and fill in your token
│   ├── users.yaml          ← email → GitHub username mapping
│   └── repos.yaml          ← list of repos to manage
├── src/
│   ├── __init__.py
│   ├── settings.py         ← config loader
│   ├── github_client.py    ← GitHub REST API wrapper
│   └── permission_manager.py ← core grant/revoke logic
├── logs/                   ← auto-created, gitignored
├── cli.py                  ← CLI entry point
├── requirements.txt
└── .gitignore
```

---

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Create your `.env` file

```bash
cp config/.env.example config/.env
```

Edit `config/.env`:

```env
GITHUB_TOKEN=ghp_your_token_here
GITHUB_OWNER=your_github_username_or_org
LOG_LEVEL=INFO
```

> **Token scopes required:** `repo` + `admin:org` (for org repos)

### 3. Add your users

Edit `config/users.yaml`:

```yaml
users:
  alice@example.com: alice-gh-username
  bob@company.com:   bob-gh-username
```

### 4. Add your repos

Edit `config/repos.yaml`:

```yaml
repos:
  - my-private-repo
  - backend-service
```

---

## CLI Usage

### Validate your token
```bash
python cli.py validate
```

### Grant access (all repos)
```bash
python cli.py grant alice@example.com
```

### Grant access (specific repos)
```bash
python cli.py grant alice@example.com --repos my-private-repo backend-service
```

### Grant with a specific permission level
```bash
python cli.py grant alice@example.com --permission push
```
Permission levels: `pull` | `triage` | `push` | `maintain` | `admin`

### Revoke access (all repos)
```bash
python cli.py revoke alice@example.com
```

### Revoke access (specific repos)
```bash
python cli.py revoke alice@example.com --repos my-private-repo
```

### Bulk grant (multiple users)
```bash
python cli.py grant-bulk alice@example.com,bob@company.com
```

### Bulk revoke (multiple users)
```bash
python cli.py revoke-bulk alice@example.com,bob@company.com
```

### List collaborators on a repo
```bash
python cli.py list-collaborators my-private-repo
```

---

## Example Output

```
────────────────────────────────────────────────────────────
  Summary: 3 succeeded, 0 failed
────────────────────────────────────────────────────────────
  ✓  [GRANT]  alice@example.com (alice-gh) → my-private-repo
  ✓  [GRANT]  alice@example.com (alice-gh) → backend-service
  ✓  [GRANT]  alice@example.com (alice-gh) → another-project
```

---

## Security Notes

- **Never commit `config/.env`** — it is listed in `.gitignore`
- Rotate your GitHub token regularly
- Use the **minimum permission** level needed for each user
