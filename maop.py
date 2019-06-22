# -*- coding: utf-8 -*-
"""
maop
=======================

Qt4 interface for Minion-Automated Operating Program

To automate python and structurize codes and data

"""
# Form implementation generated from reading ui file 'maop.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!
"""
Revisions
=================
151214 ui established
151218 add workmin
151221 add ans function and *Query*, but why reference M gives an endless recursion? because ans... Solved.
151222 changed windowTitle and windowIcon
        add btLoadClicked
151224 Add blocking to Desk to fix help
151226 global K,M
151229 btExecClicked changed to execute with argument, add btRun for original btExec function
151230 extended *btLoadClicked*
160104 add *self.ui=Form* to enable messagebox
160115 fixed *self.btExecClicked*

160220 add *nodesView*
160602 modify load default to maopDefault file
160611 add self.btWorker, self.btWorkerClicked for debug
161105 add self.mnview, mspaceInterface for self.nview
161119 add Invoker and maopUi.invoker.Invoke(func,data) for letting main thread run code
        add maopUi.ResetMin
161124 introduce K,M as module singleton variable
161126 added Invoker.Exec for executing more codes and fixed peripherals
161129 add M['settings']
170228 add shortcut keys, HotKey
170308 added F1,F2,F3
171121 modified UpdateWorkmin to use M as global
171203 modified btWorkerClicked to run alib selected text with main thread
        modified UpdateMin to include M in M itself
180102 migrate to be compatible with PyQt5
180204 fixed mspace Load chain
180321 fixed exiting problem, fixed click text error problem
180426 modify execute button to run leaf name
    upgraded F123 to run with main thread, with args
    added args to btWorkerClicked, to align with K.f
181025 add try catch to exec to prevent exiting

"""
global K,M
#singleton module variable intended to share across modules
K=None #the knowledge a mspace object
M=None #the memory a dict

try:
    from PyQt4 import QtCore
    from PyQt4.QtCore import QTimer
    from PyQt4.QtGui import QApplication, QWidget
except ImportError or ModuleNotFoundError:
    print('PyQt4 module not found, try using PyQt5')
    from PyQt5 import QtCore
    from PyQt5.QtWidgets import QApplication, QWidget
    from PyQt5.QtCore import QTimer
from WalArt.gui.QtGui4or5 import QtGuiFinder
QtGui=QtGuiFinder()

