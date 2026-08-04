from userInterface import mainScreen as ms
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon

app = QApplication(sys.argv)
screen = ms.MainScreen()
screen.show()
app.exec_()




