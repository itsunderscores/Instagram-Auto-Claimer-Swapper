import requests
import os, sys, time
import os.path
import time as t
import threading
import urllib.request
import urllib.parse
import pickle
import re
import json
import random
from uuid import uuid4
from subprocess import call

os.system("cls") #clear panel

CRED = '\033[91m'
CEND = '\033[0m'
CGREEN = '\33[92m'
BLACK   = '\033[30m'
RED     = '\033[31m'
GREEN   = '\033[32m'
YELLOW  = '\033[33m'
BLUE    = '\033[34m'
MAGENTA = '\033[35m'
CYAN    = '\033[36m'
WHITE   = '\033[37m'
RESET   = '\033[39m'

# Checking if program is up-to-date
version = "2.5"
check = requests.get(url = "https://raw.githubusercontent.com/itsunderscores/Instagram-Auto-Claimer-Swapper/main/version.txt")
if(version in check.text):
	pass
else:
	print("This version is currently out of date and is recommended you download the updated one.")
	print("https://github.com/itsunderscores/Instagram-Auto-Claimer-Swapper")
	print(check)
	exit()



global syn
def header():
	print(CRED+''' _              _           
| |_ _   _ _ __| |__   ___  
| __| | | | '__| '_ \ / _ \ 
| |_| |_| | |  | |_) | (_) |
 \__|\__,_|_|  |_.__/ \___/ 
	''')
	print(CRED+"[+] Instagram Turbo v" + version)
	print(CRED+"[-] Developed by underscores#0001")
	print(WHITE+"-------------------------------------------------------"+YELLOW)

def getproxy(file):
	proxy = random.choice(list(open(file)))
	proxy = proxy.strip()
	proxy = proxy.replace("\n", "")
	return proxy

useproxy = []

def unescape(in_str):
    in_str = in_str.encode('unicode-escape')   # bytes with all chars escaped (the original escapes have the backslash escaped)
    in_str = in_str.replace(b'\\\\u', b'\\u')  # unescape the \
    in_str = in_str.decode('unicode-escape')   # unescape unicode
    return in_str

def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

def find_between_r( s, first, last ):
    try:
        start = s.rindex( first ) + len( first )
        end = s.rindex( last, start )
        return s[start:end]
    except ValueError:
        return ""

# Check if string is blank
def is_not_blank(s):
    return bool(s and not s.isspace())

# Log to textfile
def logtofile(file, text):
	f = open(file, "w")
	f.write(str(text)+"\n") 
	f.close()
	return text

#######################################################################

###################
# LOGIN FUNCTIONS #
###################

# New Login
def login(username, password):
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

	if useproxy[0] == "1":
		proxy = { "http" : "http://" + getproxy('proxies.txt') }
	else:
		proxy = { "http" : getproxy('proxies.txt')  }

	while True:
		try:
			response = requests.post(url=url, headers=headers, data=data, timeout=5, proxies=proxy)
			if not response.text:
				pass
			else:
				break
		except requests.ConnectionError:
			print("[>] Connection timed out. Proxy is probably bad.")
			return

	cookies = response.cookies

	bad = False

	loadjson = json.loads(response.text)
	try:
		if username == loadjson["logged_in_user"]["username"]:
			print(CGREEN+"[>] Successfully logged in: " + username)
			logtofile("cookies/" + username + ".txt", cookies)
			return "1"
	except:
		pass

	try:
		if "Please wait a few minutes before you try again." in response.text:
			print(CRED+ "[!] Rate Limited. Please wait a few minutes. " + username)
			time.sleep(120)
			bad = True
			return "0"
	except:
		pass

	try:
		if "The password you entered is incorrect." in response.text:
			print(CRED+ "[!] Password is incorrect " + username)
			bad = True
			return "0"
	except:
		pass

	try:
		if loadjson["logged_in_user"]["is_active"] == False:
			print(YELLOW+"[!] Account is most likely locked. Cannot sign in: " + username)
			bad = True
			return "0"
	except:
		pass

	try:
		if loadjson["message"] == "challenge_required":
			print(YELLOW+"[!] Account is most likely locked #2. Cannot sign in: " + username)
			bad = True
			return "0"
	except:
		pass

	try:
		if loadjson["error_type"] == "ip_block":
			print(CRED+ "[!] This IP has been blocked. Waiting a few minutes before trying again.")
			time.sleep(120)
			bad = True
			return "0"
	except:
		pass

	try:
		if loadjson["error_type"] == "rate_limit_error":
			print(CRED+ "[!] Rate limited.")
			bad = True
			return "0"
	except:
		pass
	
	try:
		if loadjson["message"] == "The username you entered doesn't appear to belong to an account. Please check your username and try again.":
			print(CRED+ "[!] Username " + username +" does not belong to an account.")
			bad = True
			return "0"
	except:
		pass

	try:
		if bad == True:
			print(CRED+"[!] Failed to login: " + username + " (" + response.text + ")")
	except:
		pass

