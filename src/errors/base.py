from typing import Any

__all__ = (
    "BaseError",
    "UnprocessableError",
    "NotFoundError",
    "DatabaseError",
)


class BaseError(Exception):
    def __init__(
            self,
            *_: tuple[Any],
            message: str = "",
    ) -> None:
        self.message: str = message

        super().__init__(message)


class UnprocessableError(BaseError):
    def __init__(
            self, *_: tuple[Any], message: str = "Validation error"
    ) -> None:
        super().__init__(
            message=message,
        )


class NotFoundError(BaseError):
    def __init__(self, *_: tuple[Any], message: str = "Not found") -> None:
        super().__init__(
            message=message
        )


class DatabaseError(BaseError):
    def __init__(
            self, *_: tuple[Any], message: str = "Database error"
    ) -> None:
        super().__init__(
            message=message
        )
