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



try:
    _fromUtf8 = QtCore.QString.fromUtf8
except:
    _fromUtf8 = lambda s: s

class MainWindow():
    EXIT_CODE_REBOOT = -1234

    def __init__(self, version):
        self.version = version
        self.mw = UI.loadUi('gui.ui')

        self.mw.setWindowTitle(u'Tiler (Version ' + self.version + u')')
        self.mw.pushbutton_input.clicked.connect(self.set_input)
        self.mw.pushbutton_output.clicked.connect(self.set_output)
        self.mw.pushbutton_start.clicked.connect(self.start)

        self.native = QtGui.QCheckBox()
        self.native.setText("Use native file dialog.")
        self.native.setChecked(True)

        self.input_path = None
        self.output_path = None

        self.mw.spinbox_general.setRange(0,21)

        self.mw.combobox_type_input.addItems(['GEOTiff', 'VRT (Virtual Raster Table)'])
        self.mw.combobox_type_output_tiles.addItems(['JPG', 'PNG'])
        self.mw.combobox_type_output.addItems(['MBTILES', 'GEO Package', 'Tiles'])


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
        options = QtGui.QFileDialog.DontResolveSymlinks | QtGui.QFileDialog.ShowDirsOnly
        directory = QtGui.QFileDialog.getExistingDirectory(self.mw,
                                                           u"Результат конвертации",
                                                           # os.path.dirname(str(self.Label_RSC.text().toUtf8())),
                                                           os.path.dirname(str(self.mw.label_output.text().toUtf8())),
                                                           options)
        if directory:
            # directory_str = str(directory.toUtf8())
            self.mw.label_output.setText(directory)
            self.output_path = os.path.normpath(str(directory.toUtf8())).decode('utf-8')

    def start(self):
        general_zoom = self.mw.spinbox_general.value()
        overview_zoom = self.mw.spinbox_overview.value()
        # ans = 'y' if self.mw.checkbox_save_tiles.isChecked() else 'n'
        type_inputs = ['--resume --no-kml', '--s_srs ESPG:3857 --resume --no-kml']
        type_input = type_inputs[self.mw.combobox_type_input.currentIndex()]
        type_outputs_tiles = ['JPEG', 'PNG']
        type_output_tiles = type_outputs_tiles[self.mw.combobox_type_output_tiles.currentIndex()]
        type_outputs = ['mbtiles', 'geopackage', 'tiles']
        type_output = type_outputs_tiles[self.mw.combobox_type_output.currentIndex()]
        argv = 'gdal2mbtiles.py {} -z {} -f {} {} {}'.format(self.input_path, str(overview_zoom)+ '-' + str(general_zoom), type_output_tiles, type_input, self.output_path).split(' ')
        g2m.main(argv)

if __name__=='__main__':
    app = QtGui.QApplication(sys.argv)
    mw = MainWindow('0.11.0')
    mw.mw.show()
    sys.exit(app.exec_())
    # t = 0
    # print('Tiling took: {:.2f} seconds '.format(t))

