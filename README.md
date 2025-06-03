
<h1 align="center">GitHub Issue Creator</h1>

<p align="center">
<img src="https://img.shields.io/badge/version-0.2.0-blue">
<img src="https://img.shields.io/badge/tests-passing-green">
</p>

<p align="center">
<img src="https://user-images.githubusercontent.com/22751162/122999697-38f24280-d374-11eb-970b-f0156d026d88.png">
</p>

<p align="center">
A Python library for creating GitHub issues programmatically using the GitHub REST API.
</p>

## Summary

- [Installation](#installation)
- [Usage](#usage)
  - [Import the necessary modules](#import-the-necessary-modules)
  - [Initialize IssueCreator](#initialize-issuecreator)
  - [Create an Issue object](#create-an-issue-object)
  - [Create the issue on GitHub](#create-the-issue-on-github)
- [Exceptions](#Exceptions)
- [Configuration Notes](#configuration-notes)
- [Contributors](#contributors)


## Installation

First, install the library via pip (if it's not already installed):

```Python
pip install github-issue-creator
```

## Usage

### Import the necessary modules

```Python
from github_issue_creator import IssueCreator, Issue, IssueCreationError
```

### Initialize IssueCreator

You'll need a GitHub Personal Access Token (PAT), the repository owner's username, and the repository name.

```Python
token = "your_github_token"
repo_owner = "your_github_username"
repo_name = "your_repository_name"

creator = IssueCreator(token, repo_owner, repo_name)
```

### Create an Issue object

The `Issue` model should contain the issue details such as title, body, assignees, labels, etc.

```Python
issue = Issue(
    title="Sample Issue Title",
    body="This is the description of the issue.",
    assignees=["octocat"],  # Optional: list of GitHub usernames to assign
    labels=["bug", "help wanted"]  # Optional: list of labels
)
```

### Create the issue on GitHub

Call the `create` method to post the issue.

```Python
try:
    creator.create(issue)
except IssueCreationError as e:
    print(f"Failed to create issue: {e}")
    if e.status_code:
        print(f"Status Code: {e.status_code}")
        print(f"Response: {e.response_text}")
```

If successful, it will return an `IssueResponse` object containing details of the created issue, including the issue URL, repository URL, issue ID, number, title, state, creation date, and the author's username.

For example, it may look like this:

```Python
IssueResponse(
    repository_url="https://github.com/fake_owner/fake_repo",
    issue_url="https://github.com/fake_owner/fake_repo/issues/1",
    issue_id=123456,
    issue_number=1,
    issue_title="Test",
    issue_state="open",
    created_at="2024-06-01T00:00:00Z",
    author="test_user"
)
```

## Exceptions

- `IssueCreationError`: Raised if the issue creation fails due to an HTTP error or a request exception.

## Configuration Notes

- Make sure your GitHub token has the correct permissions to create issues in the repository.
- The `Issue` model should be defined based on the GitHub API's expected fields (check the library's `models/issue.py` for the schema).

## Contributors

Thanks to the following people who have contributed to this project:

- [pzzzl](https://github.com/pzzzl) - Maintainer
- [BrunoSantanaS](https://github.com/BrunoSantanaS)

Feel free to open a pull request or report any issues you encounter. Your contributions are always welcome!
