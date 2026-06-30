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

colourMap = np.array([[48, 57, 42], [102, 109, 102], [141, 152, 58], [211, 228, 87]])

ed.loadImage(filepath)
ed.adjustImage(50, 50)
ed.dither(fs, 4, pixelSize=3, valueThresholds=[25, 170, 190, 255],colourMap=colourMap)
ed.displayImage()


