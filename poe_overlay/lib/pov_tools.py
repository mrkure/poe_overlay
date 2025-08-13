"""tools module"""

import sys
import copy
import importlib.util
from pathlib import Path

import toml


def load_params_module(dirr):
    path = Path(rf"c:\_software\poe_overlay\poe_overlay\profiles\{dirr}") / "profile.py"
    module_name = "params"  # fixed name
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec:
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module  # register so `import xxx` works
        spec.loader.exec_module(module)
    return module


def remove_dict_keys_with_underscore(obj):
    """remove_dict_keys_with_underscore_start"""
    _mydict = copy.deepcopy(obj)

    def remove_keys_recursive(obj):
        if isinstance(obj, dict):
            return {k: remove_keys_recursive(v) for k, v in obj.items() if not k.startswith("_")}
        elif isinstance(obj, list):
            return [remove_keys_recursive(item) for item in obj]
        else:
            return obj

    return remove_keys_recursive(_mydict)


def load_settings_toml(path, base_dir):
    """load config"""
    with open(path, "r", encoding="utf-8") as f:
        data = toml.load(f)
    data["base_dir"] = base_dir
    return data


def write_settings_toml(path, settings):
    """writes path to currently active toml config"""
    base_dir = settings["base_dir"]
    settings.pop("base_dir")  # this one is added, during runtime in app_pov_overlay, value changed based on app location -> git problem
    with open(path, "w", encoding="utf-8") as f:
        toml.dump(settings, f)
    settings["base_dir"] = base_dir # return it back after save
    
