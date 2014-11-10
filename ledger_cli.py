#!/usr/bin/env python
import os
import sys

def persona_total(persona):
	return sum([float(x[2]) for x in persona]) 

def calculate_expenses_person(ledger_contents):
	expenses = dict()
	for entry in ledger_contents:
		entry = entry.split()
		entry[4] = " ".join(entry[4:])
		entry = entry[:5]
		persona = entry[3].upper() 

		if persona not in expenses:
			expenses[persona] = list()
		expenses[persona].append(entry)
	return expenses

def print_expenses():
	for key in expenses:
		print key,":",
		expenses[key] = persona_total(expenses[key]) 
		print expenses[key] 
	print

if __name__ == '__main__':
	print sys.argv
	ledger_file = "~/.pyLedger/default.ldgr" if len(sys.argv)<2 else sys.argv[1]

	ledger_contents = open(os.path.expanduser(ledger_file), 'r').readlines()[2:]

	expenses = calculate_expenses_person(ledger_contents)
	print_expenses()

	total = sum([expenses[key] for key in expenses]) 
	print "TOTAL:", total
	for key in expenses:
		print key, "owes:", total/len(expenses) - expenses[key]
