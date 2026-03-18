from enum import IntEnum

class UserStatus(IntEnum):
    ACTIVE = 1
    SUSPENDED = 2


class UserType(IntEnum):
    DEFAULT = 1
    REDACTOR = 2
    ADMIN = 3
    

class CourseUserType(IntEnum):
    STUDENT = 1
    ASSISTENT = 2
    TEACHER = 3


class CourseAccessStatus(IntEnum):
    GRANTED = 1
    CLOSED = 2


class Visibility(IntEnum):
    VISIBLE_EVERYONE = 1
    VISIBLE_TO_CREATOR = 2
    NOT_VISIBLE = 3