# This Python file uses the following encoding: utf-8
import os
from pathlib import Path
import sys
import json
from Config import freeway_dict, intersection_dict

#Main windows
from generated_ui.MainScreen import Ui_MainScreen
from generated_ui.FMain import Ui_FullDisplay
from generated_ui.MainIntersection import Ui_Widget as Ui_Intersection


#Freeway (FMain is Main Freeway) 
from generated_ui.EditFreeway import Ui_Widget as Ui_EditFreeway
from generated_ui.AddVehicles import Ui_Widget as Ui_AddVehicleFreeway

#Intersection 
from generated_ui.EditSingleVehicleIntsctn import Ui_EditSingleVehicleInsctn as Ui_EditSingleVehicleInsctn
from generated_ui.SingleIntersection import Ui_Form as Ui_SingleIntersection
from generated_ui.AddVehicleIntersection import Ui_Form as Ui_AddVehicleSettings
from generated_ui.TrafficLightSettings import Ui_TrafficLightSettings as Ui_Traffic
from generated_ui.TrafficLightSettingPopUp import Ui_TrafficLightSettingPopUp as Ui_TrafficLightSettingPopUp
from generated_ui.AddVehiclePopUp import Ui_addVehiclePopUp as Ui_addVehiclePopUp

#Other 
from PyQt6.QtWidgets import QWidget, QApplication, QMainWindow, QStackedWidget, QHBoxLayout

# GET: getting information/data from the user 
# SET: setting information/data from the user to the config 

class mainScreen(QMainWindow,Ui_MainScreen):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.show()


class mainIntersection(QMainWindow,Ui_Intersection):
    def update(self):
        intersection_dict["allow_collision"] = self.allow_collisions_chkbx.checkState()
        intersection_dict["max_speed"] = self.speed_spnbx.value()
        intersection_dict["safety_distance"] = self.safety_dist_spnbx.value()
        intersection_dict["num_int_section"] = self.num_intersection_spnbx.value()
        print('allow col cb')
        print("SPPEEEED:",intersection_dict["max_speed"])
        print("safetey", intersection_dict["safety_distance"])

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.allow_collisions_chkbx.stateChanged.connect(self.update)
        self.speed_spnbx.valueChanged.connect(self.update)
        self.show()

class fmain(QMainWindow, Ui_FullDisplay):
    
    def allow_collisions(self):
        #Sets the freeway min_speed setting to 20
        freeway_dict['allow_collision'] = self.AllowCollisions_chkbx.isChecked()

    def update(self):
        freeway_dict["num_freeway_section"] = self.NumFwaySections_spinbx.value()
        freeway_dict["max_speed"] = self.MaxSpped_spinbx.value()
        freeway_dict["min_speed"] = self.MinSpeed_spinbx.value()
        freeway_dict["safety_distance"] = self.SafetyDist_spinbx.value()
        
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.show()
        self.AllowCollisions_chkbx.stateChanged.connect(lambda: self.allow_collisions())
        self.NumFwaySections_spinbx.valueChanged.connect(self.update)
        self.MaxSpped_spinbx.valueChanged.connect(self.update)
        self.MinSpeed_spinbx.valueChanged.connect(self.update)
        self.SafetyDist_spinbx.valueChanged.connect(self.update)



class editFreeway(QMainWindow, Ui_EditFreeway):
    curLane = 1
    def get(self, laneNum): 
        freeway_dict['lane'+str(laneNum)]["subject_lane_vehicle"] = self.section_id_spin.currentText()
        freeway_dict['lane'+str(laneNum)]["left_lane_vehicle"] = self.section_id_spin.currentText()
        #Will be executed before switching screens, done by retaining current laneNum
    
    def set(self, laneNum):
        subjectLaneVehicle = freeway_dict['lane'+str(laneNum)]["subject_lane_vehicle"]
        leftLaneVehicle = freeway_dict['lane'+str(laneNum)]['left_lane_vehicle']
        self.section_id_spin.setCurrentText(subjectLaneVehicle)
        print('Lane Number:', laneNum)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        for i in range (1,6):
            freeway_dict['lane'+str(i)]["subject_lane_vehicle"] = self.section_id_spin.currentText()
        self.show()
        
