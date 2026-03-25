from sqladmin import ModelView

from ..models.course import Course


class CourseAdmin(ModelView, model=Course):
    column_list = [
        Course.id,
        Course.name,
        Course.secret,
        Course.creation_date
    ]