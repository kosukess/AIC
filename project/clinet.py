import cv2
import time
import socket 
import signal
import sys
import pickle

class client():
    def handler(self, signum, frame):
        print("\nclose socket")
        self.sock.close()
        sys.exit(0)

    def client(self):
        M_SIZE = 1024

        # Serverのアドレスを用意。Serverのアドレスは確認しておく必要がある。
        serv_address = ('192.168.55.1', 30001)
        cli_address = ('192.168.55.1', 30000)

        # ①ソケットを作成する
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(cli_address)

        signal.signal(signal.SIGINT, self.handler)

        while True:
            # ②messageを送信する
            print('Input any messages, Type [end] to exit')
            message = input()
            if message != 'end':
                data = [message]
                send_len = self.sock.sendto(pickle.dumps(data), serv_address)
                # ※sendtoメソッドはkeyword arguments(address=serv_addressのような形式)を受け付けないので注意

            else:
                print('closing socket')
                self.sock.close()
                print('done')
                break


if __name__ == "__main__":
    a = client()
    a.client()