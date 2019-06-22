# -*- coding: utf-8 -*-
"""
Created on Wed Oct  5 12:11:42 2016

@author: wein1

Revisions:
161129 move to pythonCodes
161229 add ballot 
170828 convert to module for easier use
170829 updated slicer, include pandas
"""

#%% header
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as pc
from timeit import default_timer as timer
import matplotlib.cm as cm
#%% functions
def StatStr(a):
    return "%f"%np.mean(a)+"±"+"%3f"%np.std(a)
def line(l):
    '''Getting the descriptor for a line
    where l is (x1 y1 x2 y2)
    from http://stackoverflow.com/questions/20677795/how-do-i-compute-the-intersection-point-of-two-lines-in-python
    '''
    p1=(l[0],l[1])
    p2=(l[2],l[3])
    A = (p1[1] - p2[1])
    B = (p2[0] - p1[0])
    C = (p1[0]*p2[1] - p2[0]*p1[1])
    return A, B, -C
def between(a,b,n):
    return n>=min(a,b) and n<=max(a,b)
def intersection(line1,line2):
    '''detects line segment intersection
    the line is a tuple of [x1 y1 x2 y2]
    returns intersection point(x,y) if intersects, else return False
    '''
    L1=line(line1)
    L2=line(line2)
    D  = L1[0] * L2[1] - L1[1] * L2[0]
    Dx = L1[2] * L2[1] - L1[1] * L2[2]
    Dy = L1[0] * L2[2] - L1[2] * L2[0]
    if D != 0:
        x = Dx / D
        y = Dy / D
        if between(line1[0],line1[2],x) and \
        between(line2[0],line2[2],x) and \
        between(line1[1],line1[3],y) and \
        between(line2[1],line2[3],y):
            return x,y
    return False
    
def test1x(devparam=None,tubeparam=None):
    '''
    obtain the result for 1 device
    given 
    output:
        xs, ys, os, ls: CNT x,y, orientation, length
        cts: contact condition
        valid: the index of CNT bridging the channel
    '''
    if devparam==None:
        devparam={'Wc':20,'Lc':2}
    if tubeparam==None:
        tubeparam={'n':800,'mu':1.57,'sigma':0.5}
        
    #the area is fixed to 100x250 (um)
    Wc,Lc=devparam['Wc'],devparam['Lc']
    n=tubeparam['n']
    
    xs=np.random.uniform(-50,50,n)
    ys=np.random.uniform(-125,125,n)
    ls=np.random.lognormal(tubeparam['mu'],tubeparam['sigma'],n)
    #ls=[4]*n
    os=np.random.uniform(0,2*np.pi,n)
    #channel edges
    Cu=(-Wc/2,Lc/2,Wc/2,Lc/2)
    Cd=(-Wc/2,-Lc/2,Wc/2,-Lc/2)
    #for every landing nantube, calculate if it makes a working device
    cts=[] #for recording contacted nanotubes
    for i in range(n):
        hdx=np.cos(os[i])*ls[i]/2
        hdy=np.sin(os[i])*ls[i]/2
        tline=(xs[i]-hdx,ys[i]-hdy,xs[i]+hdx,ys[i]+hdy)
        contact=int(not(intersection(Cu,tline)))+\
        int(not(intersection(Cd,tline)))
        cts.append(1-contact/2)
        
    return {'type': '1xResult',
    'devparam':devparam,'tubeparam':tubeparam,
            'xs':xs,'ys':ys,'os':os,'ls':ls,'cts':cts,
            'valid':[i for i,v in enumerate(cts) if v==1]}
