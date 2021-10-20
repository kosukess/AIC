from whiteboard import Whiteboard
import sys
import signal
import numpy as np


def main():
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    wb = Whiteboard(h=480, w=640)

    while True:
        cursor_data, gesture = wb.receive_data()
        cursor = wb.cursor_process(cursor_data)
        wb.execute_function(cursor, gesture)
        key = wb.show_whiteboard(cursor)
        wb.loop_finish_process(cursor, gesture)
        if  key == ord('q'):
            wb.sock.close()
            break
    
if __name__ == "__main__":
    main()