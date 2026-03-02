from enum import StrEnum

class UserStatus(StrEnum):
    ACTIVE = "Активен"
    SUSPENDED = "Остановлен"


class UserType(StrEnum):
    STUDENT = "Студент"
    TEACHER = "Преподаватель"
    ADMIN = "Администратор"