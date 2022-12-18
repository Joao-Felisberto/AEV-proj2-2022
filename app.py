import glob
import importlib
import json
import logging
import os

from flask import Flask
from flask_wtf.csrf import CSRFProtect

from util.config import cfg

"""
Ideas:

- have routes specified in a json file
- these routes are then dynamically loaded (in dev config)
- an attacker can then add a route in which they can execute certain code
- code executed must be limited (use zalgo?)
- get access to the token generator (somehow)

- somewhere there has to be a multi-line lambda
- import with side effects
- generators with __next__()
"""

app = Flask(__name__)
csrf = CSRFProtect()
csrf.init_app(app)

routes = {}


def load_controllers():
    with open("static/routes.json", 'r') as routesConfig:
        routes = json.loads(routesConfig.read())

    controller_files = [f for f in glob.glob("controllers/*.py") if not f.endswith("__.py")]
    controller_functions = {}
    for file in controller_files:
        controller_file = f"controllers.{file.split('/')[-1].replace('.py', '')}"
        module = importlib.import_module(controller_file)
        for func in [m for m in dir(module) if callable(getattr(module, m))]:
            controller_functions[func] = getattr(module, func)

    for endpoint, route in routes.items():
        if bool(route.get("dev", False)) and cfg["DEBUG"]:
            print(endpoint, route, "lambda")
            app.add_url_rule(endpoint, route["endpointName"],
                             lambda: (logging.debug(f"running {route['endpointName']}(...)"),
                                      exec(route["method"]),
                                      "<h1>Executed!</h1>"
                                      )[-1])
        elif bool(route.get("dev", False)):
            print(endpoint, route, "null")
            app.add_url_rule(endpoint, route["endpointName"], lambda: None)
        else:
            print(endpoint, route, "method")
            app.add_url_rule(endpoint, route["endpointName"], controller_functions[route["method"]])

    return controller_functions


# if __name__ == '__main__':
print(os.getcwd())
routes = load_controllers()

# app.run()
