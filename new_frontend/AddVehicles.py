# Form implementation generated from reading ui file 'addVehicles.ui'
#
# Created by: PyQt6 UI code generator 6.4.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Widget(object):
    def setupUi(self, Widget):
        Widget.setObjectName("Widget")
        Widget.resize(1400, 800)
        Widget.setMinimumSize(QtCore.QSize(1400, 800))
        Widget.setMaximumSize(QtCore.QSize(1400, 800))
        self.freeway_img = QtWidgets.QLabel(Widget)
        self.freeway_img.setGeometry(QtCore.QRect(1040, 110, 181, 571))
        self.freeway_img.setText("")
        self.freeway_img.setPixmap(QtGui.QPixmap("../../mdp/mockupUI/road.gif"))
        self.freeway_img.setObjectName("freeway_img")
        self.horizontalLayoutWidget = QtWidgets.QWidget(Widget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(70, 170, 411, 86))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.subjectLane = QtWidgets.QLabel(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.subjectLane.setFont(font)
        self.subjectLane.setObjectName("subjectLane")
        self.horizontalLayout.addWidget(self.subjectLane)
        spacerItem = QtWidgets.QSpacerItem(310, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.addVehicle_2 = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.addVehicle_2.setObjectName("addVehicle_2")
        self.horizontalLayout.addWidget(self.addVehicle_2)
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(Widget)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(70, 250, 411, 86))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.leftLane = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.leftLane.setFont(font)
        self.leftLane.setObjectName("leftLane")
        self.horizontalLayout_2.addWidget(self.leftLane)
        spacerItem1 = QtWidgets.QSpacerItem(310, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.addVehicle = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.addVehicle.setObjectName("addVehicle")
        self.horizontalLayout_2.addWidget(self.addVehicle)
        self.backBtn = QtWidgets.QPushButton(Widget)
        self.backBtn.setGeometry(QtCore.QRect(0, 0, 101, 32))
        self.backBtn.setObjectName("backBtn")
        self.title = QtWidgets.QLabel(Widget)
        self.title.setGeometry(QtCore.QRect(70, 110, 151, 41))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.title.setFont(font)
        self.title.setObjectName("title")
        self.label_4 = QtWidgets.QLabel(Widget)
        self.label_4.setGeometry(QtCore.QRect(1170, 430, 21, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_4.setFont(font)
        self.label_4.setAutoFillBackground(True)
        self.label_4.setObjectName("label_4")

        self.retranslateUi(Widget)
        QtCore.QMetaObject.connectSlotsByName(Widget)

    def retranslateUi(self, Widget):
        _translate = QtCore.QCoreApplication.translate
        Widget.setWindowTitle(_translate("Widget", "Widget"))
        self.subjectLane.setText(_translate("Widget", "Subject Lane"))
        self.addVehicle_2.setText(_translate("Widget", "Add Vehicle"))
        self.leftLane.setText(_translate("Widget", "Left Lane     "))
        self.addVehicle.setText(_translate("Widget", "Add Vehicle"))
        self.backBtn.setText(_translate("Widget", "Back"))
        self.title.setText(_translate("Widget", "Add Vehicles"))
        self.label_4.setText(_translate("Widget", "Ego"))
