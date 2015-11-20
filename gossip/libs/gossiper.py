import logging
import random
import yaml
import socket
from constants import STRING_TERMINATOR, MEMBERSHIP_STRING
from .common import load_membership, save_membership


class Gossiper(object):
    def gossip(self):
        current_membership = load_membership()
        random_address = self.get_random_peer(current_membership)
        self.gossip_membership(random_address, current_membership)
        success = True
        self.update_heartbeat(random_address, current_membership, success)

    def gossip_membership(random_address, current_membership):
        s = socket.socket()
        s.connect(random_address)
        logging.info('Sending {} to {}'.format(current_membership, random_address))

        s.send(MEMBERSHIP_STRING)
        s.send(yaml.dump(current_membership))
        s.send(STRING_TERMINATOR)

    def update_heartbeat(self, random_address, current_membership):
        for member in current_membership['members']:
            if random_address[0] == member['address'] and random_address[1] == member['port']:
                member['heartbeat'] = 0
        save_membership(current_membership)

    def get_random_peer(self, current_membership):
        current_member_count = len(current_membership['members'])
        random_member_index = random.randint(0, current_member_count - 1)
        random_peer = current_membership['members'][random_member_index]
        return random_peer['address'], random_peer['port']