#=============Below are generated code==================#
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(400, 600)
        self.verticalLayout = QtGui.QVBoxLayout(Form)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        
        self.widget = QtGui.QWidget(Form)
        self.widget.setMinimumSize(QtCore.QSize(0, 40))
        self.widget.setMaximumSize(QtCore.QSize(16777215, 40))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        
        self.btLoad = QtGui.QPushButton(self.widget)
        self.btLoad.setMinimumSize(QtCore.QSize(30, 30))
        self.btLoad.setMaximumSize(QtCore.QSize(30, 30))
        self.btLoad.setObjectName(_fromUtf8("btLoad"))
        self.horizontalLayout.addWidget(self.btLoad)
        self.lbTime = QtGui.QLabel(self.widget)
        self.lbTime.setObjectName(_fromUtf8("lbTime"))
        self.horizontalLayout.addWidget(self.lbTime)
        self.btExec = QtGui.QPushButton(self.widget)
        self.btExec.setMinimumSize(QtCore.QSize(30, 30))
        self.btExec.setMaximumSize(QtCore.QSize(30, 30))
        self.btExec.setObjectName(_fromUtf8("btExec"))
        self.horizontalLayout.addWidget(self.btExec)

        self.btRun = QtGui.QPushButton(self.widget)
        self.btRun.setMinimumSize(QtCore.QSize(30, 30))
        self.btRun.setMaximumSize(QtCore.QSize(30, 30))
        self.btRun.setObjectName(_fromUtf8("btRun"))
        self.horizontalLayout.addWidget(self.btRun)
        
        self.btStop = QtGui.QPushButton(self.widget)
        self.btStop.setMinimumSize(QtCore.QSize(30, 30))
        self.btStop.setMaximumSize(QtCore.QSize(30, 30))
        self.btStop.setObjectName(_fromUtf8("btStop"))
        self.horizontalLayout.addWidget(self.btStop)
        
        
        self.widget2 = QtGui.QWidget(Form)
        self.widget2.setMinimumSize(QtCore.QSize(0, 40))
        self.widget2.setMaximumSize(QtCore.QSize(16777215, 40))
        self.widget2.setObjectName(_fromUtf8("widget2"))
        #self.verticalLayout.addWidget(self.hLayout2)
        
        self.hLayout2 = QtGui.QHBoxLayout(self.widget2)
        self.hLayout2.setObjectName(_fromUtf8("hLayout2"))
        
        self.lbMessage = QtGui.QLabel(self.widget2)
        self.lbMessage.setMinimumSize(QtCore.QSize(100, 30))
        self.lbMessage.setMaximumSize(QtCore.QSize(16777215, 30))
        self.lbMessage.setObjectName(_fromUtf8("lbMessage"))
        self.hLayout2.addWidget(self.lbMessage)

        self.btNview = QtGui.QPushButton(self.widget2)
        self.btNview.setCheckable(True)
        self.btNview.setMinimumSize(QtCore.QSize(30, 30))
        self.btNview.setMaximumSize(QtCore.QSize(30, 30))
        self.btNview.setObjectName(_fromUtf8("btNview"))
        self.hLayout2.addWidget(self.btNview)

        self.btWorker = QtGui.QPushButton(self.widget2)
        #self.btWorker.setCheckable(True)
        self.btWorker.setMinimumSize(QtCore.QSize(30, 30))
        self.btWorker.setMaximumSize(QtCore.QSize(30, 30))
        self.btWorker.setObjectName(_fromUtf8("btWorker"))
        self.hLayout2.addWidget(self.btWorker)

        self.verticalLayout.addWidget(self.widget)
        self.verticalLayout.addWidget(self.widget2)
        
        self.line = QtGui.QFrame(Form)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.verticalLayout.addWidget(self.line)
        self.wMspace = QtGui.QWidget(Form)
        self.wMspace.setObjectName(_fromUtf8("wMspace"))
        self.verticalLayout.addWidget(self.wMspace)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.btLoad.setToolTip(_translate("Form", "Load default", None))
        self.btLoad.setText(_translate("Form", "", None))#
        self.lbTime.setText(_translate("Form", "Time", None))
        self.btExec.setToolTip(_translate("Form", "Execute with current argument", None))
        self.btExec.setText(_translate("Form", "", None))#
        self.btRun.setToolTip(_translate("Form", "Run current attribute as code", None))
        self.btRun.setText(_translate("Form", "", None))#
        self.btStop.setText(_translate("Form", "", None))#
        self.btStop.setToolTip(_translate("Form", "Stop", None))
        self.lbMessage.setText(_translate("Form", "  Minion-Automated Operating Program", None))
        self.btNview.setToolTip('Diagram view')
        self.btWorker.setToolTip('Run selected alib text once using main thread')
#=============Above are generated code==================#
from WalArt import mspaceExp,alib,waFile,waTool
import time,sys
iconPath=waFile.GetFolderName(waFile.Find('add.png'))

    
class Invoker(QtCore.QObject):
    '''signal other class to execute the code,
    connect sigInvoke to a function that can take a func and args.
    '''
    sigInvoke=QtCore.pyqtSignal(object,object)
    previousCode=None
    bondSlot=None
    def Invoke(self,func,args):
        '''Execute a function func with args
        '''
        self.sigInvoke.emit(func,args)
    def Exec(self,local):
        '''A function that can be passed for invoking
        takes an argument as locals
        So most codes can be executed by invoke
        '''
        exec(self.previousCode,globals(),local)
    def Connect(self,slot):
        '''Connect the invoker to a slot function that executes func(args)
        '''
        self.sigInvoke.connect(slot)
        self.bondSlot=slot
        
    def Do(self,code,local=None):
        '''
        '''
        if not local:
            local=locals()
        self.previousCode=code
        self.sigInvoke.emit(self.Exec,local)
class HotKey(object):
    def __init__(self):
        self.reg=dict()
        #reg stores registered hotkeys as keySequence:code
        self.justPressed=None
        #The hotkey just pressed
    def Register(self,keySequence,parentWindow,code):
        QtGui.QShortcut(QtGui.QKeySequence(keySequence), parentWindow, self.close)
        self.reg[keySequence]=code
        
        
