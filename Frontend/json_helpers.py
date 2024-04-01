import json
import sys

def convert_keys_to_int(d):
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
    
def split_json_objects(data):
    objects = []
    brace_count = 0
    current_object = ""
    
    for char in data:
        current_object += char
        if char == '{':
            brace_count += 1
        elif char == '}':
            brace_count -= 1
        
        if brace_count == 0 and current_object.strip():
            # print(current_object)
            try:
                objects.append(json.loads(current_object))
                current_object = ""  # Reset for the next object
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {current_object}")
                # Handle or log the error as needed
                
    return objects