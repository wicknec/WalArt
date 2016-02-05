#! /usr/bin/env python3

"""
mspace
=======================

a structure for a certain graph

"""
# NOTE: the actual command documentation is collected from docstrings of the
# commands and is appended to __doc__ after the class has been defined.
"""
Revisions
=================
151126 [node,link].ToString()
151205 mspace.[ToString(),FromString()]
    *Check*, *GetRelation*, *GetApp*
151218 repaired *Check*, add *mspace.NewNode*
    repaired *escs*
151221 *FindLinksByAttribute*,*RemoveLink*,*Ren*
151222 *str(link)*,modified *mspace.NewLink*,
    fixed *FindNodesByName* *FindLinksByAttribute*
151223 Add *Call*
151226 *link.setAtt*
151229 fixed *Call*
151229 fixed *Call* to return ans
160114 removed *Call* moved it to alib
"""

from WalArt import alib,waText,waFile

import re,time
    
import codecs
def Load(filename):
    '''Returns the mspace of given filename
'''
    f=codecs.open(filename, 'r','utf-8')
    s=f.read()
    f.close()

    r=mspace()
    r.FromString(s)
    return r

def Save(filename,m):
    s=m.ToString()
    
    f=codecs.open(filename, 'w','utf-8')
    s=f.write(s)
    f.close()


    
#unescaped,escaped
escs=[('\\',r'\\'),('\n',r'\r\n'),('"',r'\q'),("'",r'\p'),('/',r'\s')]
import xml.sax.saxutils as sx
desc=dict() #the escape dictionary and...
dune=dict() #the unescape dictionary
for i in escs:
    desc[i[0]]=i[1]
    dune[i[1]]=i[0]
def Escape(s):
    '''Escape < & > \ characters for xml
'''
    r=sx.escape(s)
    return waText.Escape(r,escs)
def Unescape(s):
    '''Unescape < & > \ characters for xml
'''
    r=waText.Unescape(s,escs)
    return sx.unescape(r)

class alphiter(object):
    ''' iterator for dict with str keys: in alphabetical order
'''
    def __init__(self,A):
        self.a=A
        self.list=list(A.keys())
        self.list.sort()

    def __next__(self):
        if len(self.list)==0:
            raise StopIteration
        else:
            return self.list.pop(0)
    def __iter__(self):
        return self

    
class node(object):
    def __init__(self,Tag='',App=''):
        self.tag=Tag
        self.app=alib().FromString(App) #in alib format
        self.links=[]
    def ToString(self,serial=0):
        '''To xml string
'''
        if serial==0:
            r='<PNL>\n'
        else:
            r='<PNL serial=%d>\n' % serial
        r+=\
        '<TAG>'+Escape(self.tag)+'</TAG>\n'+\
        '<APP>'+Escape(str(self.app))+'</APP>\n'+\
        '<LINK>'+' '.join(map(str,self.links))+'</LINK>\n'+\
        '</PNL>\n'
        return r
    def FromString(self,s):
        t,cur=waText.SkipUntil(s,'<TAG>')
        self.tag,cur=waText.ReadBrackets(s,('<TAG>','</TAG>'),cur)
        self.tag=Unescape(self.tag)
        t,cur=waText.SkipUntil(s,'<APP>')
        t,cur=waText.ReadBrackets(s,('<APP>','</APP>'),cur)
        self.app=alib().FromString(Unescape(t))
        t,cur=waText.SkipUntil(s,'<LINK>')
        t,cur=waText.ReadBrackets(s,('<LINK>','</LINK>'),cur)
        if t=='':
            self.links=[]
        else:
            self.links=[]
            t=t.split(' ')
            for l in t:
                if l!='':
                    self.links.append(int(l))
        return self

