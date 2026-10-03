DEFAULTS = {
    "host": "127.0.0.1",
    "port": 8000,
    "debug": False,
}


def _env_values(env):
    values = {}
    if "APP_HOST" in env:
        values["host"] = env["APP_HOST"]
    if "APP_PORT" in env:
        values["port"] = int(env["APP_PORT"])
    if "APP_DEBUG" in env:
        values["debug"] = env["APP_DEBUG"].lower() in {"1", "true", "yes", "on"}
    return values


def load_config(file_values=None, env=None, cli=None):
    file_values = file_values or {}
    env = env or {}
    cli = cli or {}

    result = dict(DEFAULTS)
    result.update(cli)
    result.update(_env_values(env))
    result.update(file_values)
    return result
