from health.models.health_message_model import HealthMessage
from health.constants.all_constants import HEALTH_MESSAGE


class HealthService:
    def check(self) -> HealthMessage:
        """Return app status"""
        return HEALTH_MESSAGE
