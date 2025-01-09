from PIL import ImageGrab
from types import SimpleNamespace as SN
import time
import pyautogui

pyautogui.PAUSE = 0 # Disable delay between pyautogui inputs

time.sleep(3) # Wait for the user to open Roblox

screen = ImageGrab.grab()
center = SN(x=screen.width//2, y=screen.height//2)

def get_pixel(spot):
    return screen.getpixel((spot.x, spot.y))

def click(spot=None):
    if spot is None:
        pyautogui.click(duration=1)
    else:
        pyautogui.click(spot.x, spot.y)
    
def move(spot, duration=0):
    pyautogui.moveTo(spot.x, spot.y, duration=duration)

def find_bound(bias):
    current = center
    while True:
        new = SN(x=current.x + bias.x, y=current.y + bias.y)
        if get_pixel(spot=new) != (255, 255, 255):
            return current
        current = new

bottom = find_bound(bias=SN(x=0, y=1)).y
top = find_bound(bias=SN(x=0, y=-1)).y
left = find_bound(bias=SN(x=-1, y=0)).x
right = find_bound(bias=SN(x=1, y=0)).x

side = bottom - top
bottom_left = SN(x=left, y=bottom)
print(bottom_left)

def get_gui_spot(bias):
    return SN(x=bottom_left.x + bias.x*side, y=bottom_left.y + bias.y*side)

def pick_color(color):
    def toggle_color_picker():
        # We need to move first and click second, because this game for some reason needs to know we're on a button before allowing to click, and it checks for presence by checking for movement
        target = get_gui_spot(bias=SN(x=0.2, y=0.1))
        move(spot=SN(x=target.x - 20, y=target.y))
        move(spot=target, duration=1)
        click()
    color_hex = "#%02x%02x%02x" % (color.r, color.g, color.b)

    toggle_color_picker()
    # click_gui(bias=SN(x=0.6, y=-0.3)) # Switch to color field
    # pyautogui.hotkey("ctrl", "a") # Select the current color
    # pyautogui.write(color_hex) # Write the new color
    # click_gui(bias=SN(x=0.5, y=-0.3)) # Confirm color
    # toggle_color_picker()
    
def main():
    pick_color(color=SN(r=0, g=100, b=0))

main()