import socket
import logging
from copy import deepcopy
from .constants import STRING_TERMINATOR, MEMBERSHIP_STRING
from .common import load_membership, save_membership, get_config_file_name
import yaml

class ListeningServer(object):
    def __init__(self, server_index, address, port):
        self.server_index = server_index
        self.address = address
        self.port = port
        self.config_file = get_config_file_name(self.server_index)

    def start(self):
        s = socket.socket()
        s.bind((self.address, self.port))
        s.listen()
        logging.error("Listening on {}".format((self.address, self.port)))
        while True:
            from_conn, from_address = s.accept()
            logging.error("Got a connection")
            while True:
                data = from_conn.recv(4096).decode('utf-8')
                logging.error("GOT DATA")
                logging.error(data)
                if MEMBERSHIP_STRING in data:
                    logging.error("Saving data")
                    final_data = yaml.load(data.replace(MEMBERSHIP_STRING, '').replace(STRING_TERMINATOR, ''))
                    self.update_membership(final_data)
                if STRING_TERMINATOR in data:
                    logging.error("Ending connection")
                    break

    def update_membership(self, new_membership_dict):
        logging.error("Updating Membership")
        current_membership_dict = load_membership(self.config_file)
        merged_membership_dict = self.merge_membership_dicts(current_membership_dict, new_membership_dict)
        logging.error("New Membership is {}".format(merged_membership_dict))
        save_membership(self.config_file, merged_membership_dict)

    def merge_membership_dicts(self, current_membership_dict, new_membership_dict):
        merged_membership = deepcopy(current_membership_dict)
        merged_membership['members'] = new_membership_dict['members']
        return merged_membership
