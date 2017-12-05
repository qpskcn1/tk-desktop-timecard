import os
from functools import wraps

import appdirs


def ensure_path_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)


def _ensure_returned_path_exists(f):
    @wraps(f)
    def wrapper(subpath):
        path = f(subpath)
        ensure_path_exists(path)
        return path
    return wrapper


@_ensure_returned_path_exists
def get_data_dir(module_name):
    data_dir = appdirs.user_data_dir("activitywatch")
    return os.path.join(data_dir, module_name) if module_name else data_dir


@_ensure_returned_path_exists
def get_cache_dir(module_name):
    cache_dir = appdirs.user_cache_dir("activitywatch")
    return os.path.join(cache_dir, module_name) if module_name else cache_dir


@_ensure_returned_path_exists
def get_config_dir(module_name):
    config_dir = appdirs.user_config_dir("activitywatch")
    return os.path.join(config_dir, module_name) if module_name else config_dir


@_ensure_returned_path_exists
def get_log_dir(module_name):  # pragma: no cover
    log_dir = appdirs.user_log_dir("activitywatch")
    return os.path.join(log_dir, module_name) if module_name else log_dir
