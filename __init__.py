'''
WalArt
=============================
Walnut Artifacts

Created by wicknec 2015
wicknec@gmail.com

Making scientific exploration more friendly

'''

'''
Revisions for package main file:
==============================
151102 alib
151104 alib.Load,Save
151114 add auto indexing to *alib.FromString()*
151125 removed alib.type because __class__.__mro__ is available
151210 add *alib.Parse*,*setValue*,*getValue*
151218 add *alib.Merge*
151219 add *alib.Append* to use it as a list, *Pop*, *FindLastIndex*
         modified alib.ToString() to include object values
         *ToList*
160114 add *Call*, this will simplify the execution process
160204 modified alib.setValue, alib.getValue for custom separator
'''
__all__ = ['waText','alib','waFile']

from WalArt import waText, waFile

class alib(dict):
    '''
A tree-like structure with string keys.
Used for general information recording and knowledge representation
Equivalent to AttributeLibrary in CV
The values can be str, or another alib or an object
'''
    def __init__(self,d={}):
        '''
Converts a dict to corresponding alib by converting its keys and values to strings
'''
        dict.__init__(self)
        self.type='alib'
        for i in d:
            self[str(i)]=str(d[i])
    def __iter__(self):
        '''To traverse in good order
'''
        return alibiter(self)
    def __str__(self):
        return self.ToString()

    def ToString(self,indent=False):
        '''
Converts an alib to its string representation.
e.g. [a|b][c|d][e|[f|g][h][i|[j|k]]]
indent: the leading white spaces
'''
        result=''
        if indent!=False:
            ni=indent+'    '
        else:
            ni=False
            
        for i in self:
            if indent!=False and len(result)!=0:
                result+='\n'+indent
            if isinstance(self[i],alib):
                result+='['+i+'|'+self[i].ToString(ni)+']'
            else:
                result+='['+i
                if self[i]==None or isinstance(self[i],str) and len(self[i])==0:
                    result+=']'
                else:
                    result+='|'+str(self[i])+']'

        return result
    def Parse(s):
        '''parse string s, if can be parsed to alib, return alib, else return s
'''
        ss=s.strip()
        if len(ss)>0 and ss[0]=='[':
            return alib().FromString(ss)
        else:
            return s
        
        
    def FromString(self,s):
        '''Convert from the string form, clear original data
'''
        self.clear()
        content,cur=waText.SkipUntil(s,'[',0)
        lens=len(s)
        i=1
        while cur<lens:
            if s[cur]=='[':
                content,cur = waText.ReadSimpleBrackets(s,'[]',cur)
                col=content.find('|')
                if col==-1:
                    self[content]=''
                    content,cur=waText.SkipUntil(s,'[',cur)
                    continue
                elif col==0: #then auto index
                    while str(i) in self:
                        i+=1
                    k=str(i)
                else:
                    k=content[0:col]
                    
                if col+1>=len(content):
                    self[k]=''
                elif content[col+1]=='[':
                    self[k]=alib().FromString(content[col+1:])
                else:
                    self[k]=content[col+1:]
            content,cur=waText.SkipUntil(s,'[',cur)
        return self
    def Load(self,filename):
        '''Load from text file
'''
        if waFile.GetExtension(filename)=='':
            filename+='.alib.txt'
        s=waFile.LoadText(filename)
        self.FromString(s)
        return self
    def Save(self,filename):
        '''Save contents to text file
'''
        if waFile.GetExtension(filename)=='':
            filename+='.alib.txt'
        s=self.ToString('')
        waFile.SaveText(filename,s)
    def getValue(self,path,separator='|'):
        '''Get the value of given path
path can be a string like a|b|c or a list
if the path does not exist, raise IndexError
'''
        if isinstance(path,str):
            path=path.split(separator)
        k=path.pop(0)
        v=self[k]
        for k in path:
            v=v[k]
        return v
    def setValue(self,path,v,separator='|'):
        '''Set the value of given path, create if necessary
others same as getValue.
'''
        if isinstance(path,str):
            path=path.split(separator)
        d=self
        parent=None
        #last=path.pop()
        for i in range(len(path)):
            k=path[i]
            if isinstance(d,alib):
                if k in d:
                    parent=d
                    d=d[k]
                else:
                    parent=d
                    d[k]=alib()
                    d=d[k]
            else:
                #d is a string or something else
                parent[path[i-1]]=alib()
                parent=parent[path[i-1]]
                parent[k]=''
                d=''
        if parent==None:
            raise KeyError('path is empty')
        else:
            parent[path[-1]]=v
    def Merge(self,a2):
        '''Merge a2 in. Only update new keys.
Return merged self
'''
        for k2 in a2:
            if k2 not in self:
                self[k2]=a2[k2]
        return self
    def FindLastIndex(self):
        '''Returns the last index (int), if no numeric indices, return 0
'''
        i=1
        while str(i) in self:
            i+=1
        return i-1
    
    def Pop(self,k,d=None):
        '''Same as dict.pop, but also updates list if k is int
'''
        if isinstance(k,int):
            kp=k+1
            k=str(k)
            r=d
            if k in self:
                r=self.pop(k,d)
                while str(kp) in self:
                    self[k]=self[str(kp)]
                    k=str(kp)
                    kp+=1
                if k in self:
                    self.pop(k)
            return r
        else:
            return self.pop(k,d)
    def Append(self,data):
        '''Append data to the last index
'''
        i=self.FindLastIndex()
        self[str(i+1)]=data
    def ToList(self):
        '''Convert the numeric content to a list, start from 1
'''
        l=[]
        i=1
        while str(i) in self:
            l.append(self[str(i)])
            i+=1
        return l
    def Call(self,s,args,glbs=globals()):
        '''Execute string indicated in s, using args as arguments,
and returns ans if available
'''
        if s in self:
            s=self[s]
        exec(s,glbs,locals())
        if 'ans' in locals():
            #print(locals())
            return locals()['ans']
        else:
            return None
    __call__=Call

#demo mode
if __name__ == '__main__':
    a=alib().FromString('[a|b][c|d][e|[f|g][h][i|[j|k]]]')
    a.Save('a')


class alibiter(object):
    ''' iterator for alib: output numberical keys first, then in alphabetical order
'''
    def __init__(self,A):
        self.i=1 #next number, 0 for no number
        self.a=A
        self.list=list(A.keys())
        self.list.sort()

    def __next__(self):
        if len(self.list)==0:
            raise StopIteration
        elif self.i>0 and str(self.i) in self.a:
            self.list.remove(str(self.i))
            self.i+=1
            return str(self.i-1)
        else:
            self.i=0
            return self.list.pop(0)
