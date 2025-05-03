"""Custom exceptions for user-related application errors.

This module defines domain-specific exceptions to be raised
when certain business rules are violated, such as duplicate email registration.
"""


class ExistingEmailError(Exception):
    """Exception raised when attempting to create a user with an email that already exists.

    This is typically caught in the service or API layer to return a 400 Bad Request response.
    """

    def __init__(self):
        super().__init__("User with this email already exists")
