import os
import sys
import threading
import json
from PySide6 import QtWidgets, QtGui
from scripts.portscan import port
from scripts.os_scan import check_os
import nmap as nm

DEFAULT_SETTINGS = {
    "open_port_color": "#28a745",
    "closed_port_color": "#dc3545",
    "color_scheme": "Light",
    "nmap_path": "C:\\Program Files (x86)\\Nmap\\nmap.exe",
}

def _log_event(message: str):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    log_path = os.path.join(base_dir, "data", "user", "app.log")
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(message + "\n")


def get_config_path():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, "data", "user", "user_settings.json")


def ensure_config_exists():
    """Create config file with default settings if it doesn't exist or is empty"""
    config_path = get_config_path()
    os.makedirs(os.path.dirname(config_path), exist_ok=True)
    
    # Check if file exists and has content
    file_exists = os.path.exists(config_path)
    file_has_content = file_exists and os.path.getsize(config_path) > 0
    
    if not file_has_content:
        try:
            with open(config_path, "w", encoding="utf-8") as f:
                json.dump(DEFAULT_SETTINGS, f, indent=4)
            _log_event(f"Config file initialized at {config_path}")
        except Exception as e:
            print(f"✗ Error creating config file: {e}")

# Initialize config on import
ensure_config_exists()


