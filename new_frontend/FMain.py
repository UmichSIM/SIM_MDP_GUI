# Form implementation generated from reading ui file 'fmain.ui'
#
# Created by: PyQt6 UI code generator 6.4.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_FullDisplay(object):
    def setupUi(self, FullDisplay):
        FullDisplay.setObjectName("FullDisplay")
        FullDisplay.resize(1400, 800)
        FullDisplay.setMinimumSize(QtCore.QSize(1400, 800))
        FullDisplay.setMaximumSize(QtCore.QSize(1400, 800))
        self.Back_bttn = QtWidgets.QPushButton(FullDisplay)
        self.Back_bttn.setGeometry(QtCore.QRect(40, 100, 100, 50))
        self.Back_bttn.setMinimumSize(QtCore.QSize(100, 50))
        self.Back_bttn.setMaximumSize(QtCore.QSize(100, 50))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.Back_bttn.setFont(font)
        self.Back_bttn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.Back_bttn.setObjectName("Back_bttn")
        self.GeneralFreewaySettings_title = QtWidgets.QLabel(FullDisplay)
        self.GeneralFreewaySettings_title.setGeometry(QtCore.QRect(460, 20, 451, 61))
        font = QtGui.QFont()
        font.setPointSize(35)
        self.GeneralFreewaySettings_title.setFont(font)
        self.GeneralFreewaySettings_title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.GeneralFreewaySettings_title.setObjectName("GeneralFreewaySettings_title")
        self.horizontalLayoutWidget = QtWidgets.QWidget(FullDisplay)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(40, 240, 181, 31))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.AllowCollisions_lyout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.AllowCollisions_lyout.setContentsMargins(0, 0, 0, 0)
        self.AllowCollisions_lyout.setObjectName("AllowCollisions_lyout")
        self.AllowCollisions_txt = QtWidgets.QLabel(self.horizontalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.AllowCollisions_txt.sizePolicy().hasHeightForWidth())
        self.AllowCollisions_txt.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.AllowCollisions_txt.setFont(font)
        self.AllowCollisions_txt.setObjectName("AllowCollisions_txt")
        self.AllowCollisions_lyout.addWidget(self.AllowCollisions_txt)
        self.AllowCollisions_chkbx = QtWidgets.QCheckBox(self.horizontalLayoutWidget)
        self.AllowCollisions_chkbx.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.AllowCollisions_chkbx.sizePolicy().hasHeightForWidth())
        self.AllowCollisions_chkbx.setSizePolicy(sizePolicy)
        self.AllowCollisions_chkbx.setMinimumSize(QtCore.QSize(20, 20))
        self.AllowCollisions_chkbx.setMaximumSize(QtCore.QSize(20, 20))
        self.AllowCollisions_chkbx.setBaseSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.AllowCollisions_chkbx.setFont(font)
        self.AllowCollisions_chkbx.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.AllowCollisions_chkbx.setText("")
        self.AllowCollisions_chkbx.setIconSize(QtCore.QSize(20, 20))
        self.AllowCollisions_chkbx.setChecked(True)
        self.AllowCollisions_chkbx.setObjectName("AllowCollisions_chkbx")
        self.AllowCollisions_lyout.addWidget(self.AllowCollisions_chkbx)
        self.StartSim_bttn = QtWidgets.QPushButton(FullDisplay)
        self.StartSim_bttn.setGeometry(QtCore.QRect(40, 700, 171, 50))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.StartSim_bttn.sizePolicy().hasHeightForWidth())
        self.StartSim_bttn.setSizePolicy(sizePolicy)
        self.StartSim_bttn.setMinimumSize(QtCore.QSize(0, 50))
        self.StartSim_bttn.setMaximumSize(QtCore.QSize(16777215, 50))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.StartSim_bttn.setFont(font)
        self.StartSim_bttn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.StartSim_bttn.setObjectName("StartSim_bttn")
        self.Fway_1_bttn = QtWidgets.QPushButton(FullDisplay)
        self.Fway_1_bttn.setGeometry(QtCore.QRect(530, 390, 60, 60))
        self.Fway_1_bttn.setMinimumSize(QtCore.QSize(60, 60))
        self.Fway_1_bttn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.Fway_1_bttn.setFont(font)
        self.Fway_1_bttn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.Fway_1_bttn.setAutoFillBackground(True)
        self.Fway_1_bttn.setObjectName("Fway_1_bttn")
        self.Fway_2_bttn = QtWidgets.QPushButton(FullDisplay)
        self.Fway_2_bttn.setGeometry(QtCore.QRect(700, 390, 60, 60))
        self.Fway_2_bttn.setMinimumSize(QtCore.QSize(60, 60))
        self.Fway_2_bttn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.Fway_2_bttn.setFont(font)
        self.Fway_2_bttn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.Fway_2_bttn.setAutoFillBackground(True)
        self.Fway_2_bttn.setObjectName("Fway_2_bttn")
        self.Fway_3_bttn = QtWidgets.QPushButton(FullDisplay)
        self.Fway_3_bttn.setGeometry(QtCore.QRect(870, 390, 60, 60))
        self.Fway_3_bttn.setMinimumSize(QtCore.QSize(60, 60))
        self.Fway_3_bttn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.Fway_3_bttn.setFont(font)
        self.Fway_3_bttn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.Fway_3_bttn.setAutoFillBackground(True)
        self.Fway_3_bttn.setObjectName("Fway_3_bttn")
        self.Fway_4_bttn = QtWidgets.QPushButton(FullDisplay)
        self.Fway_4_bttn.setGeometry(QtCore.QRect(1040, 390, 60, 60))
        self.Fway_4_bttn.setMinimumSize(QtCore.QSize(60, 60))
        self.Fway_4_bttn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.Fway_4_bttn.setFont(font)
        self.Fway_4_bttn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.Fway_4_bttn.setAutoFillBackground(True)
        self.Fway_4_bttn.setObjectName("Fway_4_bttn")
        self.Fway_5_bttn = QtWidgets.QPushButton(FullDisplay)
        self.Fway_5_bttn.setGeometry(QtCore.QRect(1200, 390, 60, 60))
        self.Fway_5_bttn.setMinimumSize(QtCore.QSize(60, 60))
        self.Fway_5_bttn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.Fway_5_bttn.setFont(font)
        self.Fway_5_bttn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.Fway_5_bttn.setAutoFillBackground(True)
        self.Fway_5_bttn.setObjectName("Fway_5_bttn")
        self.IntersectionImages = QtWidgets.QLabel(FullDisplay)
        self.IntersectionImages.setGeometry(QtCore.QRect(480, 110, 831, 641))
        self.IntersectionImages.setObjectName("IntersectionImages")
        self.SingleRightArrow = QtWidgets.QLabel(FullDisplay)
        self.SingleRightArrow.setGeometry(QtCore.QRect(1300, 380, 51, 81))
        self.SingleRightArrow.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.SingleRightArrow.setObjectName("SingleRightArrow")
        self.DoubleLeftArrow = QtWidgets.QLabel(FullDisplay)
        self.DoubleLeftArrow.setGeometry(QtCore.QRect(410, 380, 71, 81))
        self.DoubleLeftArrow.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.DoubleLeftArrow.setObjectName("DoubleLeftArrow")
        self.DoubleRightArrow = QtWidgets.QLabel(FullDisplay)
        self.DoubleRightArrow.setGeometry(QtCore.QRect(1330, 380, 61, 81))
        self.DoubleRightArrow.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.DoubleRightArrow.setObjectName("DoubleRightArrow")
        self.SingleLeftArrow = QtWidgets.QLabel(FullDisplay)
        self.SingleLeftArrow.setGeometry(QtCore.QRect(440, 380, 61, 81))
        self.SingleLeftArrow.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.SingleLeftArrow.setObjectName("SingleLeftArrow")
        self.verticalLayoutWidget = QtWidgets.QWidget(FullDisplay)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(40, 270, 321, 351))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.NumFwaySections_txt = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.NumFwaySections_txt.setFont(font)
        self.NumFwaySections_txt.setObjectName("NumFwaySections_txt")
        self.horizontalLayout.addWidget(self.NumFwaySections_txt)
        self.NumFwaySections_spinbx = QtWidgets.QSpinBox(self.verticalLayoutWidget)
        self.NumFwaySections_spinbx.setMinimumSize(QtCore.QSize(45, 25))
        self.NumFwaySections_spinbx.setMaximumSize(QtCore.QSize(45, 25))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.NumFwaySections_spinbx.setFont(font)
        self.NumFwaySections_spinbx.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.NumFwaySections_spinbx.setMinimum(1)
        self.NumFwaySections_spinbx.setMaximum(8)
        self.NumFwaySections_spinbx.setObjectName("NumFwaySections_spinbx")
        self.horizontalLayout.addWidget(self.NumFwaySections_spinbx)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.MaxSpeed_txt = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.MaxSpeed_txt.setFont(font)
        self.MaxSpeed_txt.setObjectName("MaxSpeed_txt")
        self.horizontalLayout_3.addWidget(self.MaxSpeed_txt)
        self.MaxSpped_spinbx = QtWidgets.QSpinBox(self.verticalLayoutWidget)
        self.MaxSpped_spinbx.setMinimumSize(QtCore.QSize(45, 25))
        self.MaxSpped_spinbx.setMaximumSize(QtCore.QSize(45, 25))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.MaxSpped_spinbx.setFont(font)
        self.MaxSpped_spinbx.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.MaxSpped_spinbx.setObjectName("MaxSpped_spinbx")
        self.horizontalLayout_3.addWidget(self.MaxSpped_spinbx)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.MinSpeed_txt = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.MinSpeed_txt.setFont(font)
        self.MinSpeed_txt.setObjectName("MinSpeed_txt")
        self.horizontalLayout_2.addWidget(self.MinSpeed_txt)
        self.MinSpeed_spinbx = QtWidgets.QSpinBox(self.verticalLayoutWidget)
        self.MinSpeed_spinbx.setMinimumSize(QtCore.QSize(45, 25))
        self.MinSpeed_spinbx.setMaximumSize(QtCore.QSize(45, 25))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.MinSpeed_spinbx.setFont(font)
        self.MinSpeed_spinbx.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.MinSpeed_spinbx.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.MinSpeed_spinbx.setObjectName("MinSpeed_spinbx")
        self.horizontalLayout_2.addWidget(self.MinSpeed_spinbx)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.SafetyDist_txt = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.SafetyDist_txt.setFont(font)
        self.SafetyDist_txt.setObjectName("SafetyDist_txt")
        self.horizontalLayout_4.addWidget(self.SafetyDist_txt)
        self.SafetyDist_spinbx = QtWidgets.QSpinBox(self.verticalLayoutWidget)
        self.SafetyDist_spinbx.setMinimumSize(QtCore.QSize(45, 25))
        self.SafetyDist_spinbx.setMaximumSize(QtCore.QSize(45, 25))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.SafetyDist_spinbx.setFont(font)
        self.SafetyDist_spinbx.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.SafetyDist_spinbx.setObjectName("SafetyDist_spinbx")
        self.horizontalLayout_4.addWidget(self.SafetyDist_spinbx)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.IntersectionImages.raise_()
        self.Back_bttn.raise_()
        self.GeneralFreewaySettings_title.raise_()
        self.horizontalLayoutWidget.raise_()
        self.StartSim_bttn.raise_()
        self.Fway_1_bttn.raise_()
        self.Fway_2_bttn.raise_()
        self.Fway_3_bttn.raise_()
        self.Fway_4_bttn.raise_()
        self.Fway_5_bttn.raise_()
        self.SingleRightArrow.raise_()
        self.DoubleLeftArrow.raise_()
        self.DoubleRightArrow.raise_()
        self.SingleLeftArrow.raise_()
        self.verticalLayoutWidget.raise_()

        self.retranslateUi(FullDisplay)
        QtCore.QMetaObject.connectSlotsByName(FullDisplay)

    def retranslateUi(self, FullDisplay):
        _translate = QtCore.QCoreApplication.translate
        FullDisplay.setWindowTitle(_translate("FullDisplay", "Widget"))
        self.Back_bttn.setText(_translate("FullDisplay", "Back"))
        self.GeneralFreewaySettings_title.setText(_translate("FullDisplay", "General Freeway Settings"))
        self.AllowCollisions_txt.setText(_translate("FullDisplay", "Allow Collisions"))
        self.StartSim_bttn.setText(_translate("FullDisplay", "Start Simulation"))
        self.Fway_1_bttn.setText(_translate("FullDisplay", "1"))
        self.Fway_2_bttn.setText(_translate("FullDisplay", "2"))
        self.Fway_3_bttn.setText(_translate("FullDisplay", "3"))
        self.Fway_4_bttn.setText(_translate("FullDisplay", "4"))
        self.Fway_5_bttn.setText(_translate("FullDisplay", "5"))
        self.IntersectionImages.setText(_translate("FullDisplay", "<html><head/><body><p><img src=\":/freeway/images/road.gif\" /><img src=\":/freeway/images/road.gif\"/><img src=\":/freeway/images/road.gif\"/><img src=\":/freeway/images/road.gif\"/><img src=\":/freeway/images/road.gif\"/></p></body></html>"))
        self.SingleRightArrow.setText(_translate("FullDisplay", "<html><head/><body><p><img src=\":/freeway/images/next.png\" width=50/></p></body></html>"))
        self.DoubleLeftArrow.setText(_translate("FullDisplay", "<html><head/><body><p><img src=\":/freeway/images/double_arrow_left.png\" width=50/></p></body></html>"))
        self.DoubleRightArrow.setText(_translate("FullDisplay", "<html><head/><body><p><img src=\":/freeway/images/double_next.png\"width=50/></p></body></html>"))
        self.SingleLeftArrow.setText(_translate("FullDisplay", "<html><head/><body><p><img src=\":/freeway/images/next_left.png\" width=\"50\"/></p></body></html>"))
        self.NumFwaySections_txt.setText(_translate("FullDisplay", "Number of Freeway Sections"))
        self.MaxSpeed_txt.setText(_translate("FullDisplay", "Maximum Speed (m/s)"))
        self.MinSpeed_txt.setText(_translate("FullDisplay", "Minimum Speed (m/s)"))
        self.SafetyDist_txt.setText(_translate("FullDisplay", "Safety Distance (m)"))
