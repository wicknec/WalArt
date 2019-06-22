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
160204 *Plot*,*Prettify*
160331 
"""
from matplotlib.pyplot import *
import matplotlib.cm as colormap
def Plot(x,y,ws,opt=None):
    '''Plot using x and y in ws
x and y specifies rows
ws is a list of wiCharts of the same type for multiple plot
opt:
  'plotType':plot
  
'''
    if not isinstance(ws,list):
        ws=[ws]
    if 'plotType' not in opt:
        opt['plotType']=plot
    l=[]
    colors=colormap.jet(np.linspace(0,1,len(ws)))
    i=0
    for w in ws:
        print(opt['plotType'])
        opt['plotType'](w.GetData(x),w.GetData(y),color=colors[i])
        #opt['plotType'](w.GetData(x),w.GetData(y))
        if 'name' in w.info:
            l.append(w.info['name'])
        hold(True)
        i+=1
        
    hold(False)
    if 'name' in ws[0].info:
        title(ws[0].info['name'])
    xlabel(ws[0].GetName(x))
    ylabel(ws[0].GetName(y))
    legend(l,loc='upperleft')
    show(block=False)
    return
dispNames={'Vd':'$V_d\mathrm{(V)}$', 'Vg':'$V_{gs}\mathrm{(V)}$',
           'Id': '$I_d\mathrm{(A)}$'}
def getDisplayName(name):
    return dispNames.get(name,name)
    
def Prettify():
    '''Set the figure to article ready
'''
    a=gca()
    a.set_xlabel(getDisplayName(a.get_xlabel()),fontsize=30)
    a.set_ylabel(getDisplayName(a.get_ylabel()),fontsize=30)
    for l in a.get_lines():
        print(l)
        l.set_linewidth(5)
    Show()
def PlaceLegend():
    '''
'''
    print('Click on figure')
    p=ginput()
    print(p[0])
    legend(loc=p[0])
    Show()
    
def Show():
    '''Show figure without blocking
'''
    return show(block=False)

    #demo mode
if __name__ == '__main__':
    import time
    from WalArt import wiChart
    w=wiChart.FromTxt('tests/test-wichart.txt')
    print(w)
    Plot(0,1,w)
    time.sleep(3)
