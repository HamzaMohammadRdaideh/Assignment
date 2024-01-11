from core.constans.user import UserConstants


class UserDoesNotExist(Exception):
    """
    while using try except you should follow the following style
    try:
        try_dody
    except {{specify_exception_class}} as e: # e is a variable will contain the error message of the exception
        exception_body
    """

    def __init__(self, message_key=UserConstants.USER_DOES_NOT_EXIST_ERROR):
        self.message_key = message_key
        self.status = 404

        super().__init__(self.message_key, self.status)


class InvalidAuthentication(Exception):
    def __init__(self, message_key=UserConstants.INVALID_AUTHENTICATION):
        self.message_key = message_key
        self.status = 401

        super().__init__(self.message_key, self.status)


class UserCreateError(Exception):
    def __init__(self, message_key=UserConstants.USER_CREATION_FAILED_ERROR):
        self.message_key = message_key
        self.status = 401

        super().__init__(self.message_key, self.status)


class UserInfoDoesNotExist(Exception):
    """
    while using try except you should follow the following style
    try:
        try_dody
    except {{specify_exception_class}} as e: # e is a variable will contain the error message of the exception
        exception_body
    """

    def __init__(self, message_key=UserConstants.INFO_NOT_FOUND):
        self.message_key = message_key
        self.status = 404
        super().__init__(self.message_key, self.status)


class UserAlreadyExist(Exception):
    """
    while using try except you should follow the following style
    try:
        try_dody
    except {{specify_exception_class}} as e: # e is a variable will contain the error message of the exception
        exception_body
    """

    def __init__(self, message_key=UserConstants.USER_ALREADY_EXIST_ERROR):
        self.message_key = message_key
        self.status = 404

        super().__init__(self.message_key, self.status)


class InvalidEmail(Exception):
    def __init__(self, language):
        self.message_key = UserConstants.INVALID_EMAIL.get(language)
        self.status = 400
        super().__init__(self.message_key, self.status)
