'''
WalArt.diagram.nodesView
=============================
Walnut Artifacts

Created by wicknec 2015
wicknec@gmail.com

Partly simulates Qt DiagramScene
(http://doc.qt.io/qt-5/qtwidgets-graphicsview-diagramscene-example.html#arrow-class-definition)
to show concept relations

'''
#-*- coding:utf-8 -*-  
'''
Revisions:
==============================
160218 implemented Arrow
160219 implemented Note, debugged, *Explore*
160220 fixed RegularPolygon for zero input
160226 set hash values for link explore color
161015 MainWindow.AddNode
161105 mspaceInterface, 
        bring main window to front after exploration
        fix third level bug
        
'''

from PyQt4.QtCore import *  
from PyQt4.QtGui import *  
import math  
  
QTextCodec.setCodecForTr(QTextCodec.codecForName("utf-8"))  

class Arrow(QGraphicsLineItem):
    def __init__(self,src,dst,parent=None):
        super(Arrow,self).__init__()
        self.src=src
        self.dst=dst
        self.parent=parent
        self.setFlag(QGraphicsItem.ItemIsSelectable,True)
        self.color=Qt.black
        self.setPen(QPen(self.color,3,Qt.SolidLine,Qt.RoundCap,Qt.RoundJoin))
        self.arrowHead=QPolygonF()
        self.arrowSize=10
        
    def boundingRect(self):
        extra=(self.pen().width()+20)/2
        return QRectF(self.line().p1(),QSizeF(self.line().p2().x()-self.line().p1().x(),\
                                              self.line().p2().y()-self.line().p1().y()))\
                                              .normalized()\
                                              .adjusted(-extra,-extra,extra,extra)


    def shape(self):
        path=super(Arrow,self).shape()
        path.addPolygon(self.arrowHead)
        return path
    
    def setColor(self,color):
        self.color=color
        self.pen().setColor(color)

    def updatePosition(self):
        line=QLineF(self.mapFromItem(self.src,0,0),self.mapFromItem(self.dst,0,0))
        self.setLine(line)

    def paint(self,painter,option,widget):
        if self.src.collidesWithItem(self.dst):
            return
        myPen=self.pen()
        myPen.setColor(self.color)
        arrowSize=20
        painter.setPen(myPen)
        painter.setBrush(self.color)

        centerLine=QLineF(self.src.pos(),self.dst.pos())
        endPolygon=self.dst.polygon()
        p1=endPolygon.first()+self.dst.pos()
        intersectPoint=QPointF()

        for i in range(endPolygon.count()):
            p2=endPolygon.at(i+1)+self.dst.pos()
            polyLine=QLineF(p1,p2)
            intersectType=polyLine.intersect(centerLine,intersectPoint)
            if intersectType==QLineF.BoundedIntersection:
                break
            p1=p2
        self.setLine(QLineF(intersectPoint,self.src.pos()))

        angle=math.acos(self.line().dx()/self.line().length())
        if self.line().dy()>=0:
            angle=math.pi*2-angle
        arrowP1=self.line().p1()+QPointF(math.sin(angle+math.pi/3)*self.arrowSize,
                                         math.cos(angle+math.pi/3)*self.arrowSize)
        arrowP2=self.line().p1()+QPointF(math.sin(angle+math.pi*2/3)*self.arrowSize,
                                         math.cos(angle+math.pi*2/3)*self.arrowSize)
        self.arrowHead.clear()
        self.arrowHead.append(self.line().p1())
        self.arrowHead.append(arrowP1)
        self.arrowHead.append(arrowP2)

        painter.drawLine(self.line())
        painter.drawPolygon(self.arrowHead)
        self.src.setZValue(self.zValue()+1)
        
        if self.isSelected():
            painter.setPen(QPen(self.color,1,Qt.DashLine))
            myLine=self.line()
            myLine.translate(0,4)
            painter.drawLine(myLine)
            myLine.translate(0,-8)
            painter.drawLine(myLine)
    def mousePressEvent(self,e):
        print(e.button())

def RegularPolygon(n,rot,radius):
    '''rot is a float usually between [0,1) signfies the rotation to the fraction of each polygon sides
    returns a polygon of n+1 points, whose first and last point coincides
'''
    p=QPolygonF()
    if n==0:
        return p
    rot=math.pi*2/n*rot
    for a in range(n+1):
        p.append(QPointF(math.cos(math.pi*2/n*a+rot)*radius,
                         math.sin(math.pi*2/n*a+rot)*radius))
    return p
