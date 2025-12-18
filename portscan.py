import nmap as nm

# target = input("Target IP:")
#pstart = int(input("Initital port: "))
#pend = int(input("Final port: "))

#scan = nm.PortScanner()

#for i in range (pstart, pend + 1):
#    out = scan.scan(target, str(i))
#    state = out['scan'][target]['tcp'][i]['state']
#    print(f'Port {i} {state}')


def scan(t, port):
    scan = nm.PortScanner()
    out = scan.scan(t, str(port))
    state = out['scan'][t]['tcp'][port]['state']
    protocol = out['scan'][t]['tcp'][port].get('name', 'unknown')
    print("Port ", port, "is ", state, ". Protocol ", protocol)

t = input ("Target:")
ps = input("Starting port: ")
pe = input("End port: ")

for i in range (int(ps), int(pe) + 1):
    scan(t,i)
