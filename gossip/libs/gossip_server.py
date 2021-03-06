import socket
import logging
import sys
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

    def start(self, file_lock):
        s = socket.socket()
        s.bind((self.address, self.port))
        s.listen()
        logging.info("Listening on {}".format((self.address, self.port)))
        while True:
            from_conn, from_address = s.accept()
            logging.info("Port {} got a connection from gossiper {}".format(self.port, from_address[1]))
            while True:
                data = self.read_data(from_conn)
                if MEMBERSHIP_STRING in data:
                    logging.info("Merging data")
                    membership_config = self.get_formatted_membership_config(data)
                    self.update_membership(membership_config, file_lock)
                if STRING_TERMINATOR in data:
                    logging.info("Ending connection")
                    break

    def read_data(self, conn):
        data = conn.recv(4096).decode('utf-8')
        return data

    def get_formatted_membership_config(self, data):
        return yaml.load(data.replace(MEMBERSHIP_STRING, '').replace(STRING_TERMINATOR, ''))

    def update_membership(self, new_membership_dict, file_lock):
        file_lock.acquire(True)

        current_membership_dict = load_membership(self.config_file_name)
        merged_membership_dict = self.merge_membership_dicts(current_membership_dict, new_membership_dict)
        save_membership(self.config_file_name, merged_membership_dict)

        file_lock.release()

    def merge_gossip_list(self, current_membership_gossip_list, new_membership_gossip_list):
        merged_gossip_list = []
        max_length = max(len(current_membership_gossip_list), len(new_membership_gossip_list))
        for i in range(max_length):
            current_item = current_membership_gossip_list[i] if len(current_membership_gossip_list) > i else sys.maxsize
            new_gossip_item = new_membership_gossip_list[i] if len(new_membership_gossip_list) > i else sys.maxsize
            merged_gossip_list.append(min(current_item, new_gossip_item))
        return merged_gossip_list

    def suspects_from_gossip(self, gossip_list):
        suspect_list = []
        for tick in gossip_list:
            suspect_list.append(1 if tick > THRESHOLD else 0)
        return suspect_list

    @staticmethod
    def merged_membership_suspects(current_membership_suspects, new_membership_suspects):
        additional_suspects = []
        if len(new_membership_suspects) > len(current_membership_suspects):
            additional_suspects = new_membership_suspects[len(current_membership_suspects):]
        return current_membership_suspects + additional_suspects

    def create_suspect_matrix(self,
                              current_membership_gossip,
                              new_membership_gossip,
                              current_membership_suspects,
                              current_membership_matrix,
                              new_membership_matrix):
        suspect_matrix = []
        max_length = max(len(current_membership_gossip), len(new_membership_gossip))
        for i in range(max_length):
            current_item = current_membership_gossip[i] if len(current_membership_gossip) > i else sys.maxsize
            new_gossip_item = new_membership_gossip[i] if len(new_membership_gossip) > i else sys.maxsize
            current_row = current_membership_matrix[i] if len(current_membership_gossip) > i else [sys.maxsize] * max_length
            new_row = new_membership_matrix[i] if len(new_membership_gossip) > i else [sys.maxsize] * max_length
            if i == self.server_index:
                suspect_matrix.append(self.merged_membership_suspects(current_membership_suspects, new_row))
            elif current_item < new_gossip_item:
                suspect_matrix.append(self.merged_membership_suspects(current_row, new_row))
            else:
                suspect_matrix.append(self.merged_membership_suspects(new_row, current_row))
        return suspect_matrix

    @staticmethod
    def merge_servers(current_servers, new_servers):
        return deepcopy(current_servers) if len(current_servers) > len(new_servers) else deepcopy(new_servers)

    def merge_membership_dicts(self, current_membership_dict, new_membership_dict):
        current_membership_gossip = current_membership_dict['server_configs']['gossip_list']
        new_membership_gossip = new_membership_dict['server_configs']['gossip_list']
        merged_gossip_list = self.merge_gossip_list(current_membership_gossip, new_membership_gossip)
        suspects_list = self.suspects_from_gossip(merged_gossip_list)

        suspect_matrix = self.create_suspect_matrix(current_membership_gossip,
                                                    new_membership_gossip,
                                                    suspects_list,
                                                    current_membership_dict['server_configs']['suspect_matrix'],
                                                    new_membership_dict['server_configs']['suspect_matrix'])

        merged_membership_dict = {'server_configs':{
            'servers': self.merge_servers(current_membership_dict['server_configs']['servers'],
                                          new_membership_dict['server_configs']['servers']),
            'gossip_list': merged_gossip_list,
            'suspect_list': suspects_list,
            'suspect_matrix': suspect_matrix
            }
        }
        return merged_membership_dict