# Signs into the accounts first to grab headers
def logintotheaccounts():
	with open('accounts.txt', 'r') as f:
		for line in f:
			username = line.split(':')[0]
			password = line.split(':')[1]
			login(username, password)
	print(CGREEN + "[>] Finished logging in.")

#######################################################################

############################
# NEW TURBO / AUTO CLAIMER #
############################

# remove username from list if claimed
# keep going if username list has more than 1
# skip and remove username if 10+ attempts and it has failed


# Random Account from folder /cookies
def getrandomcookie():
	file = random.choice(os.listdir("cookies/")) #change dir name to whatever
	return file

# Multi-threaded Turbo
sniped = []
sniped_username = []
claiming = []
def loadContents(fileName, delay, timeout):

	failed = 0

	while True:
		mycookie = getrandomcookie()
		with open("cookies/" + mycookie, 'r') as f:

			for line in f:
				csrf = find_between(line, "csrftoken=", " for")
				mid = find_between(line, "mid=", " for")
				ds_user_id = find_between(line, "ds_user_id=", " for")
				sessionid = find_between(line, "sessionid=", " for")

		cookie = "csrftoken=" + csrf + ";mid=" + mid + ";ds_user_id=" + ds_user_id + ";sessionid=" + sessionid

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
			"Cookie": "" + cookie + ""
		}

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

		if useproxy[0] == "1":
			proxy = { "http" : "http://" + getproxy('proxies.txt') }
		else:
			proxy = { "http" : getproxy('proxies.txt')  }

		# Grabs current account information
		url = "https://www.instagram.com/accounts/edit/"

		while True:
			try:
				grab = requests.get(url, headers=getheaders, timeout=10, proxies=proxy)
				if not grab.text:
					pass
				else:
					break
			except requests.ConnectionError:
				print("[>] Connection timed out. Proxy is probably bad.")
				return

		first_response = grab.content
		biography = find_between(str(first_response), '{"biography":"', '",')
		firstname = find_between(str(first_response), '"first_name":"', '",')
		email = find_between(str(first_response), '"email":"', '",')
		phone = find_between(str(first_response), '"phone_number":"', '",')
		firstname = unescape(firstname)
		biography = unescape(biography)

		firstname = ""
		biography = ""

		while True:

			try: # Claimed (Old)
				#if sniped[0] == "1":
				if sniped[0] == "5":
					print(CGREEN + "[>] Closed because we claimed " + sniped_username[0] + " successfully.")
					return;
			except:
				pass

			# Stop trying on account if 50+ failed attempts. We can also try to get a new cookie instead?
			try:
				if failed > 50:
					print("[>] Closed a thread because we had 50+ failed attempts.")
					return;
			except:
				pass

			# Going through each username in file to claim
			with open('usernames.txt', 'r') as accountfile:
				for username in accountfile:
					username = username.strip()
					username = username.replace("\n", "")

					try: # Claimed (Old)
						#if sniped[0] == "1":
						if sniped[0] == "5":
							print(CGREEN + "[>] Closed because we claimed " + sniped_username[0] + " successfully.")
							return;
					except:
						pass

					try: #We already claimed this username
						if username in sniped_username:
							print("We have already claimed this username!")
							with open("usernames.txt", "r") as f:
							    lines = f.readlines()
							with open("usernames.txt", "w") as f:
							    for line in lines:
							        if line.strip("\n") != username:
							            f.write(line)
						else:
							pass
					except:
						pass


					try:
						if useproxy[0] == "1":
							proxy = { "http" : "http://" + getproxy('proxies.txt') }
						else:
							proxy = { "http" : getproxy('proxies.txt')  }

						url2 = "https://www.instagram.com/" + username + "/"

						while True:
							try:
								grab2 = requests.get(url2, headers=getheaders, timeout=timeout, proxies=proxy)
								if not grab2.text:
									pass
								else:
									break
							except requests.ConnectionError:
								print("[>] Connection timed out. Proxy is probably bad.")
								return

						first_response2 = grab2.content

						blah = find_between(str(first_response2), str("<title>"), str("</title>"))
						gay = find_between(str(first_response2), str("\"alternateName\":\""), str("\""))

						if gay == "@" + username:
							print(YELLOW+"[>] " + username + " is not available. #1")
							failed += 1
							snipeready = False
						else:
							if "Posts - See Instagram photos and videos from" in str(first_response2):
								print(YELLOW+"[>] " + username + " is not available. #2")
								failed += 1
								snipeready = False
							else:
								if "See Instagram photos and videos from " in str(first_response2):
									print(YELLOW+"[>] " + username + " is not available. #3")
									failed += 1
									snipeready = False
								else:
									if "Create an account or log in to Instagram " in str(first_response2):
										print(CRED + "[>] Login is bad, get a new one. Most likely locked. #2")
										failed += 1
										snipeready = False
										break
									else:
										if blah == '\\nInstagram\\n':
											print(GREEN+"[>] " + username + " is available, claiming.")
											snipeready = True
											claiming.append(time.time())
										else:
											if blah == '\\nLogin \\xe2\\x80\\xa2 Instagram\\n':
												print(CRED+"[>] Login is bad, get a new one. Most likely locked. #3")
												break
												snipeready = False
					except requests.exceptions.Timeout:
						print(CRED + "[>] Request timed out.")

					try:
						if snipeready == True:
							
							if useproxy[0] == "1":
								proxy = { "http" : "http://" + getproxy('proxies.txt') }
							else:
								proxy = { "http" : getproxy('proxies.txt')  }

							data1 = 'first_name=' + firstname + '&email=' + urllib.parse.quote(email) + '&username=' + username + '&phone_number=' + urllib.parse.quote(phone) + '&biography=' + urllib.parse.quote(biography) + '&external_url=&chaining_enabled=on'
							
							while True:
								try:
									send = requests.post("https://www.instagram.com/accounts/edit/", data = data1, timeout=10, headers=postheaders, proxies=proxy)
									if not send.text:
										pass
									else:
										break
								except requests.ConnectionError:
									print("[>] Connection timed out. Proxy is probably bad.")
									return

							second_response = str(send.content)
							second_response = second_response.replace("b'", "");
							second_response = second_response.replace('\\', "");
							second_response = second_response[:-1]
							try:
								if "Something is wrong." in second_response:
									logtofile("instagram_error_3.txt", second_response)
									print(CRED + "[>] Instagram said something was wrong and to try again.")
									time.sleep(60)
									failed += 1
									break;
							except:
								pass
							try:
								data = json.loads(str(second_response))
								if data['status'] == "ok":
									print(CGREEN + "[>] Successfully claimed username: " + username)
									sniped.append("1")
									sniped_username.append(username)
									logtofile("success_" + username + ".txt", mycookie + " > " + username)
									print("[>] It took %s seconds to claim!" % (time.time() - claiming[0]))
									#return;
									#exit()
									#break;
								else:
									if data['message']['errors'][0] == "This username isn't available. Please try another.":
										print(CRED + "[>] This username is not available.")
										failed += 1
										#break;
									else:
										if data['status'] == "fail":
											print(CRED + "[>] Instagram returned fail.")
											failed += 1
											time.sleep(5)
											#break;
										else:
											if data['message'] == "Please wait a few minutes before you try again.":
												print(CRED + "[>] Rate limited.")
												failed += 1
												time.sleep(30)
											else:
												if data['message'] == "feedback_required" or data['feedback_title'] == "Try Again Later":
													print(CRED + "[>] Rate limited #2.")
													failed += 1
													time.sleep(30)
												else:
													if data['message'] == "checkpoint_required":
														print(CRED+ "[>] Rate limited #3. (Account might be locked)")
														failed += 1
														time.sleep(30)
							except:
								print(CRED + "[>] Unknown response from Instagram.")
						else:
							pass
					except:
						print(CRED + "[>] Something went wrong while claiming username.")
					
					time.sleep(delay)


