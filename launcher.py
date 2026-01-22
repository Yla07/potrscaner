from scripts.os_scan import check_os
from scripts.portscan import port
import os 
import sys

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
