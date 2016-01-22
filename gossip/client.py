import socket
import logging

from libs.constants import (INITIAL_CONFIG, BASE_CONFIG_FILE, PORT_START,
                            MAIN_ADDRESS, MAIN_PORT, COMMAND_STRING, STRING_TERMINATOR)

def send_string(socket, string):
    socket.send(string.encode('utf-8'))

def main():
    command = input("What would you like to run:")
    s = socket.socket()
    try:
        logging.info('Sending {} to MAIN'.format(command))
        s.connect((MAIN_ADDRESS, MAIN_PORT))
        send_string(s, "{}{}".format(COMMAND_STRING, command))
        send_string(s, STRING_TERMINATOR)
    except Exception as e:
        logging.error("An error occurred: {}".format(e))

if __name__ == "__main__":
    main()
