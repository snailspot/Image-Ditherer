from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import numba


class errorDiffusion():
    fileName = r"output.png"

    def dither(self, filePath, thresholdPercent=50):
        validFile = False
        try:
            image = Image.open(filePath)
            validFile = image is not None
        except:
            pass

        if validFile:
            imageData = np.array(image).astype(np.float32)
            if len(imageData.shape) == 3:
                imageData = self.__toGrayscale(imageData)

            ditheredImage = self.__ditherImage(imageData)
            self.__displayImage(ditheredImage)
            self.__saveImage(ditheredImage)

    def __threshold(self, pixArray, value):
        normalisedValue = value * 2.55
        return np.where(pixArray > normalisedValue, np.iinfo(np.uint8).max, 0)

    def __toGrayscale(self, pixArray):
        # based on the following grayscale formula gray = 0.3 * R + 0.59 * G + 0.11 * B
        grayValue = 0.3 * pixArray[:, :, 0] + 0.59 * pixArray[:, :, 1] + 0.11 * pixArray[:, :, 2]
        grayImg = np.clip(grayValue, 0, 255).astype(np.float32)
        return grayImg

    def __displayImage(self, pixArray):
        plt.imshow(pixArray[:, :], cmap='gray')
        plt.show()

    def __saveImage(self, pixArray):
        Image.fromarray(pixArray.astype(np.uint8)).save(self.fileName)

    def __ditherImage(self, pixArray):
        width, height = pixArray.shape
        for y in range(height):
            for x in range(width):
                oldPixel = pixArray[x, y]
                newPixel = 255 if oldPixel > 127 else 0
                pixArray[x, y] = newPixel
                quantError = oldPixel - newPixel
                if xInBounds := x + 1 < width:
                    pixArray[x + 1][y] = pixArray[x + 1][y] + quantError * 7/16
                if y + 1 < height:
                    if x-1 >= 0:
                        pixArray[x - 1][y + 1] = pixArray[x - 1][y + 1] + quantError * 3/16
                    pixArray[x][y + 1] = pixArray[x][y + 1] + quantError * 7/16
                    if xInBounds:
                        pixArray[x + 1][y + 1] = pixArray[x + 1][y + 1] + quantError * 1/16
        return np.clip(pixArray, 0, 255)
