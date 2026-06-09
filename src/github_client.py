"""
src/github_client.py
Thin wrapper around the GitHub REST API (collaborator endpoints).
All HTTP logic lives here so the rest of the code stays clean.
"""

import logging
import requests

log = logging.getLogger("github_pm.client")

GITHUB_API = "https://api.github.com"

# Valid GitHub collaborator permission levels
VALID_PERMISSIONS = {"pull", "triage", "push", "maintain", "admin"}


class GitHubClient:
    """
    Authenticated GitHub API client.

    Args:
        token: GitHub Personal Access Token (needs repo + admin scopes).
        owner: GitHub username or org that owns the repositories.
    """

    def __init__(self, token: str, owner: str) -> None:
        self.owner = owner
        self._session = requests.Session()
        self._session.headers.update(
            {
                "Authorization": f"Bearer {token}",
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28",
            }
        )

    # ── Internal helpers ───────────────────────────────────────────────────────

    def _url(self, *parts: str) -> str:
        return "/".join([GITHUB_API] + list(parts))

    def _handle_response(self, resp: requests.Response, *, action: str) -> dict:
        """Log and raise on non-2xx responses; return parsed JSON otherwise."""
        if resp.ok:
            return resp.json() if resp.content else {}
        log.error(
            "%s failed — HTTP %s: %s",
            action,
            resp.status_code,
            resp.text[:300],
        )
        resp.raise_for_status()

    # ── Public API ─────────────────────────────────────────────────────────────

    def add_collaborator(
        self, repo: str, username: str, permission: str = "admin"
    ) -> dict:
        """
        Invite / update a collaborator on a repository.

        Returns the API response dict (invitation object or empty dict if
        the user is already a collaborator with the same role).
        """
        if permission not in VALID_PERMISSIONS:
            raise ValueError(
                f"Invalid permission '{permission}'. "
                f"Choose from: {sorted(VALID_PERMISSIONS)}"
            )

        url  = self._url("repos", self.owner, repo, "collaborators", username)
        resp = self._session.put(url, json={"permission": permission})

        # 201 = invitation sent, 204 = already a collaborator (updated)
        if resp.status_code in (201, 204):
            log.debug("add_collaborator succeeded for %s on %s", username, repo)
            return resp.json() if resp.content else {}

        return self._handle_response(resp, action=f"add_collaborator({username}, {repo})")

    def remove_collaborator(self, repo: str, username: str) -> None:
        """Remove a collaborator from a repository."""
        url  = self._url("repos", self.owner, repo, "collaborators", username)
        resp = self._session.delete(url)

        if resp.status_code == 204:
            log.debug("remove_collaborator succeeded for %s on %s", username, repo)
            return

        self._handle_response(resp, action=f"remove_collaborator({username}, {repo})")

    def is_collaborator(self, repo: str, username: str) -> bool:
        """Return True if the user is already a collaborator on the repo."""
        url  = self._url("repos", self.owner, repo, "collaborators", username)
        resp = self._session.get(url)
        return resp.status_code == 204

    def list_collaborators(self, repo: str) -> list[dict]:
        """Return a list of all collaborators on a repository."""
        url  = self._url("repos", self.owner, repo, "collaborators")
        resp = self._session.get(url)
        return self._handle_response(resp, action=f"list_collaborators({repo})")

    def validate_token(self) -> bool:
        """Quick check that the token is valid and has the right scopes."""
        resp = self._session.get(self._url("user"))
        if resp.ok:
            login = resp.json().get("login", "?")
            log.info("Authenticated as GitHub user: %s", login)
            return True
        log.error("Token validation failed — HTTP %s", resp.status_code)
        return False