class editIntersection(QMainWindow, Ui_SingleIntersection):
    def set(self, intersectionNum):
        subject_lane_vehicle = intersection_dict['intersection' + str(intersectionNum)]['subject_lane_vehicles']
        ahead_lane_vehicle = intersection_dict['intersection' + str(intersectionNum)]['ahead_lane_vehicles']
        right_lane_vehicle = intersection_dict['intersection' + str(intersectionNum)]['right_lane_vehicles']
        left_lane_vehicle = intersection_dict['intersection' + str(intersectionNum)]['left_lane_vehicles']
        traffic_light1 = intersection_dict['intersection' + str(intersectionNum)]['traffic_light1']
        traffic_light2 = intersection_dict['intersection' + str(intersectionNum)]['traffic_light2']
        traffic_light3 = intersection_dict['intersection' + str(intersectionNum)]['traffic_light3']
        traffic_light4 = intersection_dict['intersection' + str(intersectionNum)]['traffic_light4']

        #check if user changed subj lane vehicle variabel
        #if so, set intersection_dict['intersection' + str(intersectionNum)]['subject_lane_vehicles'] = new varibale


        # print('intersection number: ', intersectionNum)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.show()

class Traffic(QMainWindow, Ui_Traffic): 
    def set(self, trafficLightSetting, intersectionNum):
        red_light_duration = intersection_dict['intersection' + str(intersectionNum)]['traffic_light'+ str(trafficLightSetting)]["red_light_duration"]
        yellow_light_duration = intersection_dict['intersection' + str(intersectionNum)]['traffic_light'+ str(trafficLightSetting)]["yellow_light_duration"]
        green_light_duration = intersection_dict['intersection' + str(intersectionNum)]['traffic_light'+ str(trafficLightSetting)]["green_light_duration"]

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.show()

class addVehicleFreeway(QMainWindow, Ui_AddVehicleFreeway):
     def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.show()

class addVehicleIntersection(QMainWindow, Ui_AddVehicleSettings):
     def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.show()

class trafficLightSettingPopUp(QMainWindow, Ui_TrafficLightSettingPopUp):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.show()

class addVehiclePopUp(QMainWindow, Ui_addVehiclePopUp):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.show()

class editSingleVehicleIntsctn(QMainWindow, Ui_EditSingleVehicleInsctn):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.show()
        
