#! /usr/bin/env python3

"""
WaText
=======================

Deals with simple text processing

"""
# NOTE: the actual command documentation is collected from docstrings of the
# commands and is appended to __doc__ after the class has been defined.
"""
Revisions
=================
151102 added List
151129 modified *Brief* add str size
        add *ReadBrackets*
151205 modified *ReadBrackets*
        add *ReadLine*
151219 extended *Brief* for variable length
        add *atoi* ,*Escape*,*Unescape*
160112 add type judge for Brief
171207 fixed error reporting in brackets not paired
"""

def List(obj):
        ''' List the contents of a list or dict
        obj: a list or dict
    '''
        result=''
        if isinstance(obj,list):
            result='List Contents:\n===================='
            for i in obj:
                result+='\n'+str(i)
        elif isinstance(obj,dict):
            result='Dict Contents:\n===================='
            for i in obj:
                result+='\n'+str(i)+' : '+str(obj[i])
        return result

def NegComp(a,b):
        '''Returns if a<b, but -1 is defined to be larger than any positive number here
'''
        if a==-1:
                return False
        elif b==-1:
                return True
        else:
                return a<b
        
def ReadSimpleBrackets(s,brackets='[]',cur=0):
        '''Read the content inside the brackets, cur should be pointing to bracket[0]
s: string containing the brackets and contents
brackets: must be single char, e.g. '()','{}'
cur: cursor position to begin with

rtype:(content,lastCursor)
content: content without the brackets
lastCursor: last cursor position at the end of bracket

returns '' and cur doesn't move if no valid brackets are found
raises ValueError if brackets in s are not paired
'''
        if s[cur]!=brackets[0]:
                return ('',cur)
        org=cur
        minl=s.find(brackets[0],cur+1)
        minr=s.find(brackets[1],cur+1)
        depth=1
        lens=len(s)
        while cur<lens:
                if NegComp(minr,minl):
                        cur=minr
                        minr=s.find(brackets[1],cur+1)
                        depth-=1
                else:
                        if minr==-1:
                                #print('in reading {%s}'%s)
                                raise ValueError('brackets not paired in {'+s[:cur]+'}')
                        cur=minl
                        minl=s.find(brackets[0],cur+1)
                        depth+=1
                if depth==0:
                        break
        return s[org+1:cur],cur+1

def SkipUntil(s,sub,cur=0):
        '''Skip contents until the appearance of the substring.
If sub not encountered, return until end.
rType:(content,subPos)
'''
        org=cur
        cur=s.find(sub,org)
        if cur==-1:
                return s[org:],len(s)
        else:
                return s[org:cur],cur
def ReadLine(s,cur=0):
        '''Return the contents of current line(without \n symbol) and move the cursor to the start of next line
If string ends, return len(s) instead of new line cur
rType: (content,cur)
'''
        r,cur=SkipUntil(s,'\n',cur)
        if s[cur]=='\n':
                cur+=1
        return r,cur
        
def Brief(s,length=30):
        '''Reture the brief of string s for no more than *length*, for quick one-line review
'''
        if not isinstance(s,str):
                return s
        
        lens=len(s)
        
        if lens<length:
                return s
        else:
                mid='..'+str(lens)+'..'
                half=int((length-len(mid))/2)
                return s[0:half]+mid+s[-half:]

def ReadBrackets(s,brackets,cur=0):
        '''Read the content inside the brackets, cur should be pointing to bracket[0]
s: string containing the brackets and contents
brackets: e.g. ['<ID>','</ID>']
cur: cursor position to begin with

rtype:(content,lastCursor)
content: content without the brackets
lastCursor: last cursor position at the end of bracket

returns '' and cur doesn't move if no valid brackets are found
raises ValueError if brackets in s are not paired
'''
        if s[cur]!=brackets[0][0]:
                return ('',cur)
        org=cur
        minl=s.find(brackets[0],cur+1)
        minr=s.find(brackets[1],cur+1)
        lenl=len(brackets[0])
        lenr=len(brackets[1])
        depth=1
        lens=len(s)
        while cur<lens:
                if NegComp(minr,minl):
                        cur=minr
                        minr=s.find(brackets[1],cur+1)
                        depth-=1
                else:
                        if minr==-1:
                                raise ValueError('brackets not paired in {'+s[cur:]+'}')
                        cur=minl
                        minl=s.find(brackets[0],cur+1)
                        depth+=1
                if depth==0:
                        break
        return s[org+lenl:cur],cur+lenr
def atoi(s):
        '''returns an int if s can be parsed to one, else just return s
'''
        try:
                return int(s)
        except Exception:
                return s
def Escape(s,escs):
        '''Returns the escaped str , escs is a (unescaped,escaped) list, like:
escs=[('"',r'\q'),('\\',r'\\'),("'",r'\p'),('/',r'\s'),('\n',r'\r\n')]
the order should be carefully designed to achieve the right replacement
'''
        r=s
        for t in escs:
                r=r.replace(t[0],t[1])
        return r
def Unescape(s,escs):
        '''The reverse of Escape, note that the replacement is in reverse order of escs
'''
        unesc=escs[:]
        unesc.reverse()
        r=s
        for t in unesc:
                r=r.replace(t[1],t[0])
        return r
        
