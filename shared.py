from PIL import ImageGrab

def check_if_canvas(color):
    channels_diff = max(color) - min(color)
    return channels_diff < 25 and min(color) > 200

def get_canvas_area_bound(center, screenshot, bias):
    current = center
    while True:
        new = current[0]+bias[0], current[1]+bias[1]
        if not check_if_canvas(screenshot.getpixel(new)):
            break
        current = new
    return current

def get_canvas_area():
    screenshot = ImageGrab.grab()
    center = (screenshot.width//2, screenshot.height//2)
    top = get_canvas_area_bound(center, screenshot, (0, -1))[1]
    left = get_canvas_area_bound(center, screenshot, (-1, 0))[0]
    bottom = get_canvas_area_bound(center, screenshot, (0, 1))[1]
    side = bottom - top
    return {"side": side, "top": top, "left": left}
