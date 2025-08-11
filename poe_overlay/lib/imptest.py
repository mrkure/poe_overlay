import importlib.util
import sys
from pathlib import Path

def load_params_module(file):
    path = Path(r"c:\_software\poe_overlay\poe_overlay\profiles") / file
    module_name = "params"  # fixed name
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec:
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module  # register so `import xxx` works
        spec.loader.exec_module(module)
    return module



# First load
params = load_params_module("3_26_bama.py")
print("First load:", params.params)

# Later, reload with different file
params = load_params_module("3_26_pconc.py")
print("After reload:", params.params)

# Test that 'import xxx' sees the new one
import params
print("From import xxx:", params.params)
