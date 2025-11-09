"""Custom exceptions for CloudMind AI."""


class CloudMindError(Exception):
    """Base exception for CloudMind AI."""
    pass


class ConfigurationError(CloudMindError):
    """Raised when configuration is invalid or missing."""
    pass


class ProviderError(CloudMindError):
    """Raised when cloud provider operations fail."""
    pass


class AuthenticationError(CloudMindError):
    """Raised when authentication fails."""
    pass


class ResourceNotFoundError(CloudMindError):
    """Raised when a resource cannot be found."""
    pass


class OptimizationError(CloudMindError):
    """Raised when optimization operations fail."""
    pass


class AIServiceError(CloudMindError):
    """Raised when AI service operations fail."""
    pass
