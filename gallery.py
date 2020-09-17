# 1200x480px TWITCH BANNER SIZE

from PIL import Image
import os

class Gallery:
    """Transforms multiple images into a single preset size canvas
    """
    allowed_ar = [
        (32, 9),
        (21, 9),
        (16, 9),
        (16, 10),
        (4, 3),
        (1, 1),
        (5, 4),
        (3, 2),
        (5, 3),
        (3, 1)
    ]
    def __init__(self, canvas, mode="RGBA"):
        """Transforms multiple images into a single preset size canvas
            
        Parameters
        ----------
        canvas : tuple
        |    Syntax (width, height)
        |    Preset size for canvas
        mode : str
        |    1 (1-bit pixels, black and white, stored with one pixel per byte)
        |    L (8-bit pixels, black and white)
        |    P (8-bit pixels, mapped to any other mode using a color palette)
        |    RGB (3x8-bit pixels, true color)
        |    RGBA (4x8-bit pixels, true color with transparency mask)
        |    CMYK (4x8-bit pixels, color separation)
        |    YCbCr (3x8-bit pixels, color video format)
        |    |    Note that this refers to the JPEG, and not the ITU-R BT.2020, standard
        |    LAB (3x8-bit pixels, the L*a*b color space)
        |    HSV (3x8-bit pixels, Hue, Saturation, Value color space)
        |    I (32-bit signed integer pixels)
        |    F (32-bit floating point pixels)
        """
        self.sw, self.sh = canvas
        self.result = Image.new(mode, canvas)


    def testRatios(self, sizes : tuple) -> list:
        """Tests the available ratios and returns the closest ratio to the sizes given

        Parameters
        ----------
        sizes : tuple
        |    Syntax (width, height)
        """
        closer = [(), 0] 
        x, y = sizes 
        allowed_ar = self.allowed_ar + [ratio[::-1] for ratio in self.allowed_ar]
        for rx, ry in allowed_ar:
            r = (x/rx) / (y/ry)
            if abs(1 - r) < abs(1 - closer[1]): 
                closer = [(rx, ry), r] 
        return closer

    def testSizes(self, aspect_ratio : tuple, sizes : tuple, limit=1000) -> list:
        """Tests the sizes by multiplying the aspect ratio by every number between 0 to limit and finding the closest to the sizes

        Parameters
        ----------
        aspect_ratio : tuple
        |   Syntax (x units, y units) or (smallest w, smallest h)
        sizes : tuple
        |   Syntax (width, height)
        limit : int (Default 1000)
        """
        rx, ry = aspect_ratio
        w, h = sizes

        closer = [0, 0]
        for i in range(limit):
            x, y = i * rx, i * ry
            if abs(w-x) < abs(w-closer[0]) and abs(h-y) < abs(h-closer[1]) and (x >= w and y >= h):
                closer = [x, y]
        return closer
    
    def addImage(self, image : Image.Image) -> Image.Image:
        """Adds image to canvas
        
        Parameters
        ----------
        image : Image.Image
        |    The image you want to add to the canvas
        """
        sizes, (w, h) = image.width(), image.height()
        ratio, change = self.testRatios(sizes)

        delta = abs(1-change)

if __name__ == "__main__":
    gallery = Gallery((1200, 480))
    
    sizes = (124, 169)
    ratio = gallery.testRatios(sizes)
    last_size = gallery.testSizes(ratio[0], sizes)

    print("For size ({}x{}px)".format(sizes[0], sizes[1]),
          "Aspect Ratio ({}:{})".format(ratio[0][0], ratio[0][1]), 
          "Last size ({}x{}px)".format(last_size[0], last_size[1]), 
          sep="\n")