from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import math
from numba import njit, prange
from .ditherAlgorithm import DitherAlgorithm


class ImageDitherer():
    fileName = r"output.png"
    __MAX_DIMENSIONS = 800
    __MAX_CONTRAST = 255
    __MIN_CONTRAST = -255
    __MAX_BRIGHTNESS = 255
    __MIN_BRIGHTNESS = -255
    __imageArray = None
    __ditheredImageArray = None
    __baseImageArray = None

    def __init__(self):
        pass

    def loadImage(self, filePath):
        validFile = False
        try:
            image = Image.open(filePath)
            validFile = image is not None
        except:
            pass
        if validFile:
            self.__baseImageArray = self.__formatImage(image)

    def dither(self, ditherMethod : DitherAlgorithm, values=2, valueThresholds = None, pixelSize=1):
            if self.__imageArray is None:
                self.loadImage(r"assets\testInputColour.png")
                self.__imageArray = np.copy(self.__baseImageArray)
            self.__ditheredImageArray = np.copy(self.__imageArray)
            self.__ditheredImageArray = self.__resizePixels(self.__ditheredImageArray, pixelSize)
            ditherMethod.ditherImage(self.__ditheredImageArray, values, valueThresholds, out=self.__ditheredImageArray)
            self.__ditheredImageArray = self.__resetSize(self.__ditheredImageArray, pixelSize)

    
    def adjustImage(self, brightnessLevel=0, contrastLevel=0):
        @njit(parallel = True, cache=True)
        def applyContrastBrightness(pixArray, brightnessLevel, contrastFactor):
            width, height = pixArray.shape
            for y in prange(height):
                for x in range(width):
                    pixel = pixArray[x, y]
                    pixel = (pixel - 127) * contrastFactor + 127 + brightnessLevel
                    pixArray[x, y] = min(255, max(0, pixel))

        self.__imageArray = np.copy(self.__baseImageArray)
        brightnessLevel = max(self.__MIN_BRIGHTNESS, min(self.__MAX_BRIGHTNESS, brightnessLevel))
        contrastLevel = max(self.__MIN_CONTRAST, min(self.__MAX_CONTRAST, contrastLevel))
        contrastFactor = (259 * (contrastLevel + 255)/(255 * (259 - contrastLevel)))
        applyContrastBrightness(self.__imageArray, brightnessLevel, contrastFactor)

    def __resizePixels(self, pixArray, pixelSize):
        return pixArray[::pixelSize, ::pixelSize]

    def __resetSize(self, pixArray, pixelSize):
        return pixArray.repeat(pixelSize, axis=0).repeat(pixelSize, axis=1)

    def __formatImage(self, image):
        image = self.__resizeImage(image)
        pixArray = np.array(image).astype(np.float32)
        if len(pixArray.shape) == 3:
            pixArray = self.__toGrayscale(pixArray)
        return pixArray

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

    def displayImage(self):
        if self.__ditheredImageArray is not None:
            plt.imshow(self.__ditheredImageArray[:, :], cmap='gray')
            plt.show()

    def saveImage(self):
        if self.__ditheredImageArray is not None:
            Image.fromarray(self.__ditheredImageArray.astype(np.uint8)).save(self.fileName)
