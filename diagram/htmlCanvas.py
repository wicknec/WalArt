# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UiWebTest.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!


import sys
from PyQt4 import QtCore, QtGui

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
    
class PythonJS(QtCore.QObject):
    __pyqtSignals__ = ("contentChanged(const QString &)") 

    @QtCore.pyqtSignature("")
    def close(self):
        sys.exit()

    @QtCore.pyqtSignature("")
    def openMap(self): 
        browser.setHtml(open('test1.html').read().decode('utf-8'))
        
class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("pyBrowser"))
        Dialog.resize(753, 493)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        self.gridLayout = QtGui.QGridLayout(Dialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        
        #self.lineEdit = QtGui.QLineEdit(Dialog)
        #self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        #self.gridLayout.addWidget(self.lineEdit, 0, 0, 1, 1)
        self.webView = QtWebKit.QWebView(Dialog)
        self.webView.setUrl(QtCore.QUrl(_fromUtf8("about:blank")))
        self.webView.setObjectName(_fromUtf8("webView"))
        self.gridLayout.addWidget(self.webView, 1, 0, 1, 1)

        browser = self.webView
        self.pjs=PythonJS()
        browser.page().mainFrame().addToJavaScriptWindowObject("python",self.pjs)
        #QtCore.QObject.connect(self.pjs,QtCore.SIGNAL("contentChanged(const QString &amp;)"),browser.showMessage)
        
        browser.page().settings().setAttribute(QtWebKit.QWebSettings.JavascriptEnabled,True)
        browser.page().settings().setAttribute(QtWebKit.QWebSettings.PluginsEnabled,True)
        

        self.retranslateUi(Dialog)
        #QtCore.QObject.connect(self.lineEdit,
        #                       QtCore.SIGNAL(_fromUtf8("returnPressed()")), self.LoadPage)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
    def LoadPage(self):
        h=self.lineEdit.text()
        self.webView.load(QtCore.QUrl(h))
        print('Loading %s ...'%QtCore.QUrl(h))



from PyQt4 import QtWebKit
from WalArt import waFile

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    Form = QtGui.QWidget()
    ui = Ui_Dialog()
    ui.setupUi(Form)
    f=waFile.Find('WalArt\\diagram\\canvas.html')
    ui.webView.load(QtCore.QUrl('file:///'+f))
    Form.show()
    sys.exit(app.exec_())
