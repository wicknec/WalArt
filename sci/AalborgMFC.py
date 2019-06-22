# -*- coding: utf-8 -*-
"""
Created on Thu Jun 22 10:10:43 2017
    proxy for Aalborg MFC command module
    used for controlling mass flow controllers

reference: http://pyvisa.readthedocs.io/en/stable/tutorial.html

@author: wein1
Revisions:
    190617 repaired parsing for channels >2
    170630 added @py compatibility
    170629 added DEBUG mode
    170622 created
"""

import visa
try:
    rm=visa.ResourceManager()
except Exception:
    print('default ResourceManager is not availabe, trying @py')
    rm=visa.ResourceManager('@py')

DEBUG=False
import time

def pQuery(res, cmd):
    ''' print and query
    '''
    ans=res.query(cmd)
    if DEBUG:
        print('%.2f:%s>>>%s'%(time.clock(),cmd,ans))
    time.sleep(0.2) #wait for 0.1s to avoid timeout problem
    return ans

class MFC(object):
    '''
        proxy of a mass flow controller
        reference:http://www.aalborg.com/images/file_to_download/A_SDPROC%20Manual%20TD200310M%20RevE.pdf
    '''
    def  __init__(self,port,channel):
        print('Opening port {%s}'%port)
        self.r = rm.open_resource(port)
        
        self.channel = channel
    
    def SetPoint(self, percent):
        ''' set MFC to this percent of flow'''
        return pQuery(self.r,'SP %d %.1f' % (self.channel, percent))
    
    def Read(self):
        ''' read the percent of flow'''
        r=pQuery(self.r,'SD').split('%I  ')
        return float(r[self.channel-1][3:])
        
    def Close(self):
        ''' close gas valve'''
        return pQuery(self.r,'VM %d 0' % self.channel)
    def Auto(self):
        ''' resume MFC to setpoint'''
        return pQuery(self.r,'VM %d 1' % self.channel)
    def Open(self):
        ''' Open fully'''
        return pQuery(self.r,'VM %d 2' % self.channel)
        
        
    
