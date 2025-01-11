from PIL import ImageGrab, Image, UnidentifiedImageError
import time
import pyautogui # For some reason fixes screen scaling for other libraries
import autoit
import os
import keyboard
from collections import namedtuple

Pixel = namedtuple("Pixel", "r g b")
Spot = namedtuple("Spot", "x y")
Part = namedtuple("Part", "x y")
Size = namedtuple("Size", "width height")
Bias = namedtuple("Bias", "x y")
Area = namedtuple("Bias", "bottom top left right")
ScreenParams = namedtuple("ScreenParams", "canvas_area color_text_box_spot current_color_spot color_confirmation_spot")

# I/O adapters below

def get_screen_pixel(spot):
    pixel = autoit.pixel_get_color(x=spot.x, y=spot.y)
    red = pixel & 0xFF
    green = (pixel >> 8) & 0xFF
    blue = (pixel >> 16) & 0xFF
    return Pixel(red, green, blue)

def get_screen_area_pixels(area):
    return map(
        lambda pixel: Pixel(*pixel),
        ImageGrab.grab(bbox=(area.left, area.top, area.right, area.bottom)).getdata(),
    )

def make_screenshot():
    return ImageGrab.grab()

def get_screenshot_pixel(screenshot, spot):
    channels = screenshot.getpixel((spot.x, spot.y))
    return Pixel(*channels)

def get_screenshot_width(screenshot):
    return screenshot.width

def get_screenshot_height(screenshot):
    return screenshot.height

def click_mouse(spot):
    autoit.mouse_move(spot.x, spot.y, speed=0)
    autoit.mouse_move(spot.x - 1, spot.y, speed=0)
    autoit.mouse_click("left", spot.x, spot.y, speed=0)

def move_mouse(spot):
    autoit.mouse_move(spot.x, spot.y, speed=0)
    autoit.mouse_move(spot.x - 1, spot.y, speed=0)
    autoit.mouse_move(spot.x, spot.y, speed=0)

def send_ctrl_a_color_in_hex_and_enter(color):
    color_hex = "{#}%02x%02x%02x" % (color.r, color.g, color.b)
    command = "^a" + color_hex + "{ENTER}"
    autoit.send(command)

def load_quantized_image_pixels(colors_amount, file_path, target_side_size):
    return map(
        lambda color_tuple: Pixel(*color_tuple),
        Image.open(file_path).convert("RGB").quantize(colors=colors_amount).convert("RGB").resize((target_side_size, target_side_size)).getdata(),
    )

# I/O adapters above

def find_bound(screenshot, center, bias):
    current = center
    while True:
        new_spot = Spot(x=current.x + bias.x, y=current.y + bias.y)
        if get_screenshot_pixel(screenshot, new_spot) != Pixel(r=255, g=255, b=255):
            return current
        current = new_spot

def get_color_picker_spot(picker_upper_left, picker_size, part):
    return Spot(
        x=int(part.x*picker_size.width) + picker_upper_left.x,
        y=int(part.y*picker_size.height) + picker_upper_left.y,
    )

