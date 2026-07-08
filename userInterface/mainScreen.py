import sys
from PyQt5.QtCore import (QCoreApplication, QMetaObject, QObject, QPoint,
    QRect, QSize, QUrl, Qt)
from PyQt5.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QLinearGradient, QPalette, QPainter, QPixmap,
    QRadialGradient)
from PyQt5.QtWidgets import *

class MainScreen(QMainWindow):
    __appHeight = 800
    __appWidth = 1200
    backgroundColor = QColor(48,48,48)
    textColor = QColor(231, 231, 231)
    headerPoint = QPoint(0, 0)
    headerSS =          f"""font: 20pt \"Cascadia Code Light\";
                        color: {textColor.name()};
                        padding-left: 20px;
                        padding-top: 12px;"""
            
    subHeadingSS =      f"""font: 14pt \"Cascadia Code Light\";
                        color: {textColor.name()};"""

    def __init__(self):
        super().__init__()
        self.setFixedSize(QSize(self.__appWidth, self.__appHeight))
        self.setWindowTitle("_dither_tool")
        self.setStyleSheet(f"background-color: {self.backgroundColor.name()};")
        self.headerLabel = self.__createLabel(self.headerPoint, self.headerSS, "__dither_tool")

        self.preProcessingLabel = self.__createLabel(QPoint(680, 90), self.subHeadingSS, "_preprocessing")
        self.ditherSettingLabel = self.__createLabel(QPoint(950, 90), self.subHeadingSS, "_dither_settings")
        self.ditherSettingLabel = self.__createLabel(QPoint(680, 380), self.subHeadingSS, "_postprocessing")
        
    
    def __createLabel(self, pos: QPoint, styleSheet, text):
        label = QLabel(self)
        label.setObjectName(u"Hero Header")
        label.move(pos)
        label.setStyleSheet(styleSheet)
        label.setText(text)
        label.adjustSize() 
        return label