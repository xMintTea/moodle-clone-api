from sqladmin import ModelView

from ..models.course import SubmittedPage


class SubmittedPageAdmin(ModelView, model=SubmittedPage):
    column_list = [
        SubmittedPage.id,
        SubmittedPage.page,
        SubmittedPage.user,
        SubmittedPage.submitted,
        SubmittedPage.reviewed
    ]

