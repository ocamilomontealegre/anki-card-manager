from abc import ABC, abstractmethod


class HealthService(ABC):
    """Abstract base class for health service implementations."""

    @abstractmethod
    def check(self) -> str:
        """Perform a health check and return a HealthMessage instance."""
        pass
