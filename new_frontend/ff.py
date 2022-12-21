# This Python file uses the following encoding: utf-8
import os
from pathlib import Path
import sys


#Main windows
from MainScreen import Ui_MainScreen
from FMain import Ui_FullDisplay
from MainIntersection import Ui_Widget as Ui_Intersection


#Freeway
from EditFreeway import Ui_Widget as Ui_EditFreeway


from PyQt6.QtWidgets import QWidget, QApplication, QMainWindow, QStackedWidget, QHBoxLayout
class mainScreen(QMainWindow,Ui_MainScreen):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.show()


class mainIntersection(QMainWindow,Ui_Intersection):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.show()


class fmain(QMainWindow,Ui_FullDisplay):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.show()


class editFreeway(QMainWindow,Ui_EditFreeway):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.show()


class MainApp(QWidget):
    def __init__(self, parent=None):

        self.mainScreen = mainScreen()
        self.mainIntersection = mainIntersection()
        self.fmain = fmain()

        self.editFreeway1 = editFreeway()
        self.editFreeway2 = editFreeway()
        self.editFreeway3 = editFreeway()
        self.editFreeway4 = editFreeway()
        self.editFreeway5 = editFreeway()
        self.stack = QStackedWidget()
        #Freeway
        self.mainScreen.Fway_bttn.clicked.connect(lambda: self.stack.setCurrentWidget(self.fmain))
        self.fmain.Back_bttn.clicked.connect(lambda: self.stack.setCurrentWidget(self.mainScreen))

        #Edit Freeway
        self.fmain.Fway_1_bttn.clicked.connect(lambda: self.stack.setCurrentWidget(self.editFreeway1))
        self.editFreeway1.general_settings_btn.clicked.connect(lambda: self.stack.setCurrentWidget(self.fmain))
        self.fmain.Fway_2_bttn.clicked.connect(lambda: self.stack.setCurrentWidget(self.editFreeway2))
        self.editFreeway2.general_settings_btn.clicked.connect(lambda: self.stack.setCurrentWidget(self.fmain))
        self.fmain.Fway_3_bttn.clicked.connect(lambda: self.stack.setCurrentWidget(self.editFreeway3))
        self.editFreeway3.general_settings_btn.clicked.connect(lambda: self.stack.setCurrentWidget(self.fmain))
        self.fmain.Fway_4_bttn.clicked.connect(lambda: self.stack.setCurrentWidget(self.editFreeway4))
        self.editFreeway4.general_settings_btn.clicked.connect(lambda: self.stack.setCurrentWidget(self.fmain))
        self.fmain.Fway_5_bttn.clicked.connect(lambda: self.stack.setCurrentWidget(self.editFreeway5))
        self.editFreeway5.general_settings_btn.clicked.connect(lambda: self.stack.setCurrentWidget(self.fmain))


        #Intersection
        self.mainScreen.Instcn_bttn.clicked.connect(lambda: self.stack.setCurrentWidget(self.mainIntersection))
        self.mainIntersection.back_bttn.clicked.connect(lambda: self.stack.setCurrentWidget(self.mainScreen))

        
        self.stack.addWidget(self.mainScreen)
        self.stack.addWidget(self.mainIntersection)
        self.stack.addWidget(self.fmain)
        self.stack.addWidget(self.editFreeway1)
        self.stack.addWidget(self.editFreeway2)
        self.stack.addWidget(self.editFreeway3)
        self.stack.addWidget(self.editFreeway4)
        self.stack.addWidget(self.editFreeway5)

        # Set Initial Settings
        self.stack.resize(800,800)
        self.stack.setCurrentIndex(0) # Default first screen
        self.stack.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    x = MainApp()
    sys.exit(app.exec())