def Display1xResult(r):
    plt.hold(False)
    plt.plot(1,1)
    
    devparam=r['devparam']
    tubeparam=r['tubeparam']
    Wc,Lc=devparam['Wc'],devparam['Lc']
    
    whole=pc.Rectangle((-50,-125),100,250,facecolor='purple',edgecolor='purple')
    rc=pc.Rectangle((-40,25),80,80,facecolor='yellow',edgecolor='yellow')
    rc2=pc.Rectangle((-40,-105),80,80,facecolor='yellow',edgecolor='yellow')
    rt=pc.Rectangle((-Wc/2,Lc/2),Wc,25-Lc/2,facecolor='yellow',edgecolor='yellow')
    rt2=pc.Rectangle((-Wc/2,-25),Wc,25-Lc/2,facecolor='yellow',edgecolor='yellow')
    ax=plt.gca()
    ax.add_patch(whole)
    ax.add_patch(rc)
    ax.add_patch(rc2)
    ax.add_patch(rt)
    ax.add_patch(rt2)
    plt.axis('tight')
    plt.axis('equal')
    plt.hold(True)
    
    xs,ys,os,ls,cts=r['xs'],r['ys'],r['os'],r['ls'],r['cts']
    
    for i in range(len(r['cts'])):
        hdx=np.cos(os[i])*ls[i]/2
        hdy=np.sin(os[i])*ls[i]/2
        contact=cts[i]
        if contact==0: #no contact
            plt.arrow(xs[i]-hdx,ys[i]-hdy,2*hdx,2*hdy,ec='k')
        elif contact==.5: #only contact on one side, save for future investigation
            plt.arrow(xs[i]-hdx,ys[i]-hdy,2*hdx,2*hdy,ec='r',fc='r')
        else: #both contact
            plt.arrow(xs[i]-hdx,ys[i]-hdy,2*hdx,2*hdy,ec='none',fc='green')
    plt.title('average density: %s per micron'%(tubeparam['n']/25000))
    print('%s contacts'%np.sum(cts))
    
def test1x1000(pdev,ptube):
    rs=[]
    print(str(tubeparam))
    start=timer()
    for i in range(1000):
        if i%200==0:
            print(i)
        rs.append(test1x(devparam,tubeparam))
    valids=[len(r['valid']) for r in rs]
    counts={}
    whos={}
    for i,v in enumerate(valids):
        if v in counts:
            counts[v]=counts[v]+1
            whos[v].append(i)
        else:
            counts[v]=1
            whos[v]=[i]
    end=timer()
    ls=rs[0]['ls']
    result={
        'type': '1x1000Result',
        'pdev':devparam,
        'ptube':tubeparam,
        #'rs':rs,#raw results from test1x
        'ls':ls,#representative length data
        'valids':valids,#number of valid channels in each test1x
        'counts':counts,#number of 0 tube, 1 tube, ... channels in 1000 tests
        'whos': whos,#details of counts
        'density':tubeparam['n']/25000,
        'r':rs[0],
        'duration':end-start,#time elapsed
        'tube':'mean:%2.2f, dev:%2.2f'%(np.mean(ls),np.sqrt(np.var(ls))),
        }
    return result
    
import pandas as pd

class slicer:
    #for simulating area density experiments
    #using test1x results
    def __init__(self):
        #basic parameters
        self.lines=3 #the number of lines drawn on each side, total 2n+1
        self.dist=10 #the distance between lines
        
        self.area=100*250 #predetermined
        self.devparam={'Wc':20,'Lc':2} #this will not affect result, just affect display
        self.tubeparam={'n':800,'mu':1.2,'sigma':0.55}
        
    def Check1Line(self,line1,cnts):
        #check how many CNTs intersects with the line
        #cnts contains xs ys os ls as in 1xresult
        os=cnts['os']
        ls=cnts['ls']
        xs=cnts['xs']
        ys=cnts['ys']
        contacts=0
        for x,y,o,l in zip(xs,ys,os,ls):
            hdx=np.cos(o)*l/2
            hdy=np.sin(o)*l/2
            tline=(x-hdx,y-hdy,x+hdx,y+hdy)
            if intersection(line1,tline):
                contacts=contacts+1
        return contacts
    def Check1Area(self,cnts,centerxy=(0,0),display=False):
        #generate lines
        #cnts are in type: 1xResult
    
        lines=[]
        n=self.lines*2+1 #total number of lines
        length=n*self.dist
        x=centerxy[0]
        y=centerxy[1]
        
        for i in range(n):
            lines.append((x-length/2+self.dist*(0.5+i),
                          y-length/2,
                          x-length/2+self.dist*(0.5+i),
                        y+length/2))
            lines.append((x-length/2,
                          y-length/2+self.dist*(0.5+i),
                          x+length/2,
                          y-length/2+self.dist*(0.5+i)))
        intersections=0
        if display:
            Display1xResult(cnts)
        for line in lines:
            intersections+=self.Check1Line(line,cnts)
            if display:
                plt.arrow(line[0],line[1],line[2]-line[0],line[3]-line[1],ec='r',fc='r')
        lineDensity=intersections/length/2/n
        print('Areal density: %f, Line density: %f(%d)'%(len(cnts['xs'])/self.area,lineDensity,intersections))
        return lineDensity
    def TestSingle(self):
        r=test1x(self.devparam,self.tubeparam)
        ns=[200+400*x for x in range(30)]
        ad=[i/25000 for i in ns]
        ld=[]
        for n in ns:
            self.tubeparam['n']=n
            r=test1x(self.devparam,self.tubeparam)
            ld.append(self.Check1Area(r))
        
        plt.plot(ad,ld,'o-')
        plt.xlabel('Areal Density')
        plt.ylabel('Line Density')
    def TestRelation(self):
        cols=['Areal','Lm','Line','duration']
        results=pd.DataFrame()
        ns=[200+400*x for x in range(30)]
        mus=[1.5,2,2.5]
        for mu in mus:
            param=self.tubeparam.copy()
            param['mu']=mu
            r=test1x(self.devparam,param)
            lm=np.mean(r['ls'])
            for n in ns:
                start=timer()
                areal=n/25000
                param['n']=n
                r=test1x(self.devparam,param)
                line=self.Check1Area(r)
                results=results.append(pd.DataFrame({cols[0]:areal,
                                             cols[1]:lm,
                                             cols[2]:line,
                                             cols[3]:timer()-start},index=[0]),ignore_index=True)
        return results
    def ShowTR(self,rs):
        fig, ax=plt.subplots()
        labels=[]
        for key, grp in rs.groupby(['Lm']):
            ax = grp.plot(ax=ax,kind='line',x='Areal',y='Line',style='o-')
            labels.append('%.3g $\mu$m'%key)
        lines, _ = ax.get_legend_handles_labels()
        ax.legend(lines,labels,loc='best')
        
        plt.show()
            
        
