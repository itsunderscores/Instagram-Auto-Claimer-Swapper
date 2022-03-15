import functions
import login
import turbo
import swapper
import target
import os, sys, time
import os.path
import requests
import threading
from subprocess import call

if __name__ == '__main__':
	functions.firsttime() #Install requirements
	functions.clear() #Clear Screen
	functions.checkversion() #Check Program Version
	functions.header() #Display Header
	mode = input(functions.YELLOW + "[>] Please choose one of the following\n[>] 1 = Autoclaimer / Turbo\n[>] 2 = Swapper\n[3] 3 = Target Handle\n[>] 4 = Login to Accounts (If you haven't done this before or it's been a while)\n[>] Selection: ")

	if mode == "1":
		print("\n")
		turbo.turbo()
	elif mode == "2":
		print("\n")
		swapper.swapper()
	elif mode == "3":
		target.target()
	elif mode == "4":
		print("\n")
		login.logintotheaccounts()
	else:
		print(functions.CRED+ "\n[?] Invalid option, try again.")
		time.sleep(3)
		pass
