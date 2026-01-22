
import os
from sys import platform
from portscan import port
t = input ("Target:")
ps = input("Starting port: ")
pe = input("End port: ")
x = 0

print ("Checking connection ...")

res = os.system(f"ping {t} " if os.name != "nt" else f"ping {t} >nul 2>&1")

if res == 0:
    print (f"{t} is up")
    for i in range (int(ps), int(pe) + 1):
        if port(t,i) == False:
            x += 1
            print ("closed")
        else:
            results = port(t,i)
            print (results)

    print ("There are ", x, "closed ports")
else:
   print("Host is down.🖕")