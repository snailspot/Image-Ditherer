import sys
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow

class MainScreen(QMainWindow):
    __appHeight = 800
    __appWidth = 1200

    def __init__(self):
        super().__init__()
        self.setFixedSize(QSize(self.__appWidth, self.__appHeight))
        self.setWindowTitle("_dither_tool")
        