import re


def slugify(value):
    value = value.lower().strip()
    value = value.replace(" ", "-")
    value = re.sub(r"[^a-z0-9-]", "", value)
    return value
