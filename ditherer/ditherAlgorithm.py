from abc import ABC, abstractmethod
import numpy as np
import matplotlib.pyplot as plt
from numba import njit, prange
import math

class DitherAlgorithm(ABC):
    @abstractmethod
    def ditherImage(self, pixArray, values, valueThresholds=None, out=None):
        pass


class BayerOrdered(DitherAlgorithm):
    @staticmethod
    @njit(parallel=True, cache=True)
    def __bayerDitherUnevenThreshold(pixArray, valueThresholds, matrix):
        width, height = pixArray.shape
        matrixWidth, matrixHeight = matrix.shape
        for y in prange(height):
            for x in range(width):
                ditherX = x % matrixWidth
                ditherY = y % matrixHeight
                ditherFactor = (matrix[ditherX, ditherY]  * (1/matrix.size)) - 0.5
                ditherValue = max(0, min(255, pixArray[x, y] + (ditherFactor *  255)))
                bestMatch = 0
                bestDist = abs(valueThresholds[0] - ditherValue)
                for i in range(1, len(valueThresholds)):
                    dist = abs(valueThresholds[i] - ditherValue)
                    if dist < bestDist:
                        bestDist = dist
                        bestMatch = i
                pixArray[x, y] = valueThresholds[bestMatch]
        return pixArray

    @staticmethod
    @njit(parallel=True, cache=True)
    def __bayerDitherQuantised(pixArray, values, matrix):
        width, height = pixArray.shape
        matrixWidth, matrixHeight = matrix.shape
        for y in prange(height):
            for x in range(width):
                ditherX = x % matrixWidth
                ditherY = y % matrixHeight
                ditherFactor = (matrix[ditherX, ditherY]  * (1/matrix.size)) - 0.5
                ditherValue = max(0, min(255, pixArray[x, y] + (ditherFactor *  255)))
                pixArray[x, y] = math.floor(ditherValue * (values-1) / 255 + 0.5) * 255 / (values-1)
        return pixArray

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
        
    def ditherImage(self, pixArray, values, valueThresholds=None, out=None):
        matrix = self.__generateThresholdMap(self.__matrixSize)
        if valueThresholds is None:
            result = self.__bayerDitherQuantised(pixArray, values, matrix)
        else:
            result = self.__bayerDitherUnevenThreshold(pixArray, valueThresholds, matrix)

        if out is not None:
            out[:] = result
            return out
        else:
            return result

    
    def setMatrixSize(self, value):
        self.__matrixSize = value if type(value) is int and value > 1 else self.__matrixSize



class FloydSteinberg(DitherAlgorithm):

    @staticmethod
    @njit(cache=True)
    def __floydSteinbergDither(pixArray, valueThresholds):
        width, height = pixArray.shape
        for y in range(height):
            for x in range(width):
                oldPixel = pixArray[x, y]
                bestMatch = 0
                bestDist = abs(valueThresholds[0] - oldPixel)
                for i in range(1, len(valueThresholds)):
                    dist = abs(valueThresholds[i] - oldPixel)
                    if dist < bestDist:
                        bestDist = dist
                        bestMatch = i
                newPixel = valueThresholds[bestMatch]
                pixArray[x, y] = newPixel
                quantError = oldPixel - newPixel
                xInBounds = x + 1 < width
                if xInBounds:
                    pixArray[x + 1, y] = pixArray[x + 1, y] + quantError * 7/16
                if y + 1 < height:
                    if x-1 >= 0:
                        pixArray[x - 1, y + 1] = pixArray[x - 1, y + 1] + quantError * 3/16
                    pixArray[x, y + 1] = pixArray[x, y + 1] + quantError * 5/16
                    if xInBounds:
                        pixArray[x + 1, y + 1] = pixArray[x + 1, y + 1] + quantError * 1/16
        return pixArray

    def ditherImage(self, pixArray, values, valueThresholds=None, out=None):
        if valueThresholds is None or len(valueThresholds) != values:
            valueThresholds = np.linspace(0, 255, values).astype(np.float32)
        result = self.__floydSteinbergDither(pixArray, valueThresholds)
        if out is not None:
            out[:] = result
            return out
        else:
            return result
        

class AtkinsonDithering(DitherAlgorithm):
    @staticmethod
    @njit(cache=True)
    def __atkinsonDither(pixArray, valueThresholds):
        width, height = pixArray.shape
        for y in range(height):
            for x in range(width):
                oldPixel = pixArray[x, y]
                bestMatch = 0
                bestDist = abs(valueThresholds[0] - oldPixel)
                for i in range(1, len(valueThresholds)):
                    dist = abs(valueThresholds[i] - oldPixel)
                    if dist < bestDist:
                        bestDist = dist
                        bestMatch = i
                newPixel = valueThresholds[bestMatch]
                pixArray[x, y] = newPixel
                quantError = oldPixel - newPixel
                xInBounds = x + 1 < width
                yInBounds = y + 1 < height
                if xInBounds:
                    pixArray[x + 1, y] = pixArray[x + 1, y] + quantError/8
                    if x + 2 < width: pixArray[x + 2, y] = pixArray[x + 2, y] + quantError/8
                if yInBounds:
                    pixArray[x, y + 1] = pixArray[x, y + 1] + quantError/8
                    if xInBounds:
                        pixArray[x + 1, y + 1] = pixArray[x + 1, y + 1] + quantError/8
                    if x - 1 >= 0:
                        pixArray[x - 1, y + 1] = pixArray[x - 1, y + 1] + quantError/8    
                    if y + 2 < height:
                        pixArray[x, y + 2] = pixArray[x, y + 2] + quantError/8
        return pixArray

    def ditherImage(self, pixArray, values, valueThresholds=None, out=None):
        if valueThresholds is None or len(valueThresholds) != values:
            valueThresholds = np.linspace(0, 255, values).astype(np.float32)
        result = self.__atkinsonDither(pixArray, valueThresholds)
        if out is not None:
            out[:] = result
            return out
        else:
            return result
        
class VerticalDiffusionDithering(DitherAlgorithm):
    @staticmethod
    @njit(cache=True)
    def __verticalDiffusionDither(pixArray, valueThresholds):
        width, height = pixArray.shape
        for y in range(height):
            for x in range(width):
                oldPixel = pixArray[x, y]
                bestMatch = 0
                bestDist = abs(valueThresholds[0] - oldPixel)
                for i in range(1, len(valueThresholds)):
                    dist = abs(valueThresholds[i] - oldPixel)
                    if dist < bestDist:
                        bestDist = dist
                        bestMatch = i
                newPixel = valueThresholds[bestMatch]
                pixArray[x, y] = newPixel
                quantError = oldPixel - newPixel
                if x + 1 > width:
                    pixArray[x + 1, y] = pixArray[x + 1, y] + quantError * 2/8
                if y + 1 < height:
                    pixArray[x, y + 1] = pixArray[x, y + 1] + quantError * 4/8
                    if y + 2 < height:
                        pixArray[x, y + 2] = pixArray[x, y + 2] + quantError * 2/8
        return pixArray

    def ditherImage(self, pixArray, values, valueThresholds=None, out=None):
        if valueThresholds is None or len(valueThresholds) != values:
            valueThresholds = np.linspace(0, 255, values).astype(np.float32)
        result = self.__verticalDiffusionDither(pixArray, valueThresholds)
        if out is not None:
            out[:] = result
            return out
        else:
            return result

