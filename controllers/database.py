def login(token, username, password):
    if username == 'guest' and password == 'Thislookssafe':
        cookietoken = token.generate_token(username)
        return cookietoken
    else:
        return False