def get_files():
    files = []
    for i in os.listdir('cookies'):
        files.append(os.path.join(os.getcwd(), 'cookies', i))
    return files

# Multi-thread depending on how many accounts we have (Turbo Option)
def multithread():
	print("")

	files = get_files()
	if len(files) <= 0:
		print("Could not locate any accounts/cookies. Please sign into them first!")
	else:
		delay = input("[>] Delay per request in seconds: ")
		timeout = input("[>] Request timeout in seconds: ")
		threads = input("[>] Threads to open: ")
		#files = os.listdir('cookies/')
		for x in range(int(threads)):
			th = threading.Thread(target=loadContents, args=("1", int(delay), int(timeout)))
			th.start()
		th.join()

#######################################################################

###############
# NEW SWAPPER #
###############

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
def verifyaccount(username, type):
	with open("cookies/" + username + ".txt", 'r') as f:
		for line in f:
			csrf = find_between(line, "csrftoken=", " for")
			mid = find_between(line, "mid=", " for")
			ds_user_id = find_between(line, "ds_user_id=", " for")
			sessionid = find_between(line, "sessionid=", " for")

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

		if useproxy[0] == "1":
			proxy = { "http" : "http://" + getproxy('proxies.txt') }
		else:
			proxy = { "http" : getproxy('proxies.txt')  }

		url = "https://www.instagram.com/accounts/edit/"

		while True:
			try:
				grab = requests.get(url, headers=getheaders, timeout=10, proxies=proxy)
				if not grab.text:
					pass
				else:
					break
			except requests.ConnectionError:
				print("[>] Connection timed out. Proxy is probably bad.")
				return


		first_response = grab.content
		biography = find_between(str(first_response), '{"biography":"', '",')
		firstname = find_between(str(first_response), '"first_name":"', '",')
		email = find_between(str(first_response), '"email":"', '",')
		phone = find_between(str(first_response), '"phone_number":"', '",')
		firstname = unescape(firstname)

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
def changeusername1(username, newusername, type):

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
		print(CRED+"[>] Something did not match with function: changeusername1")

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
		print(YELLOW+"[>] Releasing " + username + " to " + newusername)
	else:
		print(YELLOW+"[>] Swapping " + username + " to " + newusername)

	fixstring = builtstring.replace("&username=" + username, "&username=" + newusername)

	while True:

		try:
			if claimed[0] == "1":
				print(CGREEN + "[>] Closed because we swapped " + fileName + " successfully.")
				return;
		except:
			pass

		if useproxy[0] == "1":
			proxy = { "http" : "http://" + getproxy('proxies.txt') }
		else:
			proxy = { "http" : getproxy('proxies.txt')  }

		url = "https://www.instagram.com/accounts/edit/"

		while True:
			try:
				send = requests.post(url, data = fixstring, headers=postheaders, timeout=10, proxies=proxy)
				if not send.text:
					pass
				else:
					break
			except requests.ConnectionError:
				print("[>] Connection timed out. Proxy is probably bad.")
				return

		second_response = str(send.content)
		second_response = second_response.replace("b'", "");
		second_response = second_response.replace('\\', "");
		second_response = second_response[:-1]

		try:
			if "Something is wrong." in second_response:
				logtofile("instagram_error_3.txt", second_response)
				print(CRED + "[>] Instagram said something was wrong and to try again.")
				break;
		except:
			pass

		data = json.loads(str(second_response))

		# Limiting how many times to attempt to claim username
		try:
			if type == "2":
				if times_attempted > 15:
					print(CRED+ "[!] We attempted over 15 times to swap and couldn't. Account is most likely on a 14 day.")
					claimedfail.append("1")
					break;
		except:
			pass

		# Success
		try:
			if data['status'] == "ok":
				print(CGREEN + "[>] Successfully changed name to " + newusername)
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
		firstaccountusername = input(YELLOW+"[>] Enter username to the first account that are releasing the username from: ")
		randomusername = input(YELLOW+"[>] Enter username to change this first account to: ")
		secondaccountusername = input(YELLOW+"[>] Enter username to the second account that will claim the username: ")
	else:
		while True:
			try:
				username_1 = input(YELLOW+ "[>] Enter username:pass to the first account that will be releasing the username: ")
				username1 = username_1.split(':')[0]
				password1 = username_1.split(':')[1]
				logintofirst = login(username1, password1)
				if logintofirst == "1":
					break;
				else:
					print(CRED+"[>] Error with logging in to the first account. Let's try again.")
			except:
				print(CRED+"[>] Error #2 with logging in to the first account. Let's try again.")
		while True:
			try: 
				username_2 = input(YELLOW + "\n[>] Enter username:pass to the second account that will be claiming the username: ")
				username2 = username_2.split(':')[0]
				password2 = username_2.split(':')[1]
				logintofirst = login(username2, password2)
				if logintofirst == "1":
					break;
				else:
					print(CRED+"\n[>] Error with logging in to the second account. Let's try again.")
			except:
				print(CRED+"[>] Error #2 with logging in to the second account. Let's try again.")
		randomusername = input(YELLOW+"\n[>] Enter username to change this first account to: ")
		firstaccountusername = username1
		secondaccountusername = username2


	times = 1
	while True:
		if times == 1:
			print(YELLOW + "[>] Checking first account.")
			checkfirstaccount = verifyaccount(firstaccountusername, times)
			if checkfirstaccount == True:
				firstaccount = True
			else:
				firstaccount = False
		else:
			if times == 2:
				print(YELLOW + "[>] Checking second account.")
				checksecondaccount = verifyaccount(secondaccountusername, times)
				if checksecondaccount == True:
					secondaccount = True
				else:
					secondaccount = False
			else:
				break;
		times += 1

	if firstaccount == True and secondaccount == True:
		print(CGREEN+"[>] Both accounts are good to use.")
		print("")

		# It will sleep for 1 second before releasing the username so claimer can get a headstart!
		for x in range(int(1)):
			th = threading.Thread(target=changeusername1, args=(firstaccountusername, randomusername, "1"))
			th.start()
		th.join()

		# Multi thread 
		for x in range(int(3)):
			th = threading.Thread(target=changeusername1, args=(secondaccountusername, firstaccountusername, "2"))
			th.start()
		th.join()

		# Checking if the swap was a success or fail
		try:
			while True:
				if claimedfail[0] == "1":
					print(CRED + "[!] Claiming original username has failed, reverting back to the original name on first account.")
					for x in range(int(1)):
						th = threading.Thread(target=changeusername1, args=(firstaccountusername, firstaccountusername, "1"))
						th.start()
					th.join()
					break;
				else:
					if claimedfail[0] == "0":
						print(CGREEN + "[>] Everything looks good. Closing.")
						break;
					else:
						pass
		except:
			pass

	else:
		print(CRED+"[>] One of the accounts are not good to use.")
		print(YELLOW+"[>] First account ready: " + str(firstaccount))
		print(YELLOW+"[>] Second account ready: " + str(secondaccount))
	exit()

############################
#        END SWAPER        #
############################


# __MAIN__
header()

question = input(YELLOW + "[>] Would you like to use proxies from proxies.txt? (Y/N): ")
if question == "y" or question == "Y":
	useproxy.append("1")
	print("[>] Proxies being used.\n")
else:
	useproxy.append("0")
	print("[>] Proxies not being used.\n")

mode = input(YELLOW + "[>] Please choose one of the following\n[>] 1 = Turbo\n[>] 2 = Swapper\n[>] 3 = Login to Accounts (If you haven't done this before or it's been a while)\n[>] Selection: ")
if mode == "1":
	multithread()
else:
	if mode == "2":
		print("")
		swapper()
	else:
		if mode == "3":
			os.system("cls")
			header()
			logintotheaccounts()
exit()