def get_screen_params():
    screenshot = make_screenshot()
    width = get_screenshot_width(screenshot)
    height = get_screenshot_height(screenshot)
    center = Spot(x=width//2, y=height//2)
    # Below constants were taken on my PC. Imprecise. Looking for better constants only resolved in conflicts
    # Not the same constant, but a good demonstration of a conflict:
    # 1080*0.525004074074074 = 567.0043999999999, 566 required => too much
    # 900*0.525004074074074 = 472.5036666666666, 473 required => too little
    picker_w_mult = 475/1920
    picker_h_mult = 473/1080
    # Constants end
    picker_size = Size(
        width=picker_w_mult * width,
        height=picker_h_mult * height,
    )
    picker_upper_left = Spot(
        x=int(width*0.40),
        y=int(height*0.30),
    )
    return ScreenParams(
        canvas_area=Area(
            bottom=find_bound(screenshot, center, Bias(x=0, y=1)).y,
            top=find_bound(screenshot, center, Bias(x=0, y=-1)).y,
            left=find_bound(screenshot, center, Bias(x=-1, y=0)).x,
            right=find_bound(screenshot, center, Bias(x=1, y=0)).x,
        ),
        color_text_box_spot=get_color_picker_spot(
            picker_upper_left, picker_size, Part(x=0.65, y=0.77),
        ),
        current_color_spot=get_color_picker_spot(
            picker_upper_left, picker_size, Part(x=1/17, y=0.77),
        ),
        color_confirmation_spot=get_color_picker_spot(
            picker_upper_left, picker_size, Part(x=0.22, y=0.77),
        ),
    )

def load_any_image_pixels(colors_amount, directory, target_side_size):
    image = None
    for file_name in os.listdir(directory):
        try:
            image = load_quantized_image_pixels(colors_amount, file_name, target_side_size)
        except (PermissionError, UnidentifiedImageError):
            pass
        else:
            break
    return image

def sort_image_pixels(image_pixels, image_side_size):
    saved_pixels = {}
    for y in range(image_side_size):
        for x in range(image_side_size):
            spot = Spot(x=x, y=y)
            current_color = next(image_pixels)
            if current_color == Pixel(r=255, g=255, b=255):
                continue
            saved_pixels.setdefault(current_color, []).append(spot)
    return saved_pixels

def check_color_in_area(area, color):
    for pixel in get_screen_area_pixels(area):
        if pixel == color:
            return True
    return False

def transform_part_to_button_spot(bottom_left, side, part):
    return Spot(x=bottom_left.x + int(part.x*side), y=bottom_left.y + int(part.y*side))

class ChangeWaiter:
    def __init__(self, spot, old_pixel):
        self.spot = spot
        self.old_pixel = old_pixel
    @classmethod
    def record(cls, spot):
        old_pixel = get_screen_pixel(spot)
        return cls(spot, old_pixel)
    def wait(self):
        while True:
            new_pixel = get_screen_pixel(spot=self.spot)
            if new_pixel != self.old_pixel:
                return ChangeWaiter(self.spot, new_pixel)

def change_color(pixel):
    # 107 161 249: "selection blue"
    pass

def draw_image(sorted_image_pixels, screen_params, canvas_side_resolution):
    side = min(
        screen_params.canvas_area.bottom - screen_params.canvas_area.top,
        screen_params.canvas_area.right - screen_params.canvas_area.left,
    )
    COLOR_PICKER_BUTTON_PART = Part(x=0.15, y=0.1)
    LAYER_1_HIDE_BUTTON_PART = Part(x=1.43, y=-0.55)
    bottom_left = Spot(
        x=screen_params.canvas_area.left,
        y=screen_params.canvas_area.bottom,
    )
    color_picker_button_spot = transform_part_to_button_spot(bottom_left, side, COLOR_PICKER_BUTTON_PART)
    layer_1_hide_button_spot = transform_part_to_button_spot(bottom_left, side, LAYER_1_HIDE_BUTTON_PART)
    move_mouse(layer_1_hide_button_spot)
    return
    move_mouse(screen_params.color_text_box_spot)
    time.sleep(1)
    move_mouse(screen_params.current_color_spot)
    time.sleep(1)
    move_mouse(screen_params.color_confirmation_spot)
    return
    for pixel, spots in sorted_image_pixels.items():
        change_color(pixel)
        for spot in spots:
            screen_pixel_spot = Spot(
                x=side / canvas_side_resolution * pixel.spot.x,
                y=side / canvas_side_resolution * pixel.spot.y,
            )
            click(screen_pixel_spot)

def main():
    CANVAS_SIDE_RESOLUTION = 200
    COLORS_AMOUNT = 255

    input_image_pixels = load_any_image_pixels(COLORS_AMOUNT, directory=".", target_side_size=CANVAS_SIDE_RESOLUTION)
    if input_image_pixels is None:
        print("Please, provide an input image.")
        exit(1)

    compressed_input_image_pixels = sort_image_pixels(input_image_pixels, image_side_size=CANVAS_SIDE_RESOLUTION)

    time.sleep(3) # Wait for the user to open Roblox

    screen_params = get_screen_params()

    draw_image(compressed_input_image_pixels, screen_params, CANVAS_SIDE_RESOLUTION)

main()
