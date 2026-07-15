import sys
from PyQt5.QtCore import (QCoreApplication, QMetaObject, QObject, QPoint,
    QRect, QSize, QUrl, Qt)
from PyQt5.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QLinearGradient, QPalette, QPainter, QPixmap,
    QRadialGradient)
from PyQt5.QtWidgets import *
from ditherer import ditherer as d
from ditherer import ditherAlgorithm as da

class NavBar(QWidget):
    def __init__(self, tab_names, stack: QStackedWidget):
        super().__init__()
        

class MainScreen(QMainWindow):
    __appHeight = 800
    __appWidth = 1200
    backgroundColor = QColor(20,20,20)
    textColor = QColor(231, 231, 231)

    def __init__(self):
        super().__init__()

        outerLayout = QHBoxLayout()
        centralWidget = QWidget()
        centralWidget.setLayout(outerLayout)

        imgLayout = self.__createImgLayout()
        menuLayout = QVBoxLayout()
        outerLayout.addLayout(imgLayout, 5)
        outerLayout.addLayout(menuLayout, 3)

        menuLayout.addLayout(self.__createNavBar(), 0)
        menuLayout.addLayout(self.__createMenus(centralWidget), 1)

        self.setCentralWidget(centralWidget)
        self.setMinimumSize(QSize(self.__appWidth, self.__appHeight))
        self.setWindowTitle("_dither_tool")
        self.setStyleSheet(f"background-color: {self.backgroundColor.name()};")
        
    def __createImgLayout(self):
        imgLayout = QVBoxLayout()
        saveBtn = self.__createPushButton("save", "save")
        loadBtn = self.__createPushButton("load", "load")
        saveLoadLayout = QHBoxLayout()
        saveLoadLayout.addWidget(loadBtn,0)
        saveLoadLayout.addWidget(saveBtn,0)
        saveLoadLayout.addStretch(1)
        imgLayout.addLayout(saveLoadLayout, 0)

        img = QLabel()
        img.setPixmap(QPixmap('output.png'))
        img.setScaledContents(False)
        img.setAlignment(Qt.AlignCenter)
        imgLayout.addWidget(img, 1)
        return imgLayout
    
    def __createMenus(self, centralWidget):
        stackedWidget = QStackedWidget(centralWidget)
        settings = self.__createSettingsPage()
        dithering = self.__createDitheringPage()
        effects = self.__createEffectsPage()
        stackedWidget.addWidget(settings)
        stackedWidget.addWidget(dithering)
        stackedWidget.addWidget(effects)
        menus = QHBoxLayout()
        menus.addWidget(stackedWidget)
        index = 0
        for button in self.buttonGroup.buttons():
            button.clicked.connect(lambda checked, i=index: stackedWidget.setCurrentIndex(i))
            index += 1
        return menus
    
    def __createSettingsPage(self):
        settingsPage = QWidget()
        pageLayout = QVBoxLayout()
        settingsPage.setLayout(pageLayout)

        pageLayout.addStretch(1)
        
        contrastLabel = self.__createLabel("Contrast", "ContrastLabel")
        contrastSlider = self.__createSlider("ContrastSlider", d.MIN_CONTRAST, d.MAX_CONTRAST, int((d.MAX_CONTRAST + d.MIN_CONTRAST) / 2), settingsPage.width())
        pageLayout.addWidget(contrastLabel, 0)
        pageLayout.addWidget(contrastSlider, 0, alignment=Qt.AlignHCenter)
        pageLayout.addStretch(1)

        brightnessLabel = self.__createLabel("Brightness", "BrightnessLabel")
        brightnessSlider = self.__createSlider("BrightnessSlider", d.MIN_BRIGHTNESS, d.MAX_BRIGHTNESS, int((d.MIN_BRIGHTNESS + d.MAX_BRIGHTNESS) / 2), settingsPage.width())
        pageLayout.addWidget(brightnessLabel, 0)
        pageLayout.addWidget(brightnessSlider, 0, alignment=Qt.AlignHCenter)
        pageLayout.addStretch(4)

        return settingsPage

    def __createDitheringPage(self):
        ditheringPage = QWidget()
        pageLayout = QVBoxLayout()
        ditheringPage.setLayout(pageLayout)

        return ditheringPage

    def __createEffectsPage(self):
        effectsPage = QWidget()

        return effectsPage

    def __createNavBar(self):
        buttons = []
        buttons.append(self.__createPushButton("Settings", "SettingsButton"))
        buttons.append(self.__createPushButton("Dithering", "DitheringButton"))
        buttons.append(self.__createPushButton("Effects", "EffectsButton"))
        self.buttonGroup = QButtonGroup(self)
        self.buttonGroup.setExclusive(True)
        navBarLayout = QHBoxLayout()
        for button in buttons:
            self.buttonGroup.addButton(button)
            navBarLayout.addWidget(button, 1)
            button.setCheckable(True)
        self.buttonGroup.buttons()[0].setChecked(True)
        return navBarLayout
        
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
        
    def __createSlider(self, sliderName, minValue, maxValue, initValue, width):
        slider = QSlider()
        slider.setObjectName(sliderName)
        slider.setMinimumWidth(int(width * 0.6))
        slider.setMinimum(minValue)
        slider.setMaximum(maxValue)
        slider.setValue(initValue)
        slider.setOrientation(Qt.Horizontal)
        return slider
    
    def __createLabel(self, text, labelName):
        styleSheet = f"""font: 13pt \"Cascadia Code\";
                        text-align: center;
                        color: {self.textColor.name()};"""
        label = QLabel(self)
        label.setObjectName(labelName)
        label.setStyleSheet(styleSheet)
        label.setText(text)
        label.setAlignment(Qt.AlignHCenter)
        label.adjustSize() 
        return label