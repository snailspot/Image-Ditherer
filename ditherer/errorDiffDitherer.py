from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import numba


class errorDiffusion():
    fileName = r"output.png"
    __MAX_DIMENSIONS = 500

    def dither(self, filePath, thresholdPercent=50):
        validFile = False
        try:
            image = Image.open(filePath)
            validFile = image is not None
        except:
            pass

        if validFile:
            imageData = self.__formatImage(image)

            ditheredImage = self.__ditherImage(imageData)
            # self.__displayImage(ditheredImage)
            self.__saveImage(ditheredImage)

    def __threshold(self, pixArray, value):
        normalisedValue = value * 2.55
        return np.where(pixArray > normalisedValue, np.iinfo(np.uint8).max, 0)

    def __toGrayscale(self, pixArray):
        # based on the following grayscale formula gray = 0.3 * R + 0.59 * G + 0.11 * B
        grayValue = 0.3 * pixArray[:, :, 0] + 0.59 * pixArray[:, :, 1] + 0.11 * pixArray[:, :, 2]
        grayImg = np.clip(grayValue, 0, 255).astype(np.float32)
        return grayImg

    def __resizeImage(self, image):
        width, height = image.size
        if width > self.__MAX_DIMENSIONS or height > self.__MAX_DIMENSIONS:
            if width > height:
                height = int(height * (self.__MAX_DIMENSIONS / width))
                width = self.__MAX_DIMENSIONS
            else:
                width = int(width * (self.__MAX_DIMENSIONS / height))
                height = self.__MAX_DIMENSIONS
            image = image.resize((width, height), Image.BICUBIC)
        return image

    def __displayImage(self, pixArray):
        plt.imshow(pixArray[:, :], cmap='gray')
        plt.show()
    
    def __formatImage(self, image):
        image = self.__resizeImage(image)
        pixArray = np.array(image).astype(np.float32)
        if len(pixArray.shape) == 3:
            pixArray = self.__toGrayscale(pixArray)
        return pixArray

    def __saveImage(self, pixArray):
        Image.fromarray(pixArray.astype(np.uint8)).save(self.fileName)

    def __ditherImage(self, pixArray, colours = 4, colourThresholds = None):
        width, height = pixArray.shape
        if colourThresholds is None or len(colourThresholds) != colours:
            colourThresholds = np.linspace(0, 255, colours).astype(np.float32)
        for y in range(height):
            for x in range(width):
                oldPixel = pixArray[x, y]
                #newPixel = 255 if oldPixel > 127 else 0
                colourIndex = (np.abs(colourThresholds - oldPixel)).argmin()
                newPixel = colourThresholds[colourIndex]
                pixArray[x, y] = newPixel
                quantError = oldPixel - newPixel
                if xInBounds := x + 1 < width:
                    pixArray[x + 1][y] = pixArray[x + 1][y] + quantError * 7/16
                if y + 1 < height:
                    if x-1 >= 0:
                        pixArray[x - 1][y + 1] = pixArray[x - 1][y + 1] + quantError * 3/16
                    pixArray[x][y + 1] = pixArray[x][y + 1] + quantError * 5/16
                    if xInBounds:
                        pixArray[x + 1][y + 1] = pixArray[x + 1][y + 1] + quantError * 1/16
        return np.clip(pixArray, 0, 255)
