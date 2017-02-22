# -*- coding: utf-8 -*-
import sys, os, time
import logging
from Queue import Queue
from PyQt4 import uic as UI
from PyQt4.QtCore import QThread
from PyQt4.QtCore import pyqtSlot
from PyQt4.QtCore import pyqtSignal
from PyQt4 import QtCore, QtGui

import gdal2mbtiles as g2m

import gdal2mbtiles

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except:
    _fromUtf8 = lambda s: s


class ConvThread(QThread):
    """
    Класс потока для выполнения операций конвертации.
    Методы:
        run() - запуск функции func
        stop() - принудительная остановка (использовать осторожно!)
    """
    loop = pyqtSignal(object)

    def __init__(self, func):
        QThread.__init__(self)
        self.func = func

    def run(self):
        self.loop.emit(u'Петля')
        self.func()

    def stop(self):
        if self.isRunning():
            self.exit()
            self.terminate()

        else:
            self.exit()
            self.quit()

class MainWindow():
    EXIT_CODE_REBOOT = -1234

    def __init__(self, version):
        self.version = version
        self.mw = UI.loadUi('gui.ui')

        self.mw.setWindowTitle(u'Tiler (Version ' + self.version + u')')
        self.mw.pushbutton_input.clicked.connect(self.set_input)
        self.mw.pushbutton_output.clicked.connect(self.set_output)
        # self.mw.pushbutton_start.clicked.connect(self.start)
        self.mw.pushbutton_start.clicked.connect(self.thread_start)

        self.native = QtGui.QCheckBox()
        self.native.setText("Use native file dialog.")
        self.native.setChecked(True)

        self.input_path = None
        self.output_path = None

        self.mw.spinbox_general.setRange(0, 21)

        # self.mw.combobox_type_input.addItems(['GEOTiff', 'VRT (Virtual Raster Table)'])
        self.mw.combobox_type_output_tiles.addItems(['JPG', 'PNG'])
        self.mw.combobox_type_output.addItems(['MBTILES', 'GEO Package', 'Tiles'])

        self.mw.progressBar.setMinimum(0)
        self.mw.progressBar.setMaximum(100)
        self.mw.progressBar.setValue(0)
        self.pbar_thread = QtCore.QThread()
        self.pbar = g2m.ProgressBar()

        self.pbar.pbar_signal.connect(self.handle_value_updated)

        # self.pbar.moveToThread(self.pbar_thread)
        # self.pbar_thread.connect(self.pbar, QtCore.SIGNAL('QtCore_QtObject()'), self.handle_value_updated)
        # self.pbar_thread.connect(self.pbar, QtCore.SIGNAL('2pbar_signal'), self.handle_value_updated)
        # self.pbar_thread.started.connect(self.handle_value_updated)
        # self.pbar_thread.start()

    def set_input(self):
        options = QtGui.QFileDialog.Options()
        if not self.native.isChecked():
            options |= QtGui.QFileDialog.DontUseNativeDialog
        fileName = QtGui.QFileDialog.getOpenFileName(self.mw,
                                                     "Input",
                                                     str(self.mw.label_input.text().toUtf8()),
                                                     ".tif (*.tif);;All Files (*)", "", options)

        if fileName:
            self.mw.label_input.setText(fileName)
            self.input_path = os.path.normpath(str(fileName.toUtf8())).decode('utf-8')

    def set_output(self):
        options = QtGui.QFileDialog.DontResolveSymlinks | QtGui.QFileDialog.DontUseNativeDialog
        fileName = QtGui.QFileDialog.getSaveFileName(self.mw,
                                                     u"Output",
                                                     # os.path.dirname(str(self.Label_RSC.text().toUtf8())),
                                                     str(self.mw.label_output.text().toUtf8()),
                                                     ".mbtiles(*.mbtiles);;All Files (*)", "",options)
        if fileName:
            self.mw.label_output.setText(fileName+'.mbtiles')
            self.output_path = os.path.normpath(str(fileName.toUtf8()+'.mbtiles'))

    @pyqtSlot()
    def start(self):
        self.mw.progressBar.setValue(0)
        general_zoom = self.mw.spinbox_general.value()
        overview_zoom = self.mw.spinbox_overview.value()
        # ans = 'y' if self.mw.checkbox_save_tiles.isChecked() else 'n'
        type_inputs = ['--resume --no-kml', '--s_srs ESPG:3857 --resume --no-kml']
        # type_input = type_inputs[self.mw.combobox_type_input.currentIndex()]
        type_outputs_tiles = ['JPEG', 'PNG']
        type_output_tiles = type_outputs_tiles[self.mw.combobox_type_output_tiles.currentIndex()]
        type_outputs = ['mbtiles', 'geopackage', 'tiles']
        type_output = type_outputs_tiles[self.mw.combobox_type_output.currentIndex()]
        argv = 'gdal2mbtiles.py {} -z {} {}'.format(self.input_path,
                                                             str(overview_zoom) + '-' + str(general_zoom),

                                                             self.output_path).split(' ')

        g2m.main(self.pbar, argv)


    @pyqtSlot()
    def handle_value_updated(self, value):
        self.mw.progressBar.setValue(value)

    def thread_start(self):
        self.th = ConvThread(self.start)
        self.th.setTerminationEnabled(True)
        self.th.start()


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    mw = MainWindow('0.1.0')
    mw.mw.show()
    sys.exit(app.exec_())