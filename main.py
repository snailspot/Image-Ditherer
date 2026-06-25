from ditherer import ditherer as d
from ditherer import ditherAlgorithm as da
import matplotlib.pyplot as plt
import numpy as np

ed = d.ImageDitherer()
filepath = r"assets\testInput2Colour.png"
fs = da.FloydSteinberg()
bo = da.BayerOrdered()

ed.dither(filepath, bo)


