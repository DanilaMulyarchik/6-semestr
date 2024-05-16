# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtWidgets

import logging
import time

from src.find_context import find_context


CONTEXT_SIZE = (789, 476)
NO_CONTEXT_SIZE = (789, 141)


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(*NO_CONTEXT_SIZE)
        self.gridLayout_2 = QtWidgets.QGridLayout(Dialog)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")

        self.contexArea = QtWidgets.QTextEdit(Dialog)
        self.contexArea.setEnabled(False)
        self.contexArea.setVisible(False)
        self.contexArea.setReadOnly(True)
        self.contexArea.setObjectName("contexArea")
        self.gridLayout.addWidget(self.contexArea, 1, 0, 1, 2)

        self.countSpinBox = QtWidgets.QSpinBox(Dialog)
        self.countSpinBox.setAccelerated(True)
        self.countSpinBox.setMaximum(10000)
        self.countSpinBox.setObjectName("countSpinBox")
        self.gridLayout.addWidget(self.countSpinBox, 3, 1, 1, 1)

        self.wordEdit = QtWidgets.QLineEdit(Dialog)
        self.wordEdit.setToolTip("")
        self.wordEdit.setClearButtonEnabled(True)
        self.wordEdit.setObjectName("wordEdit")
        self.gridLayout.addWidget(self.wordEdit, 2, 0, 1, 2)

        self.lengthSpinBox = QtWidgets.QSpinBox(Dialog)
        self.lengthSpinBox.setAccelerated(True)
        self.lengthSpinBox.setMaximum(10000)
        self.lengthSpinBox.setObjectName("lengthSpinBox")
        self.gridLayout.addWidget(self.lengthSpinBox, 3, 0, 1, 1)

        self.findContext = QtWidgets.QPushButton(Dialog)
        self.findContext.setEnabled(False)
        self.findContext.setObjectName("findContext")
        self.gridLayout.addWidget(self.findContext, 4, 0, 1, 2)
        self.gridLayout_2.addLayout(self.gridLayout, 1, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        self.connect_all(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Контекст использования слова"))
        self.countSpinBox.setSpecialValueText(
            _translate("Dialog", "Введите количество предложений...")
        )
        self.wordEdit.setPlaceholderText(_translate("Dialog", "Введите слово..."))
        self.lengthSpinBox.setSpecialValueText(
            _translate("Dialog", "Введите длину контекста...")
        )
        self.findContext.setText(_translate("Dialog", "Поиск контекста"))

    def find_contex_clicked(self, Dialog):
        Dialog.resize(*CONTEXT_SIZE)
        self.contexArea.setVisible(True)
        self.contexArea.setEnabled(True)

        start = time.time()
        self.contexArea.setText(
            find_context(
                word=self.wordEdit.text(),
                length=self.lengthSpinBox.value(),
                count=self.countSpinBox.value(),
            )
        )
        logging.info(time.time() - start)

    def length_spin_box_value_changed(self):
        if self.lengthSpinBox.value() > 0:
            if self.countSpinBox.value() > 0 and self.wordEdit.text():
                self.findContext.setEnabled(True)
                return
        self.findContext.setEnabled(False)

    def count_spin_box_value_changed(self):
        if self.countSpinBox.value() > 0:
            if self.lengthSpinBox.value() > 0 and self.wordEdit.text():
                self.findContext.setEnabled(True)
                return
        self.findContext.setEnabled(False)

    def word_edit_text_changed(self):
        if self.wordEdit.text():
            if self.lengthSpinBox.value() > 0 and self.countSpinBox.value() > 0:
                self.findContext.setEnabled(True)
                return
        self.findContext.setEnabled(False)

    def connect_all(self, Dialog):
        self.findContext.clicked.connect(lambda: self.find_contex_clicked(Dialog))
        self.lengthSpinBox.valueChanged.connect(self.length_spin_box_value_changed)
        self.countSpinBox.valueChanged.connect(self.count_spin_box_value_changed)
        self.wordEdit.textChanged.connect(self.word_edit_text_changed)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())