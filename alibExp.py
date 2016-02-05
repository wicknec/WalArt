#! /usr/bin/env python3

"""
alibExp
=======================

Qt4 interface for alib explorer

To browse alib in a more user-friendly way than simple text
Item.data(1,-1) stores its data, i.e. a str or another alib

"""
# NOTE: the actual command documentation is collected from docstrings of the
# commands and is appended to __doc__ after the class has been defined.
"""
Revisions
=================
151125 completed reading functionality
151209 wordless gui, remove node
151210 edit text, add icon to tree, btAdd function
151214 added btRoot, explore root
151219 added *GetCurrent*, modified *RemoveDataSync* to suited with alib.Pop
151229 added *GetSelectedText*
160112 change data display to waText.Brief
160113 change non-editing to read only to allow scroll
"""


# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'alibExp.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

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

from WalArt import waFile,waText
iconPath=waFile.GetFolderName(waFile.Find('add.png'))

class alibTree(QtGui.QTreeWidget):
    dropped = QtCore.pyqtSignal(list)
    def __init__(self,parent=None):
        super(alibTree,self).__init__(parent)
        self.setAcceptDrops(True)
        self.data=None
        self.imgList=QtGui.QIcon(waFile.Join(iconPath,'list.png'))
        self.imgData=QtGui.QIcon(waFile.Join(iconPath,'data.png'))
        self.imgBlank=QtGui.QIcon(waFile.Join(iconPath,'blank.png'))
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()

        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()

        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()

            filePaths = [
                str(url.toLocalFile())
                for url in event.mimeData().urls()
            ]

            self.dropped.emit(filePaths)

        else:
            event.ignore()
    def Load(self,a):
        '''load the alib into the treeWidget
'''
        self.clear()
        self.setHeaderLabels(['Key','Value'])
        self.data=a
        for t in a:
            if isinstance(a[t],alib):
                ti=QtGui.QTreeWidgetItem([str(t)])
                self.addTopLevelItem(ti)
                self.LoadToNode(ti,a[t])
                ti.setIcon(0,self.imgList)
                ti.setExpanded(True)
            else:
                ti=QtGui.QTreeWidgetItem([str(t)])
                if a[t]!='':
                    ti.setIcon(0,self.imgData)
                else:
                    ti.setIcon(0,self.imgBlank)
                self.addTopLevelItem(ti)
            ti.setData(1,0,waText.Brief(a[t],20))
            ti.setData(1,-1,a[t])
        #help(ti)
    def LoadToNode(self,node,a):
        '''load the alib to node recursively
'''
        #print(a)
        for t in a:
            if isinstance(a[t],alib):
                ti=QtGui.QTreeWidgetItem([str(t)])
                node.addChild(ti)
                self.LoadToNode(ti,a[t])
                ti.setIcon(0,self.imgList)
                ti.setExpanded(True)
                
            else:
                ti=QtGui.QTreeWidgetItem([str(t)])
                if a[t]!='':
                    ti.setIcon(0,self.imgData)
                else:
                    ti.setIcon(0,self.imgBlank)
                i=node.addChild(ti)
            ti.setData(1,0,waText.Brief(a[t],20))
            ti.setData(1,-1,a[t])
    def ItemFromPath(self,path):
        '''Get item from a path string of keys like: a|b|c
path can also be a list of strings
'''
        if isinstance(path,str):
            path=path.split('|')
        item=None
        
        for i in range(len(self.data.keys())):
            #print(self.topLevelItem(i).text(0))
            if self.topLevelItem(i).text(0)==path[0]:
                item=self.topLevelItem(i)
                break
        if item!=None:
            k=1
            while k<len(path):
                found=False
                for i in range(item.childCount()):
                    #print(item.child(i).text(0))
                    if item.child(i).text(0)==path[k]:
                        item=item.child(i)
                        found=True
                        break
                
                if found==False:
                    return None
                else:
                    k+=1
            if k<len(path):
                return None
        return item
    
    def ItemToPath(self,item):
        fl=[item.text(0)]
        p=item.parent()
        while p!=None:
            fl.append(p.text(0))
            p=p.parent()
        fl.reverse()

    def RemoveNodeSync(self,item):
        '''Remove the node from both the view and the alib
'''
        p=item.parent()
        if p==None:
            self.data.Pop(waText.atoi(item.text(0)))
        else:
            p.data(1,-1).Pop(waText.atoi(item.text(0)))
        self.Load(self.data)
                    
from WalArt import alib

def New(d):
    '''Make a new alib explorer in the dialog, and return the object
'''
    a=alibExp()
    a.setupUi(d)
    return a


