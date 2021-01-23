import keyboard
import numpy as np
from PIL import ImageGrab
import pytesseract
import json
from pynput.keyboard import Key, Listener, KeyCode

config = json.loads(open('config.json').read())


def format_time(min, sec):
    if sec >= 60:
        over = int(sec / 60)
        sec = sec % 60
        min = min + over
    return [min, sec]


def mode_switcher(mode):
    switcher = {
        'beads': [config['beads']['timer'], config['beads']['event']],
        'u_beads': [config['beads_upgrade']['timer'], config['beads_upgrade']['event']],
        'aegis': [config['aegis']['timer'], config['aegis']['event']],
        'u_aegis': [config['aegis_upgrade']['timer'], config['aegis_upgrade']['event']],
        'gf': [config['gf']['timer'], config['gf']['event']],
        'fg': [config['fg']['timer'], config['fg']['event']]
    }
    return switcher.get(mode, [0, "Invalid"])


def process(greyImg, mode):
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
            [time_add, event] = mode_switcher(mode)
            [min, sec] = format_time(min, sec + time_add)
            sec_str = str(sec)
            if len(sec_str) == 1:
                sec_str = "0" + sec_str
            sb = event + " at " + str(min) + ":" + sec_str
            print(sb)
            return sb


def grab_image(mode):
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
    result = process(img, mode)
    if type(result) == str:
        return result
    return ''


def send_message(mode):
    time = grab_image(mode)
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


def key_reader(key, ):
    frmt = format(key)
    if frmt != "\"\'\"":
        frmt = frmt.replace('\'', '')
        if 'Key.' in frmt:
            frmt = frmt.replace('Key.', '')
    else:
        frmt = frmt.replace('\"', '')

    if frmt == config['exit_key']:
        #print('\x03')
        return False

    if frmt == config['beads']['key']:
        send_message('beads')

    if frmt == config['beads_upgrade']['key']:
        send_message('u_beads')

    if frmt == config['aegis']['key']:
        send_message('aegis')

    if frmt == config['aegis_upgrade']['key']:
        send_message('u_aegis')
    
    if frmt == config['gf']['key']:
        send_message('gf')

    if frmt == config['fg']['key']:
        send_message('fg')


def on_press(key):
    print('{0} pressed'.format(key))


with Listener(
        on_press = on_press,
        on_release = key_reader) as listener:
    listener.join()