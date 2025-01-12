This is an automatic drawing tool for Roblox drawing games, like "Draw and Donate" or "Starving Artists". Follow the instruction below to use this program. Keep in mind that it's pretty slow and it is probably a good idea to leave this program to work overnight.

# An example of a finished painting in "Starving Artists"

![An example of a finished painting in "Starving Artists"](example_starving_artists.png)

# How to download this

* Go to https://github.com/megahomyak/autopainter/releases/latest and grab a zip from there
* Drag the folder inside of it onto your desktop
* Open the folder on the desktop

# How to set this up

* Install Python 3.13.0 from here: https://www.python.org/downloads/release/python-3130/ . The program may work with other versions of Python as well, it just wasn't tested on those versions
* If you mess up during the setup, just close its window and try again
* Run "setup.bat" (by double-clicking on it)
* Wait for all dependencies to install (you will see "Ready" in the window when it's over)
* Switch to Roblox
* Make sure your canvas is open and your mouse cursor is not on the canvas
* Press the "r" key on your keyboard. Wait for about three seconds afterwards. It is important to give the program enough time to take a screenshot
* Click on the color picker button
* Click on the field for text inputs
* Click on the checkmark button in Draw and Donate or on the closing button in Starving Artists
* You're done! If button positions change in the future, run this script again

# How to use

* Drop any image into the folder with the scripts
* Set your canvas resolution to 200x200 and your brush size to 0. If you're in Starving Artists, check the setting change section below to configure the program to draw in 32x32
* Run "run.bat"
* Switch to Roblox. The program will begin drawing as soon as it sees an empty canvas of the same size as in the setup. Don't forget that your mouse obstructs the canvas!
* Hold "q" for some time to stop the program

# Changing some settings

There are some settings in `settings.json` (the file that gets generated after the setup) that you can change.

* `"canvas_side_resolution"`: self-explanatory. Allows you to choose some other canvas resolution in the game, and the script will draw in the specified resolution
* `"colors_count"`: the amount of colors the resulting image will have. Can go up to 256. Color compression is important to have better performance on small canvas resolutions
