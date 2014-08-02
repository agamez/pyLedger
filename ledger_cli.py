#!/usr/bin/env python
import os

def persona_total(persona):
	return sum([float(x[2]) for x in persona]) 

expenses = dict()
ledger_file = open(os.path.expanduser("~/.pyLedger/default.ldgr"), 'r').readlines()[1:]

for entry in ledger_file:
	entry = entry.split()
	entry[4] = " ".join(entry[4:])
	entry = entry[:5]
	persona = entry[3].upper() 

	if persona not in expenses:
		expenses[persona] = list()
	expenses[persona].append(entry)

for key in expenses:
	print key,":",
	expenses[key] = persona_total(expenses[key]) 
	print expenses[key] 
print

total = sum([expenses[key] for key in expenses]) 
print "TOTAL:", total
for key in expenses:
	print key, "owes:", total/len(expenses) - expenses[key]
