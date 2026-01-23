import os 
import sys
import json

# Initialize user settings before any GUI imports
def initialize_settings():
    """Initialize user settings before app startup"""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(base_dir, "data", "user", "user_settings.json")
    
    default_settings = {
        "open_port_color": "#28a745",
        "closed_port_color": "#dc3545",
        "color_scheme": "Light",
        "nmap_path": "C:\\Program Files (x86)\\Nmap\\nmap.exe",
    }
    
    os.makedirs(os.path.dirname(config_path), exist_ok=True)
    
    # Check if file exists and has content
    file_has_content = os.path.exists(config_path) and os.path.getsize(config_path) > 0
    
    if not file_has_content:
        try:
            with open(config_path, "w", encoding="utf-8") as f:
                json.dump(default_settings, f, indent=4)
            print(f"✓ Config file initialized at {config_path}")
        except Exception as e:
            print(f"✗ Error creating config file: {e}")

initialize_settings()

from scripts.os_scan import check_os
from scripts.portscan import port

try:
    from PySide6 import QtWidgets, QtGui
except ImportError:
    try: 
        os.system("pip install PySide6")
        from PySide6 import QtWidgets, QtGui
    except ImportError:
        os.system("python -m venv .venv")
        os.system(".venv\\Scripts\\pip install PySide6")
        from PySide6 import QtWidgets, QtGui

class launcher(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Portscanner Launcher")
        self.setFixedWidth(300)
        self.layout = QtWidgets.QVBoxLayout()

        self.welcome_label = QtWidgets.QLabel("Welcome to Portscanner <br> Lets get you started!")
        self.welcome_label.setAlignment(QtGui.Qt.AlignCenter)
        self.layout.addWidget(self.welcome_label)

        self.path_label = QtWidgets.QLabel("Select your Nmap Path:")
        self.path_label.setAlignment(QtGui.Qt.AlignCenter)
        self.layout.addWidget(self.path_label)
        self.path_input = QtWidgets.QLineEdit()
        self.layout.addWidget(self.path_input)
        self.browse_button = QtWidgets.QPushButton("Browse")
        #self.browse_button.clicked.connect(self.browse_nmap)
        self.layout.addWidget(self.browse_button)

        self.continue_button = QtWidgets.QPushButton("Continue")
        #self.continue_button.clicked.connect()
        self.layout.addWidget(self.continue_button)
        self.setLayout(self.layout)



if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = launcher()
    widget.resize(600, 450)
    widget.show()

    sys.exit(app.exec())
