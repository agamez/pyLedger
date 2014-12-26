#!/usr/bin/env python
import os
from shutil import copyfile

class Ledger():
	def split_ledger_contents(self):
		self.title = self.file_contents[0]
		self.entries_by_payer = dict()
		self.entries = list()
		self.people = list()
		for entry in self.file_contents[1:]:
			entry = entry.split()
			try:
				entry[4] = " ".join(entry[4:])
			except:
				entry.append("No description")
			entry = entry[:5]
			entry[2] = "%.02f" % float(entry[2])
			payer = entry[3].upper()

			if payer not in self.people:
				self.people.append(payer)
			if payer not in self.entries_by_payer:
				self.entries_by_payer[payer] = list()
			self.entries_by_payer[payer].append(entry)
			self.entries.append(entry)

	def calculate_totals(self):
		total = list()
		total.append(sum([float(x[2]) for x in self.entries]))
		for payer in self.entries_by_payer:
			total_payer = sum([float(x[2]) for x in self.entries_by_payer[payer]])
			diff_payer = total[0]/len(self.entries_by_payer) - total_payer
			total.append((payer, total_payer, diff_payer))
		return total

	def save(self):
		copyfile(self.file, self.file+"~")
		fd = open(self.file, "w")
		fd.write(self.file_contents[0])
		print self.entries
		for entry in self.entries:
			fd.write(' '.join(entry)+"\n")
		fd.close()
		print "Saved"

	def verify_entry(self, entry):
		return True


	def __init__(self, file="~/.pyLedger/default.ldgr"):
		self.file=os.path.expanduser(file)
		self.load()

	def load(self):
		try:
			fd = open(self.file, "rw")
			self.file_contents = fd.readlines()
			fd.close()
		except:
			self.file_contents=None

		# Split ledger contents skipping first line (title, etc)
		self.split_ledger_contents()

if __name__ == '__main__':
	import sys

	if len(sys.argv)==2:
		ledger = Ledger(sys.argv[1])
	else:
		ledger = Ledger()

	totals = ledger.calculate_totals()

	total = totals[0]
	expenses = totals[1:]

	print ledger.title

	print "TOTAL:", total
	for entry in expenses:
		person, payed, owes = entry
		if owes>0:
			print "%s paid:\t%.02f and still owes:\t%0.2f" % (person, payed, owes)
		else:
			print "%s paid:\t%.02f and is owed:\t%0.2f" % (person, payed, abs(owes))
		
