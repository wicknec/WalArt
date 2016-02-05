#! /usr/bin/env python3

"""
WalArt.wiChart
=======================

Deals with device testing data processing

Counterpart of wiChart.m
Each wiChart object represents a multidimensional curve object
"""
# NOTE: the actual command documentation is collected from docstrings of the
# commands and is appended to __doc__ after the class has been defined.
"""
author: wicknec

Revisions
=================
160202 Created
160204 implemented FromTxt
"""
from WalArt import waFile, waText, alib
import numpy as np
import io

def From1500Csv(filename):
    '''
'''
    return
    
def From4200Xls(filename):
    '''
'''
    return

def FromTxt(filename):
    '''Read data from Csv with possible comments
compatible with regular csv
'''
    fo=open(filename)
    l=fo.readline()
    w=wiChart()
    while l.startswith('%'):
        ei=l.find('=')
        if ei!=-1:
            if l[1:ei].strip()!='':
                w.info.setValue(l[1:ei].strip(),l[ei+1:-1],'.')
        l=fo.readline()
    #now l should be at the begining of data
    #a possible header
    h=l.split(',')
    try:
        t=float(h[0])
        t=l
    except:
        w.info['names']=[i.strip() for i in h]
        t=''
    t+=''.join(fo.readlines())
    fo.close()
    w.info['filename']=filename
    w.info['name']=waFile.GetFilename(filename)
    #finished reading data
    d=np.loadtxt(io.StringIO(t),delimiter=',')
    if 'names' not in w.info:
        w.info.names=['data'+str(i+1) for i in range(len(d[1,:]))]
    for i in range(len(w.info['names'])):
        w.data[w.info['names'][i]]=d[:,i]
    return w

def New():
    ''' Returns an empty wiChart object
'''
    return wiChart()


class wiChart(object):
    ''' A wiChart object represents a curve object
The basic block for testing data
'''
    def __init__(self):
        self.info=alib()
        self.data=alib()
    def __str__(self):
        '''String brief '''
        info=self.info.keys()
        data=self.data.keys()
        l=len(self.GetData(0))
        return '''wiChart object:
info fields [%s]: %s
data fields [%s,%s]: %s
'''%(len(info),list(info),len(data),l,list(data))
    def GetData(self,entry):
        '''Get a row in wiChart specified by entry
entry can be the row number, or the column name
'''
        if isinstance(entry,int):
            return self.data[self.info['names'][entry]]
        else:
            return self.data[entry]
    def GetName(self,entry):
        if isinstance(entry,int):
            return self.info['names'][entry]
        else:
            return entry

#demo mode
if __name__ == '__main__':
    import time
    w=FromTxt('tests/test-wichart.txt')
    print(w)
    time.sleep(5)
    
