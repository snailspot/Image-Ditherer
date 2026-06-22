from ditherer.errorDiffDitherer import errorDiffusion


ed = errorDiffusion()
filepath = r"assets\testInputBW.png"
ed.dither(filepath, 0.39)
