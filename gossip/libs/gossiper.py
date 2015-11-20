import logging
import random
import yaml
import socket
from .constants import STRING_TERMINATOR, MEMBERSHIP_STRING
from .common import load_membership, save_membership, get_config_file_name
from time import sleep


class Gossiper(object):
    def __init__(self, server_index):
        self.server_index = server_index
        self.config_file = get_config_file_name(self.server_index)

    def gossip(self):
        while True:
            current_membership = load_membership(self.config_file)
            random_address = self.get_random_peer(current_membership)
            success = self.gossip_about_membership(random_address, current_membership)
            self.update_heartbeat(random_address, current_membership, success)
            sleep(5)

    def gossip_about_membership(self, random_address, current_membership):
        s = socket.socket()
        try:
            logging.error('Sending {} to {}'.format(current_membership, random_address))
            s.connect(random_address)
            self.send_string(s, "{}{}".format(MEMBERSHIP_STRING, yaml.dump(current_membership)))
            self.send_string(s, STRING_TERMINATOR)
            return True
        except Exception as e:
            logging.error("An error occurred: {}".format(e))
            return False


    def send_string(self, socket, string):
        socket.send(string.encode('utf-8'))

    def update_heartbeat(self, random_address, current_membership, success):
        for member in current_membership['members']:
            if random_address[0] == member['address'] and random_address[1] == member['port']:
                if success:
                    member['heartbeat'] = 0
                else:
                    member['heartbeat'] = member.get('heartbeat', 0) + 1
        save_membership(self.config_file, current_membership)

    def members_excluding_self(self, current_membership):
        members = []
        my_port = current_membership['my_config']['port']
        my_address = current_membership['my_config']['address']
        for member in current_membership['members']:
            if member['port'] != my_port or member['address'] != my_address:
                members.append(member)
        return members

    def get_random_peer(self, current_membership):
        non_self_members = self.members_excluding_self(current_membership)
        current_member_count = len(non_self_members)
        random_member_index = random.randint(0, current_member_count - 1)
        random_peer = non_self_members[random_member_index]
        return random_peer['address'], random_peer['port']

