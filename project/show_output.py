from whiteboard import Whiteboard


def main():
    wb = Whiteboard(h=480, w=640)
    while True:
        data = wb.receive_data()
        wb.switch(data[1])
        wb.draw(data[0], data[1])
        key = wb.show_whiteboard()
        if  key == ord('q'):
            wb.sock.close()
            break
    
if __name__ == "__main__":
    main()
    





        



