import glob
import importlib
import json
import os

from flask import Flask

"""
Ideas:

- have routes specified in a json file
- these routes are then dynamically loaded

- somewhere there has to be a multi-line lambda
- import with side effects
"""

app = Flask(__name__)

routes = {}


def load_controllers():
    with open("static/routes.json", 'r') as routesConfig:
        routes = json.loads(routesConfig.read())

    controllerFiles = [f for f in glob.glob("controllers/*.py") if not f.endswith("__.py")]
    controllerFunctions = {}
    for file in controllerFiles:
        controllerFile = f"controllers.{file.split('/')[-1].replace('.py', '')}"
        module = importlib.import_module(controllerFile)
        for func in [m for m in dir(module) if callable(getattr(module, m))]:
            controllerFunctions[func] = getattr(module, func)

    for endpoint, route in routes.items():
        app.add_url_rule(endpoint, route["endpointName"], controllerFunctions[route["method"]])

    return controllerFunctions


# if __name__ == '__main__':
print(os.getcwd())
routes = load_controllers()
# app.run()
