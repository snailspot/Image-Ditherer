import sys
from PyQt5.QtCore import (QCoreApplication, QMetaObject, QObject, QPoint,
    QRect, QSize, QUrl, Qt)
from PyQt5.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QLinearGradient, QPalette, QPainter, QPixmap,
    QRadialGradient)
from PyQt5.QtWidgets import *

class NavBar(QWidget):
    def __init__(self, tab_names, stack: QStackedWidget):
        super().__init__()
        

class MainScreen(QMainWindow):
    __appHeight = 800
    __appWidth = 1200
    backgroundColor = QColor(30,30,30)
    textColor = QColor(231, 231, 231)

    def __init__(self):
        super().__init__()

        outerLayout = QHBoxLayout()
        imgLayout = QVBoxLayout()
        menuLayout = QVBoxLayout()
        outerLayout.addLayout(imgLayout, 5)
        outerLayout.addLayout(menuLayout, 3)

        navBarLayout = QHBoxLayout()
        menuLayout.addLayout(navBarLayout)
        navBarLayout.addWidget(self.__createPushButton("Settings", "SettingsButton"), 1)
        navBarLayout.addWidget(self.__createPushButton("Dithering", "DitheringButton"), 1)
        navBarLayout.addWidget(self.__createPushButton("Effects", "EffectsButton"), 1)
        menuLayout.addStretch(1)
        
        img = QLabel()
        img.setPixmap(QPixmap('output.png'))
        img.setScaledContents(False)
        imgLayout.addWidget(img, alignment=Qt.AlignHCenter)

        centralWidget = QWidget()
        centralWidget.setLayout(outerLayout)
        self.setCentralWidget(centralWidget)
        self.setMinimumSize(QSize(self.__appWidth, self.__appHeight))
        self.setWindowTitle("_dither_tool")
        self.setStyleSheet(f"background-color: {self.backgroundColor.name()};")
        



    def __createPushButton(self, label, buttonName):
        styleSheet = f"""font: 11pt \"Cascadia Code\";
                        text-align: center;
                        color: {self.textColor.name()};"""
        button = QPushButton(self)
        button.setObjectName(buttonName)
        button.setStyleSheet(styleSheet)
        button.setText(label)
        button.adjustSize()
        return button
        
    
    def __createLabel(self, pos: QPoint, styleSheet, text):
        label = QLabel(self)
        label.setObjectName(u"Hero Header")
        label.move(pos)
        label.setStyleSheet(styleSheet)
        label.setText(text)
        label.adjustSize() 
        return label