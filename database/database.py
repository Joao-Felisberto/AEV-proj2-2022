from app import tk_factory

db = {
    "guest": "Thislookssafe"
}


def login(username, password):
    if username in db and db[username] == password:
        cookietoken = tk_factory.generate_token(username)
        return cookietoken
    else:
        return False
