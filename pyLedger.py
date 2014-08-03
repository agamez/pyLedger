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
		self.reload()

	def reload(self):
		self.ledger.load()
		self.entriesTable.blockSignals(True)
		self.entriesTable.horizontalHeader().setResizeMode(QHeaderView.ResizeToContents)
		self.fill_table()
		self.updateStatusBar()
		self.entriesTable.blockSignals(False)
		self.entriesTable.setCurrentCell(self.entriesTable.rowCount()-1, 0)

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

	def on_removeEntryButton_clicked(self, b):
		row=self.entriesTable.currentRow()
		self.ledger.entries.pop(row)
		self.ledger.save()
		self.reload()

	def on_newEntryButton_clicked(self, b):
		self.entriesTable.blockSignals(True)

		row=self.entriesTable.rowCount()
		self.entriesTable.setRowCount(row+1)

		entry = (QDate.currentDate().toString("yy/MM/dd"), QTime.currentTime().toString(), "0.00", self.ledger.people[0], "")

		self.setEntry(entry, row)

		moneyItem = self.entriesTable.item(row, 2)
		self.entriesTable.setCurrentItem(moneyItem)
		self.entriesTable.editItem(moneyItem)

		self.entriesTable.blockSignals(False)
		self.ledger.entries.append()


	def on_entriesTable_itemChanged(self, item):
		entry = list()
		for x in range(0,self.entriesTable.columnCount()):
			entry.append(self.entriesTable.item(item.row(), x).text())

		if self.ledger.verify_entry(entry):
			print "Saving"
			try:
				self.ledger.entries[item.row()] = map(str, entry)
			except:
				self.ledger.entries.append(map(str, entry))
			self.ledger.save()
			self.reload()


	def on_showSummaryButton_clicked(self, b):
		totals = self.ledger.calculate_totals()

		msg = "Ledger statistics\n\n"
		msg = "Total payed: %.02f\n\n" % totals[0]
		for payer in totals[1:]:
			msg += "%s payed\t%.02f\t%s\t%.02f\n" % (payer[0], payer[1], "owes" if payer[2] > 0 else "is owned", payer[2])
		QMessageBox.about(self, "Ledger summary", msg)


if __name__ == "__main__":
	app = QApplication(sys.argv)
	ledger = Ledger()
	form = PyLedger(ledger)
	form.show()
	app.exec_()
