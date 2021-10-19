#マウス実行ファイル
from mouse import Mouse as ms
import sys
import signal


def main():
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    
    while True:
        data = ms.receive_data()
        ms.control_cursor(data[0], data[1])
        
if __name__ == "__main__":
    main()