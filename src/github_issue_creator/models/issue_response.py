"""Issue response model."""

from typing import Optional

from pydantic import BaseModel


class IssueResponse(BaseModel):
    """Represents the response data for a successfully created issue in a repository.

    Attributes:
        repository_url (str): The URL of the repository where the issue was created.
        issue_url (str): The URL of the created issue.
        issue_id (int): The unique identifier of the issue.
        issue_number (int): The number of the issue in the repository.
        issue_title (str): The title of the issue.
        issue_state (str): The current state of the issue (e.g., 'open', 'closed').
        created_at (str): The timestamp when the issue was created (in ISO 8601 format).
        author (Optional[str]): The username of the user who created the issue, if available.
    """

    repository_url: str
    issue_url: str
    issue_id: int
    issue_number: int
    issue_title: str
    issue_state: str
    created_at: str
    author: Optional[str] = None
