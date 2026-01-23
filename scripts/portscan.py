import os
import nmap as nm


def port(target, port_num, nmap_path=None):
    """Scan a single TCP port. Returns [port, service] when open, False when closed, or {"error": msg} on failure."""
    env_nmap = nmap_path or os.environ.get('NMAP')
    search_path = (env_nmap,) if env_nmap else None

    try:
        scanner = nm.PortScanner(nmap_search_path=search_path)
    except nm.PortScannerError as e:
        return {"error": f"nmap not available: {e}"}
    except Exception as e:  # pragma: no cover - defensive
        return {"error": str(e)}

    try:
        out = scanner.scan(target, str(port_num))
    except nm.PortScannerError as e:
        return {"error": f"scan failed: {e}"}
    except Exception as e:  # pragma: no cover - defensive
        return {"error": str(e)}

    host_data = out.get('scan', {}).get(target)
    if not host_data:
        return {"error": "host not found"}

    tcp_data = host_data.get('tcp', {})
    if port_num not in tcp_data:
        return False

    state = tcp_data[port_num].get('state')
    protocol = tcp_data[port_num].get('name', 'unknown')
    if state == "open":
        return [port_num, protocol]
    return False







