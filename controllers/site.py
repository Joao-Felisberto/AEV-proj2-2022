from flask import render_template, request, session, redirect, url_for

from app import tk_factory
from database.database import login
from util.config import cfg
from util.util import response


def root():
    return "<h1>WORKING!</h1>"


def dev():
    print("dev")
    return f"{open('./static/routes.json').read()}"


def api_sign_in(username='', password=''):
    print(username, password)
    if request.method == 'POST':
        print("POST")
        # Get the login credentials from the request
        username = request.form.get('username')
        password = request.form.get('password')
        # Authenticate the user
        user = login(username, password)
        if user:
            print(user)
            # token = user.decode('utf-8')
            return redirect(url_for('flagpage', token=user))
        else:
            return 'Invalid credentials', 401
    else:
        # Display the login form
        return render_template('sign_in.html')


def api_login():
    if not request.is_json:
        return 'Invalid JSON!', 400

    data = request.get_json()
    username = data.get('username', '')
    password = data.get('password', '')

    if not username or not password:
        return response('All fields are required!'), 401

    user = login(username, password)

    if user:
        session['auth'] = user
        return response('Success'), 200
    return 'Invalid credentials!', 403


def flag_page():
    token = request.args.get('token')
    current_user = tk_factory.token_verify(token)
    if current_user['admin']:
        flag = "{THIS_IS_DUMB}"  # This is hardcoded so we don't import os library
        return "<p>" + flag + "</p>"
    else:
        return "<p>This isn't the page you are looking for...!</p>"
