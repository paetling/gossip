import os
from .constants import CONFIG_FILE
import yaml

def load_membership():
    if not os.path.isfile(CONFIG_FILE):
        return ''
    with open(CONFIG_FILE, 'r') as f:
        contents = f.read()
        return yaml.load(contents)

def save_membership(merged_membership_dict):
    yaml_object = yaml.dump(merged_membership_dict)
    with open(CONFIG_FILE, 'w') as f:
        f.write(yaml_object)
