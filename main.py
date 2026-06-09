"""
main.py
Demo script that calls every feature exposed by GitHubClient.

Usage:
    python main.py

Set the two environment variables before running:
    export GITHUB_TOKEN="ghp_..."
    export GITHUB_OWNER="your-username-or-org"

You can also hard-code REPO / COLLABORATOR below for quick testing.
"""

import os
import sys
import logging
from dotenv import load_dotenv
load_dotenv()
# Make sure Python can find the src/ package when running from the project root.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from github_client import GitHubClient

# ── Logging setup ──────────────────────────────────────────────────────────────
os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
    handlers=[
        logging.FileHandler("logs/app.log"),      # saves to file
        logging.StreamHandler()                    # still prints to terminal
    ]
)
log = logging.getLogger("main")

# ── Configuration ──────────────────────────────────────────────────────────────
TOKEN = os.getenv("GITHUB_TOKEN", "")          # required
OWNER = os.getenv("GITHUB_OWNER", "")          # required

REPO         = "TEST-"                  # <-- change to a real repo
COLLABORATOR = "DVNSKA"          # <-- change to a real GitHub user
PERMISSION   = "admin"                          # pull | triage | push | maintain | admin


def main() -> None:
    # ── 0. Basic config check ──────────────────────────────────────────────────
    if not TOKEN or not OWNER:
        sys.exit(
            "ERROR: Set GITHUB_TOKEN and GITHUB_OWNER environment variables first."
        )

    client = GitHubClient(token=TOKEN, owner=OWNER)

    # ── 1. validate_token ──────────────────────────────────────────────────────
    log.info("=== 1. validate_token ===")
    ok = client.validate_token()
    if not ok:
        sys.exit("Token is invalid or lacks required scopes — aborting.")
    print(f"Token valid: {ok}\n")

    # ── 2. is_collaborator (before adding) ────────────────────────────────────
    log.info("=== 2. is_collaborator (before add) ===")
    already = client.is_collaborator(REPO, COLLABORATOR)
    print(f"Is '{COLLABORATOR}' already a collaborator on '{REPO}'? {already}\n")

    # ── 3. add_collaborator ───────────────────────────────────────────────────
    log.info("=== 3. add_collaborator ===")
    result = client.add_collaborator(REPO, COLLABORATOR, permission=PERMISSION)
    if result:
        print(f"Invitation / update response: {result}\n")
    else:
        print("add_collaborator returned empty body (user already had that role).\n")

    # ── 4. is_collaborator (after adding) ────────────────────────────────────
    log.info("=== 4. is_collaborator (after add) ===")
    now_collab = client.is_collaborator(REPO, COLLABORATOR)
    print(f"Is '{COLLABORATOR}' a collaborator now? {now_collab}\n")

    # ── 5. list_collaborators ─────────────────────────────────────────────────
    log.info("=== 5. list_collaborators ===")
    collaborators = client.list_collaborators(REPO)
    print(f"Collaborators on '{REPO}' ({len(collaborators)} total):")
    for c in collaborators:
        print(f"  • {c.get('login')} — permissions: {c.get('permissions')}")
    print()

    # ── 6. add_collaborator with an invalid permission (error handling demo) ──
    # log.info("=== 6. add_collaborator with invalid permission ===")
    # try:
    #     client.add_collaborator(REPO, COLLABORATOR, permission="superadmin")
    # except ValueError as exc:
    #     print(f"Expected ValueError caught: {exc}\n")

    # # ── 7. remove_collaborator ────────────────────────────────────────────────
    # log.info("=== 7. remove_collaborator ===")
    # client.remove_collaborator(REPO, COLLABORATOR)
    # print(f"'{COLLABORATOR}' removed from '{REPO}'.\n")

    # # ── 8. is_collaborator (after removal) ───────────────────────────────────
    # log.info("=== 8. is_collaborator (after remove) ===")
    # gone = client.is_collaborator(REPO, COLLABORATOR)
    # print(f"Is '{COLLABORATOR}' still a collaborator? {gone}\n")

    print("=== All GitHubClient features exercised successfully ===")


if __name__ == "__main__":
    main()