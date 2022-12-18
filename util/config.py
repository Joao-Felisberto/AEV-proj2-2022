import os

cfg = {
    "DEBUG": os.environ.get("FLASK_ENV", "development") == "development",  # whether to run app in debug mode or not
}

__type_casts = {t: t for t in (int, float, str, bool)}

cfg = {
    c: __type_casts[type(cfg[c])](os.environ.get(c, cfg[c]))
    for c in cfg
}
