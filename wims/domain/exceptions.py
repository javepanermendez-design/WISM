"""Business errors exposed by the application."""


class WimsError(Exception):
    """Base error with a user-facing message."""
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class InsufficientStockError(WimsError):
    """Raised when a release exceeds available stock."""


class InvalidTransitionError(WimsError):
    """Raised when an order state transition is not allowed."""


class DuplicateSkuError(WimsError):
    """Raised when a product SKU is already used."""


class ValidationError(WimsError):
    """Raised when submitted data is invalid."""


class AuthenticationError(WimsError):
    """Raised when credentials are invalid."""
