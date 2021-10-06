def switch(self, img):
    if self.preprocessdata.text=="click":
        pre_gesture = 5
    else:
        pre_gesture = 0
    
    if (self.preprocessdata.text=="clear")&(pre_gesture == 5):
        x_position, y_position = int(joints[8][0]), int(joint[8][1])
        color = img[x_position, y_positon]
        if color == 0:
            self.draw_or_not = self.draw_or_not*-1




