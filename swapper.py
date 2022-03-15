import functions
import requests
import os
import random
import json
import urllib.request
import urllib.parse
import os, sys, time
import threading
import time as t
from uuid import uuid4

first_username = []
first_array = []
first_ajax = []
first_hmac = []
first_appid = []
first_asbdid = []
first_csrf = []
first_cookie = []

second_username = []
second_array = []
second_ajax = []
second_hmac = []
second_appid = []
second_asbdid = []
second_csrf = []
second_cookie = []

# Verify Accounts for Swapper
def verifyaccount(username, type, proxy):
	with open("accounts/" + username, 'r') as f:
		for line in f:
			csrf = functions.find_between(line, "csrftoken=", " for")
			mid = functions.find_between(line, "mid=", " for")
			ds_user_id = functions.find_between(line, "ds_user_id=", " for")
			sessionid = functions.find_between(line, "sessionid=", " for")

	cookie = "csrftoken=" + csrf + ";mid=" + mid + ";ds_user_id=" + ds_user_id + ";sessionid=" + sessionid
	#print(cookie)

	getheaders={
		"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0", 
		"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
		"Accept-Language": "en-US,en;q=0.5",
		"Connection": "keep-alive",
		"Upgrade-Insecure-Requests": "1",
		"Sec-Fetch-Dest": "document",
		"Sec-Fetch-Mode": "navigate",
		"Sec-Fetch-Site": "none",
		"Sec-Fetch-User": "?1",
		"Cookie" : "" + cookie + "",
	}

	try:

		if proxy == "true":
			proxy = { "http" : "http://" + functions.getproxy('files/proxies.txt'), "https": "http://" + functions.getproxy('files/proxies.txt')  }
		else:
			proxy = { "http" : ""  }

		url = "https://www.instagram.com/accounts/edit/"

		while True:
			try:
				grab = requests.get(url, headers=getheaders, timeout=10, proxies=proxy)
				if not grab.text:
					pass
				else:
					break
			except requests.ConnectionError:
				print(functions.CRED + "[>] Connection timed out. Proxy is probably bad.")
				return


		first_response = grab.content
		biography = functions.find_between(str(first_response), '{"biography":"', '",')
		firstname = functions.find_between(str(first_response), '"first_name":"', '",')
		email = functions.find_between(str(first_response), '"email":"', '",')
		phone = functions.find_between(str(first_response), '"phone_number":"', '",')
		firstname = functions.unescape(firstname)

		firstname = ""
		biography = ""

		build_string = 'first_name=' + firstname + '&email=' + urllib.parse.quote(email) + '&username=' + username + '&phone_number=' + urllib.parse.quote(phone) + '&biography=' + urllib.parse.quote(biography) + '&external_url=&chaining_enabled=on'

		if type == 1:
			first_username.append(username)
			first_array.append(build_string)
			first_csrf.append(csrf)
			first_cookie.append(cookie)
		else:
			if type == 2:
				second_username.append(username)
				second_array.append(build_string)
				second_csrf.append(csrf)
				second_cookie.append(cookie)

		if not email:
			return False
		else:
			return True
	except:
		print("error")
		return False


# Changing the username
claimed = []
claimedfail = []
def changeusername1(username, newusername, type, proxy):

	times_attempted = 1

	# Delays one second before changing the @, so the claimer has a headstart!
	if type == "1":
		time.sleep(1)
	else:
		time.sleep(0)
		#print("")

	try:
		if username == first_username[0]:
			csrf = first_csrf[0]
			cookie = first_cookie[0]
			builtstring = first_array[0]
		else:
			if username == second_username[0]:
				csrf = second_csrf[0]
				cookie = second_cookie[0]
				builtstring = second_array[0]
	except:
		print(functions.CRED+"[>] Something did not match with function: changeusername1")

	postheaders={
		"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0",
		"Accept-Language": "en-US,en;q=0.5",
		"X-CSRFToken": "" + csrf + "",
		"Content-Type": "application/x-www-form-urlencoded",
		"X-Requested-With": "XMLHttpRequest",
		"Origin": "https://www.instagram.com",
		"Alt-Used": "www.instagram.com",
		"Connection": "keep-alive",
		"Referer": "https://www.instagram.com/accounts/edit/",
		"Cookie" : "" + cookie + "",
		"Sec-Fetch-Dest": "empty",
		"Sec-Fetch-Mode": "cors",
		"Sec-Fetch-Site": "same-origin",
		"TE": "trailers",
	}

	if type == "1":
		print(functions.YELLOW+"[>] Releasing " + username + " to " + newusername)
	else:
		print(functions.YELLOW+"[>] Swapping " + username + " to " + newusername)

	fixstring = builtstring.replace("&username=" + username, "&username=" + newusername)

	while True:

		try:
			if claimed[0] == "1":
				print(functions.CGREEN + "[>] Closed because we swapped " + fileName + " successfully.")
				return;
		except:
			pass

		if proxy == "true":
			proxy = { "http" : "http://" + functions.getproxy('files/proxies.txt'), "https": "http://" + functions.getproxy('files/proxies.txt')  }
		else:
			proxy = { "http" : ""  }

		url = "https://www.instagram.com/accounts/edit/"

		while True:
			try:
				send = requests.post(url, data = fixstring, headers=postheaders, timeout=10, proxies=proxy)
				if not send.text:
					pass
				else:
					break
			except requests.ConnectionError:
				print(functions.red + "[>] Connection timed out. Proxy is probably bad.")
				return

		second_response = send.text

		try:
			if "Something is wrong." in second_response:
				logtofile("instagram_error_3.txt", second_response)
				print(functions.CRED + "[>] Instagram said something was wrong and to try again.")
				break
		except:
			pass

		data = json.loads(second_response)

		# Limiting how many times to attempt to claim username
		try:
			if type == "2":
				if times_attempted > 15:
					print(functions.CRED+ "[!] We attempted over 15 times to swap and couldn't. Account is most likely on a 14 day.")
					claimedfail.append("1")
					break;
		except:
			pass

		# Success
		try:
			if data['status'] == "ok":
				print(functions.CGREEN + "[>] Successfully changed name to " + newusername)
				if type == "2":
					claimed.append("1")
					claimedfail.append("0")
				else:
					pass
				break;
		except:
			pass

		try:
			if "We're unable to save your changes due to an automated spam block." in send.text:
				print("[>] Instagram has marked " + username + " as spam, please wait before swapping again!")
				times_attempted += 15
		except:
			pass

		try:
			if data['message']['errors'][0] == "This username isn't available. Please try another.":
				print(CRED + "[>] This username is not available.")
				times_attempted += 1
		except:
			pass

		try:	
			if data['status'] == "fail":
				print(CRED + "[>] Instagram returned fail. Username isn't available.")
				times_attempted += 1
		except:
			pass

		try:
			if data['message'] == "Please wait a few minutes before you try again.":
				print(CRED + "[>] Rate limited.")
				times_attempted += 1
		except:
			pass

		try:
			if data['message'] == "feedback_required" or data['feedback_title'] == "Try Again Later":
				print(CRED + "[>] Rate limited #2.")
				times_attempted += 1
		except:
			pass