class Note(QGraphicsPolygonItem):
    '''
'''
    def __init__(self,text='Hello Qt\n哈哈'):
        super(Note,self).__init__()
        self.setPolygon(RegularPolygon(8,0.5,50))
        
        item = QGraphicsTextItem(text)
        item.setParentItem(self)

        self.setFlag(QGraphicsItem.ItemIsMovable)  
        #self.setPen(QPen(Qt.NoPen))
        
        self.textItem=item
        self.text=text
        self.setScale(1)
        self.setFlag(QGraphicsItem.ItemIsSelectable,True)
        self.setPen(QPen(Qt.NoPen))
        
    def setScale(self,factor):
        self.setPolygon(RegularPolygon(8,0.5,50*factor))
        font = QFont("Times",12*factor)        
        self.textItem.setFont(font)

        self.textItem.setPos(-40*factor,-30*factor)

        textop=QTextOption(Qt.AlignCenter)
        
        self.textItem.document().setDefaultTextOption(textop)
        self.textItem.document().setTextWidth(80*factor)
        #item.document().setPageSize(QSizeF(80,80))
        #print(item.document().pageSize())
    def setText(self,text):
        
        self.textItem.setHtml(text)
        self.text=text
        
    def mousePressEvent(self,e):
        print(self.pos())
        print(e.button())

        
        
          
class MainWindow(QMainWindow):  
    def __init__(self,QWidget):  
        super(MainWindow,self).__init__()   
                  
        self.scene = QGraphicsScene(self)  
        self.scene.setSceneRect(-200,-200,400,400)  
        #self.initScene()
          
        self.view = QGraphicsView()  
        self.view.setScene(self.scene)  
        self.view.setMinimumSize(400,400)  
        self.view.show()  
          
        self.setCentralWidget(self.view)  
        self.resize(600,600)  
        self.setWindowTitle(self.tr("Nodes View"))

        self.itemExplored=None
        '''A function  that is executed when node or link is clicked
   passing one argument: node name or link number
'''

        #self.testScene2()
      
      
    def testScene(self):  
        for i in range(3):  
            self.slotAddEllipseItem()
        notes=[]
        for i in range(4):
            notes.append(self.slotAddNote())
        for i in range(3):
            a=Arrow(notes[i],notes[i+1])
            a.setFlag(QGraphicsItem.ItemIsMovable)  
            self.scene.addItem(a)
    def testScene2(self):
        from WalArt import mspace
        ms=mspace.Load('E:/InnerFantasia/_mylib/python34/WalArt/minKnow.msdx')
        self.Explore(ms,'python')
      
    def slotAddEllipseItem(self):  
        item = QGraphicsEllipseItem(QRectF(0,0,80,60))  
        item.setPen(QPen(Qt.NoPen))  
        item.setBrush(QColor(qrand()%256,qrand()%256,qrand()%256))  
        scale = ((qrand()%10)+1)/5.0  
        item.scale(scale,scale)  
        item.setFlag(QGraphicsItem.ItemIsMovable)  
        self.scene.addItem(item)  
        item.setPos((qrand()%int(self.scene.sceneRect().width())) - 200,(qrand()%int(self.scene.sceneRect().height())) - 200)  
      
    def slotAddNote(self):  
        item = Note()  
        item.setBrush(QColor(200,200,200))
        scale = ((qrand()%10)+1)/5.0  
        item.setScale(scale)  
        self.scene.addItem(item)  
        item.setPos((qrand()%int(self.scene.sceneRect().width())) - 200,(qrand()%int(self.scene.sceneRect().height())) - 200)
        return item
    def AddNode(self,text,pos,size=1):
        '''Add a note into the scene
            text: text displayed on the note, should be unique throughout canvas
            pos: (x,y)
            size: item.setScale(size), size==1 corresponds to 100x100 note
            
            you can change the color by item.setBrush(QColor(r,g,b))
            as is with other properties
        '''
        if text in self.nodes:
            raise Exception('Duplicate node text %s in scene'%text)
        item=Note(text)
        item.setBrush(QColor(200,200,200))
        self.scene.addItem(item)
        item.setPos(pos[0],pos[1])
        item.setScale(size)
        item.setData(1,n) #set data number 1 to the msnode data
        self.nodes[text]=item
        return item
        
    def AddArrow(self,src,dst):
        '''
        Add arrow that connects two nodes to the scene
        src,dst: existing node reference in the scene
        '''
        item=Arrow(src,dst)        
        self.scene.addItem(item)
        return item
            
