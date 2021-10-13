import socket
import time
import signal
import sys
import pickle

class server():
    def __init__(self) -> None:
        self.M_SIZE = 1024
        host = '192.168.55.1'
        port = 30001
        locaddr = (host, port)

        # ①ソケットを作成する
        self.sock = socket.socket(socket.AF_INET, type=socket.SOCK_DGRAM)
        print('create socket')

        # ②自ホストで使用するIPアドレスとポート番号を指定
        self.sock.bind(locaddr)

        signal.signal(signal.SIGINT, self.handler)
        
    def handler(self, signum, frame):
        print("\nclose socket")
        self.sock.close()
        print("pushed Ctrl-C")
        sys.exit(0)

    def server(self):
        while True:
            # ③Clientからのmessageの受付開始
            #print('Waiting message')
            message, cli_addr = self.sock.recvfrom(self.M_SIZE)
            message = pickle.loads(message)
            print(f'Received message is [{message}]')

if __name__ == "__main__":
    a = server()
    a.server()