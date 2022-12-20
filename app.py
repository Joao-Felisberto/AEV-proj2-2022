import glob
import importlib
import json
import logging

from flask import Flask

from token_factory.tokenfactory import TokenFactory
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
app.config['SECRET_KEY'] = "super secret key"


# todo: fix
# csrf = CSRFProtect()
# csrf.init_app(app)


class Main:
    tk_factory = TokenFactory()

    def __init__(self):
        self.routes = {}

    def load_controllers(self):
        self.load_routes()

        controller_files = [f for f in glob.glob("controllers/*.py") if not f.endswith("__.py")]
        controller_functions = {}
        for file in controller_files:
            controller_file = f"controllers.{file.split('/')[-1].replace('.py', '')}"
            module = importlib.import_module(controller_file)
            for func in [m for m in dir(module) if callable(getattr(module, m))]:
                controller_functions[func] = getattr(module, func)

        for endpoint, route in self.routes.items():
            if bool(route.get("dev", False)) and cfg["DEBUG"]:
                print(endpoint, route, "lambda")
                app.add_url_rule(endpoint, route["endpointName"],
                                 lambda _ep=route['endpointName']: (
                                     logging.debug(f"running {_ep}(...)"),
                                     self.load_routes(),
                                     _res := (eval(self.routes[endpoint]["method"])),
                                     f"<h1>Executed!</h1></br><p>{_res}</p>"
                                 )[-1],
                                 methods=["GET", "POST"])
            elif bool(route.get("dev", False)):
                print(endpoint, route, "null")
                app.add_url_rule(endpoint, route["endpointName"], lambda: None,
                                 methods=["GET", "POST"])
            else:
                print(endpoint, route, "method")
                app.add_url_rule(endpoint, route["endpointName"], controller_functions[route["method"]],
                                 methods=["GET", "POST"])

        return controller_functions

    def load_routes(self):
        with open("static/routes.json", 'r') as routesConfig:
            self.routes = json.loads(routesConfig.read())


tk_factory = Main.tk_factory
routes = Main().load_controllers()