#%% for plain runner
if __name__ == '__main__':


    #%% test and plot
    mu, sigma = 3,1
    ss=np.random.lognormal(mu,sigma,1000)
    
    count, bins, ignored = plt.hist(ss, 100, normed=True, align='mid')
    x = np.linspace(min(bins), max(bins), 10000)
    pdf = (np.exp(-(np.log(x) - mu)**2 / (2 * sigma**2))
            / (x * sigma * np.sqrt(2 * np.pi)))
    plt.plot(x, pdf, linewidth=2, color='r')
    plt.axis('tight')
    plt.show()
    #%% test plotting arrow
    plt.arrow(0,0,1,1,True)
    
    #%% draw the testing device
    plt.hold(False)
    plt.plot(1,1)
    whole=pt.Rectangle((-50,-125),100,250,facecolor='purple',edgecolor='purple')
    rc=pt.Rectangle((-40,25),80,80,facecolor='yellow',edgecolor='yellow')
    rc2=pt.Rectangle((-40,-105),80,80,facecolor='yellow',edgecolor='yellow')
    rt=pt.Rectangle((-10,1),20,24,facecolor='yellow',edgecolor='yellow')
    rt2=pt.Rectangle((-10,-25),20,24,facecolor='yellow',edgecolor='yellow')
    ax=plt.gca()
    ax.add_patch(whole)
    ax.add_patch(rc)
    ax.add_patch(rc2)
    ax.add_patch(rt)
    ax.add_patch(rt2)
    plt.axis('tight')
    plt.axis('equal')
    #%% draw nanotubes
    n=200
    xs=np.random.uniform(-50,50,n)
    ys=np.random.uniform(-125,125,n)
    ls=np.random.lognormal(1,.5,n)
    #ls=[3 for i in range(n)]
    os=np.random.uniform(0,6.28,n)
    for i in range(n):
        hdx=np.cos(os[i])*ls[i]/2
        hdy=np.sin(os[i])*ls[i]/2
        plt.arrow(xs[i]-hdx,ys[i]-hdy,2*hdx,2*hdy,True)
    #%% check length distribution
    plt.hist(ls,20)
    #%% test one time under normal condition
    r=test1x()
    Display1xResult(r)
    #%% test 1000
    
        #%%
    start=timer()
    devparam={'Wc':5,'Lc':2}
    # 1.9 0.6 for 7.54 nm
    tubeparam={'n':3500,'mu':1,'sigma':.65}
    r=test1x1000(devparam,tubeparam)
    counts,ls,whos=r['counts'],r['ls'],r['whos']
    print(counts)
    print(r['tube'])
    print('tube density: {0} per square micron'.format(tubeparam['n']/25000))
    end=timer()
    print('time elapsed: %s seconds'%(end-start))
    #%% show representative instances
    Display1xResult(r['r'])
    #%% plot tube length distribution
    plt.hold(False)    
    #ls=rs[0]['ls']
    plt.hist(ls,30)
    plt.title('mean:%f, dev:%f'%(np.mean(ls),np.sqrt(np.var(ls))))
    plt.axis('normal')
    #%%  repeat 1000 times of 1000 devices
    devparam={'Wc':5,'Lc':2}
    #tubeparam={'n':1400,'mu':1.3,'sigma':0.5}
    countss=[]# {0:xxx, 1:xxx, 2:xxx, ...} for stat fraction    
        
    def OneExp(number,devparam,tubeparam):
        #return counts
        j=number
        rs=[]
        print('%s:'%j)
        for i in range(1000):
            if i%200==0:
                print(i)
            rs.append(test1x(devparam,tubeparam))
        valids=[len(r['valid']) for r in rs]
        counts={}
        whos={}
        for i,v in enumerate(valids):
            if v in counts:
                counts[v]=counts[v]+1
                whos[v].append(i)
            else:
                counts[v]=1
                whos[v]=[i]
        print('%s:%s'%(j,counts))
        return counts
    def SerialExp(devparam,tubeparam):
        start=timer()
        countss=[]
        for j in range(1000):
            countss.append(OneExp(j,devparam,tubeparam))
        end=timer()
        print('time elapsed: %s seconds'%(end-start))
        return countss
    def ParallelExp(devparam,tubeparam):
        import joblib
        start=timer()
        countss=[]
        countss=joblib.Parallel(n_jobs=8)(joblib.delayed(OneExp)(j,devparam,tubeparam) for j in range(1000))
        end=timer()
        print('time elapsed: %s seconds'%(end-start))
        return countss
    #%%
    countss=SerialExp(devparam,tubeparam)
    
    #%% analyze the 1000x1000 result for stability
    oness=[c[1] for c in countss]
    mores=[sum(c.values())-c[1]-c[0] for c in countss]
    plt.figure(figsize=(8,6))
    plt.hold(False)
    plt.hist(oness,color='b')
    plt.hold(True)
    plt.hist(mores,color='r')
    #plt.title('1000 Experiments of 1000 Devices',fontsize=30)
    plt.grid(True)
    plt.text(20,250,'DEV: '+str(devparam))
    plt.text(20,260,'CNT: '+str(tubeparam))
    plt.text(20,270,'mean length: '+str(np.exp(tubeparam['mu'])))
    plt.legend(['with 1 CNT','with 2 or more CNTs'],
            loc='upper right')
    plt.xlabel('Number of Devices',fontsize=20)
    plt.ylabel('Number of Experiments',fontsize=20)
     #%% save countss
    import pickle
    with open('countss-5x2-0219.pkl', 'wb') as out:
        pickle.dump(countss,out,-1)
    #%% load countss
    with open('countss-5x2-0118.pkl','rb') as infile:
        countss=pickle.load(infile)
         
