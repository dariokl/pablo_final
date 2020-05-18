from flask import abort, flash, redirect, url_for, request
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user

class AdminLockView(ModelView):
    def is_accessible(self):
        if current_user.is_admin and not current_user.is_anonymous:
            return True
        else:
            return abort(403)

class ExcludeModelView(AdminLockView):

    form_excluded_columns = ('course_info', 'course_name', 'assigned_date',\
                             'teacher_name', 'orders')

    column_exclude_list = ('password_hash')


class AddSearchView(ExcludeModelView):

    column_searchable_list = ['first_name']









