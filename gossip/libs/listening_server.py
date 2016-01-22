import socket
import logging
from copy import deepcopy
from .constants import STRING_TERMINATOR, MEMBERSHIP_STRING, THRESHOLD
from .common import load_membership, save_membership, get_config_file_name
import yaml
import random

class ListeningServer(object):
    def __init__(self, server_index, server_config):
        self.server_index = server_index
        self.address = server_config['address']
        self.port = server_config['port']
        self.config_file_name = get_config_file_name(self.server_index)

    def start(self):
        s = socket.socket()
        s.bind((self.address, self.port))
        s.listen()
        logging.int("Listening on {}".format((self.address, self.port)))
        while True:
            from_conn, from_address = s.accept()
            logging.info("Port {} got a connection from gossiper {}".format(self.port, from_address[1]))
            while True:
                data = from_conn.recv(4096).decode('utf-8')
                logging.info("GOT DATA")
                logging.info(data)
                if MEMBERSHIP_STRING in data:
                    logging.info("Saving data")
                    final_data = yaml.load(data.replace(MEMBERSHIP_STRING, '').replace(STRING_TERMINATOR, ''))
                    self.update_membership(final_data)
                if STRING_TERMINATOR in data:
                    logging.info("Ending connection")
                    break

    def update_membership(self, new_membership_dict):
        current_membership_dict = load_membership(self.config_file_name)
        merged_membership_dict = self.merge_membership_dicts(current_membership_dict, new_membership_dict)
        save_membership(self.config_file_name, merged_membership_dict)

    def merge_membership_dicts(self, current_membership_dict, new_membership_dict):
        merged_membership = deepcopy(current_membership_dict)
        for i, item in enumerate(current_membership_dict['gossip_list']):
            current_less_than_new = current_membership_dict['gossip_list'][i] < new_membership_dict['gossip_list'][i]
            merged_membership['gossip_list'][i] = current_membership_dict['gossip_list'][i] if current_less_than_new else new_membership_dict['gossip_list'][i]
            merged_membership['suspect_list'][i] = 1 if merged_membership['gossip_list'][i] > THRESHOLD else 0
            merged_membership['suspect_matrix'][i] = current_membership_dict['suspect_matrix'][i] if current_less_than_new else new_membership_dict['suspect_matrix'][i]
        merged_membership['suspect_matrix'][self.server_index] = merged_membership['suspect_list']
        return merged_membership
