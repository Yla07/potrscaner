import nmap as nm
import os

def check_os(t):
    os.environ['NMAP'] = r'C:\Program Files (x86)\Nmap\nmap.exe'
    scanner = nm.PortScanner()
    scanner.scan(t, arguments='-O')
    if 'osmatch' in scanner[t] and scanner[t]['osmatch']:
        if 'osclass' in scanner[t]['osmatch'][0] and scanner[t]['osmatch'][0]['osclass']:
            return scanner[t]['osmatch'][0]['osclass'][0]['osfamily']
    return None