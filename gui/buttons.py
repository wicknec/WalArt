#! /usr/bin/env python3

"""
WalArt.gui.buttons
=======================

Special buttons

"""
# NOTE: the actual command documentation is collected from docstrings of the
# commands and is appended to __doc__ after the class has been defined.
"""
Revisions
=================
151209 btLock
"""
from PyQt4 import QtGui,QtCore
from WalArt import waFile
from WalArt import waFile
iconPath=waFile.GetFolderName(waFile.Find('add.png'))
class btLock(QtGui.QToolButton):

    def __init__(self,container):
            super(btLock,self).__init__(container)
            self.imgLock=QtGui.QIcon(waFile.Join(iconPath,'lock.png'))
            self.imgUnlock=QtGui.QIcon(waFile.Join(iconPath,'unlock.png'))
            self.setIcon(self.imgLock)
            #state==True means locked
            self.state=True

    def setState(self,s):
            ''' set the state of the button to locked(True) or unlocked(False)
'''
            self.state=s
            if self.state==True:
                    self.setIcon(self.imgLock)
            else:
                    self.setIcon(self.imgUnlock)

    def getState(self):
            return self.state
            
            

