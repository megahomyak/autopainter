from pynput import keyboard, mouse
import json
from shared import get_canvas_area
from queue import SimpleQueue

mouse_clicks = SimpleQueue()

def set_up():
    canvas_area = get_canvas_area()
    color_picker_spot = mouse_clicks.get()
    color_input_spot = mouse_clicks.get()
    color_confirmation_spot = mouse_clicks.get()
    json.dump({
        "canvas_area": canvas_area,
        "side": side,
        "bottom": bottom,
        "left": left,
        "color_picker_spot": color_picker_spot,
        "color_input_spot": color_input_spot,
        "color_confirmation_spot": color_confirmation_spot,
    }, open("settings.json", "w"))
    mouse_listener.stop()
    kb_listener.stop()

def on_press(key):
    if hasattr(key, "char") and key.char == 'r':
        set_up()

def on_click(x, y, button, pressed):
    print(x, y, button, pressed)
    if button == mouse.Button.left and pressed:
        mouse_clicks.put((x, y))

kb_listener = keyboard.Listener(on_press=on_press)
kb_listener.start()
mouse_listener = mouse.Listener(on_click=on_click)
mouse_listener.start()
print("Ready")
kb_listener.join()
mouse_listener.join()
