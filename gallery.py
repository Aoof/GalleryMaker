# 1200x480px TWITCH BANNER SIZE

from PIL import Image
import os

class Gallery:
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
        self.sw, self.sh = canvas
        self.images = []
        self.result = Image.new(mode, canvas)


    def testRatios(self, sizes : tuple) -> list:
        """Tests the available ratios and returns the closest ratio to the sizes given

        Parameters
        ----------
        sizes : tuple
        |    Syntax (width, height)

        Returns
        -------
        [(ratio_x, ratio_y), change_value] -> list
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

        Returns
        -------
        [width, height] -> list
        """
        rx, ry = aspect_ratio
        w, h = sizes

        closer = [0, 0]
        for i in range(limit):
            x, y = i * rx, i * ry

            conditions = {
                "width": abs(w-x) < abs(w-closer[0]),
                "height": abs(h-y) < abs(h-closer[1]),
                "ishigher": (x > w and y > h)
            }
            if conditions["width"] and conditions["height"] and conditions["ishigher"]:
                closer = [x, y]
        return closer
    
    def addImage(self, image : Image.Image, bgcolor=(0, 0, 0, 0)) -> bool:
        """Adds image to canvas
        
        Parameters
        ----------
        image : Image.Image
        |    The image you want to add to the canvas

        Returns
        -------
        True if successfully added... False if something wrong happened
        """
        sizes = image.width, image.height
        ratio = self.testRatios(sizes)[0]
        lsizes = self.testSizes(ratio, sizes)
        try:
            background = Image.new("RGBA", lsizes, bgcolor) # Transparent Background with the last sizes needed
            bg_w, bg_h = background.size
            offset = ((bg_w - sizes[0]) // 2, (bg_h - sizes[1]) // 2)
            background.paste(image, offset)
            self.images.append(background)
            return 1
        except Exception:
            return 0


if __name__ == "__main__":
    gallery = Gallery((1200, 480))
    
    image = Image.open(os.path.join(os.path.dirname(__file__), "media\\unknown (4).png"))

    sizes = image.width, image.height
    ratio, _ = gallery.testRatios(sizes)
    last_size = gallery.testSizes(ratio, sizes)
    
    print("For size ({}x{}px)".format(sizes[0], sizes[1]),
          "Aspect Ratio ({}:{})".format(ratio[0], ratio[1]), 
          "Last size ({}x{}px)".format(last_size[0], last_size[1]), 
          sep="\n")

    image.show()
    input("Click enter to show the fixed sizes image..")
    gallery.addImage(image, (255, 0, 0, 255))
    gallery.images[0].show()

