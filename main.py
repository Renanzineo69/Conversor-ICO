import sys
from PyQt5.QtWidgets import QApplication
from ui.interface import ImageConverterApp

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageConverterApp()
    window.show()
    sys.exit(app.exec_())
