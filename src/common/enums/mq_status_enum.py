from enum import Enum


class MqTaskStatus(str, Enum):
    PENDING = "pending"
    STARTED = "started"
    RETRY = "retry"
    FAILURE = "failure"
    SUCCESS = "success"
    REVOKED = "revoked"