#%%
    import random
    def ballot(chance):
        if random.random()<chance:
            return 1
        else:
            return 0
    def OneChannel(ntube,fraction):
         #fraction is the semiconducting fraction
        result=1
        for c in range(ntube):
            result*=ballot(fraction)
        return result
    def OneExperiment(counts,fraction,includeMultipleChannel=True):
        # return the device fraction
        ndevice=0
        nsemi=0
        for k in counts:
            if k>0:
                if k==1:
                    for c in range(counts[k]):
                        ndevice+=1
                        nsemi+=OneChannel(1,fraction)
                elif includeMultipleChannel:
                    for c in range(counts[k]):
                        ndevice+=1
                        nsemi+=OneChannel(k,fraction)
        return nsemi/ndevice
    def OneFraction(fraction,countss):
        ratioOne=[]
        ratioMul=[]
        for counts in countss:
            ratioOne.append(OneExperiment(counts,fraction,False))
            ratioMul.append(OneExperiment(counts,fraction,True))
        result={'OneMean':np.mean(ratioOne),
                'OneStd':np.std(ratioOne),
                'MulMean':np.mean(ratioMul),
                'MulStd':np.std(ratioMul)}
        return result
    def Fractions(countss):
        fractions=np.linspace(0,1,11)
        rs=[]
        for f in fractions:
            rs.append(OneFraction(f,countss))
            print(f)
        onem=[r['OneMean'] for r in rs]
        onee=[r['OneStd'] for r in rs]
        mulm=[r['MulMean'] for r in rs]
        mule=[r['MulStd'] for r in rs]
        #returns things to plot
        return fractions,onem,onee,mulm,mule
    def PlotFraction(f,om,os,mm,ms):
        #plot
        fig=plt.figure()
        plt.hold(True)
        plt.errorbar(f,om,yerr=os,fmt='-ob',label='Only single tube channels')
        plt.errorbar(f,mm,yerr=ms,fmt='-or',label='All conducting channels')
        plt.xlabel('Tube semiconducting fraction',fontsize=20)
        plt.ylabel('Device semiconducting fraction',fontsize=16)
        plt.legend(loc='upperright')
        plt.hold(False)
        plt.grid(True)
    def TestBallot(chance,times=100):
        n=0
        v=0
        for t in range(times):
            n+=1
            v+=ballot(chance)
        return v/n
    def TestBallotMany(chance,times=100):
        exps=[]
        for i in range(100):
            exps.append(TestBallot(chance,times))
        print('mean:%s, std:%s'%(np.mean(exps),np.std(exps)))
        
    rf=Fractions(countss)
    PlotFraction(*rf)
