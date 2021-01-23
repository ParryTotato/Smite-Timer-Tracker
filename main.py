import keyboard
import numpy as np
from PIL import ImageGrab, Image
import pytesseract
import math
import json
from pynput.keyboard import Key, Listener
# import cv2

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
    
    # new_size_x = 300
    # new_size_y = 100
    result = ''
    # Grab a picture and convert to B/W 8-bit pixels
    # album = []
    print("something pressed")
    # for clip in range(0,5):
    img = ImageGrab.grab(bbox=(x, y, x + offx, y + offy)).convert('L')
    # img = img.resize((new_size_x, new_size_y), Image.ANTIALIAS)
    # img = cv2.resize(img, None, fx=1.2, fy=1.2, interpolation=cv2.INTER_CUBIC)
    # img.save("img.jpg")
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
    # Alex is the GOAT
    switcher = {
        0: [config['beads']['timer'], config['beads']['event']],
        1: [config['beads_upgrade']['timer'], config['beads_upgrade']['event']],
        2: [config['aegis']['timer'], config['aegis']['event']],
        3: [config['aegis_upgrade']['timer'], config['aegis_upgrade']['event']],
        4: [config['gf']['timer'], config['gf']['event']],
        5: [config['fg']['timer'], config['fg']['event']]
    }
    return switcher.get(mode, [0, "Invalid"])


def send_message(mode):
    time = grab_image(mode)
    # keyboard.hook_key("w", lambda: )
    if config["use_mode"] == "no_enter":
        keyboard.send('enter')
        keyboard.write(time)
        # keyboard.send(time)
        # keyboard.call_later(lambda: keyboard.send('space'),(), 0.1)
        # for letter in time:
        #     keyboard.send(letter)
        keyboard.call_later(lambda: keyboard.send('enter'),(), 0.1)
    # keyboard.call_later(lambda: keyboard.write(time), (), 0.1)
    elif config["use_mode"] == "yes_enter":
        keyboard.write(time)
        
def key_reader(key):
    frmt = format(key)
    if frmt != "\"\'\"":
        frmt = frmt.replace('\'', '')
        if 'Key.' in frmt:
            frmt = frmt.replace('Key.', '')
    else:
        frmt = frmt.replace('\"', '')

    if frmt == config['exit_key']:
        # Stop listener
        return False


    if frmt == config['beads']['key']:
        send_message(0)

    if frmt == config['beads_upgrade']['key']:
        send_message(1)

    if frmt == config['aegis']['key']:
        send_message(2)

    if frmt == config['aegis_upgrade']['key']:
        send_message(3)
    
    if frmt == config['gf']['key']:
        send_message(4)

    if frmt == config['fg']['key']:
        send_message(5)

def on_press(key):
    print('{0} pressed'.format(key))

with Listener(
        on_press = None,
        on_release = key_reader) as listener:
    listener.join()
