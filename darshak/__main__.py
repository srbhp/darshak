from PyQt5 import QtCore, QtWidgets
import os
import sys

# local package
from darshak.viewer import Pdf_Widget

usage = "Usage: darshak <filename>"


def main():
    app = QtWidgets.QApplication(sys.argv)
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    # app.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    # use highdpi icons
    app.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        # Ask for filename or open a file chooser
        #
        print(usage)
        filename = "sample.pdf"
        # filename = QtWidgets.QFileDialog.getOpenFileName(
        #    None, "Open PDF", "", "PDF files (*.pdf)")[0]
        print(filename)
    w = Pdf_Widget(filename)
    w.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
