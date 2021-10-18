from whiteboard import Whiteboard
import sys
import signal


def main():
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    wb = Whiteboard(h=480, w=640)
    key = wb.show_whiteboard()
    if  key == ord('q'):
        wb.sock.close()
        sys.exit()

    while True:
        data = wb.receive_data()
        #wb.switch(data[1])
        wb.draw(data[0], data[1])
        key = wb.show_whiteboard()
        if  key == ord('q'):
            wb.sock.close()
            break
    
if __name__ == "__main__":
    main()