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
Bias = namedtuple("Bias", "x y")
Bounds = namedtuple("Bias", "bottom top left right")

# I/O adapters below

def get_screen_pixel(spot):
    return Pixel(ImageGrab.grab(bbox=(spot.x, spot.y, spot.x, spot.y))[0][0])

def get_screen_width():
    return ImageGrab.grab().width

def get_screen_height():
    return ImageGrab.grab().height

def mouse_click(spot):
    autoit.mouse_click("left", spot.x, spot.y, speed=0)

def mouse_move(spot):
    autoit.mouse_move(spot.x, spot.y, speed=0)

def send_ctrl_a_color_in_hex_and_enter(color):
    color_hex = "{#}%02x%02x%02x" % (color.r, color.g, color.b)
    command = "^a" + color_hex + "{ENTER}"
    autoit.send(command)

def load_quantized_image_pixels(colors_amount, file_path, target_side_size):
    return map(
        lambda color_tuple: Pixel(color_tuple),
        Image.open(file_path).convert("RGB").quantize(colors=colors_amount).resize((target_side_size, target_side_size)).getdata(),
    )

# I/O adapters above

def get_screen_canvas_bounds():
    center = Spot(x=get_screen_width()//2, y=get_screen_height()//2)
    def find_bound(bias):
        current = center
        while True:
            new_spot = Spot(x=current.x + bias.x, y=current.y + bias.y)
            if get_screen_pixel(new_spot) != Pixel(r=255, g=255, b=255):
                return current
            current = new_spot
    return Bounds(
        bottom=bound_finder.find_bound(Bias(x=0, y=1)).y,
        top=bound_finder.find_bound(Bias(x=0, y=-1)).y,
        left=bound_finder.find_bound(Bias(x=-1, y=0)).x,
        right=bound_finder.find_bound(Bias(x=1, y=0)).x,
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

def compress_image_pixels(image_pixels, image_side_size, quantization_threshold):
    saved_pixels = {}
    for y in range(image_side_size):
        for x in range(image_side_size):
            spot = Spot(x=x, y=y)
            current_color = next(image_pixels)
            if current_color == Pixel(r=255, g=255, b=255):
                continue
            saved_pixels.setdefault(current_color, []).append(spot)
    return saved_pixels

def transform_part_to_gui_spot(bottom_left, side, part):
    return Spot(x=bottom_left.x + int(part.x*side), y=bottom_left.y + int(part.y*side))

class ChangeWaiter:
    def __init__(self, bottom_left, side, bias):
        self.spot = transform_bias_to_gui_spot(bias)
        self.old_pixel = get_screen_pixel(self.spot)
    def wait(self):
        while True:
            new_pixel = get_screen_pixel(spot=self.spot)
            if new_pixel != self.old_pixel:
                self.old_pixel = new_pixel
                break

def draw_image(compressed_image_pixels, screen_canvas_bounds, canvas_side_pixels):
    side = min(screen_canvas_bounds.bottom - screen_canvas_bounds.top, screen_canvas_bounds.right - screen_canvas_bounds.left)
    bottom_left = Spot(x=screen_canvas_bounds.left, y=screen_canvas_bounds.bottom)
    move(transform_part_to_gui_spot(part=Part(x=0.2, y=-0.13)))
    return
    for pixel, spots in compressed_image_pixels.items():
        change_color(pixel.color)
        for spot in spots:
            screen_pixel_spot = Spot(
                x=side / canvas_side_pixels * pixel.spot.x,
                y=side / canvas_side_pixels * pixel.spot.y,
            )
            click(screen_pixel_spot)

def main():
    CANVAS_SIDE_PIXELS = 338
    COLORS_AMOUNT = 255

    input_image_pixels = load_any_image_pixels(COLORS_AMOUNT, directory=".", target_side_size=CANVAS_SIDE_PIXELS)
    if input_image_pixels is None:
        print("Please, provide an input image.")
        exit(1)

    compressed_input_image_pixels = compress_image_pixels(input_image_pixels, image_side_size=CANVAS_SIDE_PIXELS, quantization_threshold=QUANTIZATION_THRESHOLD)

    time.sleep(3) # Wait for the user to open Roblox

    screen_canvas_bounds = get_screen_canvas_bounds()

    draw_image(compressed_input_image_pixels, screen_canvas_bounds, CANVAS_SIDE_PIXELS)

main()

























# OLD CODE BELOW

# Image interactor adapters:

def make_screenshot(area=None):
    move(SN(x=0, y=0))
    if area is not None:
        area = (area.left, area.top, area.right, area.bottom)
    return ImageGrab.grab(bbox=area)

def get_pixel(image, spot):
    r,g,b = image.getpixel((spot.x, spot.y))
    return SN(r=r, g=g, b=b)

def get_width(image):
    return image.width

def get_height(image):
    return image.height

def get_input_image(directory):
    image = None
    for file_name in os.listdir(directory):
        try:
            image = Image.open(file_name)
        except ValueError:
            pass
        else:
            break
    return image

def resize(image, new_size):
    return image.resize((new_size.width, new_size.height))

# Image interactor adapters end

# Gui interactor adapters:

def click(spot):
    autoit.mouse_click("left", spot.x, spot.y, speed=2)

def move(spot):
    autoit.mouse_move(spot.x, spot.y, speed=0)

def enter_text(text):
    autoit.send(text.replace("#", "{#}"))
    time.sleep(0.5)

def hold_ctrl_and_enter_text(text):
    autoit.send("^" + text.replace("#", "{#}"))
    time.sleep(0.5)

# Gui interactor adapters end

class BoundFinder:
    def __init__(self, screenshot):
        self.center = SN(x=get_width(screenshot)//2, y=get_height(screenshot)//2)
        self.screenshot = screenshot
    def find_bound(self, bias):
        current = self.center
        while True:
            new = SN(x=current.x + bias.x, y=current.y + bias.y)
            if get_pixel(image=self.screenshot, spot=new) != SN(r=255, g=255, b=255):
                return current
            current = new

def paint(spot):
    click(spot)
    time.sleep(0.01)

def iter_pixels(image):
    for x in range(get_width(image)):
        for y in range(get_height(image)):
            spot = SN(x=x, y=y)
            pixel = get_pixel(image, spot)
            yield (spot, pixel)

class PixelSizeMeasurer:
    def __init__(self, center, canvas_area, pick_color):
        self.canvas_area = canvas_area
        self.center = center
        self.pick_color = pick_color
    def measure(self):
        self.pick_color(SN(r=255, g=0, b=0))
        paint(self.center)
        time.sleep(0.5) # Painting still takes some time
        screenshot = make_screenshot(area=self.canvas_area)
        top = float("+inf")
        bottom = float("-inf")
        left = float("+inf")
        right = float("-inf")
        for spot, pixel in iter_pixels(screenshot):
            if pixel == SN(r=255, g=0, b=0):
                if spot.x < left:
                    left = spot.x
                elif spot.x > right:
                    right = spot.x
                if spot.y > bottom:
                    bottom = spot.y
                elif spot.y < top:
                    top = spot.y
        return min(bottom - top, right - left)

class GuiInteractors:
    def __init__(self, bottom_left, side):
        self.side = side
        self.bottom_left = bottom_left

    def click_gui(self, bias):
        click(spot=SN(x=self.bottom_left.x + int(bias.x*self.side), y=self.bottom_left.y + int(bias.y*self.side)))
        time.sleep(0.5)

    def pick_color(self, color):
        color_hex = "#%02x%02x%02x" % (color.r, color.g, color.b)

        self.click_gui(bias=SN(x=0.2, y=0.1)) # Open the color picker
        self.click_gui(bias=SN(x=0.7, y=-0.13)) # Switch to color field
        hold_ctrl_and_enter_text("a") # Select the current color
        enter_text(color_hex) # Write the new color
        self.click_gui(bias=SN(x=0.38, y=-0.13)) # Confirm color

def main():
    input_image = get_input_image(".")
    if input_image is None:
        print("Please, provide an input image.")
        exit(1)

    time.sleep(3) # Wait for the user to open Roblox

    bound_finder = BoundFinder(screenshot=make_screenshot())

    bottom = bound_finder.find_bound(bias=SN(x=0, y=1)).y
    top = bound_finder.find_bound(bias=SN(x=0, y=-1)).y
    left = bound_finder.find_bound(bias=SN(x=-1, y=0)).x
    right = bound_finder.find_bound(bias=SN(x=1, y=0)).x
    
    side = bottom - top
    bottom_left = SN(x=left, y=bottom)
    
    gui_interactors = GuiInteractors(bottom_left, side)

    pixel_size = PixelSizeMeasurer(center=bound_finder.center, canvas_area=SN(bottom=bottom, top=top, left=left, right=right), pick_color=gui_interactors.pick_color).measure()
    side_pixels = side // pixel_size
    print(side_pixels)
    return

    input_image = resize(input_image, SN(width=side_pixels, height=side_pixels))
    colors_to_spots = {}
    for spot, pixel in iter_pixels(input_image):
        if pixel == SN(r=255, g=255, b=255): continue
        canvas_spot = SN(x=left + spot.x*pixel_size+1, y=top + spot.y*pixel_size+1) # IDK why +1
        colors_to_spots.setdefault((pixel.r, pixel.g, pixel.b), []).append(canvas_spot)

    for color, spots in colors_to_spots.items():
        color = SN(r=color[0], g=color[1], b=color[2])
        gui_interactors.pick_color(color)
        for spot in spots:
            if keyboard.is_pressed("q"):
                exit(0)
            click(spot)
