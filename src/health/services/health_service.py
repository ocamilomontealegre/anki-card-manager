from health.constants import HEALTH_MESSAGE
from health.models.abstracts.health_service_abstract import HealthService


class HealthServiceImpl(HealthService):
    def check(self) -> str:
        """Return app status"""
        return HEALTH_MESSAGE
