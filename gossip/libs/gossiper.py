"""
Based off of this paper: http://docs.hcs.ufl.edu/pubs/GEMS2005.pdf
Server configs document looks like the following dictionary:
    {'servers': [{'address': '',
                  'port': ''},
                  ...
                ],
     'gossip_list': [int, ...],
     'suspect_list': [int, ...],
     'suspect_matrix': [[<suspect_list>], ...]}
'servers': contains how to reach each server
'gossip_list': contains last time a particular server talked to the other servers
'suspect_list': contains who a particular server thinks is down
'suspect_matrix': contains what a particular server thinks all servers think about what servers are down
                  (it is an aggregation of all servers suspect list)
NOTE: All lists should be the exact same length

Config file also contains a 'my_config' -> {'address': '', 'port': ''} for the current config

{'current_membership': {'server_configs': server_configs, 'my_config': my_config}}
"""

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
        self.config_file_name = get_config_file_name(self.server_index)

    def gossip(self):
        while True:
            current_membership = load_membership(self.config_file_name)
            self.update_heartbeat(random_address, current_membership)
            random_address = self.get_random_peer(current_membership)
            self.gossip_about_membership(random_address, current_membership)
            sleep(5)

    def gossip_about_membership(self, random_address, current_membership):
        s = socket.socket()
        try:
            logging.error('Sending {} to {}'.format(current_membership, random_address))
            s.connect(random_address)
            self.send_string(s, "{}{}".format(MEMBERSHIP_STRING, yaml.dump(current_membership)))
            self.send_string(s, STRING_TERMINATOR)
        except Exception as e:
            logging.error("An error occurred: {}".format(e))

    def send_string(self, socket, string):
        socket.send(string.encode('utf-8'))

    def update_heartbeat(self, current_membership):
        for i, val in enumerate(current_membership['server_configs']['gossip_list']):
            if i != self.server_index:
                current_membership['server_configs']['gossip_list'][i] = val + 1
            else:
                current_membership['server_configs']['gossip_list'][i] = 0
        logging.error("{} is updating heartbeats to be {}".format(self.server_index, current_membership['server_configs']['gossip_list']))
        save_membership(self.config_file_name, current_membership)

    def members_excluding_self(self, current_membership):
        """ Get a list of server indexes excluding index of the current server
        """
        server_indices = list(range(len(current_membership['server_configs']['servers'])))
        server_indices.remove(self.server_index)
        return server_indices

    def get_random_peer(self, current_membership):
        non_self_members = self.members_excluding_self(current_membership)
        random_member_server_id = non_self_members[random.randint(0, len(non_self_members) - 1)]
        random_peer_server = current_membership['server_configs']['servers'][random_member_server_id]
        return random_peer_server['address'], random_peer_server['port']

