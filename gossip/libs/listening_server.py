import socket
import logging
from copy import deepcopy
from .constants import STRING_TERMINATOR, MEMBERSHIP_STRING
from .common import load_membership, save_membership
import yaml

class ListeningServer(object):
    def __init__(self, address, port):
        self.address = address
        self.port = port

    def start(self):
        s = socket.socket()
        s.bind((self.address, self.port))
        s.listen()
        logging.info("Listening on {}".format((self.address, self.port)))
        while True:
            from_conn, from_address = s.accept()
            while True:
                data = from_conn.recv(4096)
                logging.info("GOT DATA")
                logging.info(data)
                if data == STRING_TERMINATOR:
                    break
                if MEMBERSHIP_STRING in data:
                    final_data = yaml.load(data[len(MEMBERSHIP_STRING):])
                    self.update_membership(final_data)

    def update_membership(self, new_membership_dict):
        current_membership_dict = load_membership()
        merged_membership_dict = self.merge_membership_dicts(current_membership_dict, new_membership_dict)
        save_membership(merged_membership_dict)

    def merge_membership_dicts(self, current_membership_dict, new_membership_dict):
        return deepcopy(new_membership_dict)
