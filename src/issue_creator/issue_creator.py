"""IssueCreator."""

import requests

from issue_creator.exceptions import IssueCreationError
from issue_creator.models.issue import Issue


class IssueCreator:
    """A class to create GitHub issues using the GitHub REST API."""

    def __init__(self, token: str, repo_owner: str, repo_name: str):
        """Initializes the IssueCreator instance.

        Args:
            token (str): GitHub personal access token.
            repo_owner (str): Repository owner's username.
            repo_name (str): Name of the repository.
        """
        if not token:
            raise ValueError("GitHub token is required.")
        if not repo_owner:
            raise ValueError("Repository owner is required.")
        if not repo_name:
            raise ValueError("Repository name is required.")

        self._token = token
        self._repo_owner = repo_owner
        self._repo_name = repo_name

        self._session = requests.Session()
        self._session.headers.update(
            {"Authorization": f"token {self._token}", "Accept": "application/vnd.github.v3+json"}
        )

    def create(self, issue: Issue, timeout: int = 10) -> None:
        """Creates a new GitHub issue.

        Args:
            issue (Issue): An Issue object containing the issue details.
            timeout (int): Timeout for the HTTP request in seconds.

        Raises:
            IssueCreationError: If the issue creation fails.
        """
        url = f"https://api.github.com/repos/{self._repo_owner}/{self._repo_name}/issues"
        data = issue.model_dump()

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

        print(f"Issue created successfully! URL: {response.json()['html_url']}")
