DATABASE_ERROR = 'Ошибка при обработке данных'


class DomainException(Exception):
    """Доменные исключения."""


class NotFoundException(DomainException):
    """Исключение вызываемое если сущность не найдена."""


class IncorrectDataException(DomainException):
    """Исключение вызываемое если переданная информация недопустима для обработки."""


class DatabaseException(DomainException):
    """Ошибка базы данных."""
