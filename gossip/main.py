import logging
import os
from copy import deepcopy
import threading

from gossip.libs.listening_server import ListeningServer
from gossip.libs.gossiper import Gossiper
from gossip.libs.common import get_config_file_name, save_membership
from gossip.libs.constants import INITIAL_CONFIG, BASE_CONFIG_FILE, PORT_START


def get_port(index):
    return index + PORT_START

def create_base_config_file(index, server_configs):
    file_name = get_config_file_name(index)
    logging.info("Saving the full config: {} to {}".format(server_configs, file_name))
    save_membership(file_name, server_configs)

def initial_membership_dict(servers_to_start):
    return_dict = {'server_configs':
                        {'servers': [],
                         'suspect_matrix': [],
                         'gossip_list': [0] * servers_to_start,
                         'suspect_list': [0] * servers_to_start}
                  }
    for index in range(servers_to_start):
        return_dict['server_configs']['servers'].append({'address': 'localhost',
                                                         'port': get_port(index)})
        return_dict['server_configs']['suspect_matrix'].append([0] * servers_to_start)
    return return_dict

def setup_server(index, server_configs):
    logging.info("Starting the {} listening server".format(index))
    ls = ListeningServer(index, server_configs['servers'][index])
    thread = threading.Thread(target=ls.start, args=())
    thread.daemon = True
    thread.start()

def setup_gossiper(index):
    logging.info("Start the {} gossiper".format(index))
    gossiper = Gossiper(index)
    thread = threading.Thread(target=gossiper.gossip, args=())
    thread.daemon = True
    thread.start()

def main():
    servers_to_start = int(os.getenv("SERVERS_TO_START"))
    logging.info("SERVERS TO START: {}".format(servers_to_start))
    server_configs = initial_membership_dict(servers_to_start)

    for index in range(servers_to_start):
        create_base_config_file(index, server_configs)
        setup_server(index, server_configs)
        setup_gossiper(index)

    while True:
        pass

if __name__ == '__main__':
    main()
