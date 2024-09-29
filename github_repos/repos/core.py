from typing import NewType

ErrorMessage = NewType("ErrorMessage", dict[str, str])
GithubData = NewType("GithubData", list[dict[str, str]])
TIMEOUT: int = 4