import json
import os

def get_svelte_manifest(path):
    if not os.path.exists(path):
        print(f'Path {path} not found')
        return {}

    try:
        with open(os.path.join(path, 'manifest.json'), 'r', encoding='utf-8') as file:
            return json.load(file)

    except json.JSONDecodeError:
        print('Reading JSON file error')
        return {}