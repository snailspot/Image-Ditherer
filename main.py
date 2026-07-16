from ditherer import ditherer as d
from ditherer import ditherAlgorithm as da
import matplotlib.pyplot as plt
import numpy as np
from userInterface import mainScreen as ms
import sys
from PyQt5.QtWidgets import QApplication

ed = d.ImageDitherer()
filepath = r"assets\testInputBW.png"
fs = da.FloydSteinberg()
bo = da.BayerOrdered()
ad = da.AtkinsonDithering()
vd = da.VerticalDiffusionDithering()

# colourMap = np.array([[48, 57, 42], [102, 109, 102], [141, 152, 58], [211, 228, 87]])
# colourMap2D = np.array([[48, 57, 42], [141, 152, 58]])
# colourPinkMap = np.array([[72, 31, 56] , [72, 31, 56] , [149, 64, 117], [249,192, 218]])

# ed.loadImage(filepath)
# bo.setMatrixSize(3)
# ed.adjustImage(70, contrastLevel=100)
# ed.dither(vd, pixelSize=3, colourMap=colourPinkMap, bloomSpread=10, bloomLevel=10)
# ed.displayImage()

app = QApplication(sys.argv)
screen = ms.MainScreen()
screen.show()
app.exec_()




