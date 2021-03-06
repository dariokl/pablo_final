from flask import render_template
from . import users

@users.app_errorhandler(404)
def page_not_found(e):
    return render_template("errors/404.html"), 404

@users.app_errorhandler(500)
def internal_server_error(e):
    return render_template("errors/500.html"), 500

@users.app_errorhandler(403)
def page_forbidden(e):
    return render_template("errors/403.html"), 403