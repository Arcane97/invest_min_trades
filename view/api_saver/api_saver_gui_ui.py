# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'api_saver_gui_ui.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_API_keys_saver(object):
    def setupUi(self, API_keys_saver):
        API_keys_saver.setObjectName("API_keys_saver")
        API_keys_saver.resize(591, 325)
        self.verticalLayout = QtWidgets.QVBoxLayout(API_keys_saver)
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 206, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.api_key_lbl = QtWidgets.QLabel(API_keys_saver)
        self.api_key_lbl.setObjectName("api_key_lbl")
        self.horizontalLayout.addWidget(self.api_key_lbl)
        self.label = QtWidgets.QLabel(API_keys_saver)
        self.label.setMinimumSize(QtCore.QSize(8, 0))
        self.label.setText("")
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.api_key_ledit = QtWidgets.QLineEdit(API_keys_saver)
        self.api_key_ledit.setMinimumSize(QtCore.QSize(240, 0))
        self.api_key_ledit.setText("")
        self.api_key_ledit.setObjectName("api_key_ledit")
        self.horizontalLayout.addWidget(self.api_key_ledit)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem3)
        self.horizontalLayout.setStretch(0, 10)
        self.horizontalLayout.setStretch(5, 10)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem4)
        self.api_secret_lbl = QtWidgets.QLabel(API_keys_saver)
        self.api_secret_lbl.setObjectName("api_secret_lbl")
        self.horizontalLayout_2.addWidget(self.api_secret_lbl)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem5)
        self.api_secret_ledit = QtWidgets.QLineEdit(API_keys_saver)
        self.api_secret_ledit.setMinimumSize(QtCore.QSize(240, 0))
        self.api_secret_ledit.setObjectName("api_secret_ledit")
        self.horizontalLayout_2.addWidget(self.api_secret_ledit)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem6)
        self.horizontalLayout_2.setStretch(0, 10)
        self.horizontalLayout_2.setStretch(4, 10)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.verticalLayout.addLayout(self.verticalLayout_2)
        spacerItem7 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem7)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem8 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem8)
        self.api_save_btn = QtWidgets.QPushButton(API_keys_saver)
        self.api_save_btn.setObjectName("api_save_btn")
        self.horizontalLayout_4.addWidget(self.api_save_btn)
        spacerItem9 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem9)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        spacerItem10 = QtWidgets.QSpacerItem(20, 420, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem10)
        self.verticalLayout.setStretch(0, 10)
        self.verticalLayout.setStretch(4, 10)

        self.retranslateUi(API_keys_saver)
        QtCore.QMetaObject.connectSlotsByName(API_keys_saver)

    def retranslateUi(self, API_keys_saver):
        _translate = QtCore.QCoreApplication.translate
        API_keys_saver.setWindowTitle(_translate("API_keys_saver", "Сохрание API ключа"))
        self.api_key_lbl.setText(_translate("API_keys_saver", "Введите API key"))
        self.api_secret_lbl.setText(_translate("API_keys_saver", "Введите API secret"))
        self.api_save_btn.setText(_translate("API_keys_saver", "Сохранить"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    API_keys_saver = QtWidgets.QWidget()
    ui = Ui_API_keys_saver()
    ui.setupUi(API_keys_saver)
    API_keys_saver.show()
    sys.exit(app.exec_())

