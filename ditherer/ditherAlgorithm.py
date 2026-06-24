from abc import ABC, abstractmethod
import numpy as np
import matplotlib.pyplot as plt
import numba
import math

class DitherAlgorithm(ABC):
    @abstractmethod
    def ditherImage(self, pixArray, values, valueThresholds=None):
        pass

class BayerOrdered(DitherAlgorithm):
    def __init__(self):
        self.__matrixSize = 2

    def __generateThresholdMap(self, matrixSize):
        baseMatrix = np.array([[0,3],[2,1]], dtype="float32")
        if matrixSize == 0:
            return np.array([[0]])
        prevMatrix = self.__generateThresholdMap(matrixSize-1)
        matrix = np.kron(baseMatrix, np.ones_like(prevMatrix))
        matrix = matrix + np.tile(prevMatrix, (2, 2)) * 4
        return matrix
        
    def ditherImage(self, pixArray, values=4, valueThresholds=None):
        matrix = self.__generateThresholdMap(self.__matrixSize)
        width, height = pixArray.shape
        matrixWidth, matrixHeight = matrix.shape
        if valueThresholds is None or len(valueThresholds) != values:
            valueThresholds = np.linspace(0, 255, values).astype(np.float32)
        for y in range(height):
            for x in range(width):
                ditherX = x % matrixWidth
                ditherY = y % matrixHeight
                ditherValue = (matrix[ditherX, ditherY]  * (1/matrix.size)) - 0.5
                ditherColour = pixArray[x, y] + (ditherValue *  255)
                newColour = math.floor(ditherColour * (values-1) + 0.5) / (values-1)
                colourIndex = (np.abs(valueThresholds - newColour)).argmin()
                pixArray[x, y] = valueThresholds[colourIndex]
        return np.clip(pixArray, 0, 255)
    
    def setMatrixSize(self, value):
        self.__matrixSize = value if type(value) is int and value > 1 else self.__matrixSize

class FloydSteinberg(DitherAlgorithm):
    def ditherImage(self, pixArray, values=4, valueThresholds=None):
        width, height = pixArray.shape
        if valueThresholds is None or len(valueThresholds) != values:
            valueThresholds = np.linspace(0, 255, values).astype(np.float32)
        for y in range(height):
            for x in range(width):
                oldPixel = pixArray[x, y]
                #newPixel = 255 if oldPixel > 127 else 0
                colourIndex = (np.abs(valueThresholds - oldPixel)).argmin()
                newPixel = valueThresholds[colourIndex]
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