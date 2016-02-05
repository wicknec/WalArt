#! /usr/bin/env python3

"""
WalArt.wiPlot
=======================
wicknec@2016

Customized plot involving wiChart
for processing nanodevice test data
and draw reasonably pretty figures

"""
# NOTE: the actual command documentation is collected from docstrings of the
# commands and is appended to __doc__ after the class has been defined.
"""
Revisions
=================
160202 created
"""
from matplotlib.pyplot import *
def Plot(x,y,ws,opt=[]):
    '''Plot using x and y in ws
x and y specifies rows
ws is a list of wiCharts of the same type for multiple plot
'''
    if not isinstance(ws,list):
        ws=[ws]
    l=[]
    for w in ws:
        plot(w.GetData(x),w.GetData(y))
        if 'name' in w.info:
            l.append(w.info['name'])
        hold(True)
        
    hold(False)
    if 'name' in ws[0].info:
        title(ws[0].info['name'])
    xlabel(ws[0].GetName(x))
    ylabel(ws[0].GetName(y))
    legend(l)
    show(block=False)
    return

def Prettify():
    '''Set the figure to article ready
'''
    a=gca()
    a.set_xlabel(a.get_xlabel(),fontsize=30)
    a.set_ylabel(a.get_ylabel(),fontsize=30)
    
    #demo mode
if __name__ == '__main__':
    import time
    from WalArt import wiChart
    w=wiChart.FromTxt('E:/InnerFantasia/_mylib/python34/test-wichart.txt')
    print(w)
    Plot(0,1,w)
    time.sleep(5)
