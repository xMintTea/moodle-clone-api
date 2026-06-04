from enum import IntEnum, StrEnum

class UserStatus(IntEnum):
    ACTIVE = 1
    SUSPENDED = 2


class UserType(IntEnum):
    DEFAULT = 1
    REDACTOR = 2
    ADMIN = 3
    

class CourseAccessLevel(IntEnum):
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
    
    
class QuestionTypes(StrEnum):
    SELECT_ONE = "select_one"
    SELECT_MULTIPLE = "select_multiple"
    WRITE_ANSWER = "write_answer"
    ORDER_ANSWERS = "order_answers"
    
    
class ReviewModes(StrEnum):
    AUTO = "auto"
    MANUAL = "manual"
    
class ReviewType(StrEnum):
    EXACT = "exact"   # exact match
    SUBSET = "subset" # answer must be a subset of right answers
    SCORED = "scored" # correct +1; incorrect -1; max(0, score)