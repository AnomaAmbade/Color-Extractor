from PIL import Image
from typing import Counter
import numpy as np


class ExtractColor:
    def __init__(self):
        self.common = []

    def rgb_to_hex(self, rgb):
        """RGB to hex conversion function."""
        self.hex = '#'
        for rgb_val in rgb:
            # conversion to hex
            self.hex += '%02x' % rgb_val
        return self.hex

    def extract_colors(self, file, num_of_col=5):
        """A function to extract most common colors from any given jpg or png image. 
        Requires an image file and number of colors as input. 
        Outputs a list of commonly occuring colors."""
        
        open_file = Image.open(file)

        # use asarray to convert pil images to numpy array
        # immutable array of image
        img = np.asarray(open_file)

        color_dict = {}

        for row in img:
            for col in row:
                # convert to hex color value
                hex = self.rgb_to_hex(col)

                # check for color value in dict
                if hex in color_dict.keys():
                    color_dict[hex] += 1

                # create new key in dict
                else:
                    hex = self.rgb_to_hex(col)
                    color_dict[hex] = 1

        self.common = Counter(color_dict).most_common(num_of_col)
        # print(self.common)
        return self.common
