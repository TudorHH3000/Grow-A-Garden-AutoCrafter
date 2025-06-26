# Version 0.1.0

import pyautogui
import PySimpleGUIQt as sg
import time
import os
import random
import threading
from pynput import keyboard
from pynput.keyboard import Controller as keybd
from pynput.mouse import Controller as Hamster
from pynput.mouse import Button
from ahk import AHK

# changeable shit
clickx = 1370
clicky = 620
colorrbx = (39, 41, 48)
offset = 2
ingredients = 2
textcol = "#DDDDDD"
bgcol = "#212121"
elcol = "#424242"

# tracking shit
running = False
tim = "00:00:00"
runs = 0
progress = "N/A"
st_tim = None
started = False
crafting = None
selitem = None

# config
kbd = keybd()
hamster = Hamster()
pyautogui.PAUSE = (1)
ahk = AHK()
ahk.set_coord_mode("Mouse", "Screen")

#ui
layout = [
        [sg.Text('Item list', background_color=bgcol, text_color=textcol)],
        [sg.Combo(['lightning rod', 'reclaimer', 'test value'],text_color=textcol , background_color=elcol, key='doodooselect', readonly=True)],
        [sg.Button('poopoocaca', button_color=(textcol, elcol))],
        [sg.Text(text=(f"selected item: {selitem}"), key="selecttext", background_color=bgcol)],
        [sg.Text('', background_color=bgcol, key='sep1')],
        [sg.Button(button_text="macro instructions", button_color=(textcol,elcol))],
        [sg.Text('', background_color=bgcol, key='sep2', text_color=textcol)],
        [sg.Text(text=(f"runs made: {runs}"),key='runtext', background_color=bgcol)],
        [sg.Text(text=(f"time elapsed {tim}"),key='timetext', background_color=bgcol)],
        [sg.Text(text=(f"progress: {progress}"),key='progtext', background_color=bgcol)]
        ]
    

window = sg.Window(
    title="GaG AutoCrafter",
    background_color=bgcol,
    size=(200, 500),
    margins=(20, 20),
    layout=layout,
    keep_on_top=(True)
)

# exit
def ko():
    os._exit(0)

def kep(key):
    kbd.press(key)
    time.sleep(0.1)
    kbd.release(key)
    time.sleep(1) 

def hap(button):
    hamster.press(button)
    time.sleep(0.1)
    hamster.release(button)
    time.sleep(1)

def qsel():
    selitem = values['doodooselect']
    window["selecttext"].update(f"selected item: {selitem}")
    selection()

def selection():
    global crafting, ingredients
    if crafting == "lrod":
        ingredients = 3
    elif crafting == "reclaimer":
        ingredients = 2

def startmacro():
    global progress
    progress = "started"
    time.sleep(1)
    kep("e") 
    select()

def select():
    global progress, clickx, clicky
    of = random.randint(-2, 2)
    ahk.mouse_move(1370, 600, speed=0)
    time.sleep(0.1)
    ahk.mouse_move(of, of, speed=10, relative=True)
    time.sleep(0.5)
    hap(Button.left)
    progress = "selected"
    insertcraft()

def insertcraft():
    global progress, ingredients
    if ingredients == (2): # 1e2e2e, 1e2e3e3e, 1e2e3e4e4e
        kep("1")
        kep("e")
        kep("2")
        kep("e")
        kep("2")
        kep("e")     
    elif ingredients == (3):
        kep("1")
        kep("e")
        kep("2")
        kep("e")
        kep("3")
        kep("e") 
        kep("3")
        kep("e") 
    else:
        kep("1")
        kep("e")
        kep("2")
        kep("e")
        kep("3")
        kep("e") 
        kep("4")
        kep("e") 
        kep("4")
        kep("e") 
    progress = "crafting"
    checkloop()
 
def checkloop():
    global progress, colorrbx, clickx, clicky, runs
    of = random.randint(-2, 2)
    kep("e")    
    time.sleep(4)
    if pyautogui.pixelMatchesColor(1550, 500, colorrbx):
        ahk.mouse_move(clickx, clicky, speed=0)
        time.sleep(0.1)
        ahk.mouse_move(of, of, speed=10, relative=True)
        time.sleep(0.5)
        hap(Button.left)
        time.sleep(5)
        checkloop()
    else:
        runs += 1
        progress = "collected"
        time.sleep(30)
        startmacro()
    
def on_press(key):
    global running, tim, st_tim, started
    try:
        if key.char == 'k':
            ko()
        elif key.char == 'p':
            if not running:
                running = True
                if not started:
                    st_tim = time.time()
                    started = True
                threading.Thread(target=startmacro, daemon=True).start()
    except AttributeError:
        pass

listener = keyboard.Listener(on_press=on_press)
listener.start()

# keep window
while True:
    if started == True:
        elapsed = int(time.time() - st_tim)
        h,rem = divmod(elapsed, 3600)
        m,s = divmod(rem, 60)
        tim = f"{h:02}:{m:02}:{s:02}"
        window['timetext'].update(f"time elapsed: {tim}")
        window['runtext'].update(f"runs made: {runs}")
        window['progtext'].update(f"stage: {progress}")

    event, values = window.read(timeout=100)

    if event== sg.WIN_CLOSED:
        break

    if event == 'poopoocaca':
        if values['doodooselect'] == 'lightning rod':
            crafting = "lrod"
            qsel()
        elif values['doodooselect'] == 'reclaimer':
            crafting = 'reclaimer'
            qsel()
        else:
            sg.popup("this item has not been implemented yet", title="Not implmented", keep_on_top=True, background_color='#212121', text_color=textcol, button_color=(textcol, elcol))
