import socket
import logging
import sys

from libs.constants import (INITIAL_CONFIG, BASE_CONFIG_FILE, PORT_START,
                            MAIN_ADDRESS, MAIN_PORT, COMMAND_STRING, STRING_TERMINATOR)

def send_string(socket, string):
    socket.send(string.encode('utf-8'))

def main():
    command = input("What would you like to run:")
    logging.error(command)
    s = socket.socket()
    try:
        logging.error('Sending {} to MAIN'.format(command))
        s.connect((MAIN_ADDRESS, MAIN_PORT))
        send_string(s, "{}{}".format(COMMAND_STRING, command))
        send_string(s, STRING_TERMINATOR)

        while True:
            data = s.recv(65535)
            if data:
                data = data.decode('utf-8')
                stripped = data.replace(STRING_TERMINATOR, '')
                sys.stdout.write(stripped)
                if STRING_TERMINATOR in data:
                    break
    except Exception as e:
        logging.error("An error occurred: {}".format(e))

if __name__ == "__main__":
    main()
