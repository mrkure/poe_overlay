import inspect
import pov_mouse



workers = []
for name, func in inspect.getmembers(pov_mouse, inspect.isfunction):
    if func.__module__ == pov_mouse.__name__:  # only own functions
        print(f"Calling: {name}")
        worker = func(None)
        worker["function"] = func
        print(worker)
        # args = args_for_functions.get(name, ())
        # result = func(*args)
        # if result is not None:
        #     print(f"→ Returned: {result}")


for name, func in inspect.getmembers(MyStaticClass, inspect.isfunction):

        print(f"Calling {name} with {args_for_methods[name]}")
        result = func(*args_for_methods[name])
        if result is not None:
            print(f"→ Returned: {result}")