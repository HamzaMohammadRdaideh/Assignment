from core.constans.profile import ProfileConstants


class InvalidGender(Exception):
    """
    while using try except you should follow the following style
    try:
        try_dody
    except {{specify_exception_class}} as e: # e is a variable will contain the error message of the exception
        exception_body
    """

    def __init__(self, message_key=ProfileConstants.INVALID_GENDER):
        self.message_key = message_key
        self.status = 404

        super().__init__(self.message_key, self.status)


class InvalidSalary(Exception):
    """
    while using try except you should follow the following style
    try:
        try_dody
    except {{specify_exception_class}} as e: # e is a variable will contain the error message of the exception
        exception_body
    """

    def __init__(self, message_key=ProfileConstants.INVALID_SALARY):
        self.message_key = message_key
        self.status = 404

        super().__init__(self.message_key, self.status)


class InvalidCareerLevel(Exception):
    """
    while using try except you should follow the following style
    try:
        try_dody
    except {{specify_exception_class}} as e: # e is a variable will contain the error message of the exception
        exception_body
    """

    def __init__(self, message_key=ProfileConstants.INVALID_CAREER_LEVEL):
        self.message_key = message_key
        self.status = 404

        super().__init__(self.message_key, self.status)


class InvalidYearExperience(Exception):
    """
    while using try except you should follow the following style
    try:
        try_dody
    except {{specify_exception_class}} as e: # e is a variable will contain the error message of the exception
        exception_body
    """

    def __init__(self, message_key=ProfileConstants.YEAR_OF_EXPERIENCE):
        self.message_key = message_key
        self.status = 404

        super().__init__(self.message_key, self.status)


class ProfileCreateError(Exception):
    def __init__(self, message_key=ProfileConstants.Profile_CREATION_FAILED_ERROR):
        self.message_key = message_key
        self.status = 401

        super().__init__(self.message_key, self.status)


class ProfileNotFound(Exception):
    def __init__(self, message_key=ProfileConstants.PROFILE_NOT_FOUND_ERROR):
        self.message_key = message_key
        self.status = 401

        super().__init__(self.message_key, self.status)
