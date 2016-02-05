#! /usr/bin/env python3

"""
waFile
=======================

Deals with simple file processing

"""
# NOTE: the actual command documentation is collected from docstrings of the
# commands and is appended to __doc__ after the class has been defined.
"""
Revisions
=================
151104 LoadText, SaveText
151209 *Find*,*Join*
160202 *uigetfullfile*
"""
import os
import codecs
def LoadText(filename):
        '''Load text from *filename*
    '''
        f=codecs.open(filename, 'r')
        s=f.read()
        f.close()
        return s

def SaveText(filename,s):
        '''Save string *s* to filename
'''
        f=codecs.open(filename, 'w')
        s=f.write(s)
        f.close()
def GetFilename(fullfile):
        '''Get the file name from *fullfile* name
'''
        return os.path.split(fullfile)[-1]
def GetFolderName(fullfile):
        return os.path.dirname(fullfile)
def GetExtension(filename):
        '''Get the extension
'''
        f=GetFilename(filename)
        i=f.rfind('.')
        if i==-1:
                return ''
        else:
                return f[i:]
def Find(name):
        ''' Find and return the fullname within os.sys.path if the name exists
including .pth files
if not found, return None
'''
        for d in os.sys.path:
                if os.path.exists(os.path.join(d,name)):
                        return os.path.join(d,name);
                elif os.path.isdir(d):
                        #search .pth files
                        if d!='':
                                ds=os.listdir(d)
                        else:
                                ds=os.listdir()
                        for p in ds:
                                if GetExtension(p)=='.pth':
                                        d2=LoadText(os.path.join(d,p))
                                        if os.path.exists(os.path.join(d2,name)):
                                                return os.path.join(d2,name)
        return None
                                        
def Join(path,name):
        ''' os.path.join
'''
        return os.path.join(path,name)
import tkinter as tk
from tkinter import filedialog
def uigetfullfile(basefilename=''):
        '''Act like uigetfile in matlab, returned filename can be multiple
'''
        d=GetFolderName(basefilename)
        root=tk.Tk()
        root.withdraw()
        if len(d)>0:
                file=filedialog.askopenfilenames(initialdir=d)
        else:
                file=filedialog.askopenfilenames()
        fns=root.tk.splitlist(file)
        return fns
