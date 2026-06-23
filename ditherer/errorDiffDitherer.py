from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import numba


class errorDiffusion():

    def dither(self, filePath, thresholdPercent=50):
        validFile = False
        try:
            image = Image.open(filePath)
            validFile = image is not None
        except:
            pass

        if validFile:
            imageData = np.array(image).astype(np.uint8)
            if len(imageData.shape) == 3:
                imageData = self.__toGrayscale(imageData)

            imageData = self.__threshold(imageData, thresholdPercent)

            plt.imshow(imageData[:, :], cmap='gray')
            plt.show()

    def __threshold(self, pixArray, value):
        normalisedValue = value * 2.55
        return np.where(pixArray > normalisedValue, np.iinfo(np.uint8).max, 0)

    def __toGrayscale(self, pixArray):
        # based on the following grayscale formula gray = 0.3 * R + 0.59 * G + 0.11 * B
        grayValue = 0.3 * pixArray[:, :, 0] + 0.59 * \
            pixArray[:, :, 1] + 0.11 * pixArray[:, :, 2]
        grayImg = grayValue.astype(np.uint8)
        return grayImg
