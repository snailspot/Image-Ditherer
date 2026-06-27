from ditherer import ditherer as d
from ditherer import ditherAlgorithm as da
import matplotlib.pyplot as plt
import numpy as np

ed = d.ImageDitherer()
filepath = r"assets\testInputBW.png"
fs = da.FloydSteinberg()
bo = da.BayerOrdered()

ed.loadImage(filepath)
ed.adjustImage(0, 50)
ed.dither(fs, 2)
ed.displayImage()

