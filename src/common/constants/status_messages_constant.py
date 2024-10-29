from typing import Dict

STATUS_MESSAGES: Dict[str, str] = {
    200: "Request completed successfully",
    201: "Resource successfully created",
    202: "Request accepted for processing, but not yet complete",
    204: "Request processed, but no content to return",
    400: "Invalid request format or parameters",
    401: "Authentication required or failed",
    403: "You don`t have permission to access this resource",
    404: "The requested resource was not found",
    405: "HTTP method is not supported for the requested resource",
    409: "Conflict with the current state of the resource",
    422: "Request is well-formed but contains semantic errors",
    500: "An unexpected error occurred on the server",
    502: "Server received an invalid response from an upstream server",
    503: "The server is currently unable to handle the request",
    504: "The server did not receive a timely response from an upstream server",
}
