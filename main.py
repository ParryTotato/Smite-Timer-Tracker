import keyboard
import numpy as np
from PIL import ImageGrab
import pytesseract
import json
from pynput.keyboard import Key, Listener, KeyCode

config = json.loads(open('config.json').read())

def print_controls():
    print("\n\nCONTROLS:")
    
    for event in config['events']:
        print(config['events'][event]['event_name'] + ": " + config['events'][event]['key'])
    
    print("\n")

def format_time(min, sec):
    if sec >= 60:
        over = int(sec / 60)
        sec = sec % 60
        min = min + over
    return [min, sec]


def event_getter(event):
    return [config['events'][event]['timer'], config['events'][event]['event_name']]


def process(greyImg, event):
    txt = pytesseract.image_to_string(greyImg)
    if txt != '':
        time_raw = ''.join(filter(lambda x: x.isdigit(), txt))
        time_raw = time_raw.replace('-.', ':')
        if len(time_raw) < 3:
            print("bad key reading")
            time_raw = -1
        else:
            min = int(time_raw[:-2])
            sec = int(time_raw[-2:])
            [time_add, event] = event_getter(event)
            [min, sec] = format_time(min, sec + time_add)
            sec_str = str(sec)
            if len(sec_str) == 1:
                sec_str = "0" + sec_str
            sb = event + " at " + str(min) + ":" + sec_str
            print(sb)
            return sb


def grab_image(event):
    x = config['x_cord']
    y = config['y_cord']
    off_x = config['off_x']
    off_y = config['off_y']

    # Grab a picture and convert to B/W 8-bit pixels
    img = ImageGrab.grab(bbox=(x, y, x + off_x, y + off_y)).convert('L')
    # img = img.resize((new_size_x, new_size_y), Image.ANTIALIAS)
    # img = cv2.resize(img, None, fx=1.2, fy=1.2, interpolation=cv2.INTER_CUBIC)
    # img.save("img.jpg")

    # helping with image processing
    img = np.array(img)
    result = process(img, event)
    if type(result) == str:
        return result
    return ''


def send_message(event):
    time = grab_image(event)
    if config["use_mode"] == "no_enter":
        keyboard.send('enter')
        keyboard.write(time)
        # keyboard.send(time)
        # keyboard.call_later(lambda: keyboard.send('space'),(), 0.1)
        # for letter in time:
        #     keyboard.send(letter)
        keyboard.call_later(lambda: keyboard.send('enter'), (), 0.1)
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
        #print('\x03')
        print("Bye!")
        return False

    elif frmt == config['controls_key']:
        print_controls()

    else:
        for event in config['events']:
            if frmt == config['events'][event]['key']:
                send_message(event)


def on_press(key):
    print('{0} pressed'.format(key))


print("Press " + config['controls_key'] + " to view controls.\nPress " + config['exit_key'] + " to end program.")

with Listener(
        on_press = None,
        on_release = key_reader) as listener:
    listener.join()
