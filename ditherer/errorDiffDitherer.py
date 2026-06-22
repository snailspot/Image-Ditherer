from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import numba


class errorDiffusion():

    def dither(self, filePath, thresholdValue=0.5):
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

            imageData = self.__threshold(imageData, thresholdValue)

            plt.imshow(imageData[:, :, 0], cmap='Greys_r')
            plt.show()

    def __threshold(self, pixArray, value=0.5):
        return np.where(pixArray > value, 1, 0)
