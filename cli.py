
import os
from sys import platform
from scripts.portscan import port
from scripts.os_scan import check_os

t = input ("Target:")
ps = input("Starting port: ")
pe = input("End port: ")
x = 0

os_scan = input("Enable OS Scan? (y/n): ")

print ("Checking connection ...")

res = os.system(f"ping {t} " if os.name != "nt" else f"ping {t} >nul 2>&1")

if os_scan == 'y' or os_scan == 'Y':
    if res == 0:
        os_info = check_os(t)
        if os_info:
            print (f"OS Info: {os_info}")

if res == 0:
    print (f"{t} is up")
    for i in range (int(ps), int(pe) + 1):
        if port(t,i) == False:
            x += 1
        else:
            results = port(t,i)
            print ("Port", results[0], "is open", results[1])

    print ("There are ", x, "closed ports")
else:
   print("Host is down.🖕")