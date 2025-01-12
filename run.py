import json
try:
    settings = json.load(open("settings.txt"))
except FileNotFoundError:
    print("Please, run `setup.bat` first. Read the instruction to know how. Afterwards, run this program again.")
    input("Close this window manually.")
    exit(1)

import pyautogui # For some reason fixes screen scaling for other libraries
from shared import get_canvas_area
import os
from PIL import Image, UnidentifiedImageError
import time
import autoit
import keyboard

canvas_pixel_size = settings["canvas_area"]["side"] / settings["canvas_side_resolution"]
expected_canvas_area = settings["canvas_area"]

image = None
for file_name in os.listdir("."):
    try:
        image = Image.open(file_name).convert("RGB").resize((settings["canvas_side_resolution"], settings["canvas_side_resolution"]), resample=Image.Resampling.NEAREST).quantize(colors=settings["colors_count"])
    except (PermissionError, UnidentifiedImageError):
        pass
if image is None:
    print("Please, provide an input image and run the program again.")
    input("Close this window manually.")
    exit(1)
inverse_palette = {
    v: k
    for k, v in image.palette.colors.items()
}

colors = {}
for x in range(image.width):
    for y in range(image.height):
        pixel = inverse_palette[image.getpixel((x, y))]
        if pixel != (255, 255, 255):
            colors.setdefault(pixel, []).append((x, y))

def get_screen_pixel(spot):
    pixel_num = autoit.pixel_get_color(*spot)
    r = pixel_num & 0xFF
    g = (pixel_num >> 8) & 0xFF
    b = (pixel_num >> 16) & 0xFF
    return (r, g, b)

class UpdateChecker:
    def __init__(self, spot):
        self.spot = spot
        self.old = get_screen_pixel(spot)
    def __enter__(self, *_, **__):
        pass
    def __exit__(self, *_, **__):
        while self.old == get_screen_pixel(self.spot):
            pass

def click_gui(spot):
    autoit.mouse_move(spot[0], spot[1], speed=0)
    autoit.mouse_down("left")
    time.sleep(0.2)
    autoit.mouse_up("left")

def paint(spot):
    autoit.mouse_move(spot[0], spot[1], speed=0)
    autoit.mouse_click("left")

while expected_canvas_area != get_canvas_area():
    pass

first_run = False
for color, spots in colors.items():
    with UpdateChecker(settings["color_picker_check_spot"]):
        click_gui(settings["color_picker_spot"])
    if not first_run:
        checker = UpdateChecker(settings["current_color_spot"])
        checker.__enter__()
    click_gui(settings["color_input_spot"])
    time.sleep(0.4)
    autoit.send("^a")
    time.sleep(0.2)
    autoit.send("{#}%02x%02x%02x" % color)
    time.sleep(0.2)
    autoit.send("{ENTER}")
    if first_run:
        time.sleep(0.5)
        first_run = False
    else:
        checker.__exit__()
    with UpdateChecker(settings["color_picker_check_spot"]):
        click_gui(settings["color_confirmation_spot"])
    for spot in spots:
        if keyboard.is_pressed("q"):
            exit(0)
        if keyboard.is_pressed("p"):
            time.sleep(10)
            while keyboard.read_key() != "p":
                pass
        screen_spot = (
            settings["canvas_area"]["left"] + int(canvas_pixel_size * (spot[0] + 0.5)),
            settings["canvas_area"]["top"] + int(canvas_pixel_size * (spot[1] + 0.5)),
        )
        paint(screen_spot)
        time.sleep(0.01)
