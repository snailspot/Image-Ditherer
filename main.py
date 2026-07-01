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
colourMap2D = np.array([[48, 57, 42], [141, 152, 58]])
colourPinkMap = np.array([[72, 31, 56] , [72, 31, 56] , [149, 64, 117], [249,192, 218]])

ed.loadImage(filepath)
bo.setMatrixSize(3)
ed.adjustImage(70, contrastLevel=100)
ed.dither(fs, 2, pixelSize=3, colourMap=colourMap, bloomLevel=40, bloomSpread=3)
ed.displayImage()