def load_user_settings():
    settings = dict(DEFAULT_SETTINGS)
    config_path = get_config_path()

    try:
        if os.path.exists(config_path):
            with open(config_path, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if content:
                    settings.update(json.loads(content))
    except Exception as e:
        print(f"Error loading config from {config_path}: {e}")

    return settings


def save_user_settings(settings):
    config_path = get_config_path()
    os.makedirs(os.path.dirname(config_path), exist_ok=True)
    try:
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(settings, f, indent=4)
    except Exception as e:
        print(f"Error saving config to {config_path}: {e}")

def safe_port_scan(host, port_num, nmap_path=None):
    try:
        return port(host, port_num, nmap_path)
    except Exception as e:  # pragma: no cover - defensive
        return {"error": str(e)}

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.settings_data = load_user_settings()
        self.open_port_color = self.settings_data["open_port_color"]
        self.closed_port_color = self.settings_data["closed_port_color"]
        self.color_scheme = self.settings_data["color_scheme"]
        self.nmap_path = self.settings_data["nmap_path"]

        self.apply_color_scheme(self.color_scheme)
        os.environ['NMAP'] = self.nmap_path

        self.setWindowTitle("Portscanner GUI")

        self.settings = QtWidgets.QPushButton("Settings")
        self.settings.setFixedWidth(150)
        self.settings.clicked.connect(self.settings_clicked)
        self.settings_layout = QtWidgets.QVBoxLayout()
        self.settings_layout.addWidget(self.settings)
       
        
        # IP input section
        self.ip_label = QtWidgets.QLabel("Host IP")
        self.ip_input = QtWidgets.QLineEdit()
        self.ip_input.setFixedWidth(150)
        self.ip_input.setPlaceholderText("IP address (e.g, 0.0.0.0)")
        
        self.ip_layout = QtWidgets.QHBoxLayout()
        self.ip_layout.addWidget(self.ip_label)
        self.ip_layout.addWidget(self.ip_input)
        
        # Port input section
        self.s_port_label = QtWidgets.QLabel("Start Port")
        self.s_port_input = QtWidgets.QLineEdit()
        self.s_port_input.setFixedWidth(150)
        self.s_port_input.setPlaceholderText("Enter start port")
        
        self.s_port_layout = QtWidgets.QHBoxLayout()
        self.s_port_layout.addWidget(self.s_port_label)
        self.s_port_layout.addWidget(self.s_port_input)

        # End port input section
        self.e_port_label = QtWidgets.QLabel("End Port")
        self.e_port_input = QtWidgets.QLineEdit()
        self.e_port_input.setFixedWidth(150)
        self.e_port_input.setPlaceholderText("Enter end port")
        
        self.e_port_layout = QtWidgets.QHBoxLayout()
        self.e_port_layout.addWidget(self.e_port_label)
        self.e_port_layout.addWidget(self.e_port_input)

        # Os scan checkbox

        self.os_scan_checkbox = QtWidgets.QCheckBox("Enable OS Scan")
        self.os_scan_checkbox.setChecked(False)

        
        # Run button
        self.run = QtWidgets.QPushButton("Run")
        self.run.setFixedWidth(150)
        self.run.clicked.connect(self.start_scan)

        # Output field
        self.output_field = QtWidgets.QTextEdit()
        self.output_field.setReadOnly(True)
        self.output_field.setPlaceholderText("Output will be displayed here...")
        self.output_field.setFont(QtGui.QFont("Courier", 10))

        controls_layout = QtWidgets.QVBoxLayout()
        controls_layout.addLayout(self.settings_layout)
        controls_layout.addLayout(self.ip_layout)
        controls_layout.addLayout(self.s_port_layout)
        controls_layout.addLayout(self.e_port_layout)
        controls_layout.addWidget(self.os_scan_checkbox)
        controls_layout.addWidget(self.run)
        controls_layout.addStretch()

        main_layout = QtWidgets.QHBoxLayout(self)
        main_layout.addLayout(controls_layout)
        main_layout.addWidget(self.output_field, 1)

    def settings_clicked(self):
        settings_window = QtWidgets.QDialog(self)
        settings_window.setWindowTitle("Settings")
        settings_window.setFixedSize(300, 200)

        layout = QtWidgets.QVBoxLayout()
        
        nmap_path_label = QtWidgets.QLabel("Nmap Executable Path:")
        layout.addWidget(nmap_path_label)
        nmap_path_input = QtWidgets.QLineEdit()
        nmap_path_input.setText(self.nmap_path)
        layout.addWidget(nmap_path_input)

        color_scheme_label = QtWidgets.QLabel("Color Scheme:")
        layout.addWidget(color_scheme_label)
        color_scheme_input = QtWidgets.QComboBox()
        color_scheme_input.addItems(["Light", "Dark"])
        color_scheme_input.setCurrentText(self.color_scheme)
        layout.addWidget(color_scheme_input)

        adv_color_set = QtWidgets.QPushButton("Open Advanced Color Settings")
        adv_color_set.clicked.connect(self.advanced_color_settings)
        layout.addWidget(adv_color_set)

        layout.addStretch()
        save_button = QtWidgets.QPushButton("Save")
        save_button.clicked.connect(lambda: self.save(color_scheme_input, settings_window, nmap_path_input))
        layout.addWidget(save_button)

        settings_window.setLayout(layout)
        settings_window.exec()

    def advanced_color_settings(self):
        advanced_color_window = QtWidgets.QDialog(self)
        advanced_color_window.setWindowTitle("Advanced Color Settings")
        advanced_color_window.setFixedSize(400, 300)

        closed_port_label = QtWidgets.QLabel("Closed Port Color (Hex):")
        closed_port_input = QtWidgets.QLineEdit()
        closed_port_input.setText(self.closed_port_color)
        
        open_port_label = QtWidgets.QLabel("Open Port Color (Hex):")
        open_port_input = QtWidgets.QLineEdit()
        open_port_input.setText(self.open_port_color)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(closed_port_label)
        layout.addWidget(closed_port_input)
        layout.addWidget(open_port_label)
        layout.addWidget(open_port_input)
        layout.addStretch()
        save_button = QtWidgets.QPushButton("Save")
        save_button.clicked.connect(
            lambda: self.save_colors(advanced_color_window, open_port_input, closed_port_input)
        )
        layout.addWidget(save_button)
        advanced_color_window.setLayout(layout)
        advanced_color_window.exec()


    @staticmethod
    def _normalize_color(value, fallback):
        text = value.strip()
        if text.startswith('#') and len(text) == 7:
            return text
        return fallback


    def save_colors(self, dialog, open_input, closed_input):
        self.open_port_color = self._normalize_color(open_input.text(), self.open_port_color)
        self.closed_port_color = self._normalize_color(closed_input.text(), self.closed_port_color)

        self.settings_data.update(
            {
                "open_port_color": self.open_port_color,
                "closed_port_color": self.closed_port_color,
                "color_scheme": self.color_scheme,
                "nmap_path": self.nmap_path,
            }
        )
        save_user_settings(self.settings_data)
        dialog.close()


    def save(self, color_scheme_input, settings_window, nmap_path_input):
        selected_scheme = color_scheme_input.currentText()
        self.apply_color_scheme(selected_scheme)
        self.color_scheme = selected_scheme

        self.nmap_path = nmap_path_input.text()
        os.environ['NMAP'] = self.nmap_path

        self.settings_data.update(
            {
                "open_port_color": self.open_port_color,
                "closed_port_color": self.closed_port_color,
                "color_scheme": self.color_scheme,
                "nmap_path": self.nmap_path,
            }
        )
        save_user_settings(self.settings_data)

        settings_window.close()


    def apply_color_scheme(self, scheme):
        if scheme == "Dark":
            app.setStyleSheet("QWidget { background-color: #2b2b2b; color: #f0f0f0; }")
        else:
            app.setStyleSheet("QWidget { background-color: #ffffff; color: #000000; }")
        

       



    def start_scan(self):
        self.output_field.clear()
        threading.Thread(target=self.scan_ports).start()

    def scan_ports(self):
        host = self.ip_input.text()
        start_port = self.s_port_input.text()
        end_port = self.e_port_input.text()
        closed_ports = 0

        if not host or not start_port.isdigit() or not end_port.isdigit():
            self.output_field.append("Please enter valid host and port numbers.")
            return
        start_port = int(start_port)
        end_port = int(end_port)

        self.output_field.append("Checking connection ...")
        res = os.system(f"ping {host}" if os.name != "nt" else f"ping {host} >nul 2>&1")

        if res == 0:
            self.output_field.append("<span style='background-color: green; color: white;'>"+f"{host} is up"+"</span>")
            if self.os_scan_checkbox.isChecked():
                os_info = check_os(host, self.nmap_path)
                if os_info:
                    if os_info == "Linux":
                        os_info += " 🐧"
                    elif os_info == "Windows":
                        os_info += " 🪟"
                    elif os_info == "macOS" or os_info == "Mac OS" or os_info == "Macintosh" or os_info == "iOS":
                        os_info += " 🍎"
                    self.output_field.append(f"Operating System: {os_info}")
                else:
                    self.output_field.append("Operating System: Unknown")
            for port_num in range(start_port, end_port + 1):
                results = safe_port_scan(host, port_num, self.nmap_path)
                if isinstance(results, dict) and "error" in results:
                    self.output_field.append(f"<span style='background-color: red; color: white;'>Error scanning port {port_num}: {results['error']}</span>")
                    continue
                if results is False:
                    closed_ports += 1
                else:
                    self.output_field.append(f"<span style = 'background-color: {self.open_port_color}; color: white;'>Port {results[0]} is open</span> <span style = 'background-color: black; color: white;'> {results[1]} </span>")
            self.output_field.append(f"<span style='background-color: {self.closed_port_color}; color: white;'>There are {closed_ports} closed ports</span>")
        else:
            self.output_field.append("<span style='background-color: red; color: white;'>Host is down.🖕</span>")

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.resize(600, 450)
    widget.show()

    sys.exit(app.exec())