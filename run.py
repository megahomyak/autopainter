import json
try:
    settings = json.load(open("settings.txt"))
except FileNotFoundError:
    print("Please, run `setup.bat` first. Read the instruction to know how.")
    input("You can close this window.")
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
    print("An input image was not provided. Please, provide an input image.")
    input("You can close this window.")
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

while expected_canvas_area != get_canvas_area():
    pass

def click_gui(spot):
    autoit.mouse_move(spot[0], spot[1], speed=2)
    autoit.mouse_down("left")
    time.sleep(0.1)
    autoit.mouse_up("left")
    time.sleep(0.1)

def paint(spot):
    autoit.mouse_move(spot[0], spot[1], speed=2)
    autoit.mouse_down("left")
    time.sleep(0.1)
    autoit.mouse_up("left")
    time.sleep(0.1)

for color, spots in colors.items():
    time.sleep(0.3)
    click_gui(settings["color_picker_spot"])
    time.sleep(0.3)
    click_gui(settings["color_input_spot"])
    time.sleep(0.3)
    autoit.send("^a")
    time.sleep(0.3)
    autoit.clip_put("#%02x%02x%02x" % color)
    autoit.send("^v")
    time.sleep(0.3)
    autoit.send("{ENTER}")
    time.sleep(0.3)
    click_gui(settings["color_confirmation_spot"])
    time.sleep(0.3)
    for spot in spots:
        if keyboard.is_pressed("backspace"):
            exit(0)
        if keyboard.is_pressed("enter"):
            time.sleep(10)
            while keyboard.read_key() != "enter":
                pass
        screen_spot = (
            settings["canvas_area"]["left"] + int(canvas_pixel_size * (spot[0] + 0.5)),
            settings["canvas_area"]["top"] + int(canvas_pixel_size * (spot[1] + 0.5)),
        )
        paint(screen_spot)
