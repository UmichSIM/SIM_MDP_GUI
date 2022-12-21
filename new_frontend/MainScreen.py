# Form implementation generated from reading ui file 'mainScreen.ui'
#
# Created by: PyQt6 UI code generator 6.4.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainScreen(object):
    def setupUi(self, MainScreen):
        MainScreen.setObjectName("MainScreen")
        MainScreen.resize(1400, 800)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainScreen.sizePolicy().hasHeightForWidth())
        MainScreen.setSizePolicy(sizePolicy)
        MainScreen.setMinimumSize(QtCore.QSize(0, 0))
        MainScreen.setMaximumSize(QtCore.QSize(5000, 5000))
        self.horizontalLayoutWidget = QtWidgets.QWidget(MainScreen)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 1401, 801))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.Overall_layout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.Overall_layout.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetDefaultConstraint)
        self.Overall_layout.setContentsMargins(150, 80, 150, 100)
        self.Overall_layout.setSpacing(6)
        self.Overall_layout.setObjectName("Overall_layout")
        self.InnerOverall_layout = QtWidgets.QVBoxLayout()
        self.InnerOverall_layout.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetDefaultConstraint)
        self.InnerOverall_layout.setSpacing(6)
        self.InnerOverall_layout.setObjectName("InnerOverall_layout")
        self.CarlaSimTitle_txt = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.CarlaSimTitle_txt.setMaximumSize(QtCore.QSize(16777215, 50))
        font = QtGui.QFont()
        font.setPointSize(35)
        self.CarlaSimTitle_txt.setFont(font)
        self.CarlaSimTitle_txt.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.CarlaSimTitle_txt.setObjectName("CarlaSimTitle_txt")
        self.InnerOverall_layout.addWidget(self.CarlaSimTitle_txt)
        self.UmichSubTitle_txt = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.UmichSubTitle_txt.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.UmichSubTitle_txt.setFont(font)
        self.UmichSubTitle_txt.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.UmichSubTitle_txt.setObjectName("UmichSubTitle_txt")
        self.InnerOverall_layout.addWidget(self.UmichSubTitle_txt)
        spacerItem = QtWidgets.QSpacerItem(20, 320, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.InnerOverall_layout.addItem(spacerItem)
        self.Buttons_layout = QtWidgets.QHBoxLayout()
        self.Buttons_layout.setSpacing(6)
        self.Buttons_layout.setObjectName("Buttons_layout")
        self.Fway_bttn = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Fway_bttn.sizePolicy().hasHeightForWidth())
        self.Fway_bttn.setSizePolicy(sizePolicy)
        self.Fway_bttn.setMinimumSize(QtCore.QSize(210, 60))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.Fway_bttn.setFont(font)
        self.Fway_bttn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.Fway_bttn.setObjectName("Fway_bttn")
        self.Buttons_layout.addWidget(self.Fway_bttn)
        spacerItem1 = QtWidgets.QSpacerItem(40, 40, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.Buttons_layout.addItem(spacerItem1)
        self.Instcn_bttn = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Instcn_bttn.sizePolicy().hasHeightForWidth())
        self.Instcn_bttn.setSizePolicy(sizePolicy)
        self.Instcn_bttn.setMinimumSize(QtCore.QSize(180, 60))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.Instcn_bttn.setFont(font)
        self.Instcn_bttn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.Instcn_bttn.setObjectName("Instcn_bttn")
        self.Buttons_layout.addWidget(self.Instcn_bttn)
        self.InnerOverall_layout.addLayout(self.Buttons_layout)
        self.Overall_layout.addLayout(self.InnerOverall_layout)

        self.retranslateUi(MainScreen)
        QtCore.QMetaObject.connectSlotsByName(MainScreen)

    def retranslateUi(self, MainScreen):
        _translate = QtCore.QCoreApplication.translate
        MainScreen.setWindowTitle(_translate("MainScreen", "Widget"))
        self.CarlaSimTitle_txt.setText(_translate("MainScreen", "Carla Simulator: User Interface"))
        self.UmichSubTitle_txt.setText(_translate("MainScreen", "University of Michigan - UMTRI - Version 1.0"))
        self.Fway_bttn.setText(_translate("MainScreen", "Freeway Experiment"))
        self.Instcn_bttn.setText(_translate("MainScreen", "Intersection Experiment"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_MainScreen()
    ui.setupUi(Form)
    Form.show()

    sys.exit(app.exec())
