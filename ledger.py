#!/usr/bin/env python
import os

class Ledger():
	def split_ledger_contents(self):
		self.people = self.file_contents[1].upper().split()
		self.entries_by_payer = dict()
		self.entries = list()
		for entry in self.file_contents[2:]:
			entry = entry.split()
			entry[4] = " ".join(entry[4:])
			entry = entry[:5]
			persona = entry[3].upper() 

			if persona not in self.entries_by_payer:
				self.entries_by_payer[persona] = list()
			self.entries_by_payer[persona].append(entry)
			self.entries.append(entry)

	def __init__(self, file="~/.pyLedger/default.ldgr"):
		self.file=os.path.expanduser(file)
		try:
			fd = open(self.file, "rw")
			self.file_contents = fd.readlines()
			fd.close()
		except:
			self.file_contents=None

		# Split ledger contents skipping first line (title, etc)
		self.split_ledger_contents()

if __name__ == '__main__':
	test_ledger = Ledger()
	print test_ledger.entries
