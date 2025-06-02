"""Test IssueCreator."""

from unittest.mock import MagicMock, patch

import pytest
import requests

from src.issue_creator import Issue, IssueCreationError, IssueCreator


def test_create_issue_success() -> None:
    """Test that the IssueCreator creates an issue successfully.

    Mocks a 201 Created response from the GitHub API and checks that
    the POST request is made exactly once.
    """
    issue = Issue(title="Test", body="This is a test")
    creator = IssueCreator("fake_token", "fake_owner", "fake_repo")

    mock_response = MagicMock()
    mock_response.status_code = 201
    mock_response.json.return_value = {"html_url": "https://github.com/fake_owner/fake_repo/issues/1"}

    with patch.object(creator._session, "post", return_value=mock_response) as mock_post:
        creator.create(issue)
        mock_post.assert_called_once()


def test_create_issue_http_error() -> None:
    """Test that IssueCreator raises an IssueCreationError when an HTTP error occurs.

    Simulates a 400 Bad Request response and checks that the correct error is raised,
    including status code and response text.
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
    """Test that IssueCreator raises an IssueCreationError when a request exception occurs.

    Simulates a network error (requests.RequestException) and checks that the error
    message includes the exception detail.
    """
    issue = Issue(title="Test", body="This is a test")
    creator = IssueCreator("fake_token", "fake_owner", "fake_repo")

    with patch.object(creator._session, "post", side_effect=requests.RequestException("Network Error")):
        with pytest.raises(IssueCreationError) as exc_info:
            creator.create(issue)
        assert "Request failed: Network Error" in str(exc_info.value)


def test_create_issue_status_not_201() -> None:
    """Test that IssueCreator raises an IssueCreationError if the response status code is not 201.

    Simulates a response with status code 200 and checks that the correct error
    is raised, including status code and response text.
    """
    issue = Issue(title="Test", body="This is a test")
    creator = IssueCreator("fake_token", "fake_owner", "fake_repo")

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = "OK"
    mock_response.raise_for_status.return_value = None  # No exception raised

    with patch.object(creator._session, "post", return_value=mock_response):
        with pytest.raises(IssueCreationError) as exc_info:
            creator.create(issue)
        assert "Failed to create issue." in str(exc_info.value)
        assert exc_info.value.status_code == 200
        assert "OK" in exc_info.value.response_text


def test_create_issue_prints_success_url(capfd: pytest.CaptureFixture[str]) -> None:
    """Test that IssueCreator prints the URL of the created issue on success.

    Captures the standard output and checks that the success message with the correct
    URL is printed.
    """
    issue = Issue(title="Test", body="This is a test")
    creator = IssueCreator("fake_token", "fake_owner", "fake_repo")

    mock_response = MagicMock()
    mock_response.status_code = 201
    mock_response.json.return_value = {"html_url": "https://github.com/fake_owner/fake_repo/issues/1"}

    with patch.object(creator._session, "post", return_value=mock_response):
        creator.create(issue)

    out, _ = capfd.readouterr()
    assert "Issue created successfully! URL: https://github.com/fake_owner/fake_repo/issues/1" in out
