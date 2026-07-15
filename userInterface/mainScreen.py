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
    __backgroundColor = QColor(20,20,20)
    __textColor = QColor(231, 231, 231)
    __menuTopSpacing = 100
    __menuBetweenStretch = 1
    __menuBottomStretch = 4

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
        self.setStyleSheet(f"background-color: {self.__backgroundColor.name()};")
        
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
        pageLayout.addSpacing(self.__menuTopSpacing)
        
        contrastLabel = self.__createLabel("Contrast", "ContrastLabel")
        contrastSlider = self.__createSlider("ContrastSlider", d.MIN_CONTRAST, d.MAX_CONTRAST, int((d.MAX_CONTRAST + d.MIN_CONTRAST) / 2), settingsPage.width())
        pageLayout.addWidget(contrastLabel, 0)
        pageLayout.addWidget(contrastSlider, 0, alignment=Qt.AlignHCenter)
        pageLayout.addStretch(self.__menuBetweenStretch)

        brightnessLabel = self.__createLabel("Brightness", "BrightnessLabel")
        brightnessSlider = self.__createSlider("BrightnessSlider", d.MIN_BRIGHTNESS, d.MAX_BRIGHTNESS, int((d.MIN_BRIGHTNESS + d.MAX_BRIGHTNESS) / 2), settingsPage.width())
        pageLayout.addWidget(brightnessLabel, 0)
        pageLayout.addWidget(brightnessSlider, 0, alignment=Qt.AlignHCenter)

        pageLayout.addStretch(self.__menuBottomStretch)        
        return settingsPage

    def __createDitheringPage(self):
        ditheringPage = QWidget()
        pageLayout = QVBoxLayout()
        ditheringPage.setLayout(pageLayout)
        pageLayout.addSpacing(self.__menuTopSpacing)

        ditherOptionsLabel = self.__createLabel("Dithering Algorithms", "DitherOptionsLabel")
        ditherOptions = self.__createDitheringOptions(ditheringPage.width())
        pageLayout.addWidget(ditherOptionsLabel, 0)
        pageLayout.addSpacing(40)
        pageLayout.addWidget(ditherOptions, 0, alignment=Qt.AlignHCenter)
        pageLayout.addStretch(self.__menuBetweenStretch)

        noiseLabel = self.__createLabel("Noise", "NoiseLabel")
        noiseSlider = self.__createSlider("NoiseSlider", d.MIN_NOISE, d.MAX_NOISE, d.MIN_NOISE, ditheringPage.width())
        pageLayout.addWidget(noiseLabel, 0)
        pageLayout.addWidget(noiseSlider, 0, alignment=Qt.AlignHCenter)
        pageLayout.addStretch(self.__menuBetweenStretch)

        valuesLabel = self.__createLabel("Values", "ValuesLabel")
        valuesSlider = self.__createSlider("ValuesSlider", d.MIN_VALUES, d.MAX_VALUES, d.MIN_VALUES, ditheringPage.width())
        valuesSlider.setPageStep(1)
        pageLayout.addWidget(valuesLabel, 0)
        pageLayout.addWidget(valuesSlider, 0, alignment=Qt.AlignHCenter)

        pageLayout.addStretch(self.__menuBottomStretch)
        return ditheringPage

    def __createEffectsPage(self):
        effectsPage = QWidget()
        pageLayout = QVBoxLayout()
        effectsPage.setLayout(pageLayout)
        pageLayout.addSpacing(self.__menuTopSpacing)
        
        
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
                        color: {self.__textColor.name()};"""
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
                        color: {self.__textColor.name()};"""
        label = QLabel(self)
        label.setObjectName(labelName)
        label.setStyleSheet(styleSheet)
        label.setText(text)
        label.setAlignment(Qt.AlignHCenter)
        label.adjustSize() 
        return label

    def __createDitheringOptions(self, width):
        styleSheet = f"""font: 13pt \"Cascadia Code\";
                text-align: center;
                color: {self.__textColor.name()};"""
        ditherOptions = QComboBox()
        ditherOptions.addItems(["Bayer's 2x2", "Bayer's 4x4", "Floyd Steinberg", "Atkinson", "Vertical Diffusion"])
        ditherOptions.setObjectName("DitherOptionsComboBox")
        ditherOptions.setMinimumWidth(int(width * 0.42))
        ditherOptions.setMaximumWidth(int(width * 0.42))
        ditherOptions.setStyleSheet(styleSheet)
        return ditherOptions