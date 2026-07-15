from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from numba import njit, prange
from .ditherAlgorithm import DitherAlgorithm
import warnings

MAX_DIMENSIONS = 800
MAX_CONTRAST = 255
MIN_CONTRAST = -255
MAX_BRIGHTNESS = 255
MIN_BRIGHTNESS = -255
MAX_NOISE = 100
MIN_NOISE = 0
MAX_PIXEL_SIZE = 10
MIN_PIXEL_SIZE = 1
MAX_VALUES = 6
MIN_VALUES = 2
MAX_THRESHOLD = 90

class ImageDitherer():
    fileName = r"output.png"
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

    def dither(self, ditherMethod : DitherAlgorithm, values=MIN_VALUES, valueThresholds = None, pixelSize=1, colourMap = None, noiseLevel=0, bloomLevel=0, bloomSpread=1):
            if self.__imageArray is None:
                self.loadImage(r"assets\testInputColour.png")
                self.__imageArray = np.copy(self.__baseImageArray)
            self.__ditheredImageArray = np.copy(self.__imageArray)
            values = values if colourMap is None else colourMap.size // 3
            # Adjust pixel size and dither
            if pixelSize > MIN_PIXEL_SIZE: 
                self.__ditheredImageArray = self.__resizePixels(self.__ditheredImageArray, pixelSize)
                if noiseLevel > MIN_NOISE: self.__addNoise(self.__ditheredImageArray, noiseLevel, out=self.__ditheredImageArray)
                ditherMethod.ditherImage(self.__ditheredImageArray, values, valueThresholds, out=self.__ditheredImageArray)
                self.__ditheredImageArray = self.__resetSize(self.__ditheredImageArray, pixelSize)
            else:
                if noiseLevel > MIN_NOISE: self.__addNoise(self.__ditheredImageArray, noiseLevel, out=self.__ditheredImageArray)
                ditherMethod.ditherImage(self.__ditheredImageArray, values, valueThresholds, out=self.__ditheredImageArray)

            # Apply colour map
            if colourMap is not None and colourMap.size//3 >= 2:
                self.__ditheredImageArray = self.__colourise(self.__ditheredImageArray, colourMap)
            
            # Apply Bloom
            if bloomLevel > 0 and colourMap is not None and colourMap.size//3 >= 2:
                self.__ditheredImageArray = self.addBloom(self.__ditheredImageArray, bloomLevel, bloomSpread, self.__threshold(self.__ditheredImageArray, colourMap[-2]))
            
            

    # Preprocessing methods

    def __formatImage(self, image):
        image = self.__resizeImage(image)
        pixArray = np.array(image).astype(np.float32)
        if len(pixArray.shape) == 3:
            pixArray = self.__toGrayscale(pixArray)
        return pixArray

    def __toGrayscale(self, pixArray):
        # based on the following grayscale formula gray = 0.3 * R + 0.59 * G + 0.11 * B
        grayValue = 0.3 * pixArray[:, :, 0] + 0.59 * pixArray[:, :, 1] + 0.11 * pixArray[:, :, 2]
        grayImg = np.clip(grayValue, 0, 255).astype(np.float32)
        return grayImg

    def __resizeImage(self, image):
        width, height = image.size
        if width > MAX_DIMENSIONS or height > MAX_DIMENSIONS:
            if width > height:
                height = int(height * (MAX_DIMENSIONS / width))
                width = MAX_DIMENSIONS
            else:
                width = int(width * (MAX_DIMENSIONS / height))
                height = MAX_DIMENSIONS
            image = image.resize((width, height), Image.BICUBIC)
        return image
    
    # Image adjustment methods
    
    def adjustImage(self, brightnessLevel=0, contrastLevel=0):
        self.__imageArray = np.copy(self.__baseImageArray)
        brightnessLevel = max(MIN_BRIGHTNESS, min(MAX_BRIGHTNESS, brightnessLevel))
        contrastLevel = max(MIN_CONTRAST, min(MAX_CONTRAST, contrastLevel))
        contrastFactor = (259 * (contrastLevel + 255)/(255 * (259 - contrastLevel)))
        self.__applyContrastBrightness(self.__imageArray, brightnessLevel, contrastFactor)
    
    @staticmethod
    @njit(parallel = True, cache=True)
    def __applyContrastBrightness(pixArray, brightnessLevel, contrastFactor):
        width, height = pixArray.shape
        for y in prange(height):
            for x in range(width):
                pixel = pixArray[x, y]
                pixel = (pixel - 127) * contrastFactor + 127 + brightnessLevel
                pixArray[x, y] = min(255, max(0, pixel))

    # Dither processing methods

    def __resizePixels(self, pixArray, pixelSize):
        pixelSize = min(MAX_PIXEL_SIZE, pixelSize)
        return pixArray[::pixelSize, ::pixelSize]

    def __resetSize(self, pixArray, pixelSize):
        return pixArray.repeat(pixelSize, axis=0).repeat(pixelSize, axis=1)

    def __colourise(self, pixArray, colourMap):
        colourArray = np.dstack((pixArray, pixArray, pixArray))
        imageValues = np.unique(colourArray).astype('uint8')
        if imageValues.size * 3 == colourMap.size:
            for i in range (imageValues.size):
                value = imageValues[i]
                mask = np.all(colourArray == value, axis=-1)
                colourArray[mask] = colourMap[i]
            return colourArray
        else:
            raise IndexError("Number of colours in colour map and number of values in image must match to colourise")
    
    def __addNoise(self, pixArray, noiseLevel, out=None):
        width, height = pixArray.shape
        noiseLevel =  min(MAX_NOISE, noiseLevel)  / MAX_NOISE * 20
        noise = np.random.normal(0, noiseLevel, pixArray.size)
        noise = np.reshape(noise, (width, height))
        imageWithNoise = np.clip((pixArray + noise), 0, 255)

        if out is not None:
            out[:] = imageWithNoise
            return out
        else:
            return imageWithNoise
        
    def __threshold(self, pixArray, value):
        mask = np.all(pixArray > value, axis=-1)
        return np.where(mask, 1, 0).astype(np.uint8)

    @staticmethod
    @njit(cache=True, fastmath=True)
    def addBloom(pixArray, bloomLevel, bloomSpread, thresholdMap):
        bloomFactor = np.array([0.29 * bloomLevel, 0.41 * bloomLevel, 0.23 * bloomLevel])
        bloomAmountInner = bloomFactor*0.35
        bloomAmountOuter = bloomFactor*0.11
        bloomOuter = int(bloomSpread* 1.2)
        bloomInner = int(bloomSpread* 0.45)

        pixelsToBloom = np.argwhere(thresholdMap == 1)
        bloomArray = np.zeros_like(pixArray)
        for pixel in pixelsToBloom:
            x = pixel[0]
            y = pixel[1]
            bloomArray[x-bloomOuter:x+bloomOuter, y-bloomOuter:y+bloomOuter] += bloomAmountOuter
            bloomArray[x-bloomInner:x+bloomInner, y-bloomInner:y+bloomInner] += bloomAmountInner
 
        return np.clip(pixArray + bloomArray, 0, 255)


    # Display and save image methods

    def displayImage(self):
        if self.__ditheredImageArray is not None:
            if len(self.__ditheredImageArray.shape) == 2:
                plt.imshow(self.__ditheredImageArray[:, :], cmap='gray')
            elif len(self.__ditheredImageArray.shape) == 3:
                plt.imshow(self.__ditheredImageArray.astype(np.uint8))
            plt.show()
        else:
            warnings.warn("An image must be dithered first to be displayed") 

    def saveImage(self):
        if self.__ditheredImageArray is not None:
            Image.fromarray(self.__ditheredImageArray.astype(np.uint8)).save(self.fileName)
        else:
            warnings.warn("An image must be dithered first to be saved") 
            
