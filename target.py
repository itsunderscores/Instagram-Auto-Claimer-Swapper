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

claimed = []
def start(account, target, delay, proxy):
	with open(account, 'r') as f:
		for line in f:
			csrf = functions.find_between(line, "csrftoken=", " for")
			mid = functions.find_between(line, "mid=", " for")
			ds_user_id = functions.find_between(line, "ds_user_id=", " for")
			sessionid = functions.find_between(line, "sessionid=", " for")

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

	if proxy == "true":
		proxy = { "http" : "http://" + functions.getproxy('files/proxies.txt'), "https": "http://" + functions.getproxy('files/proxies.txt')  }
	else:
		proxy = { "http" : ""  }

	while True:
		try:
			grab = requests.get("https://www.instagram.com/accounts/edit/", headers=getheaders, timeout=10, proxies=proxy)
			if not grab.text:
				pass
			else:
				break
		except requests.ConnectionError:
			print("[>] Connection timed out. Proxy is probably bad.")
			return

	first_response = grab.content
	biography = functions.find_between(str(first_response), '{"biography":"', '",')
	firstname = functions.find_between(str(first_response), '"first_name":"', '",')
	email = functions.find_between(str(first_response), '"email":"', '",')
	phone = functions.find_between(str(first_response), '"phone_number":"', '",')
	firstname = functions.unescape(firstname)
	biography = functions.unescape(biography)
	firstname = ""
	biography = ""

	if not email:
		print(functions.CRED + "[!] Something went wrong while loading account, make sure the account is still valid: " + account)
		return
	else:
		print(functions.CGREEN + "[>] Loaded Account: " + account)

	attempts = 0
	failed = 0
	while True:
		if not claimed:
			if failed > 20:
				print(functions.CRED + "[>] Closing thread due to 20 failed attempts.")
				return
			else:
				time.sleep(int(delay))
				data = 'first_name=' + firstname + '&email=' + urllib.parse.quote(email) + '&username=' + target + '&phone_number=' + urllib.parse.quote(phone) + '&biography=' + urllib.parse.quote(biography) + '&external_url=&chaining_enabled=on'
				try:
					send = requests.post("https://www.instagram.com/accounts/edit/", data = data, timeout=10, headers=postheaders, proxies=proxy)
					attempts += 1
				except requests.ConnectionError:
					failed += 1
					print("[>] Connection timed out.")

				try:
					if not send.text:
						failed += 1
						print(functions.CRED + "[>] Something went wrong getting data from Instagram, retrying")
					else:
						pass
				except:
					pass

				try:
					if "Something is wrong." in send.text:
						failed += 1
						print(functions.CRED + "[>] Instagram said something was wrong and to try again.")
						time.sleep(60)
				except:
					pass

				try:
					data = json.loads(send.text)
					if data['status'] == "ok":
						print(functions.CGREEN + "[>] Successfully claimed username: " + target + " on account: " + account + " [Attempts: " + str(attempts) + "]")
						claimed.append(target)
						functions.logtofile("success_target_" + target + ".txt", account + " > " + target)
						functions.discordwebbook("Target", account, target)
						return
						break
					else:
						if data['message']['errors'][0] == "This username isn't available. Please try another.":
							failed += 1
							print(functions.CRED + "[>] %s is not available." % (target))
						else:
							if data['status'] == "fail":
								failed += 1
								print(functions.CRED + "[>] Instagram returned fail.")
							else:
								if data['message'] == "Please wait a few minutes before you try again.":
									failed += 1
									print(functions.CRED + "[>] Rate limited.")
									time.sleep(30)
								else:
									if data['message'] == "feedback_required" or data['feedback_title'] == "Try Again Later":
										failed += 1
										print(functions.CRED + "[>] Rate limited #2.")
										time.sleep(30)
									else:
										if data['message'] == "checkpoint_required":
											failed += 1
											print(functions.CRED+ "[>] Rate limited #3. (Account might be locked)")
											time.sleep(30)
				except:
					failed += 1
					print(functions.CRED + "[>] Unknown response from Instagram.")
		else:
			#print(functions.CGREEN + "[>] %s has been claimed." % (target))
			return

def target():
	print(functions.CYAN + "\n[!] This will use all the accounts in /turbo_claim/ to claim the desired handle.")
	print(functions.CYAN + "[!] This option requires proxy, please fill /files/proxies.txt with fresh proxies.")
	question = input(functions.YELLOW + "\n[>] Are the accounts in /turbo_claim/? (Y/N) ")
	if question == "y" or question == "Y":
		check_files = functions.get_files("turbo_claim")
		if len(check_files) >= 1:
			target = input(functions.YELLOW + "[>] What is the handle you want to target: ")
			delay = input(functions.YELLOW + "[>] Delay per request: ")

			for filename in os.listdir("turbo_claim"):
				f = os.path.join("turbo_claim", filename)
				if os.path.isfile(f):
				    th = threading.Thread(target=start, args=(f, target, delay, "true"))
				    th.start()
		else:
			print(functions.CRED + "[!] Could not locate any accounts in /turbo_claim/. Fill folder up and try again")
	else:
		print(functions.CRED + "[!] Fill folder up, then come back.")