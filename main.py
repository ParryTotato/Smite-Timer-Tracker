import keyboard  # using module keyboard
import numpy as np
from PIL import ImageGrab, Image
import pytesseract
import math
import json

config = json.loads(open('config.json').read())

def format_time(min, sec):
    if sec >= 60:
        over = int(sec / 60)
        sec = sec % 60
        min = min + over
    return [min, sec]

def digit_check(x):
    return x.isdigit()

def grab_image(mode):
    x = config['x_cord']
    y = config['y_cord']
    offx = config['off_x']
    offy = config['off_y']
    
    new_size_x = 300
    new_size_y = 100
    # Grab a picture and convert to B/W 8-bit pixels
    img = ImageGrab.grab(bbox=(x, y, x + offx, y + offy)).convert('L')
    # img = img.resize((new_size_x, new_size_y), Image.ANTIALIAS)
    img.save("img.jpg")
    #helping with image processing
    img = np.array(img)
    
    result = process(img, mode)
    return result

# class Imaging:
    # def __init__(self):
    #     self.min = 100
    #     self.ocrErr = False

def process(greyImg, mode):
    # self.currentHealth
    txt = pytesseract.image_to_string(greyImg)
    # print(txt)
    if txt != '':
        time_raw = ''.join(filter(digit_check, txt))
        time_raw = time_raw.replace('-.',':')
        if len(time_raw) < 3:
            time_raw = -1
        else:
            min = int(time_raw[:-2])
            sec = int(time_raw[-2:])
            [time_add, event] = mode_switcher(mode)
            sec = sec + time_add
            [min, sec] = format_time(min, sec)
            sec_str = str(sec)
            if len(sec_str) == 1:
                sec_str = "0" + sec_str
            sb = event + " at " + str(min) + ":" + sec_str
            # print("{} at {}:{}".format(event, min, sec))
            print(sb)
            return sb

def mode_switcher(mode):
    switcher = {
        0: [160, "Beads"],
        1: [180, "Aegis"],
        2: [300, "FG"],
        3: [300, "GF"] 
    }
    return switcher.get(mode, [0, "Invalid"])

def main():
    while(True):
        if keyboard.read_key() == "home":
            keyboard.write(grab_image(0))

        if keyboard.read_key() == "end":
            keyboard.write(grab_image(1))

        if keyboard.read_key() == "page up":
            keyboard.write(grab_image(2))
        
        if keyboard.read_key() == "page down":
            keyboard.write(grab_image(3))
        # keyboard.add_hotkey('p', lambda: keyboard.write(grab_image(0)))

if __name__ == '__main__':
    main()