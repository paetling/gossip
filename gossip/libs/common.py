import os
import yaml
from .constants import BASE_CONFIG_FILE

def get_config_file_name(server_index):
    return '{}_{}'.format(BASE_CONFIG_FILE, server_index)

def load_membership(file_name):
    if not os.path.isfile(file_name):
        return ''
    with open(file_name, 'r') as f:
        contents = f.read()
        return yaml.load(contents)

def save_membership(file_name, membership_dict):
    import logging
    logging.info("Writing to file {}:".format(file_name))
    logging.info(membership_dict)
    yaml_object = yaml.dump(membership_dict)
    with open(file_name, 'w') as f:
        f.write(yaml_object)
