"""Exceptions for felt-python"""


class AuthError(Exception):
    """Class for authentication errors"""


class ExportFailedError(Exception):
    """A layer export failed"""

    def __init__(self, poll_endpoint: str):
        super().__init__(f"The export failed: {poll_endpoint}")
        self.poll_endpoint = poll_endpoint


class ExportTimeoutError(Exception):
    """A layer export didn't finish in time; poll `poll_endpoint` to keep waiting"""

    def __init__(self, poll_endpoint: str, timeout: float):
        super().__init__(
            f"The export didn't finish within {timeout:g} seconds. "
            f"Poll {poll_endpoint} to keep waiting."
        )
        self.poll_endpoint = poll_endpoint
        self.timeout = timeout
