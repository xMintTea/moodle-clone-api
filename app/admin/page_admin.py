from sqladmin import ModelView

from ..models.course import SectionPage


class PageAdmin(ModelView, model=SectionPage):
    column_list = [
        SectionPage.id,
        SectionPage.section,
        SectionPage.title,
        SectionPage.last_change_date
    ]


    form_excluded_columns = [
        SectionPage.creation_date
    ]
