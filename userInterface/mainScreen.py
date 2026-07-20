import sys
import numpy as np
from PyQt5.QtCore import (QCoreApplication, QMetaObject, QObject, QPoint,
    QRect, QSize, QUrl, Qt, QTimer)
from PyQt5.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QLinearGradient, QPalette, QPainter, QPixmap,
    QRadialGradient, QImage)
from PyQt5.QtWidgets import *
from pyqt_color_picker import ColorPickerDialog
from ditherer import ditherer as d
from ditherer import ditherAlgorithm as da

class NavBar(QWidget):
    def __init__(self, tab_names, stack: QStackedWidget):
        super().__init__()
        

class MainScreen(QMainWindow):
    __appHeight = d.MAX_DIMENSIONS + 100
    __appWidth = d.MAX_DIMENSIONS + 600
    __backgroundColor = QColor(20,20,20)
    __textColor = QColor(231, 231, 231)
    __menuTopSpacing = 100
    __menuBetweenStretch = 1
    __menuBottomStretch = 4

    __ditherer = d.ImageDitherer()
    __bayer2x2 = da.BayerOrdered()
    __bayer4x4 = da.BayerOrdered()
    __bayer4x4.setMatrixSize(3)
    __floydStien = da.FloydSteinberg()
    __atkinson = da.AtkinsonDithering()
    __vert = da.VerticalDiffusionDithering()
    __currValues = 0

    def __init__(self):
        super().__init__()
        self.__ditherPause = QTimer()
        self.__ditherPause.setSingleShot(True)
        self.__ditherPause.setInterval(200)
        self.__ditherPause.timeout.connect(self.__updatePixMap)

        self.__chosenAlgorithm = self.__bayer2x2
        outerLayout = QHBoxLayout()
        centralWidget = QWidget()
        centralWidget.setLayout(outerLayout)

        menuLayout = QVBoxLayout()
        menuLayout.addLayout(self.__createNavBar(), 0)
        menuLayout.addLayout(self.__createMenus(centralWidget), 1)
        menuLayout.addLayout(self.__createLoadSaveButtons(), 0)

        imgLayout = self.__createImgLayout()
        
        outerLayout.addLayout(imgLayout, 5)
        outerLayout.addLayout(menuLayout, 3)

        self.setCentralWidget(centralWidget)
        self.setMinimumSize(QSize(self.__appWidth, self.__appHeight))
        self.setWindowTitle("_dither_tool")
        self.setStyleSheet(f"background-color: {self.__backgroundColor.name()};")
        
    def __createImgLayout(self):
        imgLayout = QVBoxLayout()

        self.__img = QLabel()
        self.__updatePixMap()
        self.__img.setScaledContents(False)
        self.__img.setAlignment(Qt.AlignCenter)
        imgLayout.addWidget(self.__img, 1)
        return imgLayout
    
    def __createMenus(self, centralWidget):
        stackedWidget = QStackedWidget(centralWidget)
        adjust = self.__createAdjustPage()
        dithering = self.__createDitheringPage()
        effects = self.__createEffectsPage()
        stackedWidget.addWidget(adjust)
        stackedWidget.addWidget(dithering)
        stackedWidget.addWidget(effects)
        menus = QHBoxLayout()
        menus.addWidget(stackedWidget)
        index = 0
        for button in self.buttonGroup.buttons():
            button.clicked.connect(lambda checked, i=index: stackedWidget.setCurrentIndex(i))
            index += 1
        return menus
    
    def __createAdjustPage(self):
        settingsPage = QWidget()
        pageLayout = QVBoxLayout()
        settingsPage.setLayout(pageLayout)
        pageLayout.addSpacing(self.__menuTopSpacing)

        contrastLabel = self.__createLabel("Contrast", "ContrastLabel")
        self.__contrastSlider = self.__createSlider("ContrastSlider", d.MIN_CONTRAST, d.MAX_CONTRAST, int((d.MAX_CONTRAST + d.MIN_CONTRAST) / 2), settingsPage.width())
        pageLayout.addWidget(contrastLabel, 0)
        pageLayout.addWidget(self.__contrastSlider, 0, alignment=Qt.AlignHCenter)
        pageLayout.addStretch(self.__menuBetweenStretch)

        brightnessLabel = self.__createLabel("Brightness", "BrightnessLabel")
        self.__brightnessSlider = self.__createSlider("BrightnessSlider", d.MIN_BRIGHTNESS, d.MAX_BRIGHTNESS, int((d.MIN_BRIGHTNESS + d.MAX_BRIGHTNESS) / 2), settingsPage.width())
        pageLayout.addWidget(brightnessLabel, 0)
        pageLayout.addWidget(self.__brightnessSlider, 0, alignment=Qt.AlignHCenter)

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
        self.__noiseSlider = self.__createSlider("NoiseSlider", d.MIN_NOISE, d.MAX_NOISE, d.MIN_NOISE, ditheringPage.width())
        pageLayout.addWidget(noiseLabel, 0)
        pageLayout.addWidget(self.__noiseSlider, 0, alignment=Qt.AlignHCenter)
        pageLayout.addStretch(self.__menuBetweenStretch)

        valuesLabel = self.__createLabel("Values", "ValuesLabel")
        self.__valuesSlider = self.__createSlider("ValuesSlider", d.MIN_VALUES, d.MAX_VALUES, d.MIN_VALUES, ditheringPage.width())
        self.__valuesSlider.setPageStep(1)
        self.__valuesSlider.setSingleStep(1)
        self.__valuesSlider.valueChanged.connect(self.__createColourPickerButtons)
        pageLayout.addWidget(valuesLabel, 0)
        pageLayout.addWidget(self.__valuesSlider, 0, alignment=Qt.AlignHCenter)
        pageLayout.addStretch(self.__menuBetweenStretch)

        pixelLabel = self.__createLabel("Pixel Size", "PixelsLabel")
        self.__pixelSlider = self.__createSlider("PixelSlider", d.MIN_PIXEL_SIZE, d.MAX_PIXEL_SIZE, d.MIN_PIXEL_SIZE, ditheringPage.width())
        self.__pixelSlider.setPageStep(1)
        self.__pixelSlider.setSingleStep(1)
        pageLayout.addWidget(pixelLabel, 0)
        pageLayout.addWidget(self.__pixelSlider, 0, alignment=Qt.AlignHCenter)

        pageLayout.addStretch(self.__menuBottomStretch)
        return ditheringPage

    def __createEffectsPage(self):
        effectsPage = QWidget()
        pageLayout = QVBoxLayout()
        effectsPage.setLayout(pageLayout)
        pageLayout.addSpacing(self.__menuTopSpacing)

        widget = QWidget()
        widget.setFixedSize(QSize(300, 200))
        self.__colourPickerLayout = QGridLayout()
        COLS = 3
        ROWS = 2
        for col in range(COLS):
            self.__colourPickerLayout.setColumnMinimumWidth(col, 75)
        for row in range(ROWS):
            self.__colourPickerLayout.setRowMinimumHeight(row, 75)
        self.__colourPickerLayout.setHorizontalSpacing(10)
        self.__colourPickerLayout.setVerticalSpacing(10)
        self.__createColourPickerButtons(d.MIN_VALUES)
        widget.setLayout(self.__colourPickerLayout)
        pageLayout.addWidget(widget, alignment=Qt.AlignHCenter)
        pageLayout.addStretch(self.__menuBetweenStretch)

        bloomIntensityLabel = self.__createLabel("Bloom Intensity", "BloomIntensityLabel")
        self.__bloomIntensitySlider = self.__createSlider("BloomIntensitySlider", d.MIN_BLOOM_LEVEL, d.MAX_BLOOM_LEVEL, d.MIN_BLOOM_LEVEL, effectsPage.width())
        self.__bloomIntensitySlider.setPageStep(d.MAX_BLOOM_LEVEL//5)
        pageLayout.addWidget(bloomIntensityLabel, 0)
        pageLayout.addWidget(self.__bloomIntensitySlider, 0, alignment=Qt.AlignHCenter)
        pageLayout.addStretch(self.__menuBetweenStretch)

        bloomSpreadLabel = self.__createLabel("Bloom Spread", "BloomSpreadLabel")
        self.__bloomSpreadSlider = self.__createSlider("BloomSpreadSlider", d.MIN_BLOOM_SPREAD, d.MAX_BLOOM_SPREAD, d.MIN_BLOOM_SPREAD, effectsPage.width())
        self.__bloomSpreadSlider.setPageStep(d.MAX_BLOOM_SPREAD//5)
        pageLayout.addWidget(bloomSpreadLabel, 0)
        pageLayout.addWidget(self.__bloomSpreadSlider, 0, alignment=Qt.AlignHCenter)
        
        pageLayout.addStretch(self.__menuBottomStretch)
        return effectsPage

    def __createNavBar(self):
        buttons = []
        buttons.append(self.__createPushButton("Adjust", "AdjustButton"))
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
    
    def __createLoadSaveButtons(self):
        saveBtn = self.__createPushButton("save", "save")
        saveBtn.clicked.connect(self.__saveFileDialog)
        loadBtn = self.__createPushButton("load", "load")
        loadBtn.clicked.connect(self.__loadFileDialog)
        saveLoadLayout = QHBoxLayout()
        saveLoadLayout.addWidget(loadBtn,0)
        saveLoadLayout.addWidget(saveBtn,0)
        return saveLoadLayout
    
    def __loadFileDialog(self):
        filename, _ = QFileDialog.getOpenFileName(
        self,
        "Select a File",
        "",
        "Images (*.png *.jpg)"
        )

        if filename:
            self.__updatePixMap(str(filename))
            self.__resetSettings()
    
    def __saveFileDialog(self):
        filename, _ = QFileDialog.getSaveFileName(
        self,
        "Save image",
        "ditheredImage",
        "*.png"
        )
        if filename:
            self.__ditherer.saveImage(str(filename))
        
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
        slider.setPageStep((abs(minValue) + abs(maxValue))//20)
        slider.setSingleStep((abs(minValue) + abs(maxValue))//20)
        slider.valueChanged.connect(lambda value: self.__ditherPause.start())
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
        ditherOptions.currentTextChanged.connect(self.__setDitherAlgorithm)
        return ditherOptions    
    
    def __createColourPickerButtons(self, value):
        rgbValues = np.linspace(0, 255, value).astype(np.uint8)
        if self.__currValues < value:
            for i in range(self.__currValues, value):
                button = self.__createPushButton(f"{i+1} Colour", f"ColourPicker{i+1}")
                
                button.setFixedSize(QSize(75, 75))
                position = (i//3, i%3)
                self.__colourPickerLayout.addWidget(button, position[0], position[1])
        elif self.__currValues > value:
            for i in range (self.__currValues, value, -1):
                button = self.__colourPickerLayout.takeAt(self.__colourPickerLayout.count() - 1).widget()
                if button is not None:
                    button.setParent(None)
        for i in range(value):
            button = self.__colourPickerLayout.itemAt(i).widget()
            button.setStyleSheet(f"""font: 11pt \"Cascadia Code\";
                        text-align: center;
                        color: {self.__textColor.name()};
                        background-color: rgb({rgbValues[i]}, {rgbValues[i]}, {rgbValues[i]})""")
            
        self.__currValues = value
            

        
        
    
    def __updatePixMap(self, filePath= None):
        if filePath:
            self.__ditherer.loadImage(filePath)
        
        imgArray = np.ascontiguousarray(self.__ditherer.dither(ditherMethod=self.__chosenAlgorithm, \
                                                               brightness=self.__brightnessSlider.value(), contrast=self.__contrastSlider.value(), \
                                                               noiseLevel=self.__noiseSlider.value(), values=self.__valuesSlider.value(), pixelSize=self.__pixelSlider.value(), \
                                                               bloomLevel=self.__bloomIntensitySlider.value(), bloomSpread=self.__bloomSpreadSlider.value() ).astype(np.uint8))
        height, width = imgArray.shape[:2]
        if imgArray.ndim == 2:
            image = QImage(imgArray.data, width, height, width, QImage.Format_Grayscale8)
        else:
            image = QImage(imgArray.data, width, height, width*3, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(image.copy())
        self.__img.setPixmap(pixmap)
    
    def __resetSettings(self):
        self.__contrastSlider.setValue((d.MAX_CONTRAST + d.MIN_CONTRAST) // 2)
        self.__brightnessSlider.setValue((d.MAX_BRIGHTNESS + d.MIN_BRIGHTNESS) //2)

        self.__noiseSlider.setValue(d.MIN_NOISE)
        self.__valuesSlider.setValue(d.MIN_VALUES)
        self.__pixelSlider.setValue(d.MIN_PIXEL_SIZE)

        self.__bloomIntensitySlider.setValue(d.MIN_BLOOM_LEVEL)
        self.__bloomSpreadSlider.setValue(d.MIN_BLOOM_SPREAD)

    
    def __setDitherAlgorithm(self, value):
        match value:
            case "Bayer's 2x2":
                self.__chosenAlgorithm = self.__bayer2x2
            case "Bayer's 4x4": 
                self.__chosenAlgorithm = self.__bayer4x4
            case "Floyd Steinberg":
                self.__chosenAlgorithm = self.__floydStien
            case "Atkinson":
                self.__chosenAlgorithm = self.__atkinson
            case "Vertical Diffusion":
                self.__chosenAlgorithm = self.__vert
        self.__ditherPause.start()
