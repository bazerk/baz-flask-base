from flask import (Blueprint, render_template, current_app, request,
                   flash, url_for, redirect, session, abort, g)

# from flask.ext.login import (login_required, login_user, current_user,
#                             logout_user, confirm_login, fresh_login_required,
#                             login_fresh)

from ..models import User

admin = Blueprint('admin', __name__)


@admin.before_request
def restrict_bp_to_admins():
    if not User.is_admin:
        flash('You need to be an admin to access this page', 'Warning')
        return redirect(url_for('frontend.login'))


@admin.route('/users')
def users():
    return render_template('admin/users')
