from PIL import ImageGrab
import timeit
import autoit

def get_screen_pixel():
    ImageGrab.grab(bbox=(500, 500, 501, 501)).getpixel((0, 0))
def get_screen_pixel_2():
    autoit.pixel_get_color(x=500,y=500)

print(timeit.timeit(get_screen_pixel, number=100))
print(timeit.timeit(get_screen_pixel_2, number=100))
