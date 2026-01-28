
import os
import json
from scripts.portscan import port
from scripts.os_scan import check_os
import nmap as nm

DEFAULT_SETTINGS = {
    "open_port_color": "#28a745",
    "closed_port_color": "#dc3545",
    "color_scheme": "Light",
    "nmap_path": "C:\\Program Files (x86)\\Nmap\\nmap.exe",
}


def initialize_settings():
    """Ensure user settings file exists with defaults."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(base_dir, "data", "user", "user_settings.json")

    os.makedirs(os.path.dirname(config_path), exist_ok=True)
    file_has_content = os.path.exists(config_path) and os.path.getsize(config_path) > 0

    if not file_has_content:
        try:
            with open(config_path, "w", encoding="utf-8") as f:
                json.dump(DEFAULT_SETTINGS, f, indent=4)
            print(f"✓ Config file initialized at {config_path}")
        except Exception as e:
            print(f"✗ Error creating config file: {e}")


def load_user_settings():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(base_dir, "data", "user", "user_settings.json")
    settings = dict(DEFAULT_SETTINGS)
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if content:
                settings.update(json.loads(content))
    except Exception as e:
        print(f"✗ Error loading config file: {e}")
    return settings


initialize_settings()
settings = load_user_settings()
os.environ["NMAP"] = settings.get("nmap_path", DEFAULT_SETTINGS["nmap_path"])

t = input ("Target:")
ps = input("Starting port: ")
pe = input("End port: ")
x = 0

os_scan = input("Enable OS Scan? (y/n): ")

print ("Checking connection ...")

res = os.system(f"ping {t} " if os.name != "nt" else f"ping {t} >nul 2>&1")

if os_scan == 'y' or os_scan == 'Y':
    if res == 0:
        os_info = check_os(t, settings.get("nmap_path"))
        if os_info:
            print (f"OS Info: {os_info}")

if res == 0:
    print (f"{t} is up")
    for i in range (int(ps), int(pe) + 1):
        result = port(t, i, settings.get("nmap_path"))
        if isinstance(result, dict) and "error" in result:
            print(f"Error scanning port {i}: {result['error']}")
            continue
        if result is False:
            x += 1
        else:
            print ("Port", result[0], "is open", result[1])

    print ("There are ", x, "closed ports")
else:
   print("Host is down.🖕")