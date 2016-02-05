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
"""


from PyQt4 import QtCore, QtGui
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
        self.verticalLayout.addWidget(self.widget)
        self.lbMessage = QtGui.QLabel(Form)
        self.lbMessage.setMinimumSize(QtCore.QSize(0, 30))
        self.lbMessage.setMaximumSize(QtCore.QSize(16777215, 30))
        self.lbMessage.setObjectName(_fromUtf8("lbMessage"))
        self.verticalLayout.addWidget(self.lbMessage)
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
        self.btLoad.setToolTip(_translate("Form", "Load default from mspace", None))
        self.btLoad.setText(_translate("Form", "", None))#
        self.lbTime.setText(_translate("Form", "Time", None))
        self.btExec.setToolTip(_translate("Form", "Execute with current argument", None))
        self.btExec.setText(_translate("Form", "", None))#
        self.btRun.setToolTip(_translate("Form", "Run current attribute as code", None))
        self.btRun.setText(_translate("Form", "", None))#
        self.btStop.setText(_translate("Form", "", None))#
        self.btStop.setToolTip(_translate("Form", "Stop", None))
        self.lbMessage.setText(_translate("Form", "  Minion-Automated Operating Program", None))

#=============Above are generated code==================#
from WalArt import mspaceExp,alib,waFile,waTool,waText
import time,sys
iconPath=waFile.GetFolderName(waFile.Find('add.png'))
global K,M
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

        QtCore.QObject.connect(self.btStop, QtCore.SIGNAL(_fromUtf8("clicked()")),
                               self.btStopClicked)
        QtCore.QObject.connect(self.btExec, QtCore.SIGNAL(_fromUtf8("clicked()")),
                               self.btExecClicked)
        QtCore.QObject.connect(self.btRun, QtCore.SIGNAL(_fromUtf8("clicked()")),
                               self.btRunClicked)
        QtCore.QObject.connect(self.btLoad, QtCore.SIGNAL(_fromUtf8("clicked()")),
                               self.btLoadClicked)
        
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Courier New"))
        font.setPointSize(12)
        self.lbTime.setFont(font)
        

        self.env=alib()
        self.env['maop']=self

        self.deskmin=waTool.minion('Desk')
        #self.clockmin.BeQuiet()
        self.deskmin.Assign(self.QueryRoutine)
        

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

    def UpdateMin(self):
        '''Update variables of workmin
'''
        global K,M
        M=self.workmin.mem=self.env
        K=self.workmin.knowledge=self.mspaceExp.m
        
    def ClockminRoutine(self):
        '''The method that will be constantly executed by the clockmin thread
'''
        while self.clockmin.summoned:
            self.UpdateMin()
            
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
        while True:
            self.busyWerk=True
            self.workmin.Assign('M["maop"].Q("%s")'%q)

            #block desk reception until Werk is not busy
            while self.busyWerk:
                time.sleep(1)
                
            q=sys.stdin.readline().rstrip()
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
            import sys
            import traceback
            traceback.print_exc()
            self.busyWerk=False
        
    def Exit(self):
        self.clockmin.Bye()
        self.workmin.Bye()
        self.deskmin.Bye()
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

    def btLoadClicked(self):
        if self.mspaceExp.m==None:
            from WalArt import mspace
            import os
            cwd=os.getcwd()
            f=os.path.join(cwd,'minKnow.msdx')
            if not os.path.exists(f):
                m=mspace.mspace()
                mspace.Save(f,m)
                print('The default file {%s} created'%f)
            self.mspaceExp.LoadFile(f)
        self.UpdateMin()
        self.workmin.Assign("exec(K.GetApp('maop')['!init'])")
    def btExecClicked(self):
        a=self.alibExp.GetCurrent()
        if a==None:
            print('Nothing to execute')
            return
        t=self.alibExp.GetSelectedText()
        global K
        if t not in K.nodes:
            print('The selection is not found in mspace, nothing to execute')
            return
        app=K.nodes[t].app
        if '!' not in app:
            print('The selection does not contain !code, nothing to execute')
            return
        M['exec']={'node':t,'args':a,'glbs':globals()}
        t=compile("K.GetApp(M['exec']['node'])('!',M['exec']['args'],M['exec']['glbs'])",'exec of %s in %s'%(a,t),'exec')
        self.Appoint(t)
            
        
import sys
import time
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    Form = QtGui.QWidget()
    ui = maopUi()
    ui.setupUi(Form)
    Form.setWindowTitle('maop')
    Form.setWindowIcon(QtGui.QIcon(waFile.Join(iconPath,'WicFam.png')))
    Form.show()
    sys.exit(app.exec_())
    #print('exited')
    time.sleep(5)
