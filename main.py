from ditherer import ditherer as d
from ditherer import ditherAlgorithm as da
import matplotlib.pyplot as plt

ed = d.ImageDitherer()
filepath = r"assets\testInput2Colour.png"
# ed.dither(filepath, da.FloydSteinberg())
bo = da.BayerOrdered()
bo.setMatrixSize(4)
ed.dither(filepath, bo)
