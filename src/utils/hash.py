import hashlib
import json


def hash_dict(input_dict: dict) -> str:
    json_str = json.dumps(input_dict, sort_keys=True)
    sha256_hash = hashlib.sha256()
    sha256_hash.update(json_str.encode('utf-8'))
    hashed_value = sha256_hash.hexdigest()

    return hashed_value
