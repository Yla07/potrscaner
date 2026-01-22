import nmap as nm
import os

os.getenv('C:\\Program Files (x86)\\Nmap\\nmap.exe')


def port(t, port):
    scan = nm.PortScanner()
    out = scan.scan(t, str(port))
    
    # Check if scan returned valid results
    if t not in out['scan'] or 'tcp' not in out['scan'][t] or port not in out['scan'][t]['tcp']:
        return False
    
    state = out['scan'][t]['tcp'][port]['state']
    protocol = out['scan'][t]['tcp'][port].get('name', 'unknown')
    if state == "open":
        port_info = [port, protocol]
        return port_info
    else:
        return False







