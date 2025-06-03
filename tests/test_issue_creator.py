"""Test IssueCreator."""

from unittest.mock import MagicMock, patch

import pytest
import requests

from src.github_issue_creator import Issue, IssueCreationError, IssueCreator


def test_create_issue_success() -> None:
    """Test successful creation of an issue.

    This test verifies that when a valid Issue object is passed to the IssueCreator,
    and a mock 201 response is returned from the GitHub API, the IssueCreator.create()
    method returns an IssueResponse object with the correct data.
    """
    issue = Issue(title="Test", body="This is a test")
    creator = IssueCreator("fake_token", "fake_owner", "fake_repo")

    mock_response = MagicMock()
    mock_response.status_code = 201
    mock_response.json.return_value = {
        "id": 123456,
        "number": 1,
        "title": "Test",
        "state": "open",
        "created_at": "2024-06-01T00:00:00Z",
        "html_url": "https://github.com/fake_owner/fake_repo/issues/1",
        "user": {"login": "test_user"},
    }

    with patch.object(creator._session, "post", return_value=mock_response) as mock_post:
        result = creator.create(issue)

        mock_post.assert_called_once()
        assert result.__class__.__name__ == "IssueResponse"
        assert result.__class__.__module__ == "github_issue_creator.models.issue_response"
        assert result.issue_url == "https://github.com/fake_owner/fake_repo/issues/1"
        assert result.issue_id == 123456
        assert result.issue_title == "Test"
        assert result.issue_state == "open"
        assert result.author == "test_user"
        assert result.repository_url == "https://github.com/fake_owner/fake_repo"


def test_create_issue_http_error() -> None:
    """Test HTTP error handling during issue creation.

    This test simulates a scenario where the GitHub API returns an HTTP error (400 status).
    It verifies that the IssueCreator.create() method raises an IssueCreationError with
    the correct error message, status code, and response text.
    """
    issue = Issue(title="Test", body="This is a test")
    creator = IssueCreator("fake_token", "fake_owner", "fake_repo")

    mock_response = MagicMock()
    mock_response.status_code = 400
    mock_response.text = "Bad Request"
    mock_response.raise_for_status.side_effect = requests.HTTPError()

    with patch.object(creator._session, "post", return_value=mock_response):
        with pytest.raises(IssueCreationError) as exc_info:
            creator.create(issue)
        assert "HTTP error occurred while creating the issue." in str(exc_info.value)
        assert exc_info.value.status_code == 400
        assert "Bad Request" in exc_info.value.response_text


def test_create_issue_request_exception() -> None:
    """Test request exception handling during issue creation.

    This test simulates a scenario where a network error (RequestException) occurs during
    the HTTP request. It verifies that the IssueCreator.create() method raises an IssueCreationError
    with the appropriate error message.
    """
    issue = Issue(title="Test", body="This is a test")
    creator = IssueCreator("fake_token", "fake_owner", "fake_repo")

    with patch.object(creator._session, "post", side_effect=requests.RequestException("Network Error")):
        with pytest.raises(IssueCreationError) as exc_info:
            creator.create(issue)
        assert "Request failed: Network Error" in str(exc_info.value)


def test_create_issue_status_not_201() -> None:
    """Test unexpected status code handling during issue creation.

    This test simulates a scenario where the GitHub API returns a non-201 status code (e.g., 200 OK).
    It verifies that the IssueCreator.create() method raises an IssueCreationError with
    the correct status code and response text.
    """
    issue = Issue(title="Test", body="This is a test")
    creator = IssueCreator("fake_token", "fake_owner", "fake_repo")

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = "OK"
    mock_response.raise_for_status.return_value = None

    with patch.object(creator._session, "post", return_value=mock_response):
        with pytest.raises(IssueCreationError) as exc_info:
            creator.create(issue)
        assert "Failed to create issue." in str(exc_info.value)
        assert exc_info.value.status_code == 200
        assert "OK" in exc_info.value.response_text


def test_create_issue_success_with_proxy() -> None:
    """Test successful creation of an issue with a proxy.

    This test verifies that when a valid Issue object is passed to the IssueCreator,
    and a mock 201 response is returned from the GitHub API, the IssueCreator.create()
    method returns an IssueResponse object with the correct data, even when using a proxy.
    """
    proxy = {"http": "http://proxy.example.com", "https": "http://proxy.example.com"}

    issue = Issue(title="Test", body="This is a test")
    creator = IssueCreator("fake_token", "fake_owner", "fake_repo", proxy=proxy)

    mock_response = MagicMock()
    mock_response.status_code = 201
    mock_response.json.return_value = {
        "id": 123456,
        "number": 1,
        "title": "Test",
        "state": "open",
        "created_at": "2024-06-01T00:00:00Z",
        "html_url": "https://github.com/fake_owner/fake_repo/issues/1",
        "user": {"login": "test_user"},
    }

    with patch.object(creator._session, "post", return_value=mock_response) as mock_post:
        result = creator.create(issue)

        mock_post.assert_called_once()
        assert result.__class__.__name__ == "IssueResponse"
        assert result.__class__.__module__ == "github_issue_creator.models.issue_response"
        assert result.issue_url == "https://github.com/fake_owner/fake_repo/issues/1"
        assert result.issue_id == 123456
        assert result.issue_title == "Test"
        assert result.issue_state == "open"
        assert result.author == "test_user"
        assert result.repository_url == "https://github.com/fake_owner/fake_repo"

def test_create_issue_with_invalid_proxy() -> None:
    """Test issue creation with an invalid proxy.

    This test verifies that when an invalid proxy is provided, the IssueCreator.create()
    method raises an IssueCreationError with the appropriate error message.
    """
    with pytest.raises(ValueError, match="Proxy must be a dictionary"):
        IssueCreator("fake_token", "fake_owner", "fake_repo", proxy="invalid_proxy")
