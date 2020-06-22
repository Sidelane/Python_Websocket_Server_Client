from server import ChatServer
from modules.exceptions import ServerStartupException

def main():

    server = ChatServer()

    try:
        server.run()
    except ServerStartupException:
        print("[-] Error while running the Server")

if __name__ == '__main__':
    main()
