# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MfcConsole.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

"""
Created on Thu Jun 28 10:10:43 2017
    proxy for Aalborg MFC command module
    used for controlling mass flow controllers

reference: http://pyvisa.readthedocs.io/en/stable/tutorial.html

@author: wein1
Revisions:
    190617 removed axes.hold to be compatible with python 3.6+
    170629 added timing control
    170628 created
"""

from WalArt import alib, waFile
import WalArt.sci.AalborgMFC as Amfc

import time,sys
iconPath=waFile.GetFolderName(waFile.Find('add.png'))

#from PyQt4.QtCore import QTimer
try:
    from PyQt4 import QtCore
    from PyQt4.QtCore import QTimer
    from PyQt4.GtGui import QApplication, QWidget
except ModuleNotFoundError:
    print('PyQt4 module not found, try using PyQt5')
    from PyQt5 import QtCore
    from PyQt5.QtWidgets import QApplication, QWidget
    from PyQt5.QtCore import QTimer
from WalArt.gui.QtGui4or5 import QtGuiFinder
QtGui=QtGuiFinder()

# below are generated code

#from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)
try:
    from matplotlibwidget import MatplotlibWidget
except ModuleNotFoundError:
    import matplotlib
    matplotlib.use('Qt5Agg')
    from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
    from matplotlib.figure import Figure
    class MatplotlibWidget(FigureCanvas):
        """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""
        def __init__(self, parent=None, width=5, height=4, dpi=100):

            fig = Figure(figsize=(width, height), dpi=dpi)
            self.axes = fig.add_subplot(111)
            # We want the axes cleared every time plot() is called
            #self.axes.hold(False)

            self.compute_initial_figure()

            #
            FigureCanvas.__init__(self, fig)
            self.setParent(parent)

            FigureCanvas.setSizePolicy(self,
                    QtGui.QSizePolicy.Expanding,
                    QtGui.QSizePolicy.Expanding)
            FigureCanvas.updateGeometry(self)

        def compute_initial_figure(self):
            pass

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(517, 362)
        self.verticalLayout = QtGui.QVBoxLayout(Form)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        
        self.lFlow = QtGui.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lFlow.setFont(font)
        self.lFlow.setObjectName(_fromUtf8("lFlow"))
        self.horizontalLayout.addWidget(self.lFlow)
        
        self.spinFlow = QtGui.QSpinBox(Form)
        self.spinFlow.setMinimumSize(QtCore.QSize(0, 32))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.spinFlow.setFont(font)
        self.spinFlow.setMaximum(2000)
        self.spinFlow.setObjectName(_fromUtf8("spinFlow"))
        self.horizontalLayout.addWidget(self.spinFlow)
        
        self.label = QtGui.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        
        self.spinTime = QtGui.QSpinBox(Form)
        self.spinTime.setMinimumSize(QtCore.QSize(0, 32))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.spinTime.setFont(font)
        self.spinTime.setMaximum(9999999)
        self.spinTime.setObjectName(_fromUtf8("spinTime"))
        self.horizontalLayout.addWidget(self.spinTime)
        
        self.label_2 = QtGui.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout.addWidget(self.label_2)
        self.toolButton = QtGui.QToolButton(Form)
        self.toolButton.setMinimumSize(QtCore.QSize(32, 32))
        self.toolButton.setObjectName(_fromUtf8("toolButton"))
        self.horizontalLayout.addWidget(self.toolButton)
        self.label_3 = QtGui.QLabel(Form)
        self.label_3.setMinimumSize(QtCore.QSize(245, 0))
        self.label_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout.addWidget(self.label_3)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.matplotlibwidget = MatplotlibWidget(Form)
        self.matplotlibwidget.setObjectName(_fromUtf8("matplotlibwidget"))
        self.verticalLayout.addWidget(self.matplotlibwidget)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.label.setText(_translate("Form", "sccm", None))
        self.label_2.setText(_translate("Form", "s", None))
        self.toolButton.setToolTip(_translate("Form", "<html><head/><body><p>Open valve and start timing</p></body></html>", None))
        self.toolButton.setText(_translate("Form", "...", None))
        self.label_3.setText(_translate("Form", "MfcConsole wicknec@2017", None))

# above are codes generated by pyuic4
    def TimerRoutine(self):
        pass
        reading=self.mfc.Read()*self.settings['FullScaleCcm']/100
        self.flowHistory.append(reading)

        self.lFlow.setText('%.2f ccm'%reading)
        
        ys=self.flowHistory[-self.settings['DisplayLength']:]
        lys=len(self.flowHistory)
        if lys < self.settings['DisplayLength']:
            xlb=0
        else:
            xlb=lys-self.settings['DisplayLength']
        xub=xlb+len(ys)
        
        self.mpl.axes.plot(range(xlb,xub),ys,'ob-‘)
        self.mpl.draw()
        
        if self.mfcState=='Open':
            timeLeft=self.spinTime.value()
            if timeLeft<=0:
                self.toolButton.setChecked(False)
                self.mfc.Close()
                print('Mfc set to closed')
                self.spinTime.setEnabled(True)
                self.spinTime.setValue(self.originalTime)
                self.mfcState='Closed'
            else:
                self.spinTime.setValue(timeLeft-1)
        
    def btTimeClicked(self):
        if self.btTime.isChecked: #this method is invoked after state change
            self.toolButton.setChecked(True)
            self.originalTime=self.spinTime.value()
            flow=self.spinFlow.value()
            self.spinTime.setEnabled(False)
            self.mfc.SetPoint(flow/self.settings['FullScaleCcm']*100)
            print('valve set to %.1f'%(flow/self.settings['FullScaleCcm']*100))
            #time.sleep(0.3)
            self.lbMessage.setText('Timing started (%d)'%self.originalTime)
            self.mfc.Auto()
            #time.sleep(0.5)
            print('Mfc set to auto')
            self.mfcState='Open'
            
        else:
            self.toolButton.setChecked(False)
            self.mfc.Close()
            print('Mfc set to closed')
            self.spinTime.setEnabled(True)
            self.mfcState='Closed'
    
    def LoadSettings(self):
        import os
        cwd=os.getcwd()
        fSettings=os.path.join(cwd,'MfcConsole.settings.alib.txt')
        if not os.path.exists(fSettings):
            s='''[MfcPort|COM4]
            [MfcChannel|1][FullScaleCcm|1000]
            [DisplayLength|1000]
            [DefaultFlow|300][DefaultTime|10]
'''
            waFile.SaveText(fSettings,s)
            print('The default file {%s} created'%fSettings)
        a=alib()
        a.Load(fSettings)
        
        a['MfcChannel']=int(a['MfcChannel'])
        a['FullScaleCcm']=float(a['FullScaleCcm'])
        a['DisplayLength']=int(a['DisplayLength'])
        a['DefaultFlow']=int(a['DefaultFlow'])
        a['DefaultTime']=int(a['DefaultTime'])
        
        self.settings=a
        
    def Initialize(self):
        ''' perform additional tasks other than drawing UI'''
        self.lbMessage=self.label_3
        self.mpl=self.matplotlibwidget
        self.btTime=self.toolButton
        
        self.btTime.clicked.connect(self.btTimeClicked)
        #QtCore.QObject.connect(self.btTime, QtCore.SIGNAL(_fromUtf8("clicked()")),self.btTimeClicked)
        
        self.LoadSettings()
        self.spinFlow.setValue(self.settings['DefaultFlow'])
        self.spinTime.setValue(self.settings['DefaultTime'])
        
        self.mfc=Amfc.MFC(self.settings['MfcPort'],self.settings['MfcChannel'])
        print('Connected!')
        
        self.flowHistory=[] #in sccm since the program started
        self.mfcState='Closed' #used for controlling timer
        
        self.timer=QTimer()
        self.timer.timeout.connect(self.TimerRoutine)
        self.timer.start(1000)
        
        self.toolButton.setIcon(QtGui.QIcon(waFile.Join(iconPath,'time.png')))
        self.toolButton.setCheckable(True)
        
        
        
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    Form = QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.setWindowTitle('MfcConsole')
    Form.setWindowIcon(QtGui.QIcon(waFile.Join(iconPath,'WicFam.png')))    
    try:
        ui.Initialize()
        Form.show()
        sys.exit(app.exec_())
        #print('exited')
        time.sleep(5)
    except Exception:
        import traceback
        traceback.print_exc()
        time.sleep(5)
        sys.exit(app.exec_())   
    
