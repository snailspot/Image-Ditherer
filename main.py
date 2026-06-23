from ditherer.errorDiffDitherer import errorDiffusion


ed = errorDiffusion()
filepath = r"assets\testInputColour.png"
ed.dither(filepath)
