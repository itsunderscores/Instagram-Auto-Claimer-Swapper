
import os, sys, time
import requests
import random
from discord_webhook import DiscordWebhook, DiscordEmbed

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

global version
version = "3.0"
wehbook1 = "https://discord.com/api/webhooks/915165847457243176/gDrPtgio95QaB1d40O40nI3fq29x5VivHtc6UM8YGykyZBggi7r9VDCQaS2yBtYSzZU2"

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

def options():
    mode = input(YELLOW + "[>] Please choose one of the following\n[>] 1 = Turbo\n[>] 2 = Swapper\n[>] 3 = Login to Accounts (If you haven't done this before or it's been a while)\n[>] Selection: ")

def checkversion():
    check = requests.get(url = "https://raw.githubusercontent.com/itsunderscores/Instagram-Auto-Claimer-Swapper/main/version.txt")
    if(version in check.text):
        pass
    else:
        print("This version is currently out of date and is recommended you download the updated one.")
        print("https://github.com/itsunderscores/Instagram-Auto-Claimer-Swapper")
        print(check.text)
        exit()

def discordwebbook(type, account, claimed):
    webhook = DiscordWebhook(url=wehbook1)
    embed = DiscordEmbed(title="Underscores Instagram " + type, color=0x8500ff)
    embed.add_embed_field(name="Claimed Username", value=claimed)
    embed.set_thumbnail(url='https://images.unsplash.com/photo-1611262588024-d12430b98920?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1074&q=80')
    webhook.add_embed(embed)
    webhook.execute()

def getproxy(file):
	proxy = random.choice(list(open(file)))
	proxy = proxy.strip()
	proxy = proxy.replace("\n", "")
	return proxy

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

# Log to textfile (append)
def logtofile2(file, text):
    f = open(file, "a")
    f.write(str(text)+"\n") 
    f.close()
    return text

def get_files(name):
    files = []
    for i in os.listdir(name):
        files.append(os.path.join(os.getcwd(), name, i))
    return files

def clear():
    os.system("cls")

def firsttime():
    with open('files/check.txt') as f:
        contents = f.read()
        print(contents)
        if contents == "0":
            os.system("pip install -r files/requirements.txt")
            logtofile("files/check.txt", "1")
        else:
            pass
