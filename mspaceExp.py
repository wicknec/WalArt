# -*- coding: utf-8 -*-
"""
mspaceExp
=======================

Qt4 interface for mspace explorer

To browse alib in a more user-friendly way
Item.data(1,0) stores its data, i.e. a str or another alib

"""
# NOTE: the actual command documentation is collected from docstrings of the
# commands and is appended to __doc__ after the class has been defined.
"""
Revisions
=================
151210 ui established
    implemented basic lookupb
151218 btAddClicked
151222 add node and link ToolTip for description
151226 *thisNode*, *thisLink*, *linkDoubleClicked*
160105 add *mspaceExp.LoadNodes*
160113 fixed nodeClicked
"""
# Form implementation generated from reading ui file 'mspaceExp.ui'
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
    
from WalArt import alibExp,waFile,mspace
iconPath=waFile.GetFolderName(waFile.Find('add.png'))
class mspaceList(QtGui.QListWidget):
    '''A list that accept drops
'''
    def __init__(self,parent=None):
        super(mspaceList,self).__init__(parent)
        self.setAcceptDrops(True)
        self.data=None
        self.imgItem=QtGui.QIcon(waFile.Join(iconPath,'circle.png'))
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
            
    def appendItem(self,text,data=None):
        '''Append text item with item icon and data and return the item
'''
        count=self.count()
        self.addItem(text)
        item=self.item(count)
        item.setIcon(self.imgItem)
        if data!=None:
            item.setData(-1,data)#data(0) is the text data(1) is the icon
            #set 2 will overwrite the text... the mechanism is shit
        return item
    def setData(self,item,data):
        item.setData(-1,data)
    def getData(self,item):
        return item.data(-1)


