import colorsys
import time
from sys import exit

try:
    import numpy as np
except ImportError:
    exit('This script requires the numpy module\nInstall with: sudo pip install numpy')

import blinkt


def make_gaussian(fwhm):
    x = np.arange(0, blinkt.NUM_PIXELS, 1, float)
    y = x[:, np.newaxis]
    x0, y0 = 3.5, 3.5
    fwhm = fwhm
    gauss = np.exp(-4 * np.log(2) * ((x - x0) ** 2 + (y - y0) ** 2) / fwhm ** 2)
    return gauss

def pulse():
    spacing = 360.0 / 16.0
    hue = 0
    while True:
        for z in list(range(1, 10)[::-1]) + list(range(1, 10)):
            fwhm = 5.0 / z
            gauss = make_gaussian(fwhm)
            start = time.time()
            y = 4

            for x in range(blinkt.NUM_PIXELS):
                offset = x * spacing
                h = ((hue + offset) % 360) / 360.0
                #h = 0.5
                s = 1.0
                v = gauss[x, y]
                rgb = colorsys.hsv_to_rgb(h, s, v)
                r, g, b = [int(255.0 * i) for i in rgb]
                #r, g, b = [int(c * 255) for c in colorsys.hsv_to_rgb(h, 1.0, 1.0)]
                blinkt.set_pixel(x, r, g, b)

            blinkt.show()
            end = time.time()
            t = end - start

            if t < 0.04:
                time.sleep(0.04 - t)