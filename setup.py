#!/usr/bin/env python
from distutils.core import setup
from distutils.command.build import build
import os

class build_ui(build):
	def run(self):
		build.run(self)
		os.system("pyuic4 pyLedger.ui -o pyLedger_ui.py")		


setup(
	name='pyLedger',
	version='1.1',
	license = "GNU General Public License, Version 2",
	author='Alvaro Gamez Machado',
	author_email='alvaro.gamez@hazent.com',
	url='https://github.com/agamez/pyLedger',
	scripts=['pyLedger'],
	cmdclass = {"build" : build_ui},
	data_files = [('share/icons/hicolor/64x64/apps', ['ledger.png']),
		      ('share/applications/hildon', ['pyLedger.desktop']),
		      ('/opt/pyLedger', ['ledger.py', 'pyLedger.py', 'pyLedger_ui.py']),
	]
)