class link(object):
    def __init__(self,Id=0,Src='',Dst='',Att='',App='',Str=1):
        self.id=Id
        self.src=Src
        self.dst=Dst
        self.att=Att
        self.app=App #in alib format
        self.str=Str #in number
    def __str__(self):
        return self.Brief()
    
    def ToString(self):
        '''To xml string
'''
        r='<PLL>\n'+\
        '<ID>'+str(self.id)+'</ID>\n'+\
        '<A>'+Escape(self.src)+'</A>\n'+\
        '<B>'+Escape(self.dst)+'</B>\n'+\
        '<ATTRIBUTE>'+Escape(self.att)+'</ATTRIBUTE>\n'+\
        '<lTAG>'+Escape(str(self.app))+'</lTAG>\n'+\
        '<STR>'+str(self.str)+'</STR>\n'+\
        '</PLL>\n'
        return r
    def FromString(self,s):
        t,cur=waText.SkipUntil(s,'<ID>')
        t,cur=waText.ReadBrackets(s,('<ID>','</ID>'),cur)
        self.id=int(t)
        t,cur=waText.SkipUntil(s,'<A>')
        t,cur=waText.ReadBrackets(s,('<A>','</A>'),cur)
        self.src=Unescape(t)
        t,cur=waText.SkipUntil(s,'<B>')
        t,cur=waText.ReadBrackets(s,('<B>','</B>'),cur)
        self.dst=Unescape(t)
        t,cur=waText.SkipUntil(s,'<ATTRIBUTE>')
        t,cur=waText.ReadBrackets(s,('<ATTRIBUTE>','</ATTRIBUTE>'),cur)
        self.att=Unescape(t)
        t,cur=waText.SkipUntil(s,'<lTAG>')
        t,cur=waText.ReadBrackets(s,('<lTAG>','</lTAG>'),cur)
        self.app=alib().FromString(Unescape(t))
        t,cur=waText.SkipUntil(s,'<STR>')
        t,cur=waText.ReadBrackets(s,('<STR>','</STR>'),cur)
        self.str=int(t)
        return self
    def Brief(self,relatedName=''):
        '''Return a brief text representing the link
'''
        n=relatedName
        if n==self.src:
            return '--%s->%s'%(self.att,self.dst)
        elif n==self.dst:
            return '<-%s--%s'%(self.att,self.src)
        else:
            return '%s--%s->%s'%(self.src,self.att,self.dst)
    def setAtt(self,att):
        self.att=att
        
class mspace(object):
    ''' A directed concept graph
It is recommended that you only use member functions to access the mspace, to guarantee its consistency.
'''
    def __init__(self):
        self.nodes=dict()
        self.links=[link()]
        self.comment=''
        self.blankId=[]
    def ToString(self):
        s='<?Mind Space Document XML format UTF-8?>\n'
        s+='<comment>%s</comment>\n' % self.comment

        s+='<PNLbank>\n'
        i=1
        for n in alphiter(self.nodes):
            s+=self.nodes[n].ToString(i)
            i+=1
        s+='</PNLbank>\n\n'

        s+='<PLLbank>'
        s+='<BLANK_ID>%s</BLANK_ID>\n' % ' '.join(map(str,self.blankId))
        for l in self.links:
            s+=l.ToString()
        s+='</PLLbank>'
        return s
    def FromString(self,s):
        self.nodes=dict()
        self.links=[] #the zero-Id link is a constant
        t,cur=waText.SkipUntil(s,'<comment>')
        self.comment,cur=waText.ReadBrackets(s,('<comment>','</comment>'),cur)

        t,cur=waText.SkipUntil(s,'<PNLbank>')
        t,cur=waText.ReadBrackets(s,('<PNLbank>','</PNLbank>'),cur)
        lent=len(t)
        t2,cur2=waText.SkipUntil(t,'<PNL')
        
        while cur2<lent:
            t2,cur2=waText.ReadBrackets(t,('<PNL','</PNL>'),cur2)
            tn=node()
            tn.FromString(t2)
            self.nodes[tn.tag]=tn
            t2,cur2=waText.SkipUntil(t,'<PNL',cur2)
        
        t,cur=waText.SkipUntil(s,'<PLLbank>')
        t,cur=waText.ReadBrackets(s,('<PLLbank>','</PLLbank>'),cur)
        t2,cur2=waText.SkipUntil(t,'<BLANK_ID>')
        t2,cur2=waText.ReadBrackets(t,('<BLANK_ID>','</BLANK_ID>'),cur2)
        if t2=='':
            self.blankId=[]
        else:
            self.blankId=list(map(int,t2.split(' ')))
        t2,cur2=waText.SkipUntil(t,'<PLL>',cur2)
        lent=len(t)
        
        while cur2<lent:
            t2,cur2=waText.ReadBrackets(t,('<PLL>','</PLL>'),cur2)
            tl=link()
            tl.FromString(t2)
            self.links.append(tl)
            t2,cur2=waText.SkipUntil(t,'<PLL',cur2)
        return self
    def GetRelation(self,n,l):
        '''Get the relation between the node named *n* and link number *l*
the return is one of:
    src: node is the link's source
    dst: node is the link's destination
    none: either the node or link is not found or it has none of the above relation
'''
        try:
            node=self.nodes[n]
            link=self.links[l]
            if node.tag==link.src:
                return 'src'
            elif node.tag==link.dst:
                return 'dst'
            else:
                return 'none'
        except Exception:
            pass
        return 'none'
        
    def Check(self):
        '''Returns true if the mspace is good
A good mspace:
1. all links' Id matches its position, except for Id=0 means blank link, which must appear in blankId(valid)
2. all links' src, dst, att have corresponding node, except for att=''
3. all nodes connect to valid links and the names are correct
'''
        lenl=len(self.links)
        lenn=len(self.nodes)
        print('Link count: %d\nNode Count: %d' % (lenl,lenn))
        LinkValid=True
        for i in range(1,lenl):
            if self.links[i].id!=i:
                if self.links[i].id==0 and i in self.blankId:
                    print('Link%d is a blank link'%i)
                    continue
                else:
                    print('Link%d is corrupted'%i)
                    LinkValid=False
            l=self.links[i]
            if l.src in self.nodes and l.dst in self.nodes and (l.att in self.nodes or l.att==''):
                continue
            else:
                print('Link%d is corrupted'%i)
                LinkValid=False
        NodeValid=True
        for k in self.nodes:
            n=self.nodes[k]
            if k!=n.tag:
                print('Node{%s} doesn\'t match'%k)
                NodeValid=False

            try:
                for i in n.links:
                    if self.GetRelation(n.tag,i)=='none':
                        print('Node{%s} has bad link%d'%(k,i))
                        NodeValid=False
            except Exception:
                print('Node{%s} has bad links'%k)
                NodeValid=False
                continue
        return LinkValid and NodeValid
