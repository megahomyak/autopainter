from PIL import ImageGrab, Image, UnidentifiedImageError
from types import SimpleNamespace as SN
import time
import pyautogui # For some reason fixes screen scaling for other libraries
import autoit
import os
import keyboard

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
        except:
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

main()
