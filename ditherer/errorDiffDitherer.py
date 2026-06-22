from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import numba


class errorDiffusion():

    def dither(self, filePath):
        validFile = False
        try:
            image = Image.open(filePath)
            validFile = image is not None
        except:
            pass

        if validFile:
            imageData = np.array(image).astype(np.float32) / 255.
            if len(imageData.shape) == 2:
                imageData = imageData[:, :, np.newaxis]

            plt.imshow(imageData[:, :, 0], cmap='Greys_r')
            plt.show()
