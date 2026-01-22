import os
import sys
import threading
from portscan import port
from os_scan import check_os
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
        
        # IP input section
        self.ip_label = QtWidgets.QLabel("Host IP")
        self.ip_input = QtWidgets.QLineEdit()
        self.ip_input.setFixedWidth(150)
        self.ip_input.setPlaceholderText("Enter host or IP address")
        
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
        controls_layout.addLayout(self.ip_layout)
        controls_layout.addLayout(self.s_port_layout)
        controls_layout.addLayout(self.e_port_layout)
        controls_layout.addWidget(self.os_scan_checkbox)
        controls_layout.addWidget(self.run)
        controls_layout.addStretch()

        main_layout = QtWidgets.QHBoxLayout(self)
        main_layout.addLayout(controls_layout)
        main_layout.addWidget(self.output_field, 1)

       



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