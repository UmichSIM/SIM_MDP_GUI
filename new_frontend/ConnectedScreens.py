# This Python file uses the following encoding: utf-8
import os
from pathlib import Path
import sys
from Config import freeway_dict, intersection_dict

#Main windows
from generated_ui.MainScreen import Ui_MainScreen
from generated_ui.FMain import Ui_FullDisplay
from generated_ui.MainIntersection import Ui_Widget as Ui_Intersection


#Freeway (FMain is Main Freeway) 
from generated_ui.EditFreeway import Ui_Widget as Ui_EditFreeway

#Intersection 
from generated_ui.EditSingleVehicleIntsctn import Ui_EditSingleVehicleInsctn as Ui_IntersectionSpawnVehicle
from generated_ui.SingleIntersection import Ui_Form as Ui_SingleIntersection
from generated_ui.TrafficLightSettings import Ui_TrafficLightSettings
from generated_ui.AddVehicleIntersection import Ui_Form as Ui_AddVehicleSettings
from generated_ui.TrafficLightSettings import Ui_TrafficLightSettings as Ui_Traffic


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
    def allow_collisions(self):
        #Sets the freeway min_speed setting to 20
        freeway_dict['allow_collision'] = self.AllowCollisions_chkbx.isChecked()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.show()
        self.AllowCollisions_chkbx.stateChanged.connect(lambda: self.allow_collisions())



class editFreeway(QMainWindow,Ui_EditFreeway):
    def set(self, laneNum):
        subjectLaneVehicle = freeway_dict['lane'+str(laneNum)]["subject_lane_vehicle"]
        leftLaneVehicle = freeway_dict['lane'+str(laneNum)]['left_lane_vehicle']

        print('Lane Number:', laneNum)

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
    def changeFreewayLanes(self, laneNum):
        self.stack.setCurrentWidget(self.editFreeway)
        self.editFreeway.set(laneNum)
        return

    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Init Screens
        self.mainScreen = mainScreen()
        self.mainIntersection = mainIntersection()
        self.fmain = fmain()

        self.editFreeway = editFreeway()

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
        self.fmain.Fway_1_bttn.clicked.connect(lambda: self.changeFreewayLanes(1))
        self.editFreeway.back_btn.clicked.connect(lambda: self.stack.setCurrentWidget(self.fmain))
        self.fmain.Fway_2_bttn.clicked.connect(lambda: self.changeFreewayLanes(2))
        self.editFreeway.back_btn.clicked.connect(lambda: self.stack.setCurrentWidget(self.fmain))
        self.fmain.Fway_3_bttn.clicked.connect(lambda: self.changeFreewayLanes(3))
        self.editFreeway.back_btn.clicked.connect(lambda: self.stack.setCurrentWidget(self.fmain))
        self.fmain.Fway_4_bttn.clicked.connect(lambda: self.changeFreewayLanes(4))
        self.editFreeway.back_btn.clicked.connect(lambda: self.stack.setCurrentWidget(self.fmain))
        self.fmain.Fway_5_bttn.clicked.connect(lambda: self.changeFreewayLanes(5))
        self.editFreeway.back_btn.clicked.connect(lambda: self.stack.setCurrentWidget(self.fmain))

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
        self.stack.addWidget(self.editFreeway)
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
    print('Start')
    app = QApplication(sys.argv)
    x = MainApp()
    sys.exit(app.exec())