# Main Swapper
def swapper():
	dowe = input("[?] Do you have these two accounts already saved in the accounts folder? (Y / N): ")
	if dowe == "y" or dowe == "Y":
		firstaccountusername = input(functions.YELLOW+"[>] Enter username to the first account that are releasing the username from: ")
		randomusername = input(functions.YELLOW+"[>] Enter username to change this first account to: ")
		secondaccountusername = input(functions.YELLOW+"\n[>] Enter username to the second account that will claim the username: ")
	else:
		while True:
			try:
				username_1 = input(functions.YELLOW+ "[>] Enter username:pass to the first account that will be releasing the username: ")
				username1 = username_1.split(':')[0]
				password1 = username_1.split(':')[1]
				logintofirst = login(username1, password1)
				if logintofirst == "1":
					break;
				else:
					print(functions.CRED+"[>] Error with logging in to the first account. Let's try again.")
			except:
				print(functions.CRED+"[>] Error #2 with logging in to the first account. Let's try again.")
		while True:
			try: 
				username_2 = input(functions.YELLOW + "\n[>] Enter username:pass to the second account that will be claiming the username: ")
				username2 = username_2.split(':')[0]
				password2 = username_2.split(':')[1]
				logintofirst = login(username2, password2)
				if logintofirst == "1":
					break;
				else:
					print(functions.CRED+"\n[>] Error with logging in to the second account. Let's try again.")
			except:
				print(functions.CRED+"[>] Error #2 with logging in to the second account. Let's try again.")
		randomusername = input(functions.YELLOW+"\n[>] Enter username to change this first account to: ")
		firstaccountusername = username1
		secondaccountusername = username2

	question = input(functions.YELLOW + "[>] Would you like to use proxies from proxies.txt? (Y/N): ")
	if question == "Y" or question == "y":
		proxies = "true"
	else:
		proxies = "false"

	times = 1
	while True:
		if times == 1:
			print(functions.YELLOW + "[>] Checking first account.")
			checkfirstaccount = verifyaccount(firstaccountusername, times, proxies)
			if checkfirstaccount == True:
				firstaccount = True
			else:
				firstaccount = False
		else:
			if times == 2:
				print(functions.YELLOW + "[>] Checking second account.")
				checksecondaccount = verifyaccount(secondaccountusername, times, proxies)
				if checksecondaccount == True:
					secondaccount = True
				else:
					secondaccount = False
			else:
				break;
		times += 1

	if firstaccount == True and secondaccount == True:
		print(functions.CGREEN+"[>] Both accounts are good to use.")
		print("")

		# It will sleep for 1 second before releasing the username so claimer can get a headstart!
		for x in range(int(1)):
			th = threading.Thread(target=changeusername1, args=(firstaccountusername, randomusername, "1", proxies))
			th.start()

		# Multi thread 
		for x in range(int(3)):
			th = threading.Thread(target=changeusername1, args=(secondaccountusername, firstaccountusername, "2", proxies))
			th.start()

		# Checking if the swap was a success or fail
		try:
			while True:
				if claimedfail[0] == "1":
					print(functions.CRED + "[!] Claiming original username has failed, reverting back to the original name on first account.")
					for x in range(int(1)):
						th = threading.Thread(target=changeusername1, args=(firstaccountusername, firstaccountusername, "1", proxies))
						th.start()
					break
				else:
					if claimedfail[0] == "0":
						print(functions.CGREEN + "[>] Everything looks good. Closing.")
						break;
					else:
						pass
		except:
			print(functions.CRED + "[?] Something unexpected happened with swapper, ignore.")
			pass

	else:
		print(functions.CRED+"[>] One of the accounts are not good to use.")
		print(functions.YELLOW+"[>] First account ready: " + str(firstaccount))
		print(functions.YELLOW+"[>] Second account ready: " + str(secondaccount))
	exit()
