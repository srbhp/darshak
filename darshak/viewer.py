#!/usr/bin/python3

from PyQt5 import QtCore, QtWidgets, QtGui
import popplerqt5

# local packages
from darshak.fixedARLabel import ThumbWidget
import darshak.threadedRender as threaded


class Ui_MainWindow(object):
    def __init__(self, filename, parent=None):
        self.filename = filename

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowTitle("MainWindow")
        MainWindow.resize(1200, 800)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.pdfwidget = QtWidgets.QWidget()
        # self.layout = QtWidgets.QVBoxLayout()
        # self.pdfwidget.setLayout( s)
        # QtWidgets.QScrollArea(cwidget)
        self.current_width = float(MainWindow.width())
        # dpi = MainWindow.physicalDpiX()
        # //*central.height()/sizeObject.height()
        self.doc = popplerqt5.Poppler.Document.load(self.filename)
        # doc.setRenderBackend(popplerqt5.Poppler.Document.ArthurBackend)
        self.doc.setRenderHint(popplerqt5.Poppler.Document.Antialiasing)
        self.doc.setRenderHint(popplerqt5.Poppler.Document.TextAntialiasing)
        self.doc.setRenderHint(popplerqt5.Poppler.Document.ThinLineShape)
        self.doc.setRenderHint(popplerqt5.Poppler.Document.TextHinting)
        numpages = self.doc.numPages()
        print(numpages)
        self.fullLayout = QtWidgets.QHBoxLayout()
        self.fullLayout.setContentsMargins(0, 0, 0, 0)
        self.centralwidget.setLayout(self.fullLayout)
        self.area = QtWidgets.QScrollArea()
        self.area.setWidgetResizable(True)
        self.area.setWidget(self.pdfwidget)
        self.mainPdfWidget = QtWidgets.QWidget()
        self.mainPdfLayout = QtWidgets.QVBoxLayout()
        self.mainPdfLayout.setSpacing(0)
        self.mainPdfLayout.setContentsMargins(0, 0, 0, 0)
        self.controlWidget = QtWidgets.QWidget()
        self.controlLayout = QtWidgets.QHBoxLayout()
        self.controlLayout.setContentsMargins(0, 0, 0, 0)
        self.controlWidget.setLayout(self.controlLayout)
        self.mainPdfWidget.setLayout(self.mainPdfLayout)
        self.mainPdfLayout.addWidget(self.controlWidget)
        self.mainPdfLayout.addWidget(self.area)
        # Add thumbnails
        self.thumbWidget = ThumbWidget()  # QtWidgets.QWidget()
        self.thumbArea = QtWidgets.QScrollArea()
        self.thumbArea.setWidgetResizable(True)
        self.thumbArea.setWidget(self.thumbWidget)
        self.thumbArea.setMaximumWidth(500)
        self.pbar = QtWidgets.QProgressBar()
        self.mainPdfLayout.addWidget(self.pbar)
        # self.fullLayout.addWidget(self.thumbArea)
        # self.fullLayout.addWidget(self.area)
        self.splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        self.splitter.addWidget(self.thumbArea)
        self.splitter.addWidget(self.mainPdfWidget)  # self.area)
        self.fullLayout.addWidget(self.splitter)
        # self.splitter.setSizes(
        #     [self.splitter.height() * 0.05, self.splitter.height() * 0.95]
        # )
        self.splitter.setStyleSheet("QSplitter::handle { image: none; }")
        MainWindow.setCentralWidget(self.centralwidget)
        """
        for i in range(numpages):
            page = self.doc.page(i)
            image = page.renderToImage(dpi,dpi)
            pixmap=QtGui.QPixmap.fromImage(image)
            label = QtWidgets.QLabel()
            label.setPixmap(pixmap)
            label.setScaledContents(True)
            label.setSizePolicy(QtWidgets.QSizePolicy.Fixed,
            QtWidgets.QSizePolicy.Expanding)
            self.layout.addWidget(label)
            self.layout.addStretch(1)
        """
        # area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        # area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # area.setWindowTitle(filename)
        # area.setWidget(cwidget)
        # area.show()
        # return self.area


