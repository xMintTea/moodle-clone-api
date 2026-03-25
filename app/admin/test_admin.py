from sqladmin import ModelView

from ..models.course import Test


class TestAdmin(ModelView, model=Test):
    column_list = [
        Test.id,
        Test.title,
        Test.creation_date,
        Test.due_date,
        Test.section
    ]

