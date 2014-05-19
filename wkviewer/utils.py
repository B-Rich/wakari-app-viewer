from . import settings as app_settings


def without_prefix(some_path):
    prefix_length = len(app_settings.URL_PREFIX)

    # Check to handle possible old (pre-v0.3) code that doesn't include
    # the trailing slash.
    if not app_settings.URL_PREFIX.endswith("/"):
        prefix_length += 1
    return some_path[prefix_length:]
