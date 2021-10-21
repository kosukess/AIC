#マウス実行ファイル
# execute in Windows
from mouse import Mouse
import sys
import time
import signal
import msvcrt


def main():
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    ms = Mouse(h=480, w=640)
    
    while True:
        if msvcrt.kbhit():
            kb = msvcrt.getch()
            if kb.decode() == 'q':
                break
        hand_position, gesture = ms.receive_data()
        cur_cursor = ms.cursor_process(hand_position)
        ms.control_cursor(cur_cursor, gesture)
        time.sleep(0.03)

    ms.sock.close()

        
if __name__ == "__main__":
    main()