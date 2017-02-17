import json


def canonical_json(payload):
    return json.dumps(payload, sort_keys=True, separators=(',', ':'))
