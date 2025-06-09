from health.models.abstracts.health_service_abstract import HealthService
from health.constants.all_constants import HEALTH_MESSAGE


class HealthServiceImpl(HealthService):

    def check(self) -> str:
        """Return app status"""
        return HEALTH_MESSAGE
