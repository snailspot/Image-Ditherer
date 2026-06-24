from abc import ABC, abstractmethod
import numpy as np
import matplotlib.pyplot as plt
import numba

class DitherAlgorithm(ABC):
    @abstractmethod
    def ditherImage(self, pixArray, colours, colourThresholds=None):
        pass

class BayerOrdered(DitherAlgorithm):
    def generateThresholdMap(self, matrixSize):
        baseMatrix = np.array([[0,3],[2,1]], dtype="float32")
        if matrixSize == 0:
            return np.array([[0]])
        prevMatrix = self.generateThresholdMap(matrixSize-1)
        matrix = np.kron(baseMatrix, np.ones_like(prevMatrix))
        matrix = matrix + np.tile(prevMatrix, (2, 2)) * 4
        return matrix
        
    def ditherImage(self, pixArray, colours=4, colourThresholds=None):



        return pixArray

class FloydSteinberg(DitherAlgorithm):
    def ditherImage(self, pixArray, colours=4, colourThresholds=None):
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