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
		self.entriesTable.horizontalHeader().setResizeMode(QHeaderView.ResizeToContents)

		row=0
		for entry in ledger.entries:
			entryItems = map(QTableWidgetItem, entry)
			self.entriesTable.setRowCount(self.entriesTable.rowCount()+1)
			column=0
			for item in entryItems:
				if column==2:
					item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
				self.entriesTable.setItem(row,column,item)
				column+=1
			row+=1
		totals = ledger.calculate_totals()
		print self.statusBar().showMessage(str(totals))
		print totals

	def on_newEntryButton_clicked(self, b):
		row=self.entriesTable.rowCount()
		self.entriesTable.setRowCount(row+1)

		self.entriesTable.setItem(row, 0, QTableWidgetItem(QDate.currentDate().toString("yy/MM/dd")))
		self.entriesTable.setItem(row, 1, QTableWidgetItem(QTime.currentTime().toString()))
		moneyItem = QTableWidgetItem("0.00")
		moneyItem.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
		self.entriesTable.setItem(row, 2, moneyItem)

		self.entriesTable.setCurrentItem(moneyItem)


if __name__ == "__main__":
	app = QApplication(sys.argv)
	ledger = Ledger()
	form = PyLedger(ledger)
	form.show()
	app.exec_()
