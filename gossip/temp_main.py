from libs.listening_server import ListeningServer
from libs.constants import INITIAL_CONFIG, CONFIG_FILE
import logging


def setup_config():
    with open(INITIAL_CONFIG, 'r') as f1:
        with open(CONFIG_FILE, 'w+') as f2:
            f2.write(f1.read())

def main():
    setup_config()
    logging.error("Starting the listening server")
    ls = ListeningServer('localhost', 80)
    ls.start()

if __name__ == '__main__':
    main()