class maopUi(Ui_Form):
    def setupUi(self,Form):
        super(maopUi,self).setupUi(Form)
        self.ui=Form
        self.mspaceExp=mspaceExp.mspaceExp()
        self.mspaceExp.setupUi(self.wMspace)
        self.alibExp=self.mspaceExp.alibUi

        self.btLoad.setIcon(QtGui.QIcon(waFile.Join(iconPath,'import.png')))
        self.btExec.setIcon(QtGui.QIcon(waFile.Join(iconPath,'execute.png')))
        self.btRun.setIcon(QtGui.QIcon(waFile.Join(iconPath,'go.png')))
        self.btStop.setIcon(QtGui.QIcon(waFile.Join(iconPath,'no.png')))
        self.btNview.setIcon(QtGui.QIcon(waFile.Join(iconPath,'image.png')))
        self.btWorker.setIcon(QtGui.QIcon(waFile.Join(iconPath,'minion.jpg')))
        #self.btWorker.setChecked(True)


        #QtCore.QObject.connect(self.btStop, QtCore.SIGNAL(_fromUtf8("clicked()")),self.btStopClicked)
        self.btStop.clicked.connect(self.btStopClicked)
        
        #QtCore.QObject.connect(self.btExec, QtCore.SIGNAL(_fromUtf8("clicked()")),self.btExecClicked)
        self.btExec.clicked.connect(self.btExecClicked)
        #QtCore.QObject.connect(self.btRun, QtCore.SIGNAL(_fromUtf8("clicked()")),self.btRunClicked)
        self.btRun.clicked.connect(self.btRunClicked)
        #QtCore.QObject.connect(self.btLoad, QtCore.SIGNAL(_fromUtf8("clicked()")),self.btLoadClicked)
        self.btLoad.clicked.connect(self.btLoadClicked)
        
        #QtCore.QObject.connect(self.btNview, QtCore.SIGNAL(_fromUtf8("clicked()")),self.btNviewClicked)
        self.btNview.clicked.connect(self.btNviewClicked)
        
        #QtCore.QObject.connect(self.btWorker, QtCore.SIGNAL(_fromUtf8("clicked()")),self.btWorkerClicked)
        self.btWorker.clicked.connect(self.btWorkerClicked)
        
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Courier New"))
        font.setPointSize(12)
        self.lbTime.setFont(font)
        

        self.env=alib()
        self.env['maop']=self
        self.env['settings']=alib() #store general settings

        self.deskmin=waTool.minion('Desk')
        #self.clockmin.BeQuiet()
        self.deskmin.Assign(self.QueryRoutine)
        #self.deskmin.reflex=0.5
        

        self.workmin=waTool.minion('Werk')
        self.workmin.standby=.5
        self.workmin.reflex=1
        self.workmin.Go()


        self.clockmin=waTool.minion('Clock')
        self.clockmin.BeQuiet()
        self.clockmin.mem=alib() #this serves as the timed task list
        self.timedTask=self.clockmin.mem
        self.UpdateTimeToolTip()
        self.clockmin.Assign(self.ClockminRoutine)
        self.clockmin.Go()
        time.clock()


        
        print(self.workmin.Say('We are pure robots!'))
        print(self.clockmin.Say('We extend our advantage!'))
        print(self.deskmin.Say('How can we help you?'))
        self.busyWerk=True
        self.deskmin.Go()

        self.initNodesView()
        
        self.invoker=Invoker()
        self.invoker.Connect(self.GuiDo)
        
        QtGui.QShortcut(QtGui.QKeySequence('F1'), Form, self.F1)
        QtGui.QShortcut(QtGui.QKeySequence('F2'), Form, self.F2)
        QtGui.QShortcut(QtGui.QKeySequence('F3'), Form, self.F3)

        self.UpdateMin()
        
        def printM():
            return 'M is the memory of the minion'
        M.__str__=printM
        
        self.mspaceExp.FuncItemDropped=self.LoadMspace
        
        #self.ui.actionExit.triggered.connect(self.ui.close)
        def close(event):
            #the close event for the form
            print('To close the program, type "quit" in the terminal, otherwise the program would not quit completely because of the stdin')
            event.ignore()
        Form.closeEvent=close
        
    def F1(self):
        key='F1'
        print('%s fired'%key)
        if key not in self.env['settings']:
            print('but code not set in M.settings, nothing to run')
            return
        #a=self.alibExp.treeWidget.data
        code=self.env['settings'][key]
        print('Executing with Main thread...')
        self.invoker.Do(code,{'K':K,'M':M,'args':None})

    def F2(self):
        key='F2'
        print('%s fired'%key)
        if key not in self.env['settings']:
            print('but code not set in M.settings, nothing to run')
            return
        #a=self.alibExp.treeWidget.data
        code=self.env['settings'][key]
        print('Executing with Main thread...')
        self.invoker.Do(code,{'K':K,'M':M,'args':None})
    def F3(self):
        key='F3'
        print('%s fired'%key)
        if key not in self.env['settings']:
            print('but code not set in M.settings, nothing to run')
            return
        #a=self.alibExp.treeWidget.data
        code=self.env['settings'][key]
        print('Executing with Main thread...')
        self.invoker.Do(code,{'K':K,'M':M,'args':None})
        

    def UpdateMin(self):
        '''Update variables of workmin
'''
        global K,M
        M=self.workmin.mem=self.env
        K=self.workmin.knowledge=self.mspaceExp.m
        M['K']=K
        M['M']=M #this might cause some problem, but crucial
        
        
    def ClockminRoutine(self):
        '''The method that will be constantly executed by the clockmin thread
'''
        while self.clockmin.summoned:
            self.UpdateMin()
            
            #self.invoker.Invoke(self.lbTime.setText,time.ctime())
            self.lbTime.setText(time.ctime())
            time.sleep(1)
            

            for k in self.timedTask:
                if eval(self.timedTask[k]['trigger']):
                    self.workmin.Assign(self.timedTask[k]['task'])
                    self.timedTask.Pop(k)
                    self.UpdateTimeToolTip()
            
    def QueryRoutine(self):
        print('\n?')
        q=sys.stdin.readline().rstrip()
        while q!='quit':
            self.busyWerk=True
            if len(q)>0:
                self.workmin.Assign('M["maop"].Q("%s")'%q)

            #block desk reception until Werk is not busy
            while self.busyWerk:
                time.sleep(1)
                
            q=sys.stdin.readline().rstrip()
        if q=='quit':
            self.Quit()
            
    def Q(self,q):
        '''Used by the query routine above, write result to M['ans'] and display it
'''
        global K,M
        try:
            ans=eval(q)
            if ans is self.env:
                ans='M is the memory of the minion'
            self.env['ans']=ans
            print('%s\n?'% ans)
            self.busyWerk=False
        except Exception as e:
            import traceback
            traceback.print_exc()
            self.busyWerk=False
    def GuiDo(self,func,args):
        '''For invoke, let the main thread (GUI thread) to set widgets,
        Otherwise it will cause program to crash
        '''
        try:
            func(args)
        except Exception as e:
            import traceback
            print('Some went wrong when executing custom code:')
            traceback.print_exc()
            
    def ResetMin(self):
        self.workmin.Bye()
        self.workmin=waTool.minion('Werk')
        self.workmin.standby=.5
        self.workmin.reflex=1
        self.workmin.Go()
        
    def Exit(self):
        #exit the minions
        self.clockmin.BeQuiet(False)
        self.clockmin.Bye()
        self.workmin.Bye()
        self.deskmin.Bye()
        self.deskmin.WhatRuDoing()
    def Quit(self):
        #quit the program
        return
        
    def btStopClicked(self):
        self.workmin.Stop()
        self.clockmin.mem.clear()
        print(self.clockmin.Say('Timed task cleared'))
        self.UpdateTimeToolTip()
        
    def btRunClicked(self):
        a=self.alibExp.GetCurrent()
        if a==None:
            print('Nothing to execute')
        else:
            self.Appoint(a)
            
    def Appoint(self,data):
        '''Appoint tasks.
if data is a string, execute immediately
if data is an alib with field 'trigger' and 'task', then add to timed task list for execution
if data is an alib with field 1,2,3 execute in sequence
'''
        if isinstance(data,alib):
            if 'trigger' in data:
                self.timedTask.Append(data)
                self.UpdateTimeToolTip()
                print(self.clockmin.Say('a task{%s} is appointed'%data['trigger']))
            else:
                self.workmin.Assign(data)
        else:
            self.workmin.Assign(data)
            #raise ValueError('The data(%s) is incorrect'%str(data))
    def UpdateTimeToolTip(self):
        '''Update mainly to signify the contents of timed tasks
'''
        tt='Timed Task: %s\n========================\n'%len(self.timedTask)
        for k in self.timedTask:
            tt+='%s: trigger=%s\n'%(k,self.timedTask[k]['trigger'])
        self.lbTime.setToolTip(tt)
        
    def LoadMspace(self,filename):
        self.mspaceExp.LoadFile(filename)
        self.UpdateMin()
        self.mnview.setMindSpace(self.mspaceExp.m)
        self.workmin.Assign("exec(K.GetApp('maop')['!init'])")
        
    def btLoadClicked(self):
        if self.mspaceExp.m==None:
            #from WalArt import mspace
            import os
            cwd=os.getcwd()
            f=os.path.join(cwd,'maopDefault')
            if not os.path.exists(f):
                s='''[DefaultSpace|]
'''
                import WalArt.waFile as wf
                wf.SaveText(f,s)
                print('The default file {%s} created'%f)
            a=alib()
            a.Load(f)
            M['settings']=a
            if 'DefaultSpace' in a and a['DefaultSpace']:
                path=a['DefaultSpace']
                paths=path.split('\\')
                self.LoadMspace(os.path.join(*paths))
            else:
                print('The default space file %s is incorrect, please check maopDefault'%a)
    def btExecClicked(self):
        ''' This is the button of execute with current argument'''
        a=self.alibExp.GetCurrent()
        if a==None:
            print('Nothing to execute')
            return
        t=self.alibExp.GetSelectedText() #this is the selected path
        if '|' in t:
            t=t.split('|')[-1] #get the leaf name
            
        global K
        if t not in K.nodes:
            print('The selection is not found in mspace, nothing to execute')
            return
        app=K.nodes[t].app
        if '!' not in app:
            print('The selection does not contain !code, nothing to execute')
            return
        M['exec']={'attribute':t,'caller':self.alibExp.treeWidget.data,
                    'args':a,'glbs':globals()}
        t=compile("K.GetApp(M['exec']['attribute'])('!',M['exec']['args'],M['exec']['glbs'])",'exec of %s in %s'%(a,t),'exec')
        self.Appoint(t)
    def initNodesView(self):
        '''Initiate nodes view and related function
'''
        from WalArt.diagram import nodesView
        self.nview=nodesView.MainWindow(QtGui.QWidget)
        self.nview.setWindowIcon(QtGui.QIcon(waFile.Join(iconPath,'WicFam.png')))
        self.mnview=nodesView.mspaceInterface(self.mspaceExp.m,self.nview)
        def viewClose(qcloseevent):
            self.btNview.setChecked(False)
        self.nview.closeEvent=viewClose
        def nodeDoubleClicked(index):
            #print(s)
            item=self.mspaceExp.lwNode.itemFromIndex(index)
            #help(item)
            tag=item.text()
            n=self.mspaceExp.m.nodes[tag]
            self.ShowNview()
            self.mnview.Explore(tag)
        #QtCore.QObject.connect(self.mspaceExp.lwNode, QtCore.SIGNAL(_fromUtf8("doubleClicked(QModelIndex)")),nodeDoubleClicked)
        self.mspaceExp.lwNode.doubleClicked.connect(nodeDoubleClicked)
        
        def exploreItem(i):
            if isinstance(i,str):
                #should be a node name
                n=self.mspaceExp.m.nodes[i]
                self.mspaceExp.nodeClicked(n)
            else:
                #should be a link number
                l=self.mspaceExp.m.links[i]
                self.mspaceExp.linkClicked(l)
        self.nview.itemExplored=exploreItem
    def ShowNview(self):
        self.nview.show()
        self.btNview.setChecked(True)
    def HideNview(self):
        self.nview.hide()
        self.btNview.setChecked(False)
    def btNviewClicked(self):
        #print(self.btNview.isChecked())
        if self.btNview.isChecked():
            self.nview.show()
        else:
            self.nview.hide()
            
    def btWorkerClicked(self):
        ''' the button with an minion icon'''
        a=self.alibExp.treeWidget.data
        code=a.getValue(self.alibExp.GetSelectedText())
        print('Executing with Main thread...')
        try:
            self.invoker.Do(code,{'K':K,'M':M,'this':a,'args':None})
        except Exception as e:
            import traceback
            traceback.print_exc()
        
        
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    Form = QtGui.QWidget()
    ui = maopUi()
    ui.setupUi(Form)
    Form.setWindowTitle('maop')
    Form.setWindowIcon(QtGui.QIcon(waFile.Join(iconPath,'WicFam.png')))
    Form.show()
    def close(event=None):
        ui.Exit()
        Form.close()
        if event:
            event.accept()
        app.quit()
        
    ui.Quit=close
    sys.exit(app.exec_())
    #print('exited')
    time.sleep(5)
