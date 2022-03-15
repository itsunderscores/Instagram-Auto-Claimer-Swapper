## Instagram Turbo / Auto Claimer / Swapper
Version: **3.2**<br>
Last Update: **03/14/2022**<br>
<hr>

Run
```
python main.py
```

I have recoded the entire tool to make it work a thousand times better.<br>
Use this at your own descretion. I've only used this on test accounts and nothing high-end. Although, it should get the job done.<br>

<hr>

Auto Claimer/Turbo Example: https://youtu.be/fjr4wn9BY7k<br>
Swapper Example: https://www.youtube.com/watch?v=Kig-mcNS_Z0

Proxies are required for this to work properly. **Rotating and Residential are recommended.** <br>
I will keep the <a target="_blank" href="https://raw.githubusercontent.com/itsunderscores/Instagram-Auto-Claimer-Swapper/main/files/proxies.txt">proxies</a> file updated with fresh proxies for those who don't have access HQ proxies.<br>
Before swapping a high-end account, ensure it is working with throwaway accounts first.

If you need helping swapping or cannot get this **simple** program working. Feel free to contact me.<br>
https://discord.gg/vG5Rz9dASx

<hr>

**Features**
- Multi-threading<br>
- Proxy Supported
- Autoclaimer/Turbo
- Account Swapper
- FREE!

<hr>

**Change Log**: 03/14/21 v3
- Multi-threaded Login, checks all accounts in seconds
- Fixed proxies (sometimes did not use them)
- Added more login checks, proxy fixed, logs to file which accounts work/failed
- Turbo has been improved (Proxy Fixed)
- Swapper has been improved (Proxy Fixed)
- If swap is unsuccessful, original username will be reverted back
- Automatically installs pip requirements if you've never ran the program before

**Change Log**: 12/14/21 v2.5
- Option to use proxies added. (Recommended to use proxies when Turbo/Autoclaiming)
- Multiple bug fixes with login

**Change Log**: 12/13/21 v2.3
- Turbo/Autoclaimer will continue claiming (if enough accounts are loaded) after it has claimed a username already.
- Swapper has been updated in various ways.
- If the swap is unsuccessful due to 14 day, or other Instagram blocks, the original username will be reverted back.
- Faster swaps and increased realiblity
- Multiple proxies are now supported. Place proxies in **files/proxies.txt**
- Swapper is now multi-threaded and claims faster
- Autoclaimer/Turbo has been fixed, had a bug
- Detects certain error messages while logging in

<hr>

**First Mode (Auto Claimer/Turbo)**<br>
Turbo/Auto-claim list of username(s).

* I recommend buying fresh accounts and using around 50+ accounts.
* Do not use more threads than accounts
* Good delay per request is 3
* Good timeout per request is 5

1) Put your login accounts in file **files/accounts.txt** in USERNAME:PASSWORD format, and choose option 4 before continuing.

2) It will go through the list of usernames in file **files/turbo_usernames.txt** and will see if the name is available.

<hr>

**Second Mode (Swapper)**<br>
Mainly used to swap a username over to another account.

It will ask for the login of the first account that will be releasing the username. Then it'll ask for the second account login that will claim the username. Once it has verified that both accounts are working and eligble to transfer, it will swap them.

<hr>

**Third Mode (Target Handle)**<br>
Used to target a specific handle, good for swapping a handle onto a fresh account.<br>
Make sure you are using fresh proxies for this to work.

1) Put your login accounts in file **files/accounts.txt** in USERNAME:PASSWORD format, and choose option 4 before continuing.

2) Place accounts from /accounts/ in /turbo_claim/ that will claim the desired handle.

<hr>

**Fourth Mode (Login to accounts)**<br>
Grab required cookies from accounts in **files/accounts.txt** (This is required for the first mode.)
