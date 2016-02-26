import logging
import os
from copy import deepcopy
import multiprocessing
import socket
import sys
import yaml

from libs.gossip_server import ListeningServer
from libs.gossiper import Gossiper
from libs.common import get_config_file_name, save_membership, load_membership
from libs.constants import (INITIAL_CONFIG, BASE_CONFIG_FILE, PORT_START,
                            MAIN_ADDRESS, MAIN_PORT, COMMAND_STRING, STRING_TERMINATOR)

logging.getLogger().setLevel(0)
servers = [None]*1000
gossipers = [None]*1000


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

def setup_server(index, server_configs, file_lock):
    logging.info("Starting the {} listening server".format(index))
    ls = ListeningServer(index, server_configs['server_configs']['servers'][index])
    process = multiprocessing.Process(target=ls.start, args=(file_lock,))
    process.daemon = True
    process.start()
    return process

def setup_gossiper(index, file_lock):
    logging.info("Start the {} gossiper".format(index))
    gossiper = Gossiper(index)
    process = multiprocessing.Process(target=gossiper.gossip, args=(file_lock,))
    process.daemon = True
    process.start()
    return process

def ensure_config_large_enough(index, server_configs):
    current_configs = deepcopy(server_configs)
    current_length = len(current_configs['server_configs']['servers'])
    if index >= current_length:
        extra_length = index + 1 - current_length
        current_configs['server_configs']['servers'] += [{'address': 'localhost', 'port': get_port(current_length + i)} for i in range(extra_length)]
        current_configs['server_configs']['gossip_list'] += [0]*extra_length
        current_configs['server_configs']['suspect_list'] += [0]*extra_length
        current_configs['server_configs']['suspect_matrix'] += [[0]*current_length for _ in range(extra_length)]
        for i in range(len(current_configs['server_configs']['suspect_matrix'])):
            current_configs['server_configs']['suspect_matrix'][i] += [0]*extra_length

    return current_configs

def setup_gossip_for_index(index, server_configs=None):
    logging.info("SETTING UP SERVER {}".format(index))
    if server_configs is None:
        server_configs = get_live_config()
        server_configs = ensure_config_large_enough(index, server_configs)
    file_lock = multiprocessing.Lock()
    create_base_config_file(index, server_configs)
    servers[index] = setup_server(index, server_configs, file_lock)
    gossipers[index] = setup_gossiper(index, file_lock)

def kill_index(index):
    logging.info("KILLING SERVER {}".format(index))
    server = servers[index]
    servers[index] = None
    gossiper = gossipers[index]
    gossipers[index] = None

    server.terminate()
    gossiper.terminate()

def read_data(conn):
    data = conn.recv(4096).decode('utf-8')
    return data

def get_live_config():
    for i, process in enumerate(servers):
        if process is not None:
            return load_membership(get_config_file_name(i))

def list_state(socket):
    current_config = get_live_config()
    socket.send('Current State of world as seen by server 1:\n'.encode('utf-8'))
    socket.send('GOSSIP LIST\n'.encode('utf-8'))
    socket.send(str(current_config['server_configs']['gossip_list']).encode('utf-8'))
    socket.send('\n'.encode('utf-8'))
    socket.send('SUSPECT LIST\n'.encode('utf-8'))
    socket.send(str(current_config['server_configs']['suspect_list']).encode('utf-8'))
    socket.send('\n'.encode('utf-8'))

def run_command_from_client(data, server_configs, socket):
    arguments = yaml.load(data.replace(COMMAND_STRING, '').replace(STRING_TERMINATOR, '')).split(' ')
    logging.info('ARGUMENTS: {}'.format(arguments))
    if arguments[0] == 'LIST':
        list_state(socket)
        socket.send(STRING_TERMINATOR.encode('utf-8'))
    elif arguments[0] == 'ENSURE':
        setup_gossip_for_index(int(arguments[1]))
        socket.send(STRING_TERMINATOR.encode('utf-8'))
    elif arguments[0] == 'KILL':
        kill_index(int(arguments[1]))
        socket.send(STRING_TERMINATOR.encode('utf-8'))


def main():
    servers_to_start = int(os.getenv("SERVERS_TO_START"))
    logging.info("SERVERS TO START: {}".format(servers_to_start))
    server_configs = initial_membership_dict(servers_to_start)

    for index in range(servers_to_start):
        setup_gossip_for_index(index, server_configs)

    while True:
        s = socket.socket()
        s.bind((MAIN_ADDRESS, MAIN_PORT))
        s.listen()
        logging.info("Starting up MAIN server on {}".format((MAIN_ADDRESS, MAIN_PORT)))
        while True:
            from_conn, from_address = s.accept()
            logging.info("MAIN got a connection from client {}".format(from_address[1]))
            while True:
                data = read_data(from_conn)
                if COMMAND_STRING in data:
                    run_command_from_client(data, server_configs, from_conn)
                if STRING_TERMINATOR in data:
                    logging.info("Ending connection")
                    break


if __name__ == '__main__':
    main()
