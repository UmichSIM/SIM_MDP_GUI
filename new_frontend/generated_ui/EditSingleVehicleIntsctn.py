# Form implementation generated from reading ui file 'new_frontend/pyqt_ui/editSingleVehicleIntsctn.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_EditSingleVehicleInsctn(object):
    def setupUi(self, EditSingleVehicleInsctn):
        EditSingleVehicleInsctn.setObjectName("EditSingleVehicleInsctn")
        EditSingleVehicleInsctn.resize(1400, 800)
        EditSingleVehicleInsctn.setMinimumSize(QtCore.QSize(1400, 800))
        EditSingleVehicleInsctn.setMaximumSize(QtCore.QSize(1400, 800))
        self.EditSingularVehicleTitle_txt = QtWidgets.QLabel(parent=EditSingleVehicleInsctn)
        self.EditSingularVehicleTitle_txt.setGeometry(QtCore.QRect(440, 30, 561, 41))
        font = QtGui.QFont()
        font.setPointSize(35)
        self.EditSingularVehicleTitle_txt.setFont(font)
        self.EditSingularVehicleTitle_txt.setObjectName("EditSingularVehicleTitle_txt")
        self.Back_bttn = QtWidgets.QPushButton(parent=EditSingleVehicleInsctn)
        self.Back_bttn.setGeometry(QtCore.QRect(50, 50, 100, 50))
        self.Back_bttn.setMinimumSize(QtCore.QSize(100, 50))
        self.Back_bttn.setMaximumSize(QtCore.QSize(100, 50))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.Back_bttn.setFont(font)
        self.Back_bttn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.Back_bttn.setObjectName("Back_bttn")
        self.CarTitle_txt = QtWidgets.QLabel(parent=EditSingleVehicleInsctn)
        self.CarTitle_txt.setGeometry(QtCore.QRect(210, 130, 351, 21))
        font = QtGui.QFont()
        font.setPointSize(25)
        self.CarTitle_txt.setFont(font)
        self.CarTitle_txt.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.CarTitle_txt.setObjectName("CarTitle_txt")
        self.verticalLayoutWidget = QtWidgets.QWidget(parent=EditSingleVehicleInsctn)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(170, 160, 431, 481))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.Options_layout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.Options_layout.setContentsMargins(0, 0, 0, 0)
        self.Options_layout.setObjectName("Options_layout")
        self.Turn_layout = QtWidgets.QHBoxLayout()
        self.Turn_layout.setObjectName("Turn_layout")
        self.Turn_txt = QtWidgets.QLabel(parent=self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.Turn_txt.setFont(font)
        self.Turn_txt.setObjectName("Turn_txt")
        self.Turn_layout.addWidget(self.Turn_txt)
        self.Turn_dropbx = QtWidgets.QComboBox(parent=self.verticalLayoutWidget)
        self.Turn_dropbx.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.Turn_dropbx.setObjectName("Turn_dropbx")
        self.Turn_dropbx.addItem("")
        self.Turn_dropbx.addItem("")
        self.Turn_dropbx.addItem("")
        self.Turn_layout.addWidget(self.Turn_dropbx)
        self.Options_layout.addLayout(self.Turn_layout)
        self.Stop_layout = QtWidgets.QHBoxLayout()
        self.Stop_layout.setObjectName("Stop_layout")
        self.Stop_txt = QtWidgets.QLabel(parent=self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.Stop_txt.setFont(font)
        self.Stop_txt.setObjectName("Stop_txt")
        self.Stop_layout.addWidget(self.Stop_txt)
        self.Stop_dropbox = QtWidgets.QComboBox(parent=self.verticalLayoutWidget)
        self.Stop_dropbox.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.Stop_dropbox.setObjectName("Stop_dropbox")
        self.Stop_dropbox.addItem("")
        self.Stop_dropbox.addItem("")
        self.Stop_layout.addWidget(self.Stop_dropbox)
        self.Options_layout.addLayout(self.Stop_layout)
        self.VehicleModel_layout = QtWidgets.QHBoxLayout()
        self.VehicleModel_layout.setObjectName("VehicleModel_layout")
        self.VehicleModel_txt = QtWidgets.QLabel(parent=self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.VehicleModel_txt.setFont(font)
        self.VehicleModel_txt.setObjectName("VehicleModel_txt")
        self.VehicleModel_layout.addWidget(self.VehicleModel_txt)
        self.VehicleModel_dropbx = QtWidgets.QComboBox(parent=self.verticalLayoutWidget)
        self.VehicleModel_dropbx.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.VehicleModel_dropbx.setObjectName("VehicleModel_dropbx")
        self.VehicleModel_dropbx.addItem("")
        self.VehicleModel_dropbx.addItem("")
        self.VehicleModel_layout.addWidget(self.VehicleModel_dropbx)
        self.Options_layout.addLayout(self.VehicleModel_layout)
        self.Color_layout = QtWidgets.QHBoxLayout()
        self.Color_layout.setObjectName("Color_layout")
        self.Color_txt = QtWidgets.QLabel(parent=self.verticalLayoutWidget)
        self.Color_txt.setMinimumSize(QtCore.QSize(0, 21))
        self.Color_txt.setMaximumSize(QtCore.QSize(16777215, 21))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.Color_txt.setFont(font)
        self.Color_txt.setObjectName("Color_txt")
        self.Color_layout.addWidget(self.Color_txt)
        spacerItem = QtWidgets.QSpacerItem(175, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.Color_layout.addItem(spacerItem)
        self.RValue_txt = QtWidgets.QLabel(parent=self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.RValue_txt.setFont(font)
        self.RValue_txt.setObjectName("RValue_txt")
        self.Color_layout.addWidget(self.RValue_txt)
        self.RValue_inptbx = QtWidgets.QLineEdit(parent=self.verticalLayoutWidget)
        self.RValue_inptbx.setMinimumSize(QtCore.QSize(0, 0))
        self.RValue_inptbx.setMaximumSize(QtCore.QSize(100, 16777215))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.RValue_inptbx.setFont(font)
        self.RValue_inptbx.setPlaceholderText("")
        self.RValue_inptbx.setObjectName("RValue_inptbx")
        self.Color_layout.addWidget(self.RValue_inptbx)
        spacerItem1 = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Minimum)
        self.Color_layout.addItem(spacerItem1)
        self.GValue_txt = QtWidgets.QLabel(parent=self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.GValue_txt.setFont(font)
        self.GValue_txt.setObjectName("GValue_txt")
        self.Color_layout.addWidget(self.GValue_txt)
        self.GValue_inptbx = QtWidgets.QLineEdit(parent=self.verticalLayoutWidget)
        self.GValue_inptbx.setMaximumSize(QtCore.QSize(100, 16777215))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.GValue_inptbx.setFont(font)
        self.GValue_inptbx.setPlaceholderText("")
        self.GValue_inptbx.setObjectName("GValue_inptbx")
        self.Color_layout.addWidget(self.GValue_inptbx)
        spacerItem2 = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Minimum)
        self.Color_layout.addItem(spacerItem2)
        self.BValue_txt = QtWidgets.QLabel(parent=self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.BValue_txt.setFont(font)
        self.BValue_txt.setObjectName("BValue_txt")
        self.Color_layout.addWidget(self.BValue_txt)
        self.BValue_inptbx = QtWidgets.QLineEdit(parent=self.verticalLayoutWidget)
        self.BValue_inptbx.setMaximumSize(QtCore.QSize(100, 16777215))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.BValue_inptbx.setFont(font)
        self.BValue_inptbx.setPlaceholderText("")
        self.BValue_inptbx.setObjectName("BValue_inptbx")
        self.Color_layout.addWidget(self.BValue_inptbx)
        self.Options_layout.addLayout(self.Color_layout)
        self.Gap_layout = QtWidgets.QHBoxLayout()
        self.Gap_layout.setObjectName("Gap_layout")
        self.Gap_txt = QtWidgets.QLabel(parent=self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.Gap_txt.setFont(font)
        self.Gap_txt.setObjectName("Gap_txt")
        self.Gap_layout.addWidget(self.Gap_txt)
        self.Gap_spinbx = QtWidgets.QSpinBox(parent=self.verticalLayoutWidget)
        self.Gap_spinbx.setMinimumSize(QtCore.QSize(50, 35))
        self.Gap_spinbx.setMaximumSize(QtCore.QSize(50, 35))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.Gap_spinbx.setFont(font)
        self.Gap_spinbx.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.Gap_spinbx.setAccelerated(True)
        self.Gap_spinbx.setMinimum(10)
        self.Gap_spinbx.setObjectName("Gap_spinbx")
        self.Gap_layout.addWidget(self.Gap_spinbx)
        self.Options_layout.addLayout(self.Gap_layout)
        self.SafetyDist_layout = QtWidgets.QHBoxLayout()
        self.SafetyDist_layout.setObjectName("SafetyDist_layout")
        self.SafetyDist_txt = QtWidgets.QLabel(parent=self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.SafetyDist_txt.setFont(font)
        self.SafetyDist_txt.setObjectName("SafetyDist_txt")
        self.SafetyDist_layout.addWidget(self.SafetyDist_txt)
        self.SafetyDist_spinbx = QtWidgets.QSpinBox(parent=self.verticalLayoutWidget)
        self.SafetyDist_spinbx.setMinimumSize(QtCore.QSize(50, 35))
        self.SafetyDist_spinbx.setMaximumSize(QtCore.QSize(50, 35))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.SafetyDist_spinbx.setFont(font)
        self.SafetyDist_spinbx.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.SafetyDist_spinbx.setWrapping(False)
        self.SafetyDist_spinbx.setFrame(True)
        self.SafetyDist_spinbx.setAccelerated(True)
        self.SafetyDist_spinbx.setMinimum(15)
        self.SafetyDist_spinbx.setObjectName("SafetyDist_spinbx")
        self.SafetyDist_layout.addWidget(self.SafetyDist_spinbx)
        self.Options_layout.addLayout(self.SafetyDist_layout)
        self.YTrafficLight_layout = QtWidgets.QHBoxLayout()
        self.YTrafficLight_layout.setObjectName("YTrafficLight_layout")
        self.YTrafficLight_txt = QtWidgets.QLabel(parent=self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.YTrafficLight_txt.setFont(font)
        self.YTrafficLight_txt.setObjectName("YTrafficLight_txt")
        self.YTrafficLight_layout.addWidget(self.YTrafficLight_txt)
        self.YTrafficLight_chkbx = QtWidgets.QCheckBox(parent=self.verticalLayoutWidget)
        self.YTrafficLight_chkbx.setMinimumSize(QtCore.QSize(20, 20))
        self.YTrafficLight_chkbx.setMaximumSize(QtCore.QSize(20, 20))
        self.YTrafficLight_chkbx.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.YTrafficLight_chkbx.setText("")
        self.YTrafficLight_chkbx.setIconSize(QtCore.QSize(20, 20))
        self.YTrafficLight_chkbx.setChecked(True)
        self.YTrafficLight_chkbx.setObjectName("YTrafficLight_chkbx")
        self.YTrafficLight_layout.addWidget(self.YTrafficLight_chkbx)
        self.Options_layout.addLayout(self.YTrafficLight_layout)
        self.Intersection_img = QtWidgets.QLabel(parent=EditSingleVehicleInsctn)
        self.Intersection_img.setGeometry(QtCore.QRect(750, 130, 501, 611))
        self.Intersection_img.setText("")
        self.Intersection_img.setPixmap(QtGui.QPixmap("new_frontend/pyqt_ui/images/intersection.jpg"))
        self.Intersection_img.setScaledContents(True)
        self.Intersection_img.setObjectName("Intersection_img")
        self.horizontalLayoutWidget_8 = QtWidgets.QWidget(parent=EditSingleVehicleInsctn)
        self.horizontalLayoutWidget_8.setGeometry(QtCore.QRect(120, 670, 531, 61))
        self.horizontalLayoutWidget_8.setObjectName("horizontalLayoutWidget_8")
        self.Buttons_layout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_8)
        self.Buttons_layout.setContentsMargins(0, 0, 0, 0)
        self.Buttons_layout.setObjectName("Buttons_layout")
        self.DeleteVehicle_bttn = QtWidgets.QPushButton(parent=self.horizontalLayoutWidget_8)
        self.DeleteVehicle_bttn.setMinimumSize(QtCore.QSize(150, 50))
        self.DeleteVehicle_bttn.setMaximumSize(QtCore.QSize(150, 50))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.DeleteVehicle_bttn.setFont(font)
        self.DeleteVehicle_bttn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.DeleteVehicle_bttn.setObjectName("DeleteVehicle_bttn")
        self.Buttons_layout.addWidget(self.DeleteVehicle_bttn)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.Buttons_layout.addItem(spacerItem3)
        self.CancelEdit_bttn = QtWidgets.QPushButton(parent=self.horizontalLayoutWidget_8)
        self.CancelEdit_bttn.setMinimumSize(QtCore.QSize(125, 50))
        self.CancelEdit_bttn.setMaximumSize(QtCore.QSize(125, 50))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.CancelEdit_bttn.setFont(font)
        self.CancelEdit_bttn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.CancelEdit_bttn.setObjectName("CancelEdit_bttn")
        self.Buttons_layout.addWidget(self.CancelEdit_bttn)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.Buttons_layout.addItem(spacerItem4)
        self.ConfirmChange_bttn = QtWidgets.QPushButton(parent=self.horizontalLayoutWidget_8)
        self.ConfirmChange_bttn.setMinimumSize(QtCore.QSize(170, 50))
        self.ConfirmChange_bttn.setMaximumSize(QtCore.QSize(170, 50))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.ConfirmChange_bttn.setFont(font)
        self.ConfirmChange_bttn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.ConfirmChange_bttn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.ConfirmChange_bttn.setObjectName("ConfirmChange_bttn")
        self.Buttons_layout.addWidget(self.ConfirmChange_bttn)

        self.retranslateUi(EditSingleVehicleInsctn)
        QtCore.QMetaObject.connectSlotsByName(EditSingleVehicleInsctn)

    def retranslateUi(self, EditSingleVehicleInsctn):
        _translate = QtCore.QCoreApplication.translate
        EditSingleVehicleInsctn.setWindowTitle(_translate("EditSingleVehicleInsctn", "Form"))
        self.EditSingularVehicleTitle_txt.setText(_translate("EditSingleVehicleInsctn", "Edit Singular Vehicle (Intersection 1)"))
        self.Back_bttn.setText(_translate("EditSingleVehicleInsctn", "Back"))
        self.CarTitle_txt.setText(_translate("EditSingleVehicleInsctn", "Car 1 on the Left "))
        self.Turn_txt.setText(_translate("EditSingleVehicleInsctn", "Turn"))
        self.Turn_dropbx.setItemText(0, _translate("EditSingleVehicleInsctn", "Straight"))
        self.Turn_dropbx.setItemText(1, _translate("EditSingleVehicleInsctn", "Left"))
        self.Turn_dropbx.setItemText(2, _translate("EditSingleVehicleInsctn", "Right"))
        self.Stop_txt.setText(_translate("EditSingleVehicleInsctn", "Stop"))
        self.Stop_dropbox.setItemText(0, _translate("EditSingleVehicleInsctn", "Normal Stop"))
        self.Stop_dropbox.setItemText(1, _translate("EditSingleVehicleInsctn", "Gradual Stop"))
        self.VehicleModel_txt.setText(_translate("EditSingleVehicleInsctn", "Vehicle Model"))
        self.VehicleModel_dropbx.setItemText(0, _translate("EditSingleVehicleInsctn", "Audi a2"))
        self.VehicleModel_dropbx.setItemText(1, _translate("EditSingleVehicleInsctn", "Firetruck"))
        self.Color_txt.setText(_translate("EditSingleVehicleInsctn", "Color"))
        self.RValue_txt.setText(_translate("EditSingleVehicleInsctn", "R:"))
        self.RValue_inptbx.setText(_translate("EditSingleVehicleInsctn", "0"))
        self.GValue_txt.setText(_translate("EditSingleVehicleInsctn", "G:"))
        self.GValue_inptbx.setText(_translate("EditSingleVehicleInsctn", "0"))
        self.BValue_txt.setText(_translate("EditSingleVehicleInsctn", "B:"))
        self.BValue_inptbx.setText(_translate("EditSingleVehicleInsctn", "0"))
        self.Gap_txt.setText(_translate("EditSingleVehicleInsctn", "Gap"))
        self.SafetyDist_txt.setText(_translate("EditSingleVehicleInsctn", "Safety Distance (m)"))
        self.YTrafficLight_txt.setText(_translate("EditSingleVehicleInsctn", "Y Traffic Light"))
        self.DeleteVehicle_bttn.setText(_translate("EditSingleVehicleInsctn", "Delete Vehicle"))
        self.CancelEdit_bttn.setText(_translate("EditSingleVehicleInsctn", "Cancel Edit"))
        self.ConfirmChange_bttn.setText(_translate("EditSingleVehicleInsctn", "Confirm Change"))
