import logging
import random
import yaml
import socket
from .constants import STRING_TERMINATOR, MEMBERSHIP_STRING
from .common import load_membership, save_membership, get_config_file_name


class Gossiper(object):
    def __init__(self, server_index):
        self.server_index = server_index
        self.config_file = get_config_file_name(self.server_index)

    def gossip(self):
        current_membership = load_membership(self.config_file)
        random_address = self.get_random_peer(current_membership)
        self.gossip_membership(random_address, current_membership)
        success = True
        self.update_heartbeat(random_address, current_membership, success)

    def gossip_membership(random_address, current_membership):
        s = socket.socket()
        s.connect(random_address)
        logging.error('Sending {} to {}'.format(current_membership, random_address))
        self.send_string(s, "{}{}".format(MEMBERSHIP_STRING, yaml.dump(current_membership)))
        self.send_string(s, STRING_TERMINATOR)

    def send_string(self, socket, string):
        socket.send(string.encode('utf-8'))

    def update_heartbeat(self, random_address, current_membership):
        for member in current_membership['members']:
            if random_address[0] == member['address'] and random_address[1] == member['port']:
                member['heartbeat'] = 0
        save_membership(self.config_file, current_membership)

    def get_random_peer(self, current_membership):
        current_member_count = len(current_membership['members'])
        random_member_index = random.randint(0, current_member_count - 1)
        random_peer = current_membership['members'][random_member_index]
        return random_peer['address'], random_peer['port']

