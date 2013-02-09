from flask import (Blueprint, render_template, request,
                   flash, url_for, redirect, session)

from ..models import User
from ..extensions import bcrypt, twitter
from ..decorators import login_required
from forms import LoginForm, RegisterForm

frontend = Blueprint('frontend', __name__)


@frontend.route('/')
@login_required
def dashboard():
    return render_template('frontend/dashboard.html')


@frontend.route('/register', methods=['GET', 'POST'])
def register():
    twitter_name = None
    twitter_deets = None
    if 'twitter_access_token' in session:
        twitter_deets = session['twitter_access_token']
        twitter_name = twitter_deets['screen_name']

    form = RegisterForm(username=request.args.get('username', twitter_name),
                        password=request.args.get('password', None))

    if form.validate_on_submit():
        err, user = User.create(form.username.data, form.email.data,
            bcrypt.generate_password_hash(form.password.data), twitter_deets=twitter_deets)
        if err is None:
            return redirect(url_for('frontend.login'))
        else:
            flash('Problem creating user ' + err, 'error')
    return render_template('frontend/register.html', form=form, twitter_name=twitter_name)


@frontend.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('frontend.login'))


@frontend.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(login=request.args.get('login', None),
                     next=request.args.get('next', None))

    if form.validate_on_submit():
        user = User.authenticate(form.login.data,
                form.password.data, bcrypt.check_password_hash)

        if user:
            flash('Logged in', 'success')
            session['user_id'] = user.id
            remember = request.form.get('remember') == 'y'
            if remember:
                session.permanent = True
            return redirect('')
        else:
            flash('Sorry, invalid login', 'error')

    return render_template('frontend/login.html', form=form)


@frontend.route('/login-with-twitter')
def login_with_twitter():
    try:
        (url, token) = twitter.request_token()
        session['twitter_request_token'] = token
        return redirect(url)
    except Exception as err:
        flash('Problem talking to twitter %s' % err)

    return redirect(url_for('frontend.login'))


@frontend.route('/login-twitter-callback')
def login_twitter_callback():
    if 'oauth_token' not in request.args or 'oauth_verifier' not in request.args:
        return redirect(url_for('frontend.login'))
    if 'twitter_request_token' not in session:
        return redirect(url_for('frontend.login'))

    oauth_token = request.args['oauth_token']
    oauth_verifier = request.args['oauth_verifier']
    request_token = session['twitter_request_token']
    try:
        access_token = twitter.get_access_token(oauth_token, oauth_verifier, request_token)
        screen_name = access_token['screen_name']
        user = User.from_twitter(screen_name)
        if user:
            flash('Logged in', 'success')
            session['user_id'] = user.id
            return redirect('')
        else:
            session['twitter_access_token'] = access_token
            return redirect('/register')
    except Exception as err:
        flash('Problem talking to twitter %s' % err)
    return redirect(url_for('frontend.login'))
