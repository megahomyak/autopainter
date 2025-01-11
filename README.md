# How to download this

* Go to https://github.com/megahomyak/autopainter/releases/latest and grab a zip from there
* Drag the folder inside of it onto your desktop
* Open the folder on the desktop

# How to set this up

* If you mess up during the setup, just close its window and try again
* Run "setup.bat" (by double-clicking on it)
* Wait for all dependencies to install (you will see "Ready" in the window when it's over)
* Switch to Roblox
* Make sure your canvas is open and your mouse cursor is not on the canvas
* Press the "r" key on your keyboard. Wait for about three seconds afterwards. It is important to give the program enough time to take a screenshot
* Click on the color picker button
* Click on the field for text inputs. Make sure you got it right: a blinking cursor should appear
* Click on the checkmark button (the one for confirmation)
* You're done! If button positions change in the future, run this script again

# How to use

* Drop any image into the folder with the scripts
* Set your canvas resolution to 200x200 and your brush size to 0
* Run "run.bat"
* Switch to Roblox. The program will begin drawing as soon as it sees an empty canvas of the same size as in the setup. Don't forget to move your mouse out of the canvas!

# Changing some settings

There are some settings in `settings.json` (the file that gets generated after the setup) that you can change.

* `"canvas_side_resolution"`: self-explanatory. Allows you to choose some other canvas resolution in the game, and the script will draw in the specified resolution
* `"colors_count"`: the amount of colors the resulting image will have. Can go up to 256. Color compression is important to have better performance on small canvas resolutions
