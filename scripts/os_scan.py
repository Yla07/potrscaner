import os
import nmap as nm


def check_os(target, nmap_path=None):
    """Attempt OS detection. Returns family string or None on failure."""
    env_nmap = nmap_path or os.environ.get('NMAP')
    search_path = (env_nmap,) if env_nmap else None

    try:
        scanner = nm.PortScanner(nmap_search_path=search_path)
    except nm.PortScannerError as e:
        print(f"OS scan skipped: nmap not available ({e})")
        return None
    except Exception as e:  # pragma: no cover - defensive
        print(f"OS scan skipped: {e}")
        return None

    try:
        scanner.scan(target, arguments='-O')
    except nm.PortScannerError as e:
        print(f"OS scan failed: {e}")
        return None
    except Exception as e:  # pragma: no cover - defensive
        print(f"OS scan failed: {e}")
        return None

    if target not in scanner.all_hosts():
        print("OS scan failed: host not found in results")
        return None

    osmatches = scanner[target].get('osmatch') or []
    if osmatches and osmatches[0].get('osclass'):
        return osmatches[0]['osclass'][0].get('osfamily')
    return None