from PIL import ImageGrab
from types import SimpleNamespace as SN
import time
import pyautogui # For some reason helps with scaled screens on Windows when imported and used with pydirectinput
import pydirectinput

# Screen interactor adapters:

def make_screenshot(area=None):
    if area is not None:
        area = (area.left, area.top, area.right, area.bottom)
    return ImageGrab.grab(bbox=area)

def get_pixel(screenshot, spot):
    return screenshot.getpixel((spot.x, spot.y))

def get_width(screenshot):
    return screenshot.width

def get_height(screenshot):
    return screenshot.height

# Screen interactor adapters end

# Gui interactor adapters:

pydirectinput.PAUSE = 0 # Disable delay between inputs

def click(spot):
    pydirectinput.click(spot.x, spot.y, duration=0.2)

def press_buttons(buttons):
    pydirectinput.write(buttons)

def press_hot_key(hot_key, insides):
    pydirectinput.keyDown(hot_key)
    press_buttons(insides)
    pydirectinput.keyUp(hot_key)

# Gui interactor adapters end

class BoundFinder:
    def __init__(self, screenshot):
        self.center = SN(x=get_width(screenshot)//2, y=get_height(screenshot)//2)
        self.screenshot = screenshot
    def find_bound(self, bias):
        current = self.center
        while True:
            new = SN(x=current.x + bias.x, y=current.y + bias.y)
            if get_pixel(screenshot=self.screenshot, spot=new) != (255, 255, 255):
                return current
            current = new

class GuiInteractors:
    def __init__(self, bottom_left, side):
        self.side = side
        self.bottom_left = bottom_left

    def click_gui(self, bias):
        click(spot=SN(x=self.bottom_left.x + int(bias.x*self.side), y=self.bottom_left.y + int(bias.y*self.side)))

    def pick_color(self, color):
        color_hex = "#%02x%02x%02x" % (color.r, color.g, color.b)

        self.click_gui(bias=SN(x=0.2, y=0.1)) # Open the color picker
        time.sleep(0.3) # Wait for the color picker to open
        self.click_gui(bias=SN(x=0.7, y=-0.13)) # Switch to color field
        time.sleep(0.3) # Wait for the switch
        press_hot_key("ctrl", "a") # Select the current color
        time.sleep(0.3) # Wait for the selection
        press_buttons(color_hex) # Write the new color
        time.sleep(0.3) # Wait for the writing...
        self.click_gui(bias=SN(x=0.38, y=-0.13)) # Confirm color
        time.sleep(0.3) # Wait for confirmation

def main():
    time.sleep(3) # Wait for the user to open Roblox

    screenshot = make_screenshot()
    bound_finder = BoundFinder(screenshot)

    bottom = bound_finder.find_bound(bias=SN(x=0, y=1)).y
    top = bound_finder.find_bound(bias=SN(x=0, y=-1)).y
    left = bound_finder.find_bound(bias=SN(x=-1, y=0)).x
    right = bound_finder.find_bound(bias=SN(x=1, y=0)).x
    
    side = bottom - top
    bottom_left = SN(x=left, y=bottom)
    
    gui_interactors = GuiInteractors(bottom_left, side)

    gui_interactors.pick_color(color=SN(r=0, g=100, b=0))

main()
