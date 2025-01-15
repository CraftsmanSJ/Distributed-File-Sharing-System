import json
import os

def load_peers():
    # Load peers from peers.json
    config_path = os.path.join(os.path.dirname(__file__), 'peers.json')
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            return json.load(f)['peers']
    return []
