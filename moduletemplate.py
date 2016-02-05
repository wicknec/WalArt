#! /usr/bin/env python3

"""
WaText
=======================

Deals with simple text processing

"""
# NOTE: the actual command documentation is collected from docstrings of the
# commands and is appended to __doc__ after the class has been defined.
"""
Revisions
=================
151102 added List
"""
import os

def List(obj):
        ''' List the contents of a list or dict
        
    '''
        result=''
        if isinstance(obj,list):
            result='List Contents:\n===================='
            for i in obj:
                result+='\n'+str(i)
        elif isinstance(obj,dict):
            result='Dict Contents:\n===================='
            for i in obj:
                result+='\n'+str(i)+' : '+str(obj[i])
        return result

class waText(object):

    def __init__(self):
        return

    def reset(self):
        bdb.Bdb.reset(self)
        self.forget()

    def forget(self):
        self.lineno = None
        self.stack = []
        self.curindex = 0
        self.curframe = None
        self.tb_lineno.clear()
