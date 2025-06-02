"""Custom exceptions."""


class IssueCreationError(Exception):
    """Custom exception raised when an issue creation fails."""

    def __init__(self, message: str, status_code: int = None, response_text: str = None):
        """Initialize an IssueCreationError instance.

        :param message: The error message to display.
        :param status_code: (Optional) The HTTP status code associated with the error.
        :param response_text: (Optional) The response text from the HTTP request.
        """
        self.status_code = status_code
        self.response_text = response_text
        super().__init__(message)

    def __str__(self):
        """Return a string representation of the IssueCreationError.

        Combines the error message, optional status code, and optional response text
        into a single formatted string for display or logging.
        """
        base_msg = f"IssueCreationError: {self.args[0]}"
        if self.status_code:
            base_msg += f" | Status code: {self.status_code}"
        if self.response_text:
            base_msg += f" | Response: {self.response_text}"
        return base_msg
