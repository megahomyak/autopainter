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

spots = SimpleQueue()

keyboard.add_hotkey("c", lambda: spots.put(mouse.get_position()))

print("Listening for mouse positions... (1)")
color_picker_spot = spots.get()
print("Listening for mouse positions... (2)")
color_input_spot = spots.get()
print("Listening for mouse positions... (3)")
color_confirmation_spot = spots.get()
print("Listening for mouse positions... (4)")
current_color_spot = spots.get()
print("Listening for mouse positions... (5)")
color_picker_check_spot = spots.get()
json.dump({
    "canvas_area": canvas_area,
    "color_picker_spot": color_picker_spot,
    "color_input_spot": color_input_spot,
    "color_confirmation_spot": color_confirmation_spot,
    "colors_count": 256,
    "canvas_side_resolution": 200,
    "color_picker_check_spot": color_picker_check_spot,
    "current_color_spot": current_color_spot,
}, open("settings.txt", "w"))
