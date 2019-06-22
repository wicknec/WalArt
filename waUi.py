#! /usr/bin/env python3

"""
waUi
=======================

Deals with simple dialogs

"""
# NOTE: the actual command documentation is collected from docstrings of the
# commands and is appended to __doc__ after the class has been defined.
"""
Revisions
=================
151102 added List
"""
from tkinter import *

def uiSelectOne(options,prompt=''):
    '''Return the index of selection
    '''
    root = Tk()    
    users=options
    var=IntVar()
    var.initialize(0)
    Label(root,text=prompt+'\nChoose').pack()
    def quitf():
        root.quit()
        root.destroy()
    for x in range(len(users)):
        l = Radiobutton(root, text=users[x], variable=var,value=x,command=quitf)
        l.pack(anchor = 'w')
        
    root.mainloop()
    return var.get()
    #print(users[ans])
if __name__=='__main__':
    import time
    i=uiSelectOne(['A','B','C'],'Test')
    print(i)
    time.sleep(5)