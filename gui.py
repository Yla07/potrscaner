import os
import sys
import threading
from scripts.portscan import port
from scripts.os_scan import check_os
from PySide6 import QtWidgets, QtGui

def safe_port_scan(host, port_num):
    try:
        return port(host, port_num)  # Indicate success
    except Exception as e:
        return False  # Indicate failure

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

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
        pass  # Placeholder for settings functionality
        print("Settings clicked")
        settings_window = QtWidgets.QDialog(self)
        settings_window.setWindowTitle("Settings")
        settings_window.setFixedSize(300, 200)

        layout = QtWidgets.QVBoxLayout()
        
        nmap_path_label = QtWidgets.QLabel("Nmap Executable Path:")
        layout.addWidget(nmap_path_label)
        nmap_path_input = QtWidgets.QLineEdit()
        nmap_path_input.setText(os.getenv('NMAP', 'C:\\Program Files (x86)\\Nmap\\nmap.exe'))
        layout.addWidget(nmap_path_input)

        color_scheme_label = QtWidgets.QLabel("Color Scheme:")
        layout.addWidget(color_scheme_label)
        color_scheme_input = QtWidgets.QComboBox()
        color_scheme_input.addItems(["Light", "Dark"])
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
        print("Advanced Color Settings clicked")
        advanced_color_window = QtWidgets.QDialog(self)
        advanced_color_window.setWindowTitle("Advanced Color Settings")
        advanced_color_window.setFixedSize(400, 300)

        closed_port_label = QtWidgets.QLabel("Closed Port Color (Hex):")
        closed_port_input = QtWidgets.QLineEdit()
        
        open_port_label = QtWidgets.QLabel("Open Port Color (Hex):")
        open_port_input = QtWidgets.QLineEdit()

        os_icons = QtWidgets.QCheckBox("Enable OS Icons")
        os_icons.setChecked(True)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(closed_port_label)
        layout.addWidget(closed_port_input)
        layout.addWidget(open_port_label)
        layout.addWidget(open_port_input)
        layout.addWidget(os_icons)
        layout.addStretch()
        save_button = QtWidgets.QPushButton("Save")
        save_button.clicked.connect(advanced_color_window.close)
        layout.addWidget(save_button)
        advanced_color_window.setLayout(layout)
        advanced_color_window.exec()


    def save(self, color_scheme_input, settings_window, nmap_path_input):
        selected_scheme = color_scheme_input.currentText()
        print(f"Selected color scheme: {selected_scheme}")

        if selected_scheme == "Dark":
            app.setStyleSheet("QWidget { background-color: #2b2b2b; color: #f0f0f0; }")
        if selected_scheme == "Light":
            app.setStyleSheet("")

        os.environ['NMAP'] = nmap_path_input.text()
        
        print(f"Nmap path set to: {os.environ['NMAP']}")
        
        settings_window.close()
        

       



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
                os_info = check_os(host)
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
                results = safe_port_scan(host, port_num)
                if results == False:
                    closed_ports += 1
                else:
                    self.output_field.append("<span style = 'background-color: #0f752a; color: white;'>Port "+str(results[0])+" is open</span> <span style = 'background-color: black; color: white;'> "+str(results[1])+" </span>")
            self.output_field.append(f"There are {closed_ports} closed ports")
        else:
            self.output_field.append("<span style='background-color: red; color: white;'>Host is down.🖕</span>")

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.resize(600, 450)
    widget.show()

    sys.exit(app.exec())