#from WalArt import mspace
class mspaceInterface:
    '''associate with a nodeview and mindspace
    '''
    def __init__(self,mindspace,nodeview):
        self.mindSpace=mindspace
        self.nodeView=nodeview
        self.nodes=dict()
        #default settings
        self.settings={'DisplayText':[], #a list of possible field to display
                       }
        #self.nodes is the linked nodes in nodeView
    def setMindSpace(self,m):
        self.ClearScene()
        self.mindSpace=m
    def RenderNote(self,note):
        '''Render note according to settings
        The current note text should be the node name
        '''
        text=note.text
        att=self.mindSpace.nodes[text].app
        for address in self.settings['DisplayText']:
            try:
                text=att.getValue(address)
                break
            except Exception:
                pass
        if text!=note.text:
            note.setText(text)
    def ShowNote(self,nodeName,**kwargs):
        if 'color' not in kwargs:
            kwargs['color']=QColor(200,200,200)
        if 'pos' not in kwargs:
            kwargs['pos']=QPointF(0,0)
        elif not isinstance(kwargs['pos'],QPointF):
            pos=kwargs['pos']
            kwargs['pos']=QPointF(pos[0],pos[1])
        
        n=self.mindSpace.nodes[nodeName]
        item=Note(nodeName)
        self.RenderNote(item)
        self.nodes[nodeName]=item
        item.mousePressEvent=self.exploreItem
        item.setData(1,n) #set data number 1 to the msnode data
        self.nodeView.scene.addItem(item)
        item.setBrush(kwargs['color'])
        item.setPos(kwargs['pos'])
        if 'scale' in kwargs:
            item.setScale(kwargs['scale'])
    def ClearScene(self):
         self.nodeView.scene.clear()
         self.nodes.clear()
    def exploreItem(self,e):
        '''Action when node or link is clicked
        '''
        #print('exploreItem called with: {%s,%s}'%(e,what))
        item=self.nodeView.scene.itemAt(e.scenePos())
        print('item{%s} clicked'%item)
        if isinstance(item,QGraphicsTextItem):
                item=item.getParentItem()
        if e.button()==2: #right click
            if isinstance(item,Note):
                self.Explore(item.data(1).tag)
                self.nodeView.itemExplored(item.data(1).tag)
        else:
            if isinstance(item,Arrow):
                print(item.data(1).att)
                self.nodeView.itemExplored(item.data(1).id)
            else:
                print('%s:\n%s'%(item.text,item.data(1).app.ToString('')))
                self.nodeView.itemExplored(item.data(1).tag)
    def Explore(self,nodeName):
        '''Explore the node in mspace with nodeName
'''
        ms=self.mindSpace
        self.ClearScene()
        #level 0 node
        if nodeName not in self.mindSpace.nodes:
            raise Exception('{%s} not in mspace'%nodeName)
        self.ShowNote(nodeName,
                      color=QColor(200,200,200),pos=(0,0),scale=1.5)
        
        n=self.mindSpace.nodes[nodeName]
        #level 1 nodes
        ns=[] #name of node to be shown in view
        ls=[] #index of links to be shown
        for ln in n.links:
            if self.mindSpace.GetRelation(nodeName,ln)=='src':
                name=self.mindSpace.links[ln].dst
            else:
                name=self.mindSpace.links[ln].src
            if name not in self.nodes:
                ns.append(name)
                self.nodes[name]=None
            ls.append(ln)
        #draw level 1 nodes
        n1=len(ns)
        poss=RegularPolygon(n1,0.5,150) #uses to generate evenly spaced points
        for i in range(n1):
            self.ShowNote(ns[i],color=QColor(175,175,175),
                          pos=poss[i],scale=1)
        #level 2 nodes
        ns2=[]
        for n in ns:
            for ln in self.mindSpace.nodes[n].links: #traverse all links
                if self.mindSpace.GetRelation(n,ln)=='src':
                    name=ms.links[ln].dst
                else:
                    name=ms.links[ln].src
                if name not in self.nodes:
                    ns2.append(name)
                    self.nodes[name]=None
                if ln not in ls:
                    ls.append(ln)
        #draw level 2 nodes
        n2=len(ns2)
        poss=RegularPolygon(n2,0.5,250) #1.618 ratio
        for i in range(n2):
            self.ShowNote(ns2[i],color=QColor(150,150,150),
                          pos=poss[i],scale=0.6)

        #draw links
        pcolors={'':QColor.fromRgb(0,0,0)}
        z=0
        for ln in ls:
            l=self.mindSpace.links[ln]
            item=Arrow(self.nodes[l.src],self.nodes[l.dst])
            if l.att not in pcolors:
                pcolors[l.att]=QColor.fromHsv(hash(l.att)%256,200,200)
            item.setColor(pcolors[l.att])
            item.setData(1,l)
            item.setToolTip(l.att)
            
            self.nodeView.scene.addItem(item)
            item.setZValue(z)
            z-=1
            item.mousePressEvent=self.exploreItem
            
        self.nodeView.activateWindow() #bring main window to front
  
if __name__ == '__main__':  
    import sys  
    app = QApplication(sys.argv)  
    mainwindow = MainWindow(QWidget)
    mainwindow.show()
    mainwindow.testScene2()
    sys.exit(app.exec_())  
