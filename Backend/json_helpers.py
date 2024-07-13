import sys
from pympler import asizeof
import json

def convert_keys_to_int(d) -> dict | list:
    """
    Recursively converts string keys that can be converted into integers
    into integer keys in a dictionary or list of dictionaries.
    """
    if isinstance(d, dict):
        return {int(k) if k.isdigit() else k: convert_keys_to_int(v) for k, v in d.items()}
    elif isinstance(d, list):
        return [convert_keys_to_int(item) for item in d]
    else:
        return d
    

def all_levels_dict_and_json_cost(my_dict):
    print("==============================")
    def print_dict(d, indent=0):
        for key, value in d.items():
            if isinstance(value, dict):
                print(f"{' ' * indent}{key}:")
                print_dict(value, indent + 4)
            else:
                print(f"{' ' * indent}{key}: {value}")

    my_json = json.dumps(my_dict)

    print_dict(my_dict)
    print("-- -- --")
    print(f"shallow dictionary: {sys.getsizeof(my_dict)}")
    print(f"deep dictionary: {asizeof.asizeof(my_dict)}")
    print(f"json: {asizeof.asizeof(my_json)}")
    print("==============================")

    return my_json

def json_cost(my_dict):
    json_dict = json.dumps(my_dict)
    print(f"json: {asizeof.asizeof(json_dict)}")
    return json_dict

def plain_json(my_dict):
    json_dict = json.dumps(my_dict)
    return json_dict
    