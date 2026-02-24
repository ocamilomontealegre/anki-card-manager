from common.constants import STATUS_MESSAGES


def get_status_message(status_code: int) -> str:
    return STATUS_MESSAGES.get(status_code, "Unknown status code")
