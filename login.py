import functions
import requests
import os
import random
import threading
import json
import os, sys, time
import time as t
from uuid import uuid4

def login(username, password, proxy):
	uid = uuid4()
	url = "https://i.instagram.com/api/v1/accounts/login/"
	headers = { 'User-Agent': 'Instagram 113.0.0.39.122 Android (24/5.0; 515dpi; 1440x2416; huawei/google; Nexus 6P; angler; angler; en_US)',
		"Accept": "/",
		"Accept-Encoding": "gzip, deflate",
		"Accept-Language": "en-US",
		"X-IG-Capabilities": "3brTvw==",
		"X-IG-Connection-Type": "WIFI",
		"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
		'Host': 'i.instagram.com',
		'Connection': 'keep-alive'
	}
	data = {
		'uuid': uid,
		'password': password,
		'username': username,
		'device_id': uid,
		'from_reg': 'false',
		'_csrftoken': 'YcJzPesTYxMTfmpSOiVn3pfRAJdrETFD',
		'login_attempt_countn': '0'
	}

	if proxy == "true":
		proxy = { "http" : "http://" + functions.getproxy('files/proxies.txt'), "https": "http://" + functions.getproxy('files/proxies.txt')  }
	else:
		proxy = { "http" : ""  }

	while True:
		attempts = 0
		if attempts >= 5:
			print("[>] Could not check %s due to failing 5 times" % (username))
			functions.logtofile2("accounts_couldnotcheck.txt", username + ":" + password)
		try:
			response = requests.post(url=url, headers=headers, data=data, timeout=10, proxies=proxy)
			if not response.text:
				pass
				attempts += 1
			else:
				break
		except requests.ConnectionError:
			attempts += 1

	cookies = response.cookies
	bad = False
	loadjson = json.loads(response.text)

	try:
		if username == loadjson["logged_in_user"]["username"]:
			print(functions.CGREEN+"[>] Successfully logged in: " + username)
			functions.logtofile("accounts/" + username + "", cookies)
			functions.logtofile2("accounts_working.txt", username + ":" + password)
			return "1"
	except:
		pass

	try:
		if "You can't use Instagram because your account didn't follow our Community Guidelines." in response.text or "Your account has been permanently disabled" in response.text:
			print(functions.CRED+ "[!] Account is permanately suspended: " + username)
			functions.logtofile2("accounts_suspended.txt", username + ":" + password)
			bad = True
			return "0"
	except:
		pass

	try:
		if "Please wait a few minutes before you try again." in response.text:
			print(functions.CRED+ "[!] Rate Limited. Please wait a few minutes. " + username)
			functions.logtofile2("accounts_rate_limited.txt", username + ":" + password)
			bad = True
			return "0"
	except:
		pass

	try:
		if "The password you entered is incorrect." in response.text:
			print(functions.CRED+ "[!] Password is incorrect " + username)
			functions.logtofile2("accounts_failed.txt", username + ":" + password)
			bad = True
			return "0"
	except:
		pass

	try:
		if loadjson["logged_in_user"]["is_active"] == False:
			print(functions.YELLOW+"[!] Account is most likely locked. Cannot sign in: " + username)
			functions.logtofile2("accounts_locked.txt", username + ":" + password)
			bad = True
			return "0"
	except:
		pass

	try:
		if loadjson["message"] == "challenge_required":
			print(functions.YELLOW+"[!] Account is most likely locked #2. Cannot sign in: " + username)
			functions.logtofile2("accounts_locked.txt", username + ":" + password)
			bad = True
			return "0"
	except:
		pass

	try:
		if loadjson["error_type"] == "ip_block":
			print(functions.CRED+ "[!] This IP has been blocked. Waiting a few minutes before trying again. Cannot sign in: " + username)
			functions.logtofile2("accounts_rate_limited.txt", username + ":" + password)
			bad = True
			return "0"
	except:
		pass

	try:
		if loadjson["error_type"] == "rate_limit_error":
			print(functions.CRED+ "[!] Rate limited.")
			functions.logtofile2("accounts_rate_limited.txt", username + ":" + password)
			bad = True
			return "0"
	except:
		pass
	
	try:
		if loadjson["message"] == "The username you entered doesn't appear to belong to an account. Please check your username and try again.":
			print(functions.CRED+ "[!] Username " + username +" does not belong to an account.")
			functions.logtofile2("accounts_failed.txt", username + ":" + password)
			bad = True
			return "0"
	except:
		pass

	try:
		if bad == True:
			print(functions.CRED+"[!] Failed to login: " + username)
			functions.logtofile2("accounts_failed.txt", username + ":" + password)
	except:
		pass

def logintotheaccounts():
	question = input(functions.YELLOW + "[>] Would you like to use proxies from proxies.txt? (Y/N): ")
	if question == "Y" or question == "y":
		proxies = "true"
	else:
		proxies = "false"

	with open('files/accounts.txt', 'r') as f:
		for line in f:
			username = line.split(':')[0]
			password = line.split(':')[1]
			th = threading.Thread(target=login, args=(username, password, proxies))
			th.start()
			#login(username, password, proxies)
	#print(functions.CGREEN + "[>] Finished logging in.")
