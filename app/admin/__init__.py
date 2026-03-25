from sqladmin import Admin

from .user_admin import UserAdmin
from .course_admin import CourseAdmin
from .section_admin import SectionAdmin
from .page_admin import PageAdmin
from .submitted_page_admin import SubmittedPageAdmin


def register_views(admin: Admin):
    admin.add_view(UserAdmin)
    admin.add_view(CourseAdmin)
    admin.add_view(SectionAdmin)
    admin.add_view(PageAdmin)
    admin.add_view(SubmittedPageAdmin)