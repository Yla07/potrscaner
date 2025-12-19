import nmap as nm
import os
# target = input("Target IP:")
#pstart = int(input("Initital port: "))
#pend = int(input("Final port: "))

#scan = nm.PortScanner()

#for i in range (pstart, pend + 1):
#    out = scan.scan(target, str(i))
#    state = out['scan'][target]['tcp'][i]['state']
#    print(f'Port {i} {state}')


def port(t, port):
    scan = nm.PortScanner()
    out = scan.port(t, str(port))
    state = out['scan'][t]['tcp'][port]['state']
    protocol = out['scan'][t]['tcp'][port].get('name', 'unknown')
    if state == "open":
     print("Port ", port, "is open", ". Protocol ", protocol)
    else:
       return False
t = input ("Target:")
ps = input("Starting port: ")
pe = input("End port: ")
x = 0

print ("Checking connection ...")

res = os.system(f"ping {t} > /dev/null 2>&1" if os.name != "nt" else f"ping {t} >nul 2>&1")

if res == 0:
    print (f"{t} is up")
    for i in range (int(ps), int(pe) + 1):
        if port(t,i) == False:
            x+=1
        else:
            continue

    print ("There are ", x, "closed ports")
else:
   print("Host is down.🖕")





