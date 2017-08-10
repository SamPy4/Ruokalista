from pynput.keyboard import Key, Listener
import os

def on_press(key):
    if key == Key.ctrl_r:
        print("OPEN")
        os.system("main_ruokalista.py")

with Listener(on_press=on_press) as listener:
    listener.join()
