## More Complete example

These 3 files consist of an class file ` bitmap.py ` that stores all the data about an image, included the abilities to draw the image and alter the meta data.

Instead of having fixed image data like the previous examples this will allow you to store the information in a text file (with it's own specific formatting requirements) this can then be loaded, giving much flexability

Because the rendering and all other associated work is performed by the bitmap code, the pygame loop and code is simplified.

You will need all 3 files:

* ` Ghost.junk ` is the image file containing the meta data and pixel data
* ` bitmap.py ` the class definition to hold and manipulate and draw image data
* ` BitmapRenderer.py ` the pygame project that loads and displays your custom images

in this folder to get this project to work.

You don't need to make changes to the ` bitmap.py ` file but you will need to edit and create your own bitmap files to make new images and alter the ` BitmapRender.py ` code to load and display your own images.
