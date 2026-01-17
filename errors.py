class AppError(Exception):
    status_code = 400
    message = "Application error"

    # pass custom error message
    def __init__(self, message=None):
        if message:
            self.message = message

    def to_dict(self):
        return {
            "error": self.message,
            "code": self.status_code
        }


class ConflictError(AppError):
    status_code = 409
    message = "Conflict"


class AuthError(AppError):
    status_code = 401
    message = "Unauthorized"


class NotFoundError(AppError):
    status_code = 404
    message = "Not found"


class InternalError(AppError):
    status_code = 500
    message = "Internal server error"