class Pdf_Widget(QtWidgets.QMainWindow):
    resized = QtCore.pyqtSignal()
    scrollSignal = QtCore.pyqtSignal()

    def __init__(self, filename, defaultScale=2.75, parent=None):
        super(Pdf_Widget, self).__init__(parent=parent)
        self.ui = Ui_MainWindow(filename)
        self.ui.setupUi(self)

        self.numpages = self.ui.doc.numPages()
        self.ui.pbar.setMaximum(self.numpages)
        self.resized.connect(self.reRender)
        self.defaultScale = defaultScale
        self.rescaleToWidth = True
        self.threadpool = QtCore.QThreadPool()
        self.rescaleToWidth = True
        self.renderFirstpapge()

        combo = QtWidgets.QComboBox()
        combo.addItem("Fit Width")
        combo.addItem("Zoom 50%")
        combo.addItem("Zoom 100%")
        combo.addItem("Zoom 150%")
        combo.addItem("Zoom 200%")
        combo.addItem("Zoom 400%")
        combo.addItem("Zoom 800%")
        combo.currentIndexChanged.connect(self.changeZoom)
        # Add annotation Bottom
        # annotButtom = QtWidgets.QPushButton("Annotations")
        # annotButtom.setCheckable(True)
        # annotButtom.clicked.connect(self.show_annotations)
        # self.ui.controlLayout.addWidget(annotButtom)
        #
        #
        thumbButton = QtWidgets.QPushButton()
        thumbButton.setIcon(QtGui.QIcon("darshak/icons/thumbnails.svg"))

        thumbButton.setCheckable(True)
        thumbButton.clicked.connect(self.showHideThumb)
        self.statusPageNo = QtWidgets.QLineEdit()
        # self.statusPageNo.setFrameStyle(QtWidgets.QFrame.NoFrame)
        self.statusPageNo.setText("1")
        self.statusPageNo.returnPressed.connect(self.goToPage)
        self.statusPageNo.setAlignment(QtCore.Qt.AlignCenter)
        self.statusPageNo.setFixedWidth(60)
        self.ui.controlLayout.addWidget(thumbButton)
        self.ui.controlLayout.addStretch(1)
        self.ui.controlLayout.addWidget(self.statusPageNo, 1)
        self.ui.controlLayout.addWidget(
            QtWidgets.QLabel(" / {}".format(self.numpages)), 1
        )
        self.ui.controlLayout.addStretch(1)
        self.ui.controlLayout.addWidget(combo)
        self.getthumbnails()
        self.sliderBar1 = self.ui.thumbArea.verticalScrollBar()
        self.sliderBar2 = self.ui.area.verticalScrollBar()
        self.sliderBar2.valueChanged.connect(self.SyncScroll)
        self.ui.thumbWidget.clicked.connect(self.thubmClick)

    def goToPage(self):
        try:
            gopage = int(self.statusPageNo.text()) - 1  # Added 1 earlier
            loc = self.ui.pdfwidget.height() * gopage / self.numpages
            self.sliderBar2.setValue(loc)
        except Exception as e:
            print(e)
            print("Unable to go to page : \n Please eneter correct page ")

    def showHideThumb(self):
        hide_me = self.ui.splitter.widget(0)
        hide_me.setHidden(not hide_me.isHidden())

    def thubmClick(self, pos):
        print((self.sliderBar1.maximum(), 1.0 * self.sliderBar2.maximum()))
        factor = 1
        #  self.ui.pdfwidget.height() /(1.0 * self.ui.thumbWidget.height())
        self.sliderBar2.setValue(int(pos.y() * factor))

    def SyncScroll(self):
        # sliderValue = self.sliderBar2.value()
        if self.sliderBar2.maximum() == 0:
            curpage = 1
        else:
            curpage = (
                int(
                    self.numpages
                    * (self.sliderBar2.value())
                    / self.sliderBar2.maximum()
                    - 0.1
                )
                + 1
            )
        self.statusPageNo.setText("{}".format(curpage))
        # self.sliderBar1.setValue(sliderValue)

    def getthumbnails(self):
        scalefactor = 0.5
        fake_dpi = scalefactor * self.physicalDpiX()

        worker = threaded.GetAllPage(self.ui.doc, fake_dpi, True)
        self.threadpool.start(worker)
        worker.signals.finished.connect(self.add_thumblabel)

    def changeZoom(self, index):
        print(index)
        if index == 0:
            self.rescaleToWidth = True
            self.renderFirstpapge()
        if index == 1:
            self.rescaleToWidth = False
            self.renderFirstpapge(0.5)
        if index == 2:
            self.rescaleToWidth = False
            self.renderFirstpapge(1)
        if index == 3:
            self.rescaleToWidth = False
            self.renderFirstpapge(1.5)
        if index == 4:
            self.rescaleToWidth = False
            self.renderFirstpapge(2.0)
        if index == 5:
            self.rescaleToWidth = False
            self.renderFirstpapge(4.0)
        if index == 6:
            self.rescaleToWidth = False
            self.renderFirstpapge(8.0)

    """
    def wheelEvent(self, event):
        if (  self.renderPage < self.numpages -1):
            self.renderPage=self.renderPage+1
            sizeObject = QtWidgets.QDesktopWidget().screenGeometry(-1)
            fake_dpi=self.scalefactor*self.physicalDpiX()*self.width()/sizeObject.width()
            worker =threaded.getImageThread(self.ui.doc,fake_dpi,
            self.renderPage)
            self.threadpool.start( worker )
            worker.signals.finished.connect(self.add_qlabel )
            self.threadpool.waitForDone()
    """

    def clearLayout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clearLayout(item.layout())

    def contextMenuEvent(self, event):
        contextMenu = QtWidgets.QMenu(self)
        impMenu = QtWidgets.QMenu("Zoom ", self)
        zoom_width = QtWidgets.QAction("Fit Width", self, checkable=True)
        impMenu.addAction(zoom_width)
        zoom_50 = QtWidgets.QAction("Zoom 50%", self, checkable=True)
        impMenu.addAction(zoom_50)
        zoom_100 = QtWidgets.QAction("Zoom 100%", self, checkable=True)
        impMenu.addAction(zoom_100)
        zoom_150 = QtWidgets.QAction("Zoom 150%", self, checkable=True)
        impMenu.addAction(zoom_150)
        zoom_200 = QtWidgets.QAction("Zoom 200%", self, checkable=True)
        impMenu.addAction(zoom_200)
        zoom_400 = QtWidgets.QAction("Zoom 400%", self, checkable=True)
        impMenu.addAction(zoom_400)
        zoom_800 = QtWidgets.QAction("Zoom 800%", self, checkable=True)
        impMenu.addAction(zoom_800)

        contextMenu.addMenu(impMenu)
        # openAct = contextMenu.addAction("Open")
        quitAct = contextMenu.addAction("Quit")
        action = contextMenu.exec_(self.mapToGlobal(event.pos()))
        if action == zoom_50:
            self.rescaleToWidth = False
            self.renderFirstpapge(0.50)
        if action == zoom_150:
            self.rescaleToWidth = False
            self.renderFirstpapge(1.50)
        if action == zoom_100:
            self.rescaleToWidth = False
            self.renderFirstpapge(1.0)
        if action == zoom_200:
            self.rescaleToWidth = False
            self.renderFirstpapge(2.0)
        if action == zoom_400:
            self.rescaleToWidth = False
            self.renderFirstpapge(4.0)
        if action == zoom_width:
            self.rescaleToWidth = True
            self.renderFirstpapge()
        if action == quitAct:
            self.close()

    def resizeEvent(self, event):
        self.resized.emit()
        return super(Pdf_Widget, self).resizeEvent(event)

    def reRender(self):
        # tsize = float(self.width())
        """
        change_size = abs((self.ui.current_width-tsize)/(1.*tsize))
        if ( change_size > 0.05 and self.rescaleToWidth ):
            self.renderFirstpapge()
            self.ui.current_width = tsize
        """

    def renderFirstpapge(self, scalefactor=None):
        if scalefactor is None:
            tscale = self.defaultScale
        else:
            tscale = scalefactor
        fake_dpi = tscale * self.physicalDpiX()

        worker = threaded.GetAllPage(self.ui.doc, fake_dpi, self.rescaleToWidth)
        self.workingState = -1
        self.threadpool.start(worker)
        worker.signals.finished.connect(self.add_qlabel)
        worker.signals.starting.connect(self.annimateProgressBar)

    def annimateProgressBar(self, page):
        self.ui.pbar.setValue(page + 1)

    def closeEvent(self, *args, **kwargs):
        self._closing = True
        self.threadpool.waitForDone()

    def add_qlabel(self, tlabel):
        self.ui.pbar.hide()
        xlayout = self.ui.pdfwidget.layout()
        if xlayout is not None:
            QtWidgets.QWidget().setLayout(xlayout)
        self.ui.pdfwidget.setLayout(tlabel)
        # self.ui.layout.addWidget(tlabel,stretch=1)

    def add_thumblabel(self, tlabel):
        xlayout = self.ui.thumbWidget.layout()
        if xlayout is not None:
            QtWidgets.QWidget().setLayout(xlayout)
        self.ui.thumbWidget.setLayout(tlabel)

    def show_annotations(self):
        self.w = FloatingButtonWidget()
        self.w.setGeometry(QtCore.QRect(100, 100, 400, 200))
        self.w.show()


class FloatingButtonWidget(QtWidgets.QWidget):
    def __init__(self):
        super(FloatingButtonWidget, self).__init__()
        # super().__init__(parent)
        self.paddingLeft = 5
        self.paddingTop = 5
        self.controlLayout = QtWidgets.QHBoxLayout()
        self.controlLayout.setObjectName("controlLayout")
        self.controlLayout.setContentsMargins(0, 0, 0, 0)
        self.controlLayout.setSpacing(0)
        # add buttons
        self.addButton = QtWidgets.QPushButton()
        self.addButton.setObjectName("addButton")
        self.addButton.setText("Add")
        self.controlLayout.addWidget(self.addButton)
        self.setLayout(self.controlLayout)
        self.setObjectName("FloatingButtonWidget")
        self.setWindowFlags(
            QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint
        )
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowOpacity(0.5)
        self.setFixedWidth(30)
        self.setFixedHeight(30)
        self.setWindowTitle("FloatingButtonWidget")
        self.setStyleSheet("background-color: #ffffff;")
        self.setGeometry(QtWidgets.QApplication.desktop().screen().rect())
        self.setWindowFlags(
            QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint
        )
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowOpacity(0.5)
        self.setFixedWidth(30)
