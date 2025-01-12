import pyautogui # For some reason fixes screen scaling for other libraries
import keyboard
import mouse
import json
from shared import get_canvas_area
from queue import SimpleQueue

print("Ready")

while keyboard.read_key() != "r":
    pass

print("Taking a screenshot...")
canvas_area = get_canvas_area()

mouse_clicks = SimpleQueue()

mouse.on_click(lambda: mouse_clicks.put(mouse.get_position()))

print("Listening for mouse clicks... (1)")
color_picker_spot = mouse_clicks.get()
print("Listening for mouse clicks... (2)")
color_input_spot = mouse_clicks.get()
print("Listening for mouse clicks... (3)")
color_confirmation_spot = mouse_clicks.get()
json.dump({
    "canvas_area": canvas_area,
    "color_picker_spot": color_picker_spot,
    "color_input_spot": color_input_spot,
    "color_confirmation_spot": color_confirmation_spot,
    "colors_count": 256,
    "canvas_side_resolution": 200,
}, open("settings.txt", "w"))
