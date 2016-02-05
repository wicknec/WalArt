'''
waTool
=============================
Walnut Artifacts

Created by wicknec

Tools that can be used by minions
and of course, humans can also use them

'''

'''
Revisions for package main file:
==============================
151102 minion
151110 *DontStop* for continuous running, *Stop* to clear all tasks
151111 *reflex* for controlling execution speed
151121 changed *GoToWork* to *Go*, the simple the better
151219 modified *Assign*
160131 add tasklock
'''
__all__ = ['minion','SysOp']

import threading
import time
import WalArt.waText
from WalArt import alib
class minion(threading.Thread):
    '''
Simple automata that can move by itself.
Occupies a thread
FUNCTIONS:
    Say(s)
    Equip(tool)
    Go()
    DontStop(tasks)
    Assign(tasks)
'''
    Counter=1
    def __init__(self,name='',BeQuiet=False):
        '''Converts a dict to corresponding alib by converting its keys and values to strings
'''
        threading.Thread.__init__(self)
        
        self.mem=None
        self.knowledge=None
        
        if len(name)==0:
            self.name='Minion#'+str(minion.Counter)
        else:
            self.name=name
        self.task=[]#current tasks
        self.tasklock=threading.Lock()
        
        self.ctask=[]#tasks that is set to continuously doing
        
        self.quiet=BeQuiet
        self.reflex=0 #seconds to wait for next task
        self.summoned=True #If false, stop running
        
        #Enters standby when all tasks are done instead of terminating
        #=False for no standby, =float for seconds to wait until next round
        self.standby=False

        if not self.quiet:
            print(self.Say("Hello!"))
        minion.Counter+=1
        
    def Say(self,s):
        '''Generates speech for the minion.
    s: Things to say
    rType: str
'''
        saying=self.name+'['+time.ctime()+'] : '+s
        return saying
    def Equip(self,tool):
        '''Equip the minion with a tool so that it can use
'''
        pass
        return
    def Go(self):
        '''Same as Thread.start()
'''
        self.start()
    def DontStop(self,t):
        '''Tell the minion to do these tasks continuously
'''
        self.ctask=t
        self.task=t[:]
        self.start()
    def BeQuiet(self,quiet=True):
        self.quiet=quiet
    def run(self): #Overwrite Thread.run
        '''This function is executed automatically on self.start()
'''
        while self.summoned>0:
            if len(self.task)>0:
                self.DoTask(self.PopTask())
                if len(self.task)==0 and len(self.ctask)!=0 and self.summoned:
                    self.task=self.ctask[:]
            else:
                if self.standby:
                    self.Wait(self.standby)
                else:
                    self.summoned=False
                    
        if not self.quiet:
            print(self.Say('Good bye!'))
    def Stop(self):
        '''Stop the minion
'''
        self.task.clear()
        self.ctask.clear()
        if not self.quiet:
            print(self.Say('Stopped'))
        
    def Bye(self):
        '''Stop the minion, and unsummon it
'''
        self.Stop()
        self.summoned=False

    def DoTask(self,t):
        '''Called by run() t is the task
'''
        #short hand
        M=self.mem
        K=self.knowledge
        
        if self.quiet==False:
            print(self.Say("Doing task: "+WalArt.waText.Brief(str(t))))
        try:
            if hasattr(t,'__call__'):
                t()
            else:
                exec(t)
        except Exception as e:
            import sys
            import traceback
            traceback.print_exc()
        if self.reflex>0:
            time.sleep(self.reflex)

    def Assign(self,s):
        '''Assign tasks to minion, task can be a function or text command
If s is a string
        a function , add directly
        an alib, add the numeric content as tasks to the front
'''
        self.tasklock.acquire()
        if isinstance(s,alib):
            l=s.ToList()
            self.task=l+self.task
        else:
            self.task.append(s)
        self.tasklock.release()
        return
    def Wait(self,seconds):
        '''Let the minion wait
'''
        time.sleep(seconds)
    def PopTask(self):
        '''Pop task with thread safe
'''
        self.tasklock.acquire()
        t=self.task.pop(0)
        self.tasklock.release()
        return t
        
