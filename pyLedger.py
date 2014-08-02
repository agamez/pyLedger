#!/usr/bin/env python
import sys

from PyQt4.QtCore import *
from PyQt4.QtGui import *
import pyLedger_ui
import editEntry_ui

class PyLedger(QMainWindow, pyLedger_ui.Ui_MainWindow):
	def __init__(self):
		super(PyLedger, self).__init__()
		self.setupUi(self)

if __name__ == "__main__":
	app = QApplication(sys.argv)
	form = PyLedger()
	form.show()
	app.exec_()