class MainApp(QWidget):
    def changeFreewayLanes(self, laneNum):
        self.editFreeway.get(self.editFreeway.curLane)
        self.editFreeway.curLane = laneNum
        self.editFreeway.set(laneNum)
        self.stack.setCurrentWidget(self.editFreeway)
        return
    
    def editFreewayLaneVehicle(self, laneNum):
        self.stack.setCurrentWidget(self.addVehicleFreeway)

        #Add input to config file
        return

    def changeIntersections(self, intersectionNum):
        self.stack.setCurrentWidget(self.editIntersection)
        self.editIntersection.set(intersectionNum)

    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Init Screens
        self.mainScreen = mainScreen()
        self.mainIntersection = mainIntersection()
        self.fmain = fmain()

        self.editFreeway = editFreeway()
        self.editIntersection = editIntersection()
        
        self.addVehicleFreeway = addVehicleFreeway()
        self.addVehicleIntersection = addVehicleIntersection()  

        self.Traffic1 = Traffic()
        self.Traffic2 = Traffic()
        self.Traffic3 = Traffic()
        self.Traffic4 = Traffic()

        self.trafficLightSettingPopUp = trafficLightSettingPopUp()
        self.addVehiclePopUpTraffic = addVehiclePopUp()
        self.addVehiclePopUpFreeway = addVehiclePopUp()
        self.editSingleVehicleIntsctn = editSingleVehicleIntsctn()
        

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

        #Edit Freeway Section
        self.editFreeway.add_vehicles_btn.clicked.connect(lambda: self.editFreewayLaneVehicle(1))
        self.addVehicleFreeway.back_bttn.clicked.connect(lambda: self.changeFreewayLanes(1))


        #Add Freeway Vehicle
        self.addVehicleFreeway.addSubjectVehicle_bttn.clicked.connect(lambda:self.stack.setCurrentWidget(self.addVehiclePopUpFreeway))
        self.addVehiclePopUpFreeway.buttonBox.clicked.connect(lambda: self.stack.setCurrentWidget(self.addVehicleFreeway))
        self.addVehicleFreeway.addLeftLaneVehicle_bttn.clicked.connect(lambda:self.stack.setCurrentWidget(self.addVehiclePopUpFreeway))
        self.addVehiclePopUpFreeway.buttonBox.clicked.connect(lambda: self.stack.setCurrentWidget(self.addVehicleFreeway))

        
        #Intersection
        self.mainScreen.Instcn_bttn.clicked.connect(lambda: self.stack.setCurrentWidget(self.mainIntersection))
        self.mainIntersection.back_bttn.clicked.connect(lambda: self.stack.setCurrentWidget(self.mainScreen))

        #Edit Intersection
        self.mainIntersection.intersectionLane_1_bttn.clicked.connect(lambda: self.changeIntersections(1))
        self.editIntersection.back_bttn.clicked.connect(lambda: self.stack.setCurrentWidget(self.mainIntersection))
        self.mainIntersection.intersectionLane_2_bttn.clicked.connect(lambda: self.changeIntersections(2))
        self.editIntersection.back_bttn.clicked.connect(lambda: self.stack.setCurrentWidget(self.mainIntersection))
        self.mainIntersection.intersectionLane_3_bttn.clicked.connect(lambda: self.changeIntersections(3))
        self.editIntersection.back_bttn.clicked.connect(lambda: self.stack.setCurrentWidget(self.mainIntersection))
        self.mainIntersection.intersectionLane_4_bttn.clicked.connect(lambda: self.changeIntersections(4))
        self.editIntersection.back_bttn.clicked.connect(lambda: self.stack.setCurrentWidget(self.mainIntersection))
        
        #Add Vehicle Intersection
        self.editIntersection.vehicles_bttn.clicked.connect(lambda:self.stack.setCurrentWidget(self.addVehicleIntersection))
        self.addVehicleIntersection.back_bttn.clicked.connect(lambda: self.stack.setCurrentWidget(self.changeIntersections(1)))

        #Add Vehicle Inersection
        self.addVehicleIntersection.addSubject_bttn.clicked.connect(lambda:self.stack.setCurrentWidget(self.addVehiclePopUpTraffic))
        self.addVehiclePopUpTraffic.buttonBox.clicked.connect(lambda:self.stack.setCurrentWidget(self.addVehicleIntersection))
        self.addVehicleIntersection.addAhead_bttn.clicked.connect(lambda:self.stack.setCurrentWidget(self.addVehiclePopUpTraffic))
        self.addVehiclePopUpTraffic.buttonBox.clicked.connect(lambda:self.stack.setCurrentWidget(self.addVehicleIntersection))
        self.addVehicleIntersection.addLeft_bttn.clicked.connect(lambda:self.stack.setCurrentWidget(self.addVehiclePopUpTraffic))
        self.addVehiclePopUpTraffic.buttonBox.clicked.connect(lambda:self.stack.setCurrentWidget(self.addVehicleIntersection))
        self.addVehicleIntersection.addRight_bttn.clicked.connect(lambda:self.stack.setCurrentWidget(self.addVehiclePopUpTraffic))
        self.addVehiclePopUpTraffic.buttonBox.clicked.connect(lambda:self.stack.setCurrentWidget(self.addVehicleIntersection))


        #Edit Single Vehicle Intersection
        self.editIntersection.lane_1_bttn.clicked.connect(lambda:self.stack.setCurrentWidget(self.editSingleVehicleIntsctn))
        self.editSingleVehicleIntsctn.Back_bttn.clicked.connect(lambda: self.stack.setCurrentWidget(self.changeIntersections(1)))
        self.editIntersection.lane_2_bttn.clicked.connect(lambda:self.stack.setCurrentWidget(self.editSingleVehicleIntsctn))
        self.editSingleVehicleIntsctn.Back_bttn.clicked.connect(lambda: self.stack.setCurrentWidget(self.changeIntersections(2)))
        self.editIntersection.lane_3_bttn.clicked.connect(lambda:self.stack.setCurrentWidget(self.editSingleVehicleIntsctn))
        self.editSingleVehicleIntsctn.Back_bttn.clicked.connect(lambda: self.stack.setCurrentWidget(self.changeIntersections(3)))
        self.editIntersection.lane_4_bttn.clicked.connect(lambda:self.stack.setCurrentWidget(self.editSingleVehicleIntsctn))
        self.editSingleVehicleIntsctn.Back_bttn.clicked.connect(lambda: self.stack.setCurrentWidget(self.changeIntersections(4)))

        
        #Traffic
        self.editIntersection.trafficLight_bttn.clicked.connect(lambda:self.stack.setCurrentWidget(self.Traffic1))
        self.Traffic1.Back_bttn.clicked.connect(lambda: self.stack.setCurrentWidget(self.changeIntersections(1)))
        self.editIntersection.trafficLight_bttn.clicked.connect(lambda:self.stack.setCurrentWidget(self.Traffic2))
        self.Traffic2.Back_bttn.clicked.connect(lambda: self.stack.setCurrentWidget(self.changeIntersections(1)))
        self.editIntersection.trafficLight_bttn.clicked.connect(lambda:self.stack.setCurrentWidget(self.Traffic3))
        self.Traffic3.Back_bttn.clicked.connect(lambda: self.stack.setCurrentWidget(self.changeIntersections(1)))
        self.editIntersection.trafficLight_bttn.clicked.connect(lambda:self.stack.setCurrentWidget(self.Traffic4))
        self.Traffic4.Back_bttn.clicked.connect(lambda: self.stack.setCurrentWidget(self.changeIntersections(1)))

        #Traffic Light Pop Up
        self.editIntersection.trafficLight_bttn.clicked.connect(lambda:self.stack.setCurrentWidget(self.trafficLightSettingPopUp))
        self.trafficLightSettingPopUp.buttonBox.clicked.connect(lambda: self.stack.setCurrentWidget(self.changeIntersections(1)))


        # Add All Screens to Stack
        self.stack.addWidget(self.mainScreen)
        self.stack.addWidget(self.mainIntersection)
        self.stack.addWidget(self.fmain)
        self.stack.addWidget(self.editFreeway)
        self.stack.addWidget(self.addVehicleFreeway)
        self.stack.addWidget(self.editIntersection)
        self.stack.addWidget(self.Traffic1)
        self.stack.addWidget(self.Traffic2)
        self.stack.addWidget(self.Traffic3)
        self.stack.addWidget(self.Traffic4)
        self.stack.addWidget(self.addVehicleIntersection)
        self.stack.addWidget(self.trafficLightSettingPopUp)
        self.stack.addWidget(self.addVehiclePopUpTraffic)
        self.stack.addWidget(self.addVehiclePopUpFreeway)
        self.stack.addWidget(self.editSingleVehicleIntsctn)

        # Set Initial Settings
        self.stack.resize(800,800)
        self.stack.setCurrentIndex(0) # Default first screen
        self.stack.show()

if __name__ == "__main__":
    print('Start')
    app = QApplication(sys.argv)
    x = MainApp()
    sys.exit(app.exec())

