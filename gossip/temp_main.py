from libs.listening_server import ListeningServer
import logging

def main():
    logging.error("Starting the listening server")
    ls = ListeningServer('localhost', 80)
    ls.start()

if __name__ == '__main__':
    main()
