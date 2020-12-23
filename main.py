import keyboard
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


def grab_image(mode):
    x = config['x_cord']
    y = config['y_cord']
    offx = config['off_x']
    offy = config['off_y']
    
    new_size_x = 300
    new_size_y = 100
    # Grab a picture and convert to B/W 8-bit pixels
    # album = []
    for clip in range(0,5):
        img = ImageGrab.grab(bbox=(x, y, x + offx, y + offy)).convert('L')
        img = img.resize((new_size_x, new_size_y), Image.ANTIALIAS)
        #helping with image processing
        img = np.array(img)
        result = process(img, mode)
        if type(result) == str:
            return result

    return ''

# class Imaging:
    # def __init__(self):
    #     self.min = 100
    #     self.ocrErr = False

def process(greyImg, mode):
    # self.currentHealth
    txt = pytesseract.image_to_string(greyImg)
    # print(txt)
    if txt != '':
        time_raw = ''.join(filter(lambda x: x.isdigit(), txt))
        time_raw = time_raw.replace('-.',':')
        if len(time_raw) < 3:
            print("fail")
            time_raw = -1
        else:
            min = int(time_raw[:-2])
            sec = int(time_raw[-2:])
            [time_add, event] = mode_switcher(mode)
            [min, sec] = format_time(min, sec + time_add)
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
        3: [300, "GF"],
        4: [130, "U_Beads"],
        5: [150, "U_Aegis"] 
    }
    return switcher.get(mode, [0, "Invalid"])


def send_message(mode):
    time = grab_image(mode)
    # keyboard.hook_key("w", lambda: )
    if config["use_mode"] == "no_enter":
        keyboard.send('enter')
        keyboard.write(time)
        keyboard.call_later(lambda: keyboard.send('enter'),(), 0.1)
    # keyboard.call_later(lambda: keyboard.write(time), (), 0.1)
    elif config["use_mode"] == "yes_enter":
        keyboard.write(time)
        


def main():
    while(True):
        if keyboard.read_key() == config['beads_button']:
            send_message(0)

        if keyboard.read_key() == config['aegis_button']:
            send_message(1)

        if keyboard.read_key() == config['fg_button']:
            send_message(2)

        if keyboard.read_key() == config['gf_button']:
            send_message(3)
        
        if keyboard.read_key() == config['beads_upgrade_button']:
            send_message(4)

        if keyboard.read_key() == config['aegis_upgrade_button']:
            send_message(5)
        # keyboard.add_hotkey('p', lambda: keyboard.write(grab_image(0)))

if __name__ == '__main__':
    main()
