# Smite Insta Timer
A python app that will write timers to team chat in Smite when certain buttons are pressed.

The OCR that the program uses is Tesseract OCR. You can download it [here](https://github.com/tesseract-ocr/tessdoc/blob/master/Downloads.md)

The configuration file has coordinates which are for locating the timer, which you can change as needed.
It also allows you to set custom keybinds for events
Two modes of timing are accepted: "no_enter" where you just press the button at once, and "yes_enter" where you have to press enter manually to open the text chat and send message

#Installation
Open cmd prompt in windows or a terminal in linux and run the following.
```
pip install -r requirements.txt
```

#Running
```
python main.py
```
