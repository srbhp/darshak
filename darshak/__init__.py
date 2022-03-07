from PyQt5 import QtCore, QtWidgets
from darshak import Pdf_Widget
import os
import sys

usage = "Usage: darshak.py <filename>"
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    app.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    # use highdpi icons
    app.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        # Ask for filename or open a file chooser
        #
        print(usage)
        filename = QtWidgets.QFileDialog.getOpenFileName(
            None, "Open PDF", "", "PDF files (*.pdf)")[0]
        print(filename)
    w = Pdf_Widget(filename)
    w.show()
    sys.exit(app.exec_())
