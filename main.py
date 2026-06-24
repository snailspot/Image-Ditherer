from ditherer.ditherer import imageDitherer
import ditherer.ditherAlgorithm as da


ed = imageDitherer()
filepath = r"assets\testInputColour.png"
ed.dither(filepath, da.floydSteinberg())
