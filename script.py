from PIL import ImageGrab
from types import SimpleNamespace as SN
import time
import pyautogui # For some reason fixes screen scaling for other libraries
import pyautoit

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

def click(spot):
    pyautoit.mouse_click("left", spot.x, spot.y, speed=0)

def enter_text(text):
    pyautoit.send(text)

def hold_ctrl_and_enter_text(text):
    with ait.hold("ctrl"):
        time.sleep(1)
        enter_text(text)
        time.sleep(1)

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
        hold_ctrl_and_enter_text("a") # Select the current color
        time.sleep(0.3) # Wait for the selection
        return
        enter_text(color_hex) # Write the new color
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
