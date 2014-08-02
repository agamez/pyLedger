#!/usr/bin/env python
import sys

from PyQt4.QtCore import *
from PyQt4.QtGui import *
import pyLedger_ui
import editEntry_ui
from ledger import Ledger


class PyLedger(QMainWindow, pyLedger_ui.Ui_MainWindow):
	def __init__(self, ledger):
		super(PyLedger, self).__init__()
		self.setupUi(self)

		row=0
		for entry in ledger.entries:
			entryItems = map(QTableWidgetItem, entry)
			self.entriesTable.setRowCount(self.entriesTable.rowCount()+1)
			column=0
			for item in entryItems:
				self.entriesTable.setItem(row,column,item)
				column+=1
			row+=1


if __name__ == "__main__":
	app = QApplication(sys.argv)
	ledger = Ledger()
	form = PyLedger(ledger)
	form.show()
	app.exec_()
