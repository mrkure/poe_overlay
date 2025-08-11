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

# def read_config_toml():
#     """load config"""
#     config = r"c:\_software\poe_overlay\poe_overlay\profiles"
#     toml_file = [str(f) for f in Path(config).glob("*.toml")][0]
#     with open(toml_file, "r", encoding="utf-8") as f:
#         data = toml.load(f)
#     return data

def read_config_toml(path):
    """load config"""
    with open(path, "r", encoding="utf-8") as f:
        data = toml.load(f)
    return data

def write_configs_toml(path, settings):
    """writes path to currently active toml config"""
    with open(path, "w", encoding="utf-8") as f:
        toml.dump(settings, f)

# def read_configs_toml(self):
#     """load config"""
#     toml_files = [str(f) for f in Path(self.CONFIG_PATH).glob("*.toml")]
#     for file in toml_files:
#         with open(file, "r", encoding="utf-8") as f:
#             self.configs[file] = toml.load(f)

# def write_configs_toml(self):
#     """writes path to currently active toml config"""

#     def remove_keys_recursive(obj, keys_to_remove):
#         if isinstance(obj, dict):
#             return {k: remove_keys_recursive(v, keys_to_remove) for k, v in obj.items() if k not in keys_to_remove}
#         elif isinstance(obj, list):
#             return [remove_keys_recursive(item, keys_to_remove) for item in obj]
#         else:
#             return obj

#     for key, value in self.configs.items():
#         config = remove_keys_recursive(value, ["function", "id", "flasks_pointer", "running", "active_profile_name"])
#         with open(key, "w", encoding="utf-8") as f:
#             toml.dump(config, f)