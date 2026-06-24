from ditherer import ditherer as d
from ditherer import ditherAlgorithm as da
import matplotlib.pyplot as plt

ed = d.ImageDitherer()
filepath = r"assets\testInputColour.png"
# ed.dither(filepath, da.FloydSteinberg())
bo = da.BayerOrdered()
print(bo.generateThresholdMap(3))