#%% test with different fix number of times
    def TestFixedNumbers():
        fractions=np.linspace(0,1,21)
        rs=[]
        counts={1:50}
        numbers=[50,100,200,500]
        specs=['-or','-og','-ob','-om']
        toplot={}
        for n,spec in zip(numbers,specs):
            toplot[n]={'mean':[],'dev':[],'spec':spec}
            counts[1]=n
            for f in fractions:
                r=[]
                for t in range(1000):
                    r.append(OneExperiment(counts,f,False))
                toplot[n]['mean'].append(np.mean(r))
                toplot[n]['dev'].append(np.std(r))
                print(f)
        fig=plt.figure()
        plt.hold(True)
        for n in numbers:
            #plt.errorbar(fractions,toplot[n]['mean'],yerr=toplot[n]['dev'],fmt=toplot[n]['spec']
            plt.plot(fractions,toplot[n]['dev'],
                       toplot[n]['spec'] ,label='%s trials'%n)
        plt.xlabel('Tube semiconducting fraction',fontsize=20)
        plt.ylabel('Result deviation',fontsize=20)
        plt.legend(loc='upperleft')
        plt.hold(False)
        plt.grid(True)
    TestFixedNumbers()
        
    #%% see effects of different length and density
    start=timer()
    devparam={'Wc':50,'Lc':2}
    #mu sigma combinations
    
    mss=[#(0.52,0.64),#saeeds sample2
        (1.05,0.47),#saeeds sample
        (1.9,0.6),#yongpings sample
        (2.47,0.35),#aqeels sample lower yields
    ]
    #mss=[(0.6,0.4),(0.8,0.5)]
    ns=[int(n) for n in np.logspace(1,3.6,num=20)]
    rs=[]
    start=timer()
    for m,s in mss: 
        for n in ns: #different density
            tubeparam={'n':n,'mu':m,'sigma':s}
            rs.append(test1x1000(devparam,tubeparam))
    stop=timer()
    print('time elapsed: %s seconds'%(stop-start))
    #%% stat it
    d={}
    for r in rs:
        ms='({mu},{sigma})'.format(**r['ptube'])
        if ms in d:
            d[ms].append(r)
        else:
            d[ms]=[r]
    
    cmap=plt.get_cmap('jet')
    import matplotlib.colors as colors
    sm=cm.ScalarMappable(cmap=cmap, 
                         norm=colors.Normalize(vmin=0, vmax=len(d)))
    #%%
    fig=plt.figure()
    ax=fig.add_subplot(111)
    ax2=ax.twinx()
    plt.hold(True)
    for i,k in enumerate(d):
        xs=[r['ptube']['n']/25000 for r in d[k]]
        ys=[]
        y2s=[]
        for r in d[k]:
            ys.append(r['counts'].get(1,0)/1000)
            y2s.append(sum(r['counts'].values(),
                               -r['counts'].get(0,0)-r['counts'].get(1,0))/1000)
        c=sm.to_rgba(i)
        ax.plot(xs,ys,'o-',label=k+':'+d[k][-1]['tube'],
                color=c,markersize=9)
        ax2.plot(xs,y2s,'*-',
                 color=c,markersize=12)
    handles,labels = ax.get_legend_handles_labels()
    
    #xmin,xmax,ymin,ymax=min(xs),max(xs),0,1
    xmin,xmax,ymin,ymax=min(xs),0.01,0,1
    
    ax.axis((xmin,xmax,ymin,ymax))
    ax2.axis((xmin,xmax,ymin,ymax))
    
    ax.legend(handles, labels,loc='upper left')
    ax.grid(True)
    ax.set_ylabel('Single Tube Channel Fraction (o)',fontsize=20)
    ax2.set_ylabel('Multiple Tube Channel Fraction (*)',fontsize=20)
    ax.set_xlabel('Tube Density($/\mu m^2$)',fontsize=20)
    plt.show()