#It is suggested that you use the following methods to access mspace to guarantee
    #data integrity
    def GetApp(self,x):
        '''Get the attached alib for the input str or int
if none is found, return None
'''
        try:
            if isinstance(x,str):
                return self.nodes[x].app
            else:
                return self.links[x].app
        except Exception:
            pass
        return None

    def FindNodesByName(self,s, countLimit=None):
        '''Return the nodes whose name matches s in terms of re
'''
        p=re.compile(s)
        result=[]
        for n in self.nodes:
            if re.match(p,n):
                if countLimit==None or len(result)<countLimit:
                    result.append(self.nodes[n])
                else:
                    break
        return result
    def FindLinksByAttribute(self,s, countLimit=None):
        '''Return a list of links whose attribute matches regex *s*
'''
        p=re.compile(s)
        result=[]
        for l in self.links:
            if l.id!=0 and re.match(p,l.att):
                if countLimit==None or len(result)<countLimit:
                    result.append(l)
                else:
                    break
        return result
    
    def NewNode(self,name):
        '''Add node, the name cannot be ''
'''
        if name in self.nodes:
            raise ValueError('Node already exists')
        elif name=='':
            raise ValueError("Node name cannot be empty")
        else:
            self.nodes[name]=node(name,'[cts|%s]'%time.ctime())
            
    def NewLink(self,src,dst,att=''):
        '''Add link
'''
        if src not in self.nodes:
            raise ValueError('src Node does not exist')
        if dst not in self.nodes:
            raise ValueError('dst Node does not exist')
        if att!='' and att not in self.nodes:
            raise ValueError('dst Node does not exist')
        if len(self.blankId)>0:
            i=self.blankId.pop()
            l=self.links[i]
        else:
            i=len(self.links)
            l=link(i)
            self.links.append(l)
        l.id=i
        l.src=src
        l.dst=dst
        l.att=att
        l.app=alib().FromString('[cts|%s]'%time.ctime())
        self.nodes[src].links.append(i)
        self.nodes[dst].links.append(i)
    def RemoveLink(self,l):
        '''Remove the link with number *l* out of database by setting it to invalid
Completely removal uses self.Tidy
'''
        l=self.links[l]
        if l.id==0:
            raise ValueError('Link is already removed')
        else:
            self.nodes[l.src].links.remove(l.id)
            self.nodes[l.dst].links.remove(l.id)
            print('Link{%s} removed'%l.id)
            l.id=0
            
    def Ren(self,oldname,newname=''):
        '''If newname is '', delete the according node, else rename it
'''
        if oldname in self.nodes:
            if newname in self.nodes:
                raise ValueError('New name already exists')
            #update attribute links
            for l in self.FindLinksByAttribute('^%s$'%oldname):
                l.att=newname
            n=self.nodes[oldname]
            #update connecting links
            if newname!='':
                for l in n.links:
                    r=self.GetRelation(oldname,l)
                    if r=='src':
                        self.links[l].src=newname
                    else:
                        self.links[l].dst=newname
            else:
                ls=n.links[:]
                for l in ls:
                    self.RemoveLink(l)
            #update the node
            n=self.nodes.pop(oldname)
            if newname=='':
                print('Node{%s} removed'%oldname)
            else:
                n.tag=newname
                n.app['mts']=time.ctime()
                self.nodes[newname]=n

        else:
            raise ValueError('According node does not exist')
        

#demo mode
if __name__ == '__main__':
    q='''import sys
print('\n?')
q=sys.stdin.readline().rstrip()
while q!='quit':
    try:
        print(eval(q))
    except Exception as e:
        import traceback
        traceback.print_exc()
    print('\n?')
    q=sys.stdin.readline().rstrip()'''
    from WalArt import waTool
    ms=Load('E:\InnerFantasia\_mylib\python34\MaterialMesh.msdx')
    ms.Check()
    
    Save(ms,'test.msdx')
'''
    a=alib()
    a['task']=alib().FromString('[|%s]'%q)
    a['m']=ms
    m=waTool.minion('Bob')
    m.Assign(a)
    m.reflex=1
    m.Go()
    m.join()
    time.sleep(1)
    '''
