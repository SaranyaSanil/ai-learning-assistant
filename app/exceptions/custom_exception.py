class DuplicateResourceError(Exception):
    pass


class DatabaseError(Exception):
    pass


class ServiceError(Exception):
    pass


class BadRequest(Exception):
    pass


class UnauthorizedError(Exception):
    pass

class ResourceNotFoundError(Exception):
    pass

class ExpiredSignatureError(Exception):
    pass

class InvalidTokenError(Exception):
    pass