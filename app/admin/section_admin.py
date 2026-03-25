from sqladmin import ModelView

from ..models.course import CourseSection


class SectionAdmin(ModelView, model=CourseSection):
    column_list = [
        CourseSection.id,
        CourseSection.course,
        CourseSection.title,
        CourseSection.visibility
    ]