class alibExp(object):
    def setupUi(self, Dialog):

        Dialog.setObjectName(_fromUtf8("Form"))
        Dialog.resize(474, 414)
        Dialog.setWindowIcon(QtGui.QIcon(waFile.Join(iconPath,'settings.png')))
        
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.groupBox = QtGui.QGroupBox(Dialog)
        self.groupBox.setMinimumSize(QtCore.QSize(0, 60))
        self.groupBox.setMaximumSize(QtCore.QSize(16777215, 60))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout.addWidget(self.groupBox)
        self.horizontalLayout = QtGui.QHBoxLayout(self.groupBox)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))

        self.btRoot = QtGui.QToolButton(self.groupBox)
        self.btRoot.setMinimumSize(QtCore.QSize(30, 30))
        self.btRoot.setMaximumSize(QtCore.QSize(30, 30))
        self.btRoot.setObjectName(_fromUtf8("btRoot"))
        self.btRoot.setIcon(QtGui.QIcon(waFile.Join(iconPath,'circle.png')))
        self.btRoot.setToolTip('Explore the root node')
        self.horizontalLayout.addWidget(self.btRoot)

        
        self.lineEdit = QtGui.QLineEdit(self.groupBox)
        self.lineEdit.setMinimumSize(QtCore.QSize(0, 30))
        self.lineEdit.setMaximumSize(QtCore.QSize(16777215, 30))
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.horizontalLayout.addWidget(self.lineEdit)
        self.btAdd = QtGui.QToolButton(self.groupBox)
        self.btAdd.setMinimumSize(QtCore.QSize(30, 30))
        self.btAdd.setMaximumSize(QtCore.QSize(30, 30))
        self.btAdd.setObjectName(_fromUtf8("btAdd"))
        self.btAdd.setIcon(QtGui.QIcon(waFile.Join(iconPath,'add.png')))
        self.btAdd.setToolTip('Add this path to the tree')
        self.horizontalLayout.addWidget(self.btAdd)
        
        self.btMinus = QtGui.QPushButton(self.groupBox)
        self.btMinus.setMinimumSize(QtCore.QSize(30, 30))
        self.btMinus.setMaximumSize(QtCore.QSize(30, 30))
        self.btMinus.setObjectName(_fromUtf8("btMinus"))
        self.btMinus.setIcon(QtGui.QIcon(waFile.Join(iconPath,'minus.png')))
        self.btMinus.setToolTip('Delete this node')
        self.horizontalLayout.addWidget(self.btMinus)

        import WalArt.gui.buttons
        self.btLock = WalArt.gui.buttons.btLock(self.groupBox)
        self.btLock.setMinimumSize(QtCore.QSize(30, 30))
        self.btLock.setMaximumSize(QtCore.QSize(30, 30))
        self.btLock.setObjectName(_fromUtf8("btLock"))
        self.btLock.setToolTip('Unlock to start editing node content')
        self.horizontalLayout.addWidget(self.btLock)
        self.splitter = QtGui.QSplitter(Dialog)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.verticalLayout.addWidget(self.splitter)
        self.treeWidget = alibTree(self.splitter)
        self.treeWidget.setObjectName(_fromUtf8("treeWidget"))
        self.treeWidget.headerItem().setText(0, _fromUtf8("1"))
        
        self.plainTextEdit = QtGui.QPlainTextEdit(self.splitter)
        self.plainTextEdit.setObjectName(_fromUtf8("plainTextEdit"))
        
        
        self.messenger = QtGui.QLabel(Dialog)
        self.messenger.setMinimumSize(QtCore.QSize(0, 30))
        self.messenger.setMaximumSize(QtCore.QSize(16777215, 30))
        self.messenger.setObjectName(_fromUtf8("messenger"))
        self.verticalLayout.addWidget(self.messenger)

        self.retranslateUi(Dialog)

        QtCore.QObject.connect(self.treeWidget, QtCore.SIGNAL(_fromUtf8("clicked(QModelIndex)")),
                               self.itemSelected)
        self.plainTextEdit.setAcceptDrops(True)
        
        self.treeWidget.setDragDropMode(QtGui.QAbstractItemView.InternalMove)
        self.treeWidget.setFrameShadow(QtGui.QFrame.Plain)
        self.treeWidget.setFrameShape(QtGui.QFrame.Box)

  
        QtCore.QObject.connect(self.btLock, QtCore.SIGNAL(_fromUtf8("clicked()")),
                               self.btLockClicked)
        QtCore.QObject.connect(self.btMinus, QtCore.SIGNAL(_fromUtf8("clicked()")),
                               self.btMinusClicked)
        QtCore.QObject.connect(self.btAdd, QtCore.SIGNAL(_fromUtf8("clicked()")),
                               self.btAddClicked)
        QtCore.QObject.connect(self.btRoot, QtCore.SIGNAL(_fromUtf8("clicked()")),
                               self.btRootClicked)
        self.treeWidget.dropEvent=self.itemDropped
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        self.setEditing(False)

    def Message(self,text):
        self.messenger.setText(text)
    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.groupBox.setTitle(_translate("Dialog", "alibExplorer", None))
        self.btAdd.setText(_translate("Dialog", "+", None))
        self.btMinus.setText(_translate("Dialog", "", None))
        self.btLock.setText(_translate("Dialog", "...", None))
        self.messenger.setText(_translate("Dialog", "Messege", None))

    def itemSelected(self, index):
        item=self.treeWidget.itemFromIndex(index)
        #help(item)
        #d=item.data(1,0)
        d=item.data(1,-1)
        
        #self.plainTextEdit.setEnabled(not self.btLock.getState())
        if isinstance(d,alib):
            self.plainTextEdit.setPlainText(d.ToString(''))
        else:
            self.plainTextEdit.setPlainText(str(d))
        self.setEditing(False)

        fl=[item.text(0)]
        p=item.parent()
        while p!=None:
            fl.append(p.text(0))
            p=p.parent()
        fl.reverse()
        self.lineEdit.setText('|'.join(fl))
        self.Message('')
    def setEditing(self,b):
        '''b==True for editing mode, else no editing mode
'''
        self.plainTextEdit.setReadOnly(not b)
        self.lineEdit.setReadOnly(b)
        self.btLock.setState(not b)
        if b == True:
            self.Message('Modify value and hit lock to save.')
    def dragEnterEvent(self,e):
        e.acceptPropsedAction()
    def btLockClicked(self):
        editing=not self.btLock.getState()

        si=self.treeWidget.selectedItems()
        if editing==True:
            if len(si)==0:
                #self.Message('Begin editing whole alib')
                self.treeWidget.data.FromString(self.plainTextEdit.toPlainText())
                self.treeWidget.Load(self.treeWidget.data)
                self.Message('Change saved')
                self.setEditing(not editing)
                return
            else:
                si=si[0]
            #help(self.plainTextEdit)
            if str(si.data(1,-1))==self.plainTextEdit.toPlainText():
                self.Message('Nothing changed')
            else:
                #record data
                v=alib.Parse(self.plainTextEdit.toPlainText())
                k=si.text(0)
                if si.parent()==None:
                    self.treeWidget.data[k]=v
                else:
                    si.parent().data(1,-1)[k]=v
                self.treeWidget.Load(self.treeWidget.data)
                self.Message('Change saved')
        else:
            if len(si)==0:
                self.Message('Begin editing whole alib')
        self.setEditing(not editing)
    def itemDropped(self,event):
        #print('called')
        if event.mimeData().hasUrls:
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()

            filePaths = [
                str(url.toLocalFile())
                for url in event.mimeData().urls()
            ]
            #print(str(event))
            self.messenger.setText(filePaths[0])
            self.lineEdit.setText(filePaths[0])
            #self.dropped.emit(filePaths)

            from WalArt import alib
            self.treeWidget.Load(alib().Load(filePaths[0]))
            
        else:
            event.ignore()
            
    def Load(self,a):
        self.treeWidget.Load(a)
        self.btRootClicked()
        
    def btMinusClicked(self):
        path=self.lineEdit.text()
        item=self.treeWidget.ItemFromPath(path)
        if item==None:
            self.Message('Warning: the node does not exist')
        else:
            self.treeWidget.RemoveNodeSync(item)
            self.Message('node{%s} deleted'%path)
    def btAddClicked(self):
        path=self.lineEdit.text()
        item=self.treeWidget.ItemFromPath(path)
        
        if item==None:
            self.treeWidget.data.setValue(path,'')
            self.treeWidget.Load(self.treeWidget.data)
            self.Message('Node{%s} added'%path)
        else:
            try:
                #insert a number and shift other number forward,
                #for convenience of auto numbering
                i=int(item.text(0))
                if item.parent()==None:
                    a=self.treeWidget.data
                else:
                    a=item.parent().data(1,-1)
                boundary=i
                while str(boundary) in a:
                    boundary+=1
                while boundary!=i:
                    a[str(boundary)]=a[str(boundary-1)]
                    boundary-=1
                a[str(i)]=''
                self.treeWidget.Load(self.treeWidget.data)
                self.Message('Node{%s} added with shifts'%path)
            except ValueError:
                self.Message('Node{%s} already exists, nothing added'%path)
    def btRootClicked(self):
        
        d=self.treeWidget.data
        si=self.treeWidget.selectedItems()
        #self.treeWidget.deselectAll()
        for i in si:
            i.setSelected(False)
        #self.plainTextEdit.setEnabled(not self.btLock.getState())
        if isinstance(d,alib):
            self.plainTextEdit.setPlainText(d.ToString(''))
        else:
            self.plainTextEdit.setPlainText(str(d))
        self.setEditing(False)

        self.lineEdit.setText('')
        self.Message('Root node explored')
    def GetCurrent(self):
        '''returns the object that is currently exploring
it is the data of selected treenode, or the whole alib if nothing is selected
'''
        si=self.treeWidget.selectedItems()
        if len(si)>0:
            return si[0].data(1,-1)
        else:
            return self.treeWidget.data
    def GetSelectedText(self):
        '''Similar as GetCurrent'''
        si=self.treeWidget.selectedItems()
        if len(si)>0:
            return si[0].text(0)
        else:
            return ''
        
import sys
import time
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    Form = QtGui.QWidget()
    ui = alibExp()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
    time.sleep(5)
