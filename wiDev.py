#! /usr/bin/env python3

"""
WalArt.wiDev
=======================
wicknec@2016

Customized plot involving wiChart
for processing nanodevice test data
functions related to specific device processing

"""
# NOTE: the actual command documentation is collected from docstrings of the
# commands and is appended to __doc__ after the class has been defined.
"""
Revisions
=================
160202 created
160204 *Plot*,*Prettify*
"""
import numpy as np
from WalArt import wiChart
def SeparateSteps(wo):
    ''' Separate acquired Output curves by gate voltage steps into multiple wiCharts
'''
    Vgs=np.unique(wo.data['Vg'])
    ws=[]
    for V in Vgs:
        w=wiChart.New()
        w.info=wo.info.copy()
        w.info['name']='$V_{gs}=\ %s\ \mathrm{V}$'%V
        w.info['Vgs']=V
        w.info['allvar']=2
        cond=lambda x: x==V
        indices=wiChart.Find(wo.data['Vg'],cond)
        w.info['names']=['Vd','Id']
        w.data['Vd']=[wo.data['Vd'][i] for i in indices]
        w.data['Id']=[wo.data['Id'][i] for i in indices]
        ws.append(w)
    return ws
    
    #demo mode
if __name__ == '__main__':
    import time
    from WalArt import wiChart
    from wiPlot import *
    w=wiChart.FromTxt('tests/test-Output.txt')
    print(w)
    ws=SeparateSteps(w)
    Plot(0,1,ws)
    Prettify()
    time.sleep(3)
