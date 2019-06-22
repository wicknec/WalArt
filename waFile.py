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
180211 updated .Join to support multiple paths, conform with os.path.join
180315 added uigetfulldir
180317 modifed Join to account for /
    fixed uigetfulldir
180318 fixed Join
180320 fixed Join again, 3.4.3 does not support (path,*name)
180408 use io instead of codecs for automatic \n conversion, also specify utf-8
"""
import os
import codecs
def LoadText(filename):
        '''Load text from *filename*
    '''
        #f=codecs.open(filename, 'r')
        import io
        with io.open(filename,'r',encoding='utf-8') as f:
                s=f.read()
        return s

def SaveText(filename,s):
        '''Save string *s* to filename
'''
        #f=codecs.open(filename, 'w')
        import io
        with io.open(filename,'w',encoding='utf-8') as f:
                s=f.write(s)

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
                                        
def Join(path,*name):
        ''' os.path.join
'''
        if '/' in path:
            names=[path]
            names.extend(name)
            return '/'.join(names)
        else:
            return os.path.join(path,*name)
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
    
def uigetfulldir(basename=''):
        #d=GetFolderName(basefilename)
        root=tk.Tk()
        root.withdraw()
        if basename:
                pth=filedialog.askdirectory(initialdir=basename)
        else:
                pth=filedialog.askdirectory()
        return pth
