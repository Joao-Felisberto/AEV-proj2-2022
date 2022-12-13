def root():
    print("working")
    return "<h1>WORKING!</h1>"


def dev():
    print("dev")
    return f"{open('./static/routes.json').read()}"
