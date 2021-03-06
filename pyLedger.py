#!/usr/bin/env python
import sys
import os

from PyQt4.QtCore import *
from PyQt4.QtGui import *
import pyLedger_ui
from ledger import Ledger


class PyLedger(QMainWindow, pyLedger_ui.Ui_MainWindow):
	def __init__(self, ledger):
		super(PyLedger, self).__init__()
		self.ledger=ledger
		self.setupUi(self)
		if ledger:
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
		self.entriesTable.setRowCount(row)
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
		try:
			max_owes = max([t[2] for t in totals[1:]])
			next_payer = [t[0] for t in totals[1:] if t[2]==max_owes][0]
			self.statusBar().showMessage("Total spent: %.02f. %s owes: %.02f. %s owes: %.02f. %s should pay next." % (totals[0], totals[1][0], totals[1][2], totals[2][0], totals[2][2], next_payer))
		except:
			self.statusBar().showMessage("Empty ledger")

	def on_removeEntryButton_clicked(self, b):
		if not self.ledger:
			QMessageBox.warning(self, "Error", "You must open an existing ledger or create a new one")
			return
		row=self.entriesTable.currentRow()
		self.ledger.entries.pop(row)
		self.ledger.save()
		self.reload()

	def on_newEntryButton_clicked(self, b):
		if not self.ledger:
			QMessageBox.warning(self, "Error", "You must open an existing ledger or create a new one")
			return
		self.entriesTable.blockSignals(True)

		next_payer = self.ledger.people[0] if self.ledger.people else ""
		entry = (QDate.currentDate().toString("yy/MM/dd"), QTime.currentTime().toString(), "0.00", next_payer, "")

		row=self.entriesTable.rowCount()
		self.entriesTable.setRowCount(row+1)

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
			try:
				self.ledger.entries[item.row()] = map(str, entry)
			except:
				self.ledger.entries.append(map(str, entry))
			self.ledger.save()
			self.reload()


	def on_showSummaryButton_clicked(self, b):
		if not self.ledger:
			QMessageBox.warning(self, "Error", "You must open an existing ledger or create a new one")
			return
		totals = self.ledger.calculate_totals()

		msg = "Ledger statistics\n\n"
		msg = "Total payed: %.02f\n\n" % totals[0]
		for payer in totals[1:]:
			msg += "%s payed\t%.02f\t%s\t%.02f\n" % (payer[0], payer[1], "owes" if payer[2] > 0 else "is owed", payer[2])
		QMessageBox.about(self, "Ledger summary", msg)

	def on_actionOpen_triggered(self, b):
		new_ledger = QFileDialog.getOpenFileName(self, 'Open ledger', '/', 'Ledger files (*.ldgr)')
		if new_ledger:
			if self.ledger:
				self.ledger.save()
			self.ledger = Ledger(str(new_ledger))
			self.reload()

	def on_actionNew_triggered(self, b):
		new_ledger = QFileDialog.getSaveFileName(self, 'New ledger', '/', 'Ledger files (*.ldgr)')
		if new_ledger:
			title, ok = QInputDialog.getText(self, 'Ledger title', 'Ledger title')
			if ok:
				self.ledger = Ledger(str(new_ledger), str(title))
				self.reload()


	def on_actionSetDefault_triggered(self, b):
		if not self.ledger:
			QMessageBox.warning(self, "Error", "You must open an existing ledger or create a new one")
			return
		default_ledger = os.path.expanduser('~/.default.ldgr')
		if not os.path.exists(default_ledger) or os.path.islink(default_ledger):
			try:
				os.remove(default_ledger)
			except:
				pass
			os.symlink(self.ledger.file, default_ledger)


if __name__ == "__main__":
	app = QApplication(sys.argv)
	try:
		ledger = Ledger()
		form = PyLedger(ledger)
	except:
		form = PyLedger(None)
	form.show()
	app.exec_()
