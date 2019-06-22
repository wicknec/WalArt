#! /usr/bin/env python3

"""
WalArt.gui.btDragDrop
=======================

a special button

"""
# NOTE: the actual command documentation is collected from docstrings of the
# commands and is appended to __doc__ after the class has been defined.
"""
Revisions
=================
based on http://blog.csdn.net/fengda2870/article/details/48974363
160520 can drop and click
"""
from PyQt4 import QtGui,QtCore
from WalArt import waFile
from WalArt import waFile
import sys
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


class Button(QtGui.QPushButton):
    '''A button that accepts url drop,
reassign Button.DropAction(self, url) to change the action
'''
    def __init__(self, parent):
        super(Button, self).__init__(parent)
        self.setAcceptDrops(True)
        #self.setDragDropMode(QAbstractItemView.InternalMove)
    def DropAction(self,url):
        pass
        return
    def RegisterClickAction(self,action):
        QtCore.QObject.connect(self,QtCore.SIGNAL(_fromUtf8("clicked()")),
                               action)
        return
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            super(Button, self).dragEnterEvent(event)

    def dragMoveEvent(self, event):
        super(Button, self).dragMoveEvent(event)

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            #遍历输出拖动进来的所有文件路径
            for url in event.mimeData().urls():                
                print(url.toLocalFile())
                self.DropAction(url.toLocalFile())
            event.acceptProposedAction()
        else:
            super(Button,self).dropEvent(event)

class MyWindow(QtGui.QWidget):
    def Message(self,text):
        self.messenger.setText(text)
    def __init__(self):
        super(MyWindow,self).__init__()
        self.setGeometry(100,100,200,160)
        self.setWindowTitle("Filenames")

        self.btn = Button(self)
        self.btn.setGeometry(QtCore.QRect(90, 90, 61, 51))
        self.btn.setText("Drop url on Me!")
        self.messenger=QtGui.QLabel(self)

        def c():
            self.Message('Pushed')
        self.btn.RegisterClickAction(c)
        def d(url):
            self.Message(url)
        self.btn.DropAction=d
        layout = QtGui.QVBoxLayout(self)
        layout.addWidget(self.btn)
        layout.addWidget(self.messenger)
        self.setLayout(layout)

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = MyWindow()
    window.Message('Welcome')
    window.show()
    sys.exit(app.exec_())
            

