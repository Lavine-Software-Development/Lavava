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