#===========The generated part==============
class mspaceExp(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(400, 600)
        Form.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.verticalLayout = QtGui.QVBoxLayout(Form)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.splitter_2 = QtGui.QSplitter(Form)
        self.splitter_2.setOrientation(QtCore.Qt.Vertical)
        self.splitter_2.setObjectName(_fromUtf8("splitter_2"))
        self.groupBox = QtGui.QGroupBox(self.splitter_2)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.splitter_3 = QtGui.QSplitter(self.groupBox)
        self.splitter_3.setOrientation(QtCore.Qt.Vertical)
        self.splitter_3.setObjectName(_fromUtf8("splitter_3"))
        self.widget_3 = QtGui.QWidget(self.splitter_3)
        self.widget_3.setMinimumSize(QtCore.QSize(0, 50))
        self.widget_3.setMaximumSize(QtCore.QSize(16777215, 50))
        self.widget_3.setObjectName(_fromUtf8("widget_3"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.widget_3)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.lineEdit = QtGui.QLineEdit(self.widget_3)
        self.lineEdit.setMinimumSize(QtCore.QSize(0, 30))
        self.lineEdit.setMaximumSize(QtCore.QSize(16777215, 30))
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.horizontalLayout.addWidget(self.lineEdit)
        self.btSearch = QtGui.QToolButton(self.widget_3)
        self.btSearch.setMinimumSize(QtCore.QSize(30, 30))
        self.btSearch.setMaximumSize(QtCore.QSize(30, 30))
        self.btSearch.setObjectName(_fromUtf8("btSearch"))
        self.horizontalLayout.addWidget(self.btSearch)
        self.splitter = QtGui.QSplitter(self.splitter_3)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.lwNode = mspaceList(self.splitter) #this row is modified
        self.lwNode.setObjectName(_fromUtf8("lwNode"))
        self.lwLink = mspaceList(self.splitter) #also modified
        self.lwLink.imgItem=QtGui.QIcon(waFile.Join(iconPath,'minus.png'))#this row is added
        self.lwLink.setObjectName(_fromUtf8("lwLink"))
        self.verticalLayout_2.addWidget(self.splitter_3)
        self.lbMessage = QtGui.QLabel(self.groupBox)
        self.lbMessage.setMinimumSize(QtCore.QSize(0, 25))
        self.lbMessage.setMaximumSize(QtCore.QSize(16777215, 25))
        self.lbMessage.setObjectName(_fromUtf8("lbMessage"))
        self.verticalLayout_2.addWidget(self.lbMessage)
        self.wAlibPanel = QtGui.QWidget(self.splitter_2)
        self.wAlibPanel.setMinimumSize(QtCore.QSize(0, 200))
        self.wAlibPanel.setObjectName(_fromUtf8("wAlibPanel"))

        
        self.verticalLayout.addWidget(self.splitter_2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
#===========custom added part===============
        self.m=None
        self.filename=None
        #used to screen clicks
        self.dClicked=False
        
        self.alibUi=alibExp.alibExp()
        self.alibUi.setupUi(self.wAlibPanel)

        self.btSearch.setToolTip('Search and match(Enter)')
        self.btSearch.setIcon(QtGui.QIcon(waFile.Join(iconPath,'search.png')))

        self.btAdd = QtGui.QToolButton(self.widget_3)
        self.btAdd.setMinimumSize(QtCore.QSize(30, 30))
        self.btAdd.setMaximumSize(QtCore.QSize(30, 30))
        self.btAdd.setObjectName(_fromUtf8("btAdd"))
        self.horizontalLayout.addWidget(self.btAdd)
        self.btAdd.setToolTip('Add node')
        self.btAdd.setIcon(QtGui.QIcon(waFile.Join(iconPath,'add.png')))

        self.btMinus = QtGui.QToolButton(self.widget_3)
        self.btMinus.setMinimumSize(QtCore.QSize(30, 30))
        self.btMinus.setMaximumSize(QtCore.QSize(30, 30))
        self.btMinus.setObjectName(_fromUtf8("btMinus"))
        self.horizontalLayout.addWidget(self.btMinus)
        self.btMinus.setToolTip('Delete node or link')
        self.btMinus.setIcon(QtGui.QIcon(waFile.Join(iconPath,'minus.png')))

        self.btSave = QtGui.QToolButton(self.widget_3)
        self.btSave.setMinimumSize(QtCore.QSize(30, 30))
        self.btSave.setMaximumSize(QtCore.QSize(30, 30))
        self.btSave.setObjectName(_fromUtf8("btSave"))
        self.horizontalLayout.addWidget(self.btSave)
        self.btSave.setToolTip('Save the mspace')
        self.btSave.setIcon(QtGui.QIcon(waFile.Join(iconPath,'save.png')))

        self.lwNode.dropEvent=self.itemDropped
        
        QtCore.QObject.connect(self.btSearch, QtCore.SIGNAL(_fromUtf8("clicked()")),
                               self.btSearchClicked)
        QtCore.QObject.connect(self.lineEdit, QtCore.SIGNAL(_fromUtf8("returnPressed()")),
                               self.btSearchClicked)
        QtCore.QObject.connect(self.lwNode, QtCore.SIGNAL(_fromUtf8("clicked(QModelIndex)")),
                               self.nodeClicked)
        QtCore.QObject.connect(self.lwLink, QtCore.SIGNAL(_fromUtf8("clicked(QModelIndex)")),
                               self.linkClicked)
        QtCore.QObject.connect(self.btSave, QtCore.SIGNAL(_fromUtf8("clicked()")),
                               self.btSaveClicked)
        QtCore.QObject.connect(self.btAdd, QtCore.SIGNAL(_fromUtf8("clicked()")),
                               self.btAddClicked)

        QtCore.QObject.connect(self.lwLink, QtCore.SIGNAL(_fromUtf8("doubleClicked(QModelIndex)")),
                               self.linkDoubleClicked)
    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.groupBox.setTitle(_translate("Form", "mspaceExplorer", None))
        self.btSearch.setText(_translate("Form", "...", None))
        self.lwNode.setToolTip(_translate("Form", "Nodes", None))
        self.lwLink.setToolTip(_translate("Form", "Links", None))
        self.lbMessage.setToolTip(_translate("Form", "meesage", None))
        self.lbMessage.setText(_translate("Form", "Drag msdx in Nodes box to explore", None))

#========end of the generated part==============================

    def Load(self,m):
        '''Load the mspace into mspaceExp
'''
        if isinstance(m,mspace.mspace):
            self.m=m
        else:
            raise ValueError('invalid mspace object')
    
    def Message(self,s):
        self.lbMessage.setText(s)
        
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
            m=mspace.Load(filePaths[0])
            self.filename=filePaths[0]
            self.Load(m)
            self.groupBox.setTitle(filePaths[0])
            self.Message('file{%s} loaded'%filePaths[0])
            self.m.Check()
            #self.lineEdit.setText(filePaths[0])
            #self.dropped.emit(filePaths)
            self.btSearchClicked()
        else:
            event.ignore()
    def btSearchClicked(self):
        p=self.lineEdit.text()
        ns=self.m.FindNodesByName(p,100)
        self.LoadNodes(ns)
        
    def LoadNodes(self,nodes):
        '''Load a list of nodes to Node List
'''
        self.lwNode.clear()
        for n in nodes:
            #item=QtGui.QListWidgetItem(n.tag)
            #print(n.tag)
            item=self.lwNode.appendItem(n.tag)
            if 'description' in n.app:
                item.setToolTip(n.app['description'])
            #item.setData(0,n)
        self.Message('%d nodes loaded'%len(nodes))
    def nodeClicked(self,index):
        item=self.lwNode.itemFromIndex(index)
        #help(item)
        tag=item.text()
        n=self.m.nodes[tag]
        self.alibUi.Load(n.app)

        self.Message(tag)
        self.lwLink.clear()
        #help(self.lwLink)
        for l in n.links:
            p=self.m.links[l]
            i=self.lwLink.appendItem(p.Brief(n.tag),l)
            if 'description' in p.app:
                i.setToolTip(p.app['description'])
    def linkClicked(self,index):
        if self.dClicked==True:
            self.dClicked=False
            return
        item=self.lwLink.itemFromIndex(index)
        #num=item.text()
        #num=int(num[num.rfind('[')+1:-2])
        num=item.data(-1)
        l=self.m.links[num]
        self.Message(l.Brief())
        self.alibUi.Load(l.app)
    def btSaveClicked(self):
        if self.filename!=None:
            mspace.Save(self.filename,self.m)
            self.m.Check()
            self.Message('file{%s} saved'%self.filename)
        else:
            self.Message('path{%s} is incorrect'%self.filename)
    def btAddClicked(self):
        name=self.lineEdit.text()
        self.m.NewNode(name)
        self.btSearchClicked()

    def linkDoubleClicked(self,index):
        #this will also fire the itemClicked event
        #print('executed')
        item=self.lwLink.itemFromIndex(index)
        num=item.data(-1)
        l=self.m.links[num]
        #r=self.m.GetRelation(l,self.thisNode().tag)
        r=item.data(0)
        if r[0]=='-':
            self.lwNode.clear()
            self.lwNode.appendItem(l.dst)
        elif r[0]=='<':
            self.lwNode.clear()
            self.lwNode.appendItem(l.src)
        else:
            self.Message('The selected link is invalid')
        self.dClicked=True

    def thisNode(self):
        '''Return the selected node, or None'''
        its=self.lwNode.selectedItems()
        if len(its)==0:
            return None
        else:
            return self.m.nodes[its[0].text()]
    def thisLink(self):
        '''Return the selected link, or None'''
        its=self.lwLink.selectedItems()
        if len(its)==0:
            return None
        else:
            return self.m.links[its[0].data(-1)]
    def LoadFile(self,filename):
        f=filename
        m=mspace.Load(f)
        self.filename=f
        self.Load(m)
        self.groupBox.setTitle(f)
        self.Message('file{%s} loaded'%f)
        self.m.Check()
        self.btSearchClicked()
        
import sys
import time
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    Form = QtGui.QWidget()
    ui = mspaceExp()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
    time.sleep(5)
