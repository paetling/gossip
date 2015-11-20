from .libs.listening_server import ListeningServer

def main():
    ls = ListeningServer('localhost', 80)
    ls.start()

if __name__ == '__main__':
    main()
