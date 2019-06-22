#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  3 14:29:12 2017

@author: wicknec

For compatibility from PyQt4 to PyQt5
"""
state=0
VERBOSE=False

try:
    from PyQt4 import QtGui as QtGui4
    from PyQt4 import Qt
    state=4
except ModuleNotFoundError:
    from PyQt5 import QtGui as QtGui5
    from PyQt5 import QtWidgets
    from PyQt5 import Qt
    state=5
    
class QtGuiFinder:
    def __init__(self):
        self.state=0
        
    def __getattr__(self,attr):
        #print('get attr called with attr=%s'%attr)
        if state==4:
            return eval('QtGui4.%s'%attr)
        else:
            try: 
                return eval('QtGui5.%s'%attr)
            except AttributeError:
                if VERBOSE:
                    print('%s not found in QtGui5, trying QtWidget...'%attr)
                return eval('QtWidgets.%s'%attr)
    def getVersion(self):
        return state