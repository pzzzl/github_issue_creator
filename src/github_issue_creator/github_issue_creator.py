"""IssueCreator."""

from typing import Any

import requests

from github_issue_creator.exceptions import IssueCreationError
from github_issue_creator.models.issue import Issue
from github_issue_creator.models.issue_response import IssueResponse


class IssueCreator:
    """A class to create GitHub issues using the GitHub REST API."""

    def __init__(self, token: str, repo_owner: str, repo_name: str, proxy: dict[str, str] = None) -> None:
        """Initializes the IssueCreator instance.

        Args:
            token (str): GitHub personal access token.
            repo_owner (str): Repository owner's username.
            repo_name (str): Name of the repository.
            proxy (dict[str, str], optional): Proxy settings for the HTTP session. Defaults to None.

        Raises:
            ValueError: If token, repo_owner, or repo_name is not provided.
            ValueError: If proxy is not a dictionary.
        """
        if not token:
            raise ValueError("GitHub token is required.")
        if not repo_owner:
            raise ValueError("Repository owner is required.")
        if not repo_name:
            raise ValueError("Repository name is required.")

        self._token: str = token
        self._repo_owner: str = repo_owner
        self._repo_name: str = repo_name
        self._proxy: dict[str, str] = proxy

        if self._proxy:
            if self._proxy and not isinstance(self._proxy, dict):
                raise ValueError("Proxy must be a dictionary")

            self._session: requests.Session = requests.Session()
            self._session.proxies.update(self._proxy)
        else:
            self._session: requests.Session = requests.Session()

        self._session.headers.update(
            {"Authorization": f"token {self._token}", "Accept": "application/vnd.github.v3+json"}
        )

    def create(self, issue: Issue, timeout: int = 10) -> IssueResponse:
        """Creates a new GitHub issue and returns useful information.

        Args:
            issue (Issue): An Issue object containing the issue details.
            timeout (int): Timeout for the HTTP request in seconds.

        Returns:
            IssueResponse: Information about the created issue.

        Raises:
            IssueCreationError: If the issue creation fails.
        """
        url: str = f"https://api.github.com/repos/{self._repo_owner}/{self._repo_name}/issues"
        data: dict[str, Any] = issue.model_dump()
        response: requests.Response | None = None

        try:
            response = self._session.post(url, json=data, timeout=timeout)
            response.raise_for_status()
        except requests.HTTPError:
            raise IssueCreationError(
                message="HTTP error occurred while creating the issue.",
                status_code=response.status_code,
                response_text=response.text,
            )
        except requests.RequestException as e:
            raise IssueCreationError(message=f"Request failed: {str(e)}")

        if response.status_code != 201:
            raise IssueCreationError(
                message="Failed to create issue.", status_code=response.status_code, response_text=response.text
            )

        response_data: Any = response.json()

        return IssueResponse(
            repository_url=f"https://github.com/{self._repo_owner}/{self._repo_name}",
            issue_url=response_data.get("html_url"),
            issue_id=response_data.get("id"),
            issue_number=response_data.get("number"),
            issue_title=response_data.get("title"),
            issue_state=response_data.get("state"),
            created_at=response_data.get("created_at"),
            author=response_data.get("user", {}).get("login"),
        )
