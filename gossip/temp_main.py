from libs.listening_server import ListeningServer
from libs.gossiper import Gossiper
from libs.common import get_config_file_name, save_membership
from libs.constants import INITIAL_CONFIG, BASE_CONFIG_FILE
import logging
import os
from copy import deepcopy
import threading

def get_port(index):
    return index + 80

def create_base_config_file(index, membership):
    full_config = deepcopy(membership)
    full_config['my_config'] = {'address': 'localhost',
                                'port': get_port(index)}
    file_name = get_config_file_name(index)
    logging.error("Saving the full config: {} to {}".format(full_config, file_name))
    save_membership(file_name, full_config)

def create_membership_dict(servers_to_start):
    return_dict = {'members': []}
    for index in range(servers_to_start):
        return_dict['members'].append({'address': 'localhost',
                                       'port': get_port(index)})
    return return_dict

def setup_server(index):
    logging.error("Starting the {} listening server".format(index))
    ls = ListeningServer(index, 'localhost', get_port(index))
    thread = threading.Thread(target=ls.start, args=())
    thread.daemon = True
    thread.start()

def setup_gossiper(index):
    logging.error("Start the {} gossiper".format(index))
    gossiper = Gossiper(index)
    thread = threading.Thread(target=gossiper.gossip, args=())
    thread.daemon = True
    thread.start()

def main():
    servers_to_start = int(os.getenv("SERVERS_TO_START"))
    logging.error("SERVERS TO START")
    logging.error(servers_to_start)
    membership_dict = create_membership_dict(servers_to_start)
    logging.error(membership_dict)

    for index in range(servers_to_start):
        create_base_config_file(index, membership_dict)
        setup_server(index)
        setup_gossiper(index)

    while True:
        pass

if __name__ == '__main__':
    main()
