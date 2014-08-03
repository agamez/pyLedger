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
		self.ledger=ledger
		self.setupUi(self)

		self.entriesTable.blockSignals(True)
		self.entriesTable.horizontalHeader().setResizeMode(QHeaderView.ResizeToContents)
		self.fill_table()
		self.updateStatusBar()
		self.entriesTable.blockSignals(False)

	def fill_table(self):
		row=0
		for entry in self.ledger.entries:
			self.entriesTable.setRowCount(row+1)
			self.setEntry(entry, row)
			row+=1

	def setEntry(self, entry, row):
		entryItems = map(QTableWidgetItem, entry)
		column=0
		for item in entryItems:
			if column==2:
				item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
			self.entriesTable.setItem(row,column,item)
			column+=1

	def updateStatusBar(self):
		totals = self.ledger.calculate_totals()
		max_owes = max([t[2] for t in totals[1:]])
		next_payer = [t[0] for t in totals[1:] if t[2]==max_owes][0]
		self.statusBar().showMessage("Total spent: %.02f. %s owes: %.02f. %s owes: %.02f. %s should pay next." % (totals[0], totals[1][0], totals[1][2], totals[2][0], totals[2][2], next_payer))

	def on_newEntryButton_clicked(self, b):
		self.entriesTable.blockSignals(True)

		row=self.entriesTable.rowCount()
		self.entriesTable.setRowCount(row+1)

		entry = (QDate.currentDate().toString("yy/MM/dd"), QTime.currentTime().toString(), "0.00", "", "")

		self.setEntry(entry, row)

		moneyItem = self.entriesTable.item(row, 2)
		self.entriesTable.setCurrentItem(moneyItem)
		self.entriesTable.editItem(moneyItem)

		self.entriesTable.blockSignals(False)


	def on_entriesTable_itemChanged(self, item):
		entry = list()
		for x in range(0,self.entriesTable.columnCount()):
			entry.append(self.entriesTable.item(item.row(), x).text())

		if self.ledger.verify_entry(entry):
			print "Saving"
			self.ledger.entries.append(entry)
			self.ledger.save()


	def on_showSummaryButton_clicked(self, b):
		print "Save changes"


if __name__ == "__main__":
	app = QApplication(sys.argv)
	ledger = Ledger()
	form = PyLedger(ledger)
	form.show()
	app.exec_()
