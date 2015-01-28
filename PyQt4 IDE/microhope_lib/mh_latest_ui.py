from PyQt4 import QtCore, QtGui
import sys

class Mh_ui(QtGui.QMainWindow):
	def __init__(self):
		QtGui.QMainWindow.__init__(self)

		self.centralwidget = QtGui.QWidget(self)
		self.resize(1019, 737)
		self.verticalLayoutWidget = QtGui.QWidget(self.centralwidget)
		self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 10, 1021, 461))
		self._text_widget_verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
		self._text_widget_verticalLayout.setMargin(0)
		self.textEdit = QtGui.QTextEdit(self.verticalLayoutWidget)
		self._text_widget_verticalLayout.addWidget(self.textEdit)
		self.verticalLayoutWidget_2 = QtGui.QWidget(self.centralwidget)
		self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(0, 470, 1021, 21))
		self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget_2)
		self.verticalLayout.setMargin(0)
		self.label = QtGui.QLabel(self.verticalLayoutWidget_2)
		self.label.setStyleSheet("QLabel { background-color : green; color : blue; }")
		self.verticalLayout.addWidget(self.label)
		self.verticalLayoutWidget_3 = QtGui.QWidget(self.centralwidget)
		self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(0, 490, 1021, 221))
		self.verticalLayout_2 = QtGui.QVBoxLayout(self.verticalLayoutWidget_3)
		self.verticalLayout_2.setMargin(0)
		self.textEdit_2 = QtGui.QTextEdit(self.verticalLayoutWidget_3)
		self.textEdit_2.setReadOnly(True)
		self.textEdit_2.setPlainText("sample")
		self.verticalLayout_2.addWidget(self.textEdit_2)
		self.setCentralWidget(self.centralwidget)
		self.menubar = QtGui.QMenuBar(self)
		self.menubar.setGeometry(QtCore.QRect(0, 0, 1019, 25))
		self.setMenuBar(self.menubar)
		self.statusbar = QtGui.QStatusBar(self)
		self.setStatusBar(self.statusbar)


