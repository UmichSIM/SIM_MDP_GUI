# This Python file uses the following encoding: utf-8
import os
from pathlib import Path
import sys
from Config import freeway_dict, intersection_dict

#Main windows
from MainScreen import Ui_MainScreen
from FMain import Ui_FullDisplay
from MainIntersection import Ui_Widget as Ui_Intersection


#Freeway (FMain is Main Freeway) 
from EditFreeway import Ui_Widget as Ui_EditFreeway

#Intersection 
from EditSingleVehicleIntsctn import Ui_EditSingleVehicleInsctn as Ui_IntersectionSpawnVehicle
from SingleIntersection import Ui_Form as Ui_SingleIntersection
from TrafficLightSettings import Ui_TrafficLightSettings
from AddVehicleIntersection import Ui_Form as Ui_AddVehicleSettings
from TrafficLightSettings import Ui_TrafficLightSettings as Ui_Traffic


#Other 
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
        
class editIntersection(QMainWindow, Ui_SingleIntersection):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.show()

class trafficLightSetting(QMainWindow, Ui_TrafficLightSettings):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.show()

class addVehicleIntersection(QMainWindow, Ui_AddVehicleSettings):
     def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.show()

class Traffic(QWidget,Ui_Traffic):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.show()
        
class MainApp(QWidget):
    def print_debug(self):
        print("allow collision was clicked")

    def __init__(self, parent=None):

        # Init Screens
        self.mainScreen = mainScreen()
        self.mainIntersection = mainIntersection()
        self.fmain = fmain()

        self.editFreeway1 = editFreeway()
        self.editFreeway2 = editFreeway()
        self.editFreeway3 = editFreeway()
        self.editFreeway4 = editFreeway()
        self.editFreeway5 = editFreeway()

        self.editIntersection1 = editIntersection()
        self.editIntersection2 = editIntersection()
        self.editIntersection3 = editIntersection()
        self.editIntersection4 = editIntersection()

        self.Traffic1 = Traffic()
        self.Traffic2 = Traffic()
        self.Traffic3 = Traffic()
        self.Traffic4 = Traffic()
        

        self.stack = QStackedWidget()

        # Connect Buttons
        #Freeway
        self.mainScreen.Fway_bttn.clicked.connect(lambda: self.stack.setCurrentWidget(self.fmain))
        self.fmain.Back_bttn.clicked.connect(lambda: self.stack.setCurrentWidget(self.mainScreen))

        #Edit Freeway
        self.fmain.Fway_1_bttn.clicked.connect(lambda: self.stack.setCurrentWidget(self.editFreeway1))
        # if self.fmain.Fway_1_bttn.clicked:
        #     print(self.fmain.NumFwaySections_spinbx)
        self.editFreeway1.general_settings_btn.clicked.connect(lambda: self.stack.setCurrentWidget(self.fmain))
        self.fmain.Fway_2_bttn.clicked.connect(lambda: self.stack.setCurrentWidget(self.editFreeway2))
        self.editFreeway2.general_settings_btn.clicked.connect(lambda: self.stack.setCurrentWidget(self.fmain))
        self.fmain.Fway_3_bttn.clicked.connect(lambda: self.stack.setCurrentWidget(self.editFreeway3))
        self.editFreeway3.general_settings_btn.clicked.connect(lambda: self.stack.setCurrentWidget(self.fmain))
        self.fmain.Fway_4_bttn.clicked.connect(lambda: self.stack.setCurrentWidget(self.editFreeway4))
        self.editFreeway4.general_settings_btn.clicked.connect(lambda: self.stack.setCurrentWidget(self.fmain))
        self.fmain.Fway_5_bttn.clicked.connect(lambda: self.stack.setCurrentWidget(self.editFreeway5))
        self.editFreeway5.general_settings_btn.clicked.connect(lambda: self.stack.setCurrentWidget(self.fmain))
        self.fmain.AllowCollisions_chkbx.toggled.connect(self.print_debug)

        """if self.fmain.AllowCollisions_chkbx.isChecked() == True:
            self.print_debug()
        elif self.fmain.AllowCollisions_chkbx.isChecked() == False:
            self.print_debug()"""
        """
        if self.fmain.AllowCollisions_chkbx.isChecked() == True:
            self.print_debug
        """

       
        #Intersection
        self.mainScreen.Instcn_bttn.clicked.connect(lambda: self.stack.setCurrentWidget(self.mainIntersection))
        self.mainIntersection.back_bttn.clicked.connect(lambda: self.stack.setCurrentWidget(self.mainScreen))

        #Edit Intersection
        self.mainIntersection.intersectionLane_1_bttn.clicked.connect(lambda: self.stack.setCurrentWidget(self.editIntersection1))
        self.editIntersection1.pushButton.clicked.connect(lambda: self.stack.setCurrentWidget(self.mainIntersection))
        self.mainIntersection.intersectionLane_2_bttn.clicked.connect(lambda: self.stack.setCurrentWidget(self.editIntersection2))
        self.editIntersection2.pushButton.clicked.connect(lambda: self.stack.setCurrentWidget(self.mainIntersection))
        self.mainIntersection.intersectionLane_3_bttn.clicked.connect(lambda: self.stack.setCurrentWidget(self.editIntersection3))
        self.editIntersection3.pushButton.clicked.connect(lambda: self.stack.setCurrentWidget(self.mainIntersection))
        self.mainIntersection.intersectionLane_4_bttn.clicked.connect(lambda: self.stack.setCurrentWidget(self.editIntersection4))
        self.editIntersection4.pushButton.clicked.connect(lambda: self.stack.setCurrentWidget(self.mainIntersection))
        
        #Traffic
        self.editIntersection1.trafficLight_bttn.clicked.connect(lambda:self.stack.setCurrentWidget(self.Traffic1))
        self.Traffic1.Back_bttn.clicked.connect(lambda: self.stack.setCurrentWidget(self.editIntersection1))
        self.editIntersection2.trafficLight_bttn.clicked.connect(lambda:self.stack.setCurrentWidget(self.Traffic2))
        self.Traffic2.Back_bttn.clicked.connect(lambda: self.stack.setCurrentWidget(self.editIntersection2))
        self.editIntersection3.trafficLight_bttn.clicked.connect(lambda:self.stack.setCurrentWidget(self.Traffic3))
        self.Traffic3.Back_bttn.clicked.connect(lambda: self.stack.setCurrentWidget(self.editIntersection3))
        self.editIntersection4.trafficLight_bttn.clicked.connect(lambda:self.stack.setCurrentWidget(self.Traffic4))
        self.Traffic4.Back_bttn.clicked.connect(lambda: self.stack.setCurrentWidget(self.editIntersection4))


        # Add All Screens to Stack
        self.stack.addWidget(self.mainScreen)
        self.stack.addWidget(self.mainIntersection)
        self.stack.addWidget(self.fmain)
        self.stack.addWidget(self.editFreeway1)
        self.stack.addWidget(self.editFreeway2)
        self.stack.addWidget(self.editFreeway3)
        self.stack.addWidget(self.editFreeway4)
        self.stack.addWidget(self.editFreeway5)
        self.stack.addWidget(self.editIntersection1)
        self.stack.addWidget(self.editIntersection2)
        self.stack.addWidget(self.editIntersection3)
        self.stack.addWidget(self.editIntersection4)
        self.stack.addWidget(self.Traffic1)
        self.stack.addWidget(self.Traffic2)
        self.stack.addWidget(self.Traffic3)
        self.stack.addWidget(self.Traffic4)
    

        # Set Initial Settings
        self.stack.resize(800,800)
        self.stack.setCurrentIndex(0) # Default first screen
        self.stack.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    x = MainApp()
    sys.exit(app.exec())
