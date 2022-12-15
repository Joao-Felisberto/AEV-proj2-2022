from flask import render_template, request, session

from controllers.database import login
from util.util import response


def root():
    print("working")
    return "<h1>WORKING!</h1>"


def dev():
    print("dev")
    return f"{open('./static/routes.json').read()}"


def api_sign_in(username='', password=''):
    print(username, password)
    return render_template('sign_in.html')


def api_login():
    if not request.is_json:
        return 'Invalid JSON!', 400

    data = request.get_json()
    username = data.get('username', '')
    password = data.get('password', '')

    if not username or not password:
        return response('All fields are required!'), 401

    user = login(token, username, password)

    if user:
        session['auth'] = user
        return response('Success'), 200
    return 'Invalid credentials!', 403


def flag_page():
    current_user = token.token_verify(session.get('auth'))
    if current_user['admin']:
        flag = "{THIS_IS_DUMB}"  # This is hardcoded so we don't import os library
        return "<p>" + flag + "</p>"
    else:
        return "<p>This isn't the page you are looking for...!</p>"
