"""Issue model."""

from typing import List, Optional

from pydantic import BaseModel


class Issue(BaseModel):
    """A model representing a GitHub issue."""

    title: str
    body: str
    labels: Optional[List[str]] = []
    assignees: Optional[List[str]] = []
