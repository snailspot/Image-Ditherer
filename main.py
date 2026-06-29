from ditherer import ditherer as d
from ditherer import ditherAlgorithm as da
import matplotlib.pyplot as plt
import numpy as np

ed = d.ImageDitherer()
filepath = r"assets\testInputBW.png"
fs = da.FloydSteinberg()
bo = da.BayerOrdered()
ad = da.AtkinsonDithering()
vd = da.VerticalDiffusionDithering()

ed.loadImage(filepath)
ed.dither(fs, 3, pixelSize=4)

ed.displayImage()


