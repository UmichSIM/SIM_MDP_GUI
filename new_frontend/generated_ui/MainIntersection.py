# Form implementation generated from reading ui file 'mainIntersection.ui'
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
        self.back_bttn = QtWidgets.QPushButton(Widget)
        self.back_bttn.setGeometry(QtCore.QRect(40, 100, 100, 50))
        self.back_bttn.setMinimumSize(QtCore.QSize(100, 50))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.back_bttn.setFont(font)
        self.back_bttn.setObjectName("back_bttn")
        self.verticalLayoutWidget = QtWidgets.QWidget(Widget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(40, 220, 371, 341))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.allow_collisions_label = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.allow_collisions_label.setFont(font)
        self.allow_collisions_label.setObjectName("allow_collisions_label")
        self.horizontalLayout_4.addWidget(self.allow_collisions_label)
        self.allow_collisions_chkbx = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.allow_collisions_chkbx.setMinimumSize(QtCore.QSize(200, 0))
        self.allow_collisions_chkbx.setText("")
        self.allow_collisions_chkbx.setChecked(True)
        self.allow_collisions_chkbx.setObjectName("allow_collisions_chkbx")
        self.horizontalLayout_4.addWidget(self.allow_collisions_chkbx)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.speed_label = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.speed_label.setFont(font)
        self.speed_label.setObjectName("speed_label")
        self.horizontalLayout_5.addWidget(self.speed_label)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem)
        self.speed_spnbx = QtWidgets.QSpinBox(self.verticalLayoutWidget)
        self.speed_spnbx.setMinimumSize(QtCore.QSize(50, 0))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.speed_spnbx.setFont(font)
        self.speed_spnbx.setObjectName("speed_spnbx")
        self.horizontalLayout_5.addWidget(self.speed_spnbx)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.num_intersection_label = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.num_intersection_label.setFont(font)
        self.num_intersection_label.setObjectName("num_intersection_label")
        self.horizontalLayout_6.addWidget(self.num_intersection_label)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem1)
        self.num_intersection_spnbx = QtWidgets.QSpinBox(self.verticalLayoutWidget)
        self.num_intersection_spnbx.setMinimumSize(QtCore.QSize(50, 0))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.num_intersection_spnbx.setFont(font)
        self.num_intersection_spnbx.setObjectName("num_intersection_spnbx")
        self.horizontalLayout_6.addWidget(self.num_intersection_spnbx)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.safety_dist_label = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.safety_dist_label.setFont(font)
        self.safety_dist_label.setObjectName("safety_dist_label")
        self.horizontalLayout_7.addWidget(self.safety_dist_label)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem2)
        self.safety_dist_spnbx = QtWidgets.QSpinBox(self.verticalLayoutWidget)
        self.safety_dist_spnbx.setMinimumSize(QtCore.QSize(50, 0))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.safety_dist_spnbx.setFont(font)
        self.safety_dist_spnbx.setObjectName("safety_dist_spnbx")
        self.horizontalLayout_7.addWidget(self.safety_dist_spnbx)
        self.verticalLayout.addLayout(self.horizontalLayout_7)
        self.start_simulation = QtWidgets.QPushButton(Widget)
        self.start_simulation.setGeometry(QtCore.QRect(40, 700, 171, 50))
        self.start_simulation.setMinimumSize(QtCore.QSize(0, 50))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.start_simulation.setFont(font)
        self.start_simulation.setObjectName("start_simulation")
        self.intersectionLane_1_bttn = QtWidgets.QPushButton(Widget)
        self.intersectionLane_1_bttn.setGeometry(QtCore.QRect(560, 420, 50, 50))
        self.intersectionLane_1_bttn.setMinimumSize(QtCore.QSize(50, 50))
        self.intersectionLane_1_bttn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.intersectionLane_1_bttn.setFont(font)
        self.intersectionLane_1_bttn.setAutoFillBackground(True)
        self.intersectionLane_1_bttn.setObjectName("intersectionLane_1_bttn")
        self.intersectionLane_2_bttn = QtWidgets.QPushButton(Widget)
        self.intersectionLane_2_bttn.setGeometry(QtCore.QRect(700, 420, 50, 50))
        self.intersectionLane_2_bttn.setMinimumSize(QtCore.QSize(50, 50))
        self.intersectionLane_2_bttn.setMaximumSize(QtCore.QSize(50, 50))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.intersectionLane_2_bttn.setFont(font)
        self.intersectionLane_2_bttn.setAutoFillBackground(True)
        self.intersectionLane_2_bttn.setObjectName("intersectionLane_2_bttn")
        self.intersectionLane_3_bttn = QtWidgets.QPushButton(Widget)
        self.intersectionLane_3_bttn.setGeometry(QtCore.QRect(840, 420, 50, 50))
        self.intersectionLane_3_bttn.setMinimumSize(QtCore.QSize(50, 50))
        self.intersectionLane_3_bttn.setMaximumSize(QtCore.QSize(30, 30))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.intersectionLane_3_bttn.setFont(font)
        self.intersectionLane_3_bttn.setAutoFillBackground(True)
        self.intersectionLane_3_bttn.setObjectName("intersectionLane_3_bttn")
        self.intersectionLane_4_bttn = QtWidgets.QPushButton(Widget)
        self.intersectionLane_4_bttn.setGeometry(QtCore.QRect(980, 420, 50, 50))
        self.intersectionLane_4_bttn.setMinimumSize(QtCore.QSize(50, 50))
        self.intersectionLane_4_bttn.setMaximumSize(QtCore.QSize(30, 30))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.intersectionLane_4_bttn.setFont(font)
        self.intersectionLane_4_bttn.setAutoFillBackground(True)
        self.intersectionLane_4_bttn.setObjectName("intersectionLane_4_bttn")
        self.intersectionLane_5_bttn = QtWidgets.QPushButton(Widget)
        self.intersectionLane_5_bttn.setGeometry(QtCore.QRect(1120, 420, 50, 50))
        self.intersectionLane_5_bttn.setMinimumSize(QtCore.QSize(50, 50))
        self.intersectionLane_5_bttn.setMaximumSize(QtCore.QSize(30, 30))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.intersectionLane_5_bttn.setFont(font)
        self.intersectionLane_5_bttn.setAutoFillBackground(True)
        self.intersectionLane_5_bttn.setObjectName("intersectionLane_5_bttn")
        self.intersectionLane_6_bttn = QtWidgets.QPushButton(Widget)
        self.intersectionLane_6_bttn.setGeometry(QtCore.QRect(1260, 420, 50, 50))
        self.intersectionLane_6_bttn.setMinimumSize(QtCore.QSize(50, 50))
        self.intersectionLane_6_bttn.setMaximumSize(QtCore.QSize(30, 30))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.intersectionLane_6_bttn.setFont(font)
        self.intersectionLane_6_bttn.setAutoFillBackground(True)
        self.intersectionLane_6_bttn.setObjectName("intersectionLane_6_bttn")
        self.mainIntersectionTitle_txt = QtWidgets.QLabel(Widget)
        self.mainIntersectionTitle_txt.setGeometry(QtCore.QRect(480, 50, 521, 41))
        font = QtGui.QFont()
        font.setPointSize(35)
        self.mainIntersectionTitle_txt.setFont(font)
        self.mainIntersectionTitle_txt.setObjectName("mainIntersectionTitle_txt")
        self.intersections_img = QtWidgets.QLabel(Widget)
        self.intersections_img.setGeometry(QtCore.QRect(520, 130, 841, 611))
        self.intersections_img.setObjectName("intersections_img")
        self.intersections_img.raise_()
        self.back_bttn.raise_()
        self.verticalLayoutWidget.raise_()
        self.start_simulation.raise_()
        self.intersectionLane_1_bttn.raise_()
        self.intersectionLane_2_bttn.raise_()
        self.intersectionLane_3_bttn.raise_()
        self.intersectionLane_4_bttn.raise_()
        self.intersectionLane_5_bttn.raise_()
        self.intersectionLane_6_bttn.raise_()
        self.mainIntersectionTitle_txt.raise_()

        self.retranslateUi(Widget)
        QtCore.QMetaObject.connectSlotsByName(Widget)

    def retranslateUi(self, Widget):
        _translate = QtCore.QCoreApplication.translate
        Widget.setWindowTitle(_translate("Widget", "Widget"))
        self.back_bttn.setText(_translate("Widget", "Back"))
        self.allow_collisions_label.setText(_translate("Widget", "Allow Collisions"))
        self.speed_label.setText(_translate("Widget", "Max Speed (km/h)"))
        self.num_intersection_label.setText(_translate("Widget", "Number of Intersections"))
        self.safety_dist_label.setText(_translate("Widget", "Safety Distance (m)"))
        self.start_simulation.setText(_translate("Widget", "Start Simulation"))
        self.intersectionLane_1_bttn.setText(_translate("Widget", "1"))
        self.intersectionLane_2_bttn.setText(_translate("Widget", "2"))
        self.intersectionLane_3_bttn.setText(_translate("Widget", "3"))
        self.intersectionLane_4_bttn.setText(_translate("Widget", "4"))
        self.intersectionLane_5_bttn.setText(_translate("Widget", "5"))
        self.intersectionLane_6_bttn.setText(_translate("Widget", "6"))
        self.mainIntersectionTitle_txt.setText(_translate("Widget", "General Intersection Settings"))
        self.intersections_img.setText(_translate("Widget", "<html><head/><body><p><img src=\":/intersection/images/Intersection 1_cut.png\" height=\"600\"/><img src=\":/intersection/images/Intersection 1_cut.png\" height=\"600\"/><img src=\":/intersection/images/Intersection 1_cut.png\" height=\"600\"/><img src=\":/intersection/images/Intersection 1_cut.png\" height=\"600\"/><img src=\":/intersection/images/Intersection 1_cut.png\" height=\"600\"/><img src=\":/intersection/images/Intersection 1_cut.png\"height=600/></p></body></html>"))
