from sqladmin import ModelView

from ..models.user import User


class UserAdmin(ModelView, model=User):
    column_list = [
        User.id,
        User.first_name,
        User.middle_name,
        User.last_name,
        User.email,
        User.user_type,
        User.user_status